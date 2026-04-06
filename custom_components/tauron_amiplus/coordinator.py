"""Update coordinator for TAURON sensors."""
import datetime
import logging

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_call_later
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .connector import TauronAmiplusConnector, TauronAmiplusRawData
from .const import (DEFAULT_UPDATE_INTERVAL, DOMAIN, RETRY_INTERVALS)
from .statistics import TauronAmiplusStatisticsUpdater

_LOGGER = logging.getLogger(__name__)


class TauronAmiplusUpdateCoordinator(DataUpdateCoordinator[TauronAmiplusRawData]):

    def __init__(
            self,
            hass: HomeAssistant,
            config_entry_id: str,
            username: str,
            password: str,
            meter_id: str,
            meter_name: str,
            show_generation: bool = False,
            show_12_months: bool = False,
            show_balanced: bool = False,
            show_balanced_year: bool = False,
            show_configurable: bool = False,
            show_configurable_date: datetime.date | None = None,
            store_statistics: bool = False,
            show_payment: bool = False,
    ):
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=DEFAULT_UPDATE_INTERVAL,
                         update_method=self.update_method)
        self.connector = TauronAmiplusConnector(username, password, meter_id, hass, config_entry_id, show_generation, show_12_months,
                                                show_balanced, show_balanced_year, show_configurable,
                                                show_configurable_date, show_payment)
        self.meter_id = meter_id
        self.meter_name = meter_name
        self.show_generation = show_generation
        self.show_12_months = show_12_months
        self.show_balanced = show_balanced
        self.show_configurable = show_configurable
        self.show_configurable_date = show_configurable_date
        self.store_statistics = store_statistics
        self._retry_count = 0
        self._retry_unsub = None

    def _cancel_retry(self):
        if self._retry_unsub is not None:
            self._retry_unsub()
            self._retry_unsub = None

    def _is_data_incomplete(self, data: TauronAmiplusRawData) -> bool:
        """Return True if any of the core sensor fields are missing."""
        if data is None or data.consumption is None:
            return True
        c = data.consumption
        return c.json_daily is None or c.json_monthly is None or c.json_yearly is None or c.json_reading is None

    async def update_method(self) -> TauronAmiplusRawData:
        self._cancel_retry()
        self.log("Starting data update")
        data = await self._update()
        self.log("Downloaded all data")
        if data is not None and self.store_statistics:
            self.log("Starting statistics update")
            await self.generate_statistics(data)
            self.log("Updated all statistics")

        if self._is_data_incomplete(data):
            if self._retry_count < len(RETRY_INTERVALS):
                delay = RETRY_INTERVALS[self._retry_count]
                self.log(f"Incomplete data — retry {self._retry_count + 1}/{len(RETRY_INTERVALS)} in {delay}")
                @callback
                def _do_retry(_now):
                    self._retry_unsub = None
                    self.hass.async_create_task(
                        self.async_request_refresh(),
                        f"tauron_amiplus_retry_{self.meter_id}",
                    )
                self._retry_unsub = async_call_later(self.hass, delay.total_seconds(), _do_retry)
                self._retry_count += 1
            else:
                self.log("Max retries reached — waiting for next scheduled update")
                self._retry_count = 0
        else:
            self._retry_count = 0

        return data

    async def generate_statistics(self, data):
        statistics_updater = TauronAmiplusStatisticsUpdater(self.hass, self.connector, self.meter_id, self.meter_name,
                                                            self.show_generation, self.show_balanced)
        await statistics_updater.update_all(data)

    async def _update(self) -> TauronAmiplusRawData:
        return await self.connector.get_raw_data()

    def log(self, msg):
        _LOGGER.debug(f"[{self.meter_id}]: {msg}")
