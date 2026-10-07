---
name: automation
description: Die Automationen (Kampagnen, Marketing Cockpit) eines KlickTipp-Kontos bauen, ändern und prüfen — Startbedingung, E-Mails, SMS, Wartezeiten, Entscheidungen, Tags, Ziele, Sprünge — oder eine aus einer fertigen Vorlage starten (Katalog der Business Automation Masterclass oder ein geteilter Vorlagen-Link). Nutze ihn, sobald es um einen Ablauf geht, eine mehrstufige Kampagne, eine Begrüßungsserie, ein Webinar oder einen Termin, eine Kampagnenvorlage oder „was passiert nach X" — und erst recht, wenn du gerade sagen wolltest, ein Teil davon gehe nur im Editor.
---

# KlickTipp-Automationen

Jeder Schritt einer Automation hat ein Werkzeug — Start, E-Mail, SMS, Warten, Entscheidung, Tag,
Ziel, Sprung, Benachrichtigung, Splittest, Ende. Sag nie „das geht nur im Editor". Die einzige
Ausnahme: **Aktivieren** tut ein Mensch in KlickTipp, siehe Reihenfolge, Schritt 7.

Die Werkzeugbeschreibungen kommen aus einer Vorlage und unterscheiden die Aktionstypen kaum. Wähle
nach [references/actions.md](references/actions.md), nicht nach der Beschreibung. Die
veröffentlichten Verträge stehen Wort für Wort in [references/contracts.md](references/contracts.md).

## Mit einer Vorlage anfangen, wenn eine passt

Bevor du einen Ablauf Schritt für Schritt baust, prüfe, ob es ihn fertig gibt:
`search-automation-templates` mit dem Ziel des Nutzers („Termin nachfassen", „Bewertungen sammeln",
„Geburtstag"). Der Katalog enthält die Automationen der Business Automation Masterclass — Termine,
Angebote, Bewertungen, Onboarding, Events, Sales-Funnels — mit ihren E-Mails. Wer einen Link
`…/template/…` einfügt, meint eine geteilte Vorlage; sie läuft über dieselben Werkzeuge.

Finden → `get-automation-template` → Name und Zuordnungen mit dem Nutzer klären →
`import-automation-template` → mit den Werkzeugen unten fertigstellen. Der Import legt die
Automation **pausiert** an und versendet nichts. Ablauf, Argumente und was die Antwort bedeutet:
[references/templates.md](references/templates.md).

## Best Practices — der Normalfall, keine Option

Vor der ersten Aktion prüfen. BP‑1/BP‑2 gehen dem Wortlaut des Nutzers vor; sag in einem Satz, dass
du abgewichen bist. BP‑3/BP‑4 baust du ein, ohne zu fragen.

| | Wann | statt | tu | weil |
|---|---|---|---|---|
| **BP‑1** | auf eine Reaktion warten (geklickt, geöffnet, gekauft) | Warten → Entscheidung | **Ziel**, Warten nur als Obergrenze | wer sofort klickt, liegt sonst 2 Tage herum |
| **BP‑2** | ein fester Termin (Webinar, Launch, Kursstart) | „6 Tage warten" | **Datumsfeld** als Anker jeder Wartezeit | Späteinsteiger bekommen sonst alles zu spät |
| **BP‑3** | Einstieg kurz vor dem Termin | Erinnerungen durchlaufen lassen | **Schranke** vor jeder Erinnerung | vergangene Zeitpunkte feuern sofort |
| **BP‑4** | ein Zweig hängt an „geöffnet"/„geklickt" | stillschweigend bauen | bauen **und** den Bot-Vorbehalt sagen | Provider öffnen und klicken selbst |

## Modell

Ein Graph aus Aktionen mit festen IDs. Jede neue Aktion hängt an einer bestehenden: `afterActionId`
sagt woran, `branch` wohin — `next` nach gewöhnlichen Aktionen, `yes`/`no` nur an Entscheidungen.

- **`revision`** aus dem letzten `get-automation` gehört in jeden Schreibvorgang. Abgewiesen = jemand
  hat den Graphen geändert; neu lesen, wiederholen.
- **Nur inaktive Automationen sind beschreibbar.** Eine laufende hältst du mit `stop-automation`
  an — vorher fragen.
- **`dryRun: true`** rechnet, ohne zu speichern. Immer nutzen, wenn der Anhängepunkt unklar ist.

## Reihenfolge

0. Gibt es eine Vorlage dafür? Siehe *Mit einer Vorlage anfangen* oben.
1. Den Ablauf an den Best Practices messen.
2. `create-automation-draft` — legt den Entwurf **samt** Startaktion an. Die Startaktion nicht selbst
   anlegen; sie wird mit `update-automation-start-action` eingestellt.
3. **Nachricht vor Aktion.** `create-automation-email-draft`, `create-automation-sms-draft`,
   `create-notification-email-draft` oder `create-notification-sms-draft`, Inhalt setzen, dann
   `add-automation-email-action` / `add-automation-sms-action` mit ihrer ID.
4. `get-automation` — Graph, Aktions-IDs, `revision`.
5. Aktionen in Ablaufreihenfolge anhängen. Jede Antwort trägt die Revision für den nächsten Schritt.
6. `validate-automation`.
7. `prepare-automation-activation` — **aktiviert nicht**, es liefert den Link zum Dialog. Den Start
   bestätigt ein Mensch in KlickTipp. Melde nie eine Aktivierung, die nicht stattgefunden hat.

## BP‑1 · Auf eine Reaktion warten ist ein Ziel, kein Warten

„E-Mail, 2 Tage warten, dann prüfen, ob geklickt" lässt den, der nach 5 Minuten klickt, 2 Tage liegen.

Ein Ziel (`add-automation-goal-action`) wird **dort ausgewertet, wo der Kontakt gerade steht** —
auch mitten in einer Wartezeit — und zieht ihn direkt daran vorbei.

> E-Mail → **Ziel „hat geklickt"** → Tag, SMS, …
> daneben das Warten als Obergrenze → Zweig für alle, die nicht reagiert haben

„2 Tage warten und dann prüfen" heißt fast immer „sobald, spätestens nach 2 Tagen". Ein festes
Warten nur, wenn es ausdrücklich gewollt ist (eine Frist, eine Sperrfrist).

- Ein Ziel wirkt in der **ganzen** Automation, nicht an seiner Position.
- **Pro Durchlauf zählt nur das erste erreichte Ziel.** Mehrere Ziele sind Alternativen, keine Stationen.
- Ein Ziel, **an dem nichts hängt, bewirkt nichts**; `validate-automation` meldet es.
- Ein Ziel ist Knoten **und** globale Bedingung. Den Anhängepunkt mit `dryRun` prüfen, dann
  `get-automation` lesen.

## BP‑4 · Öffnungen und Klicks können Maschinen sein

Provider und Sicherheitsscanner laden Bilder und rufen Links vorab ab (Gmail regelmäßig) → „geöffnet"
und „geklickt" ohne Menschen. Mit abgeschalteten Bildern zählt eine echte Öffnung nicht.

Ein Klick ist das stärkere Signal, kein Beweis. Vor einem Zweig, der etwas Sichtbares tut (SMS,
Verkaufsmail, Rabatt): den Vorbehalt sagen. Maschinensicher sind nur eine Antwort, ein Formular, ein Kauf.

## BP‑2 · Terminkampagnen hängen am Termin

`days` zählt ab dem Moment, in dem **dieser** Kontakt die Aktion erreicht. Wer 5 Tage später
einsteigt, wartet weitere 6. Im Entwurf unsichtbar, erst im Betrieb sichtbar.

1. Hinter der Startaktion `add-automation-set-field-action`: Datum **und Uhrzeit** in ein
   Datum/Zeit-Feld. Operator aus `get-automation-editor-capabilities`, Feld-ID aus
   `search-automation-editor-references`.
2. Jede Wartezeit über `delayField`; `delayTime` **negativ = vor** dem Termin:

   | Ziel | settings |
   |---|---|
   | 24 h vorher | `{"delayType": "customfield hours", "delayTime": -24, "delayField": "<Feld>"}` |
   | 1 h vorher | `{"delayType": "customfield hours", "delayTime": -1, "delayField": "<Feld>"}` |
   | zum Termin | `{"delayType": "from field", "delayField": "<Feld>"}` |
   | am Tag danach | `{"delayType": "customfield days", "delayTime": 1, "delayField": "<Feld>"}` |

3. Entscheidungen und Sprünge an dieselbe Achse hängen.
4. **Das Feld am Ende leeren** — sonst trägt der Kontakt das Datum in jeden weiteren Durchlauf und in
   jede Automation, die dasselbe Feld liest.

**Vorher fragen:** Datum, Uhrzeit, ob es sich wiederholt. Ohne Uhrzeit gibt es kein „eine Stunde
vorher", und ein reines Datumsfeld schiebt jede Erinnerung auf Mitternacht.

Ohne festen Termin (Begrüßungsserie, Nachfass-Sequenz) sind gewöhnliche Wartezeiten richtig.

## BP‑3 · Späteinsteiger und leere Felder

**Vergangene Zeitpunkte warten nicht, sie sind fällig.** Wer sich 1 h vor dem Webinar anmeldet,
läuft ohne Pause durch „24 h vorher", „12 h vorher", „1 h vorher" → drei Erinnerungen auf einmal.

- **Schranke vor jeder Erinnerung:** Entscheidung mit `is after`, `field` = das Datumsfeld, `value`
  relativ (`+24 hours`, `+1 hour`). Der Nein-Zweig springt mit `add-automation-go-to-action` zur
  nächsten Aktion, die noch in der Zukunft liegt.
- **Anmeldung nach dem Termin** direkt hinter dem Setzen des Feldes abzweigen → Aufzeichnung,
  nächster Termin oder Ende.
- **Ein leeres Datumsfeld heißt gar kein Warten**, auch für jede folgende Wartezeit. Aus zwei Wochen
  werden Sekunden. Einmal am Anfang mit `is not empty` prüfen.

## Bedingungen und IDs

Rate weder IDs noch Operatoren.

- `get-automation-editor-capabilities` — erlaubte Aktionstypen, Schema der `settings`,
  Pflichtfelder, Bedingungsoperatoren, Plugin-Bedingungen.
- `search-automation-editor-references` — Name → ID für E-Mails, SMS, Tags, Felder, Signaturen,
  Kalender, Outbounds, Automationen, Segmente.
- `search-automations` — eine bestehende Automation des Kontos finden.

**Öffnungen und Klicks sind Tags.** „Hat E-Mail 1 geöffnet" läuft über den Smart-Tag der Nachricht
aus `get-automation-email` / `get-notification-email`. Diese ID gehört in `field` — nicht die E-Mail-ID.

## Fallen

| | |
|---|---|
| `emailID` bei SMS | heißt auch dort `emailID`, meint aber die ID eines **SMS**-Entwurfs. Gleiches gilt für beide Benachrichtigungsaktionen. |
| leerer Entscheidungszweig | erlaubt. Nichts anzuhängen ist ein fertiger Ablauf. |
| `delete-automation-action` | braucht an einer Entscheidung `keep_yes`, `keep_no` oder `subtree`, sonst `keep_next` oder `subtree`. Die E-Mails bleiben. |
| `move-automation-action` | `subtree` nimmt den folgenden Graphen mit; eine Entscheidung mit gefüllten Zweigen nur als Teilbaum. |
| `copy-automation-action` | neue Aktions-ID, **dieselbe** Nachricht. Wer den Text der Kopie ändert, trifft das Original — vorher mit `copy-automation-email` / `copy-automation-sms` kopieren. Für eine Benachrichtigung gibt es über diese Verbindung kein Kopierwerkzeug: einen neuen Entwurf anlegen. |
| `add-automation-go-to-action` | springt zu einer Aktions-**ID** aus `get-automation`, nicht zu einem Namen. |
| SMS-Testversand abgelehnt | Die Ablehnung nennt `check-sms-readiness`; das gibt es über diese Verbindung nicht. Prüfe mit `get-automation-sms`, ob Anbieter, Absender und Text gesetzt sind. |

## Was diese Verbindung nicht kann

Eine Automation oder einen Automations-Entwurf **löschen**, die Facebook-Audience- und
FullContact-Aktionen, die personalisierte Vorschau und den Spam- und Linkcheck einer
Automations-E-Mail. Das geht in KlickTipp selbst; sag es so, statt einen Umweg zu bauen. Einen
Entwurf, den niemand mehr braucht, lässt du inaktiv stehen.

## Grenzen

E-Mail-**Inhalt** (HTML, Blöcke, Gestaltung) → `email`. Einzelne Aussendungen → `newsletter`.
Kontakte → `contacts`, Tags → `tags`, Felder als solche → `custom-fields`. Was eine Automation
erreicht hat → `dashboard`.

## Bevor du schreibst

Bauen erreicht niemanden (der Entwurf ist inaktiv), und ein Vorlagen-Import auch nicht — die
importierte Automation ist pausiert. Beides legt aber Objekte im Konto an, die bleiben; Name und
Zuordnungen also vor dem Import klären, nicht danach. `stop-automation` und
`move-automation-contacts` greifen in den laufenden Betrieb ein: **sag, was passiert, hol die
Zustimmung, dann ruf auf.** Ein Testversand an eine Adresse, die das Konto noch nicht kennt, legt
einen getaggten Kontakt an, der Automationen starten kann; ein SMS-Test kostet SMS-Guthaben.
