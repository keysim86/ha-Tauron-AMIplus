# Changelog

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
