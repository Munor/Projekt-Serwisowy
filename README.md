Projekt Serwisowy
-----------------

Aplikacja webowa do zarządzania zgłoszeniami serwisowymi, oparta na Flask i SQLAlchemy z SQLite.

Funkcjonalności:
- Dodawanie zgłoszeń (klienci/firmy)
- Typ urządzenia i producent (dla laptopów)
- Numer seryjny, opis problemu
- Lista zgłoszeń z opcją wydania

Struktura:
service_app/
├── service_manager.py
├── models.py
├── static/css/styl.css
├── templates/add.html
├── templates/index.html
└── service.db

Wymagania:
- Python 3.8+
- Flask, Flask-SQLAlchemy (pip install flask flask-sqlalchemy)

Instalacja:
1. Sklonuj: git clone [URL]
2. Wejdź: cd Projekt-Serwisowy
3. Zainstaluj: pip install flask flask-sqlalchemy
4. Uruchom: python service_manager.py
5. Otwórz: http://127.0.0.1:5000/

Użycie:
- Lista: / - przeglądaj i wydaj
- Dodaj: /add - wypełnij formularz

Baza danych:
- SQLite (service.db)
- Tabela: requests (id, dane klienta/firmy, typ, numer seryjny, opis, status)

Autor: Mikołaj
Planowane funkcjonalności:
Edycja zgłoszeń – możliwość zmiany danych przed wydaniem.
Wyszukiwanie i filtrowanie – po nazwisku, sprzęcie, statusie.
Walidacja danych – sprawdzanie poprawności formularzy.
Logowanie – dostęp tylko dla uprawnionych użytkowników.
Lepszy interfejs – Poprawa responsywności.
