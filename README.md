[![GitHub Latest Release][releases_shield]][latest_release]
[![GitHub All Releases][downloads_total_shield]][releases]
[![Installations][installations_shield]][releases]
[![HACS Default][hacs_shield]][hacs]

[hacs_shield]: https://img.shields.io/static/v1.svg?label=HACS&message=Default&style=popout&color=green&labelColor=41bdf5&logo=HomeAssistantCommunityStore&logoColor=white
[hacs]: https://hacs.xyz/docs/default_repositories
[latest_release]: https://github.com/keysim86/ha-Tauron-AMIplus/releases/latest
[releases_shield]: https://img.shields.io/github/release/keysim86/ha-Tauron-AMIplus.svg?style=popout
[releases]: https://github.com/keysim86/ha-Tauron-AMIplus/releases
[downloads_total_shield]: https://img.shields.io/github/downloads/keysim86/ha-Tauron-AMIplus/total
[installations_shield]: https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fanalytics.home-assistant.io%2Fcustom_integrations.json&query=%24.tauron_amiplus.total&style=popout&color=41bdf5&label=analytics

# Tauron AMIplus

Integracja do Home Assistant pobierająca dane o zużyciu i oddaniu energii elektrycznej z serwisu [eLicznik Tauron](https://elicznik.tauron-dystrybucja.pl) oraz należności z [Mój Tauron](https://moj.tauron.pl).

## Sensory

### Pobór energii

| Sensor | Opis |
|--------|------|
| Odczyt licznika (pobór) | Aktualny stan licznika poboru w kWh |
| Zużycie energii dobowe | Zużycie za poprzedni dzień |
| Zużycie energii miesięczne | Zużycie w bieżącym miesiącu |
| Zużycie energii roczne | Zużycie w bieżącym roku |
| Zużycie energii ostatnie 12 miesięcy | Zużycie za ostatnie 12 miesięcy |
| Zużycie energii (konfigurowalne) | Zużycie od wybranej daty |

### Oddanie energii (prosument)

Włączane opcjonalnie w ustawieniach integracji.

| Sensor | Opis |
|--------|------|
| Odczyt licznika (oddanie) | Aktualny stan licznika oddania w kWh |
| Oddanie energii dobowe | Oddanie za poprzedni dzień |
| Oddanie energii miesięczne | Oddanie w bieżącym miesiącu |
| Oddanie energii roczne | Oddanie w bieżącym roku |
| Oddanie energii ostatnie 12 miesięcy | Oddanie za ostatnie 12 miesięcy |
| Oddanie energii (konfigurowalne) | Oddanie od wybranej daty |

### Bilans (prosument)

Włączane opcjonalnie w ustawieniach integracji.

| Sensor | Opis |
|--------|------|
| Bilans dobowy | Bilans poboru i oddania za poprzedni dzień |
| Bilans miesięczny | Bilans w bieżącym miesiącu |
| Bilans roczny | Bilans w bieżącym roku |
| Bilans ostatnie 12 miesięcy | Bilans za ostatnie 12 miesięcy |
| Bilans (konfigurowalny) | Bilans od wybranej daty |

### Mój Tauron

Włączane opcjonalnie w ustawieniach integracji.

| Sensor | Opis |
|--------|------|
| Należności Mój Tauron | Kwota najbliższej nieopłaconej faktury w PLN. `0.0 zł` gdy brak zaległości (nadpłata). Atrybut `payments` zawiera pełną listę oczekujących płatności z terminami. |

## Instalacja

### HACS (zalecane)

[![Otwórz w HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=keysim86&repository=ha-Tauron-AMIplus&category=integration)

1. Otwórz HACS → **Integracje**
2. Kliknij ⋮ → **Własne repozytoria**
3. Wpisz `keysim86/ha-Tauron-AMIplus`, kategoria: **Integracja**
4. Zainstaluj **Tauron AMIplus**
5. Uruchom ponownie Home Assistant

### Ręczna

Pobierz [tauron_amiplus.zip](https://github.com/keysim86/ha-Tauron-AMIplus/releases/latest/download/tauron_amiplus.zip) i rozpakuj do katalogu `config/custom_components/tauron_amiplus`, następnie zrestartuj Home Assistant.

## Konfiguracja

Przejdź do: **Ustawienia → Urządzenia i usługi → Dodaj integrację → Tauron AMIplus**

[![Dodaj integrację](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=tauron_amiplus)

W kreatorze podaj:
- Login i hasło do konta eLicznik
- Wybierz licznik z listy (integracja pobiera je automatycznie)

Po dodaniu wejdź w **Konfiguruj** aby włączyć opcjonalne sensory (generacja, bilans, Mój Tauron, sensor konfigurowalny).

## Częstotliwość odświeżania

Dane są pobierane co **8,5 godziny**. Jeśli po odświeżeniu jakikolwiek sensor byłby niedostępny lub nieznany (brakujące dane dobowe, miesięczne, roczne lub odczyt licznika), integracja automatycznie ponawia próbę po **5 min**, następnie **15 min** i **30 min**. Po 3 nieudanych próbach wraca do normalnego harmonogramu.

Odświeżenie następuje też po:
- restarcie Home Assistant
- przeładowaniu integracji
- zmianie konfiguracji

## FAQ

**Dlaczego sensory dobowe pokazują dane z poprzedniego dnia?**

eLicznik udostępnia dane z opóźnieniem — dane za dany dzień pojawiają się dopiero następnego dnia.

**Jak wyświetlić dane godzinowe w panelu Energii?**

W ustawieniach integracji włącz opcję **Zapisuj statystyki godzinowe**. Następnie w panelu Energii wybierz encje statystyk (`tauron_importer.*`) zamiast sensorów.

**Skąd pobrać ID licznika?**

ID licznika (`energy_meter_id`) jest wybierane automatycznie z listy podczas konfiguracji przez UI.

**Co oznacza sensor "Należności Mój Tauron"?**

Sensor pobiera informacje o nieopłaconych fakturach z [mój.tauron.pl](https://moj.tauron.pl). Wartość to kwota najbliższej faktury w PLN. Przy braku zaległości (np. nadpłata) sensor wyświetla `0.0 zł`.

**Co zrobić gdy w statystykach brakuje dni?**

Luki pojawiają się gdy eLicznik nie ma danych dla danego dnia (np. błąd odczytu licznika). Po ich uzupełnieniu na stronie eLicznik można wypełnić luki usługą `tauron_amiplus.download_statistics`.

## Wymagania

- Home Assistant 2022.12+
- HACS 1.34.0+
