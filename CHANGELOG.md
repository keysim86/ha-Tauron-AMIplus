# Changelog

## [Unreleased]

### Changed
- `connector.py`: pamięć podręczna dni z kompletem danych godzinowych jest zapisywana na dysk
  (`.storage/tauron_amiplus_daily_cache_<wpis>`, zapis 30 s po każdym udanym pobraniu, z kopii — serializacja
  idzie w osobnym wątku). Wcześniej żyła tylko w pamięci, więc każdy restart Home Assistant pobierał od nowa
  dane dzień po dniu (przy 12 miesiącach i zakresie konfigurowalnym ponad tysiąc zapytań, kilka minut bez
  wartości w sensorach). Uszkodzony albo nieczytelny plik = pusta pamięć i zwykłe pobieranie.
- Usługa `clear_cache` czyści też plik na dysku; usunięcie wpisu integracji usuwa plik (`async_remove_entry`).

## [1.1.14] - 2026-10-25

### Fixed
- `__init__.py`: integracja blokowała start Home Assistant na 5 minut ("Something is blocking Home Assistant
  from wrapping up the start up phase", w logu `Setup timed out for bootstrap waiting on ... debouncer
  cooldown=10, immediate=True`). Pierwsze odświeżanie szło przez `async_request_refresh()`, a Debouncer
  koordynatora uruchamia je we własnym zwykłym zadaniu, na które HA czeka przy starcie — opakowanie w zadanie
  w tle nie pomagało. Po restarcie pamięć podręczna dni jest pusta, więc to odświeżanie pobiera dane godzinowe
  dzień po dniu i trwa minuty. Teraz `async_refresh()` bezpośrednio w zadaniu w tle wpisu
  (`config_entry.async_create_background_task`, anulowane przy wyładowaniu wpisu).

## [1.1.13] - 2026-10-08

### Fixed
- `services.py`: zgodność z Home Assistant 2026.10 — usługi `download_statistics` i `clear_cache` czytały
  `DeviceEntry.config_entries`, co od 2026.10 loguje ostrzeżenie o wycofaniu (przestanie działać w 2027.10).
  Teraz wpis konfiguracji z `DeviceEntry.config_entry_id`, a na starszych HA (bez tego pola) jak dotąd
  z `config_entries`; brana jest zawsze pozycja tej integracji. Nieznane urządzenie albo urządzenie innej
  integracji — błąd w logu zamiast wyjątku.
- `manifest.json`: hassfest odrzucał wymagania — `requests` jest zależnością samego Home Assistant (integracja
  i tak go nie używa), a przypięte `beautifulsoup4==4.12.3` kłóciło się z `4.13.3` z zależności HA. Teraz tylko
  `beautifulsoup4>=4.12.3`.

## [1.1.12] - 2026-05-30

### Fixed
- `connector.py`: Tauron przeszedł na Keycloak SSO — stary flow logowania przestał działać; nowy flow: (1) GET strony logowania, (2) regex wyciąga URL formularza `kc-form-login`, (3) POST credentials do tego URL z `allow_redirects=True`
- `connector.py`: timeout sesji ustawiony przez `async_create_clientsession` jest ignorowany przez HA; dodano `ClientTimeout(total=30)` bezpośrednio do każdego `session.request()` / `session.get()`
- `connector.py`: `ServerDisconnectedError` spowodowany zbyt dużą liczbą równoległych requestów — `asyncio.gather` w `get_raw_values_daily_for_range` tworzył do ~120 równoległych połączeń jednocześnie; dodano `asyncio.Semaphore(3)` w `execute_post` limitujący maksymalnie 3 równoległe requesty do serwera Taurona

## [1.1.11] - 2026-04-06

### Added
- Automatyczny retry gdy dane są niekompletne (jakikolwiek sensor pokazałby "niedostępny"/"nieznany"): kolejne próby po 5 min, 15 min i 30 min zamiast czekania 8,5h do następnego normalnego odświeżenia. Po 3 nieudanych próbach integracja wraca do normalnego harmonogramu. Dotyczy pól: `json_daily`, `json_monthly`, `json_yearly`, `json_reading`.

## [1.1.10] - 2026-04-05

### Fixed
- Zwiększono liczbę prób przy `ServerDisconnectedError` z 1 do 3 (opóźnienia 3s i 10s) — serwer Taurona jest na tyle niestabilny że pojedynczy retry nie wystarczał

## [1.1.9] - 2026-04-04

### Fixed
- Sensor "Należności Mój Tauron" pokazywał "nieznany" gdy brak nieopłaconych faktur (np. nadpłata); teraz wyświetla `0.0 zł` z pustą listą `payments`

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
