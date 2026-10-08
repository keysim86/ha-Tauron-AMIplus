"""Spook - Not your homie."""
from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import device_registry as dr

from .const import DOMAIN
from .statistics import TauronAmiplusStatisticsUpdater
from .typing_helpers import TauronAmiplusConfigEntry

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)


def _config_entry_for_device(hass: HomeAssistant, device_id: str) -> TauronAmiplusConfigEntry | None:
    """Wpis konfiguracji Tauron AMIplus urządzenia z wywołania usługi.

    Od HA 2026.10 odczyt `DeviceEntry.config_entries` loguje ostrzeżenie (koniec w 2027.10) —
    nowsze HA mają `config_entry_id`; starsze (hacs.json: od 2022.12) tylko `config_entries`.
    """
    device = dr.async_get(hass).async_get(device_id)
    if device is None:
        _LOGGER.error(f"Unknown device: {device_id}")
        return None
    entry_id = getattr(device, "config_entry_id", None)
    entry_ids = [entry_id] if entry_id is not None else list(device.config_entries)
    for i in entry_ids:
        entry = hass.config_entries.async_get_entry(i)
        if entry is not None and entry.domain == DOMAIN:
            return entry
    _LOGGER.error(f"Device {device_id} does not belong to {DOMAIN}")
    return None


class DownloadStatisticsService:

    domain = DOMAIN
    service = "download_statistics"
    schema = vol.Schema({
        vol.Required("device_id"): cv.string,
        vol.Required("start_date"): cv.date
    })

    def __init__(self, hass: HomeAssistant):
        self._hass = hass

    async def async_handle_service(self, call: ServiceCall) -> None:
        now = datetime.date.today()
        start_date = call.data["start_date"]
        if start_date > now:
            _LOGGER.error(f"Failed to download statistics, date from the future: {start_date}")
            return
        config_entry = _config_entry_for_device(self._hass, call.data["device_id"])
        if config_entry is None:
            return
        await TauronAmiplusStatisticsUpdater.manually_update(self._hass, start_date, config_entry)


class ClearCacheService:

    domain = DOMAIN
    service = "clear_cache"
    schema = vol.Schema({
        vol.Required("device_id"): cv.string,
    })

    def __init__(self, hass: HomeAssistant):
        self._hass = hass

    async def async_handle_service(self, call: ServiceCall) -> None:
        config_entry = _config_entry_for_device(self._hass, call.data["device_id"])
        if config_entry is None:
            return
        config_entry.runtime_data.coordinator.connector.clear_cache()


def register_all_services(hass: HomeAssistant) -> None:
    services = [DownloadStatisticsService(hass), ClearCacheService(hass)]
    for service in services:
        hass.services.async_register(service.domain, service.service, service.async_handle_service, service.schema)
