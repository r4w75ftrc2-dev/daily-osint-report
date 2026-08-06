# Daily Security OSINT Report

Automatický systém pro denní monitoring bezpečnostních událostí se zaměřením na:

- leteckou bezpečnost (aviation security)
- incidenty s UAV/drony
- narušení provozu letišť
- bezpečnostní události v Evropě
- vybrané globální bezpečnostní indikátory

---

## Funkce systému

Systém automaticky:

1. Sbírá články z RSS zdrojů.
2. Klasifikuje články podle témat.
3. Vyhodnocuje úroveň rizika.
4. Překládá vybrané informace do češtiny.
5. Vytváří denní bezpečnostní report.
6. Generuje PDF výstup.
7. Odesílá shrnutí přes Telegram.
8. Archivuje výsledky v repozitáři.

---

## Architektura
RSS zdroje
|
v
collector.py
|
v
articles.json
|
v
classifier_v2.py
|
v
classified_articles_v2.json
|
v
report.py
|
v
daily_report.md
|
+----------------+
| |
v v
pdf_report.py telegram_notify.py
|
v
PDF report

---

## Struktura projektu
daily-osint-report

├── .github/
│ └── workflows/
│ └── daily.yml

├── src/
│ ├── collector.py
│ ├── classifier_v2.py
│ ├── config.py
│ ├── translator.py
│ ├── report.py
│ ├── pdf_report.py
│ └── telegram_notify.py

├── fonts/
│ └── DejaVuSans.ttf

├── reports/
│ └── PDF archiv

├── articles.json
├── classified_articles_v2.json
├── daily_report.md
├── requirements.txt
└── README.md

---

## Automatické spuštění

Workflow je řízen pomocí:

Spuštění:

- automaticky každý den podle nastaveného času
- ručně přes GitHub Actions

---

## Výstupy

### Markdown report

Soubor:
daily_report.md


Obsahuje:

- Executive Summary
- HIGH / MEDIUM / LOW události
- UAV monitoring
- Analyst Note
- odkazy na zdroje

---

### PDF report

Ukládá se do:
eports/


Obsahuje:

- titulní stranu
- statistický přehled
- barevné zvýraznění rizik
- českou diakritiku
- odkazy na zdroje

---

### Telegram

Po dokončení workflow odešle:

- počet HIGH událostí
- počet UAV incidentů
- počet leteckých událostí
- nejvýznamnější událost

---

## GitHub Secrets

Pro Telegram jsou používány:
TELEGRAM_TOKEN
TELEGRAM_CHAT_ID


Nikdy nejsou uloženy přímo v kódu.

---

## Lokální spuštění

Instalace závislostí:

```bash

pip install -r requirements.txt

Spuštění jednotlivých částí:
python src/collector.py

python src/classifier_v2.py

python src/report.py

python src/pdf_report.py

python src/telegram_notify.py

Aktuální verze

Verze:

1.0

Stav:

stabilní automatický provoz
denní generování reportu
Telegram distribuce
PDF archivace
Budoucí rozvoj

Plánované možnosti:

zasílání PDF e-mailem
rozšíření evropského monitoringu
detailnější geografická analýza
odstranění duplicitních zpráv
databáze historických incidentů
pokročilé AI shrnutí


---

Pak:

Commit zpráva:

```text
Add project documentation
