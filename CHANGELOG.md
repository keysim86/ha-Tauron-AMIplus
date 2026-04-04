# Changelog

## [1.1.8] - 2026-04-04

### Fixed
- Dodano retry przy `ServerDisconnectedError` w `get_raw_data()`: przy pierwszym rozłączeniu serwera Tauron integracja czeka 5s i ponawia całe pobieranie danych zamiast od razu zgłaszać błąd do koordynatora

## [1.1.7] - 2026-04-04

### Fixed
- `ServerDisconnectedError` podczas walidacji sesji eLicznik propagował się do koordynatora i blokował wszystkie sensory; dodano try/except w `try_restore_session()` — błąd sieci podczas walidacji jest teraz traktowany jako nieważna sesja, co skutkuje automatycznym ponownym logowaniem

## [1.1.6] - 2026-04-04

### Fixed
- Startup HA anulowany przez `CancelledError`: `async_request_refresh()` był `await`owany bezpośrednio w `async_setup_entry`, co blokowało setup do czasu zakończenia pełnego fetchu danych (DNS + 365 requestów HTTP); zmieniono na `hass.async_create_background_task()` — setup kończy się natychmiast, dane pobierane są w tle

## [1.1.5] - 2026-04-04

### Fixed
- Startup HA blokowany przez `async_add_entities(sensors, True)` — `update_before_add=True` triggeruje pełny fetch danych (365 HTTP requestów) dla każdego sensora podczas rejestracji platformy; zmieniono na `async_add_entities(sensors)` — dane są dostarczane przez `_handle_coordinator_update` po zakończeniu pierwszego cyklu koordynatora

## [1.1.4] - 2026-04-03

### Fixed
- Przywrócono `async_request_refresh()` zamiast `async_config_entry_first_refresh()` — przy niedostępnym API Taurona podczas startu HA integracja rzucała `ConfigEntryNotReady` bez logów, blokując ładowanie; sensory pozostawały w stanie "niedostępny" bezterminowo

## [1.1.3] - 2026-04-03

### Fixed
- Brak wartości sensorów po restarcie HA: zmieniono kolejność inicjalizacji — `async_config_entry_first_refresh()` jest teraz wywoływane przed rejestracją sensorów, dzięki czemu dane są dostępne od razu; poprzednio przy nieudanym pierwszym pobraniu sensory czekały 8,5h na kolejny cykl

## [1.1.2] - 2026-04-03

### Fixed
- Krytyczny błąd: wyjątek z `login_service()` w `get_moj_tauron()` propagował się poza blok try/except, powodując błąd koordynatora i brak aktualizacji WSZYSTKICH sensorów; przeniesiono całe wywołanie `login_service()` wewnątrz try/except

## [1.1.1] - 2026-04-03

### Fixed
- Brak etykiety tekstowej dla opcji "Pokaż sensor należności" w config flow i options flow — wyświetlała się nazwa zmiennej zamiast opisu; dodano tłumaczenia w `pl.json`, `en.json` i `strings.json`

## [1.1.0] - 2026-04-03

### Added
- Sensor **Należności Mój Tauron** — pobiera nieopłacone faktury z portalu mój.tauron.pl; wartość to kwota pierwszej należności (PLN), atrybut `payments` zawiera pełną listę; wymagane włączenie opcji "Pokaż sensor należności" w konfiguracji integracji
- Nowa opcja w config flow i options flow: **Pokaż sensor należności (Mój Tauron)**
- Zależność `beautifulsoup4` dodana do wymagań integracji

## [1.0.5] - 2026-03-25

### Zmieniono
- Zrównoleglono żądania HTTP (asyncio.gather) — pobieranie danych jest teraz znacznie szybsze
- Zużycie i generacja pobierane jednocześnie zamiast sekwencyjnie
- Dane dzienne dla zakresu dat (miesiąc, rok, 30 dni) pobierane równolegle zamiast po kolei

## [1.0.4] - 2026-03-25

### Zmieniono
- Spolszczono nazwy sensorów (zużycie, oddanie, bilans)

## [1.0.3] - 2026-03-24

### Zmieniono
- Dodano opisy release z CHANGELOG

## [1.0.2] - 2026-03-24

### Zmieniono
- Poprawiono tworzenie GitHub release — usunięto target_commitish

## [1.0.1] - 2026-03-24

### Zmieniono
- Poprawiono workflow release — aktualizacja manifest.json przez Forgejo API zamiast git push

## [1.0.0] - 2026-03-24

### Zmieniono
- Fork z PiotrMachowski/Home-Assistant-custom-components-Tauron-AMIplus
- Zaktualizowano linki w README i manifest.json na własne repo
- Dodano workflow automatycznego release (Forgejo → GitHub)
- Dodano CHANGELOG
