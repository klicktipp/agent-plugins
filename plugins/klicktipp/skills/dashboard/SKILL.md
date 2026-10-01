---
name: dashboard
description: Die Zahlen eines KlickTipp-Kontos als Dashboard — welche E-Mails gut liefen und welche nicht, Zustellung, Öffnungen, Klicks, Bounces, Abmeldungen der Aussendungen, die tägliche Aktivität des Kontos, Tags über die Zeit, Automationen und ihre E-Mails und SMS. Nutze ihn bei Report, Auswertung, Statistik, Öffnungs- oder Klickrate, Zustellbarkeit oder dem Vergleich mehrerer Aussendungen. Baut das Dashboard als Claude-Artifact oder im Canvas von ChatGPT und Codex. Nur lesend.
---

# KlickTipp Dashboard

Ein Dashboard ist nur so gut wie die Zahlen darunter. Dieser Skill beschreibt, **welche Zahlen das
Konto überhaupt hergibt**, wie man sie günstig einsammelt, wie man sie richtig liest, und wie
daraus eine Seite wird, die jemand ohne Erklärung versteht.

Die Reihenfolge ist Absicht: erst messen, dann rechnen, dann gestalten. Ein hübsches Dashboard mit
einer falsch gerechneten Öffnungsrate ist schlechter als gar keins, weil ihm geglaubt wird.

Die veröffentlichten Verträge der Statistik-Werkzeuge, Wort für Wort mit jedem Parameter, stehen in
[references/contracts.md](references/contracts.md).

## 1. Was es wirklich gibt — und was nicht

Das ist der wichtigste Abschnitt. Die häufigste Art, hier zu scheitern, ist eine Kennzahl zu
versprechen, die die Werkzeuge nicht hergeben, und sie dann zu schätzen, ohne es zu sagen.

| Frage | Antwort | Woher |
| --- | --- | --- |
| Wie steht das Konto insgesamt da? | **ein Aufruf** | `get-account-statistics` — die letzten zehn Aussendungen mit Raten, die Tags mit dem meisten Zuwachs heute, die Aktivität je Tag, die Mailanbieter der Kontakte, die Bounces nach Art |
| Was hat eine Aussendung erreicht? | **vollständig** | `get-campaign-statistics` — E-Mail- und SMS-Newsletter und jeder Autoresponder |
| Wann ging sie raus, in welchem Zustand ist sie? | **vollständig** | `search-newsletters` (Versanddatum) · `get-newsletter`, `include: ["deliveryStatus"]` |
| Wie viele erreicht ein Versand gerade? | **vollständig** | `get-newsletter`, `include: ["audienceReach"]` |
| Wie haben Kontakte einen Tag über die Zeit bekommen? | **je Stunde, Tag, Monat, Jahr** | `get-tag-statistics` |
| Was hat ein Splittest ergeben? | **vollständig** | `get-newsletter-split-test-statistics`, Skill `splittest` |
| Wie läuft eine Automation, wo warten ihre Kontakte? | **mit ihrer ID** | `get-automation-statistics` · `get-automation-waiting-contact-counts` |
| Was hat eine E-Mail oder SMS einer Automation erreicht? | **mit ihrer ID** | `get-automation-email-statistics` · `get-automation-sms-statistics` |
| **Wie viele Kontakte hat das Konto?** | **gibt es nicht** | siehe unten |

**Die Kontaktzahl ist die Lücke.** `search-contacts` ist Cursor-paginiert, maximal 100 pro Seite,
und liefert **keine Gesamtzahl**. Ein Konto mit 80.000 Kontakten zu zählen hieße 800 Aufrufe. Tu
das nicht. Auch `ispShares` aus `get-account-statistics` ist keine Kontaktzahl, sondern eine
Verteilung — addier sie nicht zu einer Summe, die niemand gemessen hat.

Nimm stattdessen `audienceReach` eines Newsletters mit Zielgruppe `all_contacts`: das ist die Zahl
der aktiven Kontakte, die KlickTipp selbst berechnet, in einem Aufruf. Es kommen `minRecipients`
und `maxRecipients` zurück — sind sie verschieden, ist es eine Spanne, und dann zeig eine Spanne.
Gibt es keinen solchen Newsletter, **lass die Kachel weg**, statt eine Zahl zu erfinden.

**Automationen brauchen ihre ID von außen.** Die vier Automations-Werkzeuge nehmen eine
Automations-, E-Mail- oder SMS-ID, aber kein Werkzeug dieses Plugins listet Automationen auf.
`get-campaign-statistics` weist eine Automation ab und verweist auf `get-automation-statistics`.
Die ID steht in der App-URL der Automation; frag danach, statt zu raten. Eine Aktions-ID der
Automation ist **keine** E-Mail- oder SMS-ID.

## 2. Einsammeln, ohne das Konto leerzulesen

Für den Überblick reicht oft ein einziger Aufruf:

```
get-account-statistics  days=30                 → die letzten zehn Aussendungen, Aktivität,
                                                  Tags, Anbieter, Bounces
```

Mehr als zehn Aussendungen, oder ein bestimmter Zeitraum:

```
search-newsletters  status="sent"  sendDateFrom=…  sendDateBefore=…  limit=25
  └─ je Newsletter: get-campaign-statistics  campaignId=<newsletterId>
search-newsletters  status="draft"  limit=1     → nur für die Zählung
search-newsletters  status="scheduled" limit=1  → dito
```

Die `newsletterId` aus `search-newsletters` ist die `campaignId` von `get-campaign-statistics`.
Für die auffälligen Aussendungen kommt je ein `get-newsletter` mit `include: ["metadata"]` dazu —
der Betreff (Abschnitt 4). Das sind etwa 30 bis 40 Aufrufe für ein volles Dashboard. Drei Regeln halten es dabei:

**Ein Zeitraum, nicht „alles".** Frag nach dem Zeitraum, oder nimm die letzten 90 Tage und schreib
es hin. `sendDateFrom` und `sendDateBefore` sind halboffen — „From" schließt ein, „Before" schließt
aus — und ISO 8601 mit explizitem Offset (`2026-09-01T10:00:00+02:00`).

**Der Zeitraum wählt Aussendungen aus, nicht Zähler.** Die Zahlen von `get-campaign-statistics`,
`get-automation-*-statistics` und die Lebenszeit-Summen von `get-automation-statistics` sind
**Summen über die ganze Lebenszeit** und nicht auf einen Zeitraum beschränkt. Eine Öffnung von
gestern auf einen Newsletter vom Juni zählt beim Juni-Newsletter. Schreib das dazu, wenn ein
Zeitraum über der Seite steht. Nur `get-tag-statistics` antwortet wirklich über einen Zeitraum,
`get-account-statistics` mit `activity` je Tag, und `get-automation-statistics` mit `conversion`
zwischen `from` und `to`.

**Entwürfe haben kein Versanddatum.** Ein Entwurf fällt in kein `sendDate`-Fenster, auch wenn ein
Termin gesetzt und wieder abgesagt wurde. Für „wie viele Entwürfe liegen herum" zählst du über
`status="draft"`, nicht über ein Zeitfenster.

Wird die Liste lang, kommt ein `nextCursor` zurück: unverändert zurückgeben, zusammen mit
**denselben** Filtern. Ein Cursor aus einer anderen Suche wird abgewiesen.

## 3. Lesen und rechnen — hier werden Dashboards falsch

**Die Raten kommen fertig.** `get-campaign-statistics` und `get-account-statistics` liefern sie so,
wie das KlickTipp-Dashboard sie rechnet, in **Prozent mit einer Nachkommastelle** — `42.3` heißt
42,3 %, nicht 4230 %. Rechne sie nicht selbst nach anderen Formeln nach: dann stünde im Report eine
andere Zahl als in der App, und beide wären „richtig".

| Feld | Nenner | Was es ist |
| --- | --- | --- |
| `openRate` | `sent` | Öffnungsrate |
| `clickRate` | **`opensUnique`** | **Klick-zu-Öffnung (CTOR)** — der Anteil der Leser, die klickten. Nicht die Klickrate über alle Empfänger |
| `clickRateOfRecipients` | `sent` | Klickrate über alle Empfänger — die Zahl, die man neben die Öffnungsrate stellt |

**`clickRate` ist die Falle.** Wer sie als „Klickrate" beschriftet, zeigt eine Zahl, die um den
Kehrwert der Öffnungsrate größer ist als das, was der Leser unter dem Wort versteht — bei 25 %
Öffnungen das Vierfache. Beschrifte sie als
„Klick-zu-Öffnung" und stell `clickRateOfRecipients` als „Klickrate" daneben. In
`recentCampaigns` von `get-account-statistics` gibt es nur `openRate` und `clickRate` — dort ist
`clickRate` dieselbe Klick-zu-Öffnung.

Was nicht fertig kommt, rechnest du aus den Zählern, immer über `sent`:

| Kennzahl | Formel | Fallstrick |
| --- | --- | --- |
| Zustellrate | `sent / recipients` | `failed` sagt, was nicht rausging |
| Bounce-Rate | `(hardBounces + softBounces + spamBounces) / sent` | hart, weich und Spam **getrennt** zeigen — hart ist eine tote Adresse, weich ein Moment, Spam eine Ablehnung als Spam |
| Abmelderate | `unsubscriptions / sent` | |
| Beschwerderate | `spamComplaints / sent` | die wichtigste Zahl im Dashboard, siehe unten |

**Teile nie durch null, und zeig keine Null, die keine ist.** Eine Aussendung, die noch nicht
rausging, antwortet mit Nullen, und die fertigen Raten sind dann `0.0`. Bei `sent: 0` zeig „—",
nicht „0 %" und nicht `NaN`.

**SMS haben keine Öffnungen.** Für eine SMS-Kampagne sind `opensTotal`, `opensUnique`, `openRate`,
`clickRate` und die Browser-Ansichten `null` — nicht null Prozent, sondern nicht vorhanden. Dort ist
`clickRateOfRecipients` die Kennzahl. Mischt die Seite E-Mail und SMS, steht bei der SMS
„keine Öffnungen (SMS)", nicht ein leeres Feld.

**`opensTotal` gehört trotzdem hin**, aber als eigene Zahl: `opensTotal / opensUnique` sagt, wie
oft eine Öffnerin im Schnitt zurückkommt. Das ist interessant und wird selten gezeigt.

**Sag dazu, was eine Öffnung heute wert ist.** Apple Mail Privacy Protection lädt Bilder vorab, ohne
dass jemand die Mail gesehen hat. Öffnungsraten sind dadurch nach oben verzerrt und über die Zeit
nicht sauber vergleichbar. Ein Dashboard, das die Öffnungsrate groß und unkommentiert zeigt, führt
in die Irre — **Klicks sind das härtere Signal**, und der Skill stellt sie deshalb gleichberechtigt
daneben.

**`links` ist schon sortiert**, meistgeklickt zuerst, mit `clicksTotal` und `clicksUnique`. Für
„welcher Link zog" reicht die Liste; sie gehört in die Detailansicht einer Aussendung.

### Was die übrigen Werkzeuge sagen — und was nicht

- **`get-account-statistics`.** `activity` hat je Tag Anmeldungen, Abmeldungen, SMS-Anmeldungen,
  Importe, Bounces und Beschwerden, **aber keine Versände, Öffnungen oder Klicks** — die gibt es
  nur je Aussendung. `days` (1–90) wirkt nur auf `activity`. `topTags` ist der Zuwachs von heute,
  gestern und vorgestern, kein Ranking über den Zeitraum.
- **`get-tag-statistics`.** Zählt die Kontakte, die den Tag **jetzt** tragen, jeweils in der
  Periode, in der sie ihn zuletzt bekamen. Ein wieder entfernter Tag zählt nirgends, ein zweites
  Taggen verschiebt den Kontakt in die neuere Periode — kein Protokoll jeder Vergabe. **Eine
  fehlende Periode heißt null**, nicht „keine Daten": füll sie im Diagramm mit null auf, statt die
  Linie über die Lücke zu ziehen. Höchstens zehn Tags und 2000 Perioden je Aufruf; `from`/`to` sind
  Unix-Zeitstempel.
- **`get-automation-statistics`.** `totals` sind Lebenszeit-Summen. `conversion` gilt nur zwischen
  `from` und `to` und ist `null`, wenn das Konto keine Conversion-Statistik hat
  (`conversionAvailable: false`) — dann die Conversion-Kachel weglassen und den Grund nennen.
- **`get-automation-waiting-contact-counts`.** Eine Momentaufnahme, wer gerade an welcher Aktion
  wartet. Aktionen ohne Wartende fehlen in der Liste.
- **`get-automation-email-statistics`.** Eine **Benachrichtigungs-E-Mail** zählt keine Versände,
  Öffnungen und Klicks: `sent`, `opened`, `clicked` sind `null`, `links` ist leer. Nur Bounces und
  Beschwerden gibt es dort.
- **`get-automation-sms-statistics`.** Keine Öffnungen, `clickRateOfRecipients` wie bei
  `get-campaign-statistics`. Eine SMS ohne Versand antwortet mit Nullen und ohne Bounces.
- **`get-newsletter-split-test-statistics`.** Der Gewinner wird **gemeldet, nie berechnet**:
  solange `isDecided` `false` ist, gibt es keinen, auch wenn eine Variante vorn liegt. Zeig dann
  „Test läuft", keinen Sieger.

### Was hervorzuheben ist

Nicht alle Zahlen sind gleich wichtig. Zwei verdienen eine Warnfarbe, weil an ihnen die
Zustellbarkeit des ganzen Kontos hängt:

- **Beschwerden über 0,1 %** — das ist die Schwelle, an der große Anbieter anfangen, den Absender
  schlechter zuzustellen.
- **Harte Bounces über 2 %** — deutet auf eine gekaufte oder alte Liste hin und beschädigt die
  Reputation der Absenderdomain.

Diese beiden Grenzen sind Branchenübliches, keine KlickTipp-Einstellung; schreib sie als
Orientierung dazu, nicht als Urteil.

## 4. Was lief gut, was nicht

Das ist die Frage hinter fast jedem Report: **welche E-Mails haben funktioniert, welche nicht, und
woran lag es vermutlich.** Eine Tabelle mit Raten beantwortet sie nicht — der Leser müsste selbst
vergleichen. Das Dashboard tut es für ihn, und zwar so, dass das Urteil prüfbar bleibt.

### Der Maßstab ist das eigene Konto

Beurteile jede Aussendung gegen den **Median des Kontos** im selben Zeitraum, nicht gegen
Branchenwerte. Öffnungsraten hängen an Liste, Branche und Mailanbietern; „22 % ist gut" stimmt für
das eine Konto und ist für das andere ein Einbruch. Der Median, nicht der Mittelwert: eine einzelne
Mail an 50 treue Kunden zieht einen Mittelwert hoch, den Median nicht.

Zeig je Aussendung die **Abweichung vom Median in Prozentpunkten** („Klickrate 3,1 %, +1,2 Pp über
dem Median"). Die einzigen festen Grenzen bleiben die zwei aus Abschnitt 3 — Beschwerden und harte
Bounces.

### Welche Zahl was beurteilt

| Was beurteilt wird | Kennzahl | Lies so |
| --- | --- | --- |
| Betreff, Absender, Versandzeit — wurde die Mail geöffnet? | `openRate` | nur relativ innerhalb des Kontos, wegen Apple Mail Privacy Protection |
| Inhalt — hat er die Leser zum Klicken gebracht? | `clickRate` (Klick-zu-Öffnung) | die ehrlichste Inhaltskennzahl: misst den Inhalt, nicht den Betreff |
| Wirkung insgesamt | `clickRateOfRecipients` | was von allen Empfängern übrig blieb |
| Wert | `conversionsUnique / sent` | nur mit Conversion-Pixel; sonst „nicht gemessen", nicht 0 |
| Schaden | `unsubscriptions`, `spamComplaints`, `hardBounces` je `sent` | eine Mail mit guten Klicks und doppelt so vielen Abmeldungen wie üblich ist kein Erfolg |

Die Kombination sagt mehr als jede Zahl allein — und genau sie gehört als **Vermutung** an jede
auffällige Aussendung:

| Muster | Naheliegende Vermutung |
| --- | --- |
| Öffnungen hoch, Klick-zu-Öffnung niedrig | der Betreff verspricht etwas, das der Inhalt nicht hält |
| Öffnungen niedrig, Klick-zu-Öffnung hoch | der Inhalt trägt, Betreff oder Versandzeit nicht |
| beides hoch | Thema und Aufmachung passen — das ist die Mail, an der man sich orientiert |
| Abmeldungen oder Beschwerden deutlich über dem Median | Thema, Ton oder Frequenz stößt ab, unabhängig von den Klicks |
| ein Link zieht fast alle Klicks | der Rest des Inhalts arbeitet nicht mit; `links` zeigt welcher |

### Wann eine Aussendung auffällt

Als Faustregel, die du dazuschreibst:

- **Auffällig** ist eine Rate, die **mehr als ein Viertel** über oder unter dem Median liegt.
- **Zu klein zum Urteil** ist eine Aussendung mit weniger als **200 Versendeten** — dort entscheidet
  ein Dutzend Menschen über die Rate. Zeig sie, aber ohne Urteil und ohne Platz in Top oder Flop.
- **Noch frisch** ist eine Aussendung, die jünger als **drei Tage** ist: die Zähler sind
  Lebenszeit-Summen und wachsen noch. Markier sie, statt sie mit fertigen zu vergleichen.

Vergleiche nur Vergleichbares: **E-Mail und SMS getrennt** (SMS haben keine Öffnungen), und wo die
Zielgruppen sehr verschieden sind — ein Newsletter an alle, eine Mail an ein Tag mit 300
Stammkunden —, sag das neben dem Vergleich. `get-newsletter` mit `include: ["audience"]` zeigt,
an wen eine Aussendung ging.

### Was dazugehört, um es zu erklären

Für die auffälligen Aussendungen — nicht für alle — lies nach, was eine Vermutung stützt:

- **Betreff**: `get-newsletter` mit `include: ["metadata"]`. Ohne Betreff ist jede Aussage über
  Öffnungen geraten.
- **Versandzeit**: Wochentag und Uhrzeit aus dem Versanddatum von `search-newsletters`.
- **Der stärkste Link**: der erste Eintrag in `links` von `get-campaign-statistics`.

**Ein entschiedener Splittest ist der einzige echte Beweis.** Er schickt Varianten zur selben Zeit an
dieselbe Zielgruppe; alles andere hier ist Korrelation. Gibt es im Zeitraum einen, gehört
`get-newsletter-split-test-statistics` mit seinem Gewinner in diesen Abschnitt.

**Automationen** werden nicht gegen Newsletter verglichen, sondern Schritt gegen Schritt: die
E-Mails einer Automation mit `get-automation-email-statistics` nebeneinander zeigen, wo Leser
aussteigen.

## 5. Die Seite

**Bau das Dashboard immer, statt die Zahlen nur aufzuzählen** — als **eine** einzelne, in sich
geschlossene HTML-Seite, die direkt im Gespräch erscheint: bei Claude als **Artifact**, bei Codex
und ChatGPT im **Canvas**. Nicht als Datei mit einem Pfad daneben, und nicht als Tabelle im
Fließtext. Ein Report soll sich öffnen und weiterreichen lassen, ohne dass jemand erst etwas
herunterlädt.

Wie das geht, hängt von der Umgebung ab, und das ist der einzige Unterschied:

| Umgebung | Weg |
| --- | --- |
| Claude Code | das `Artifact`-Werkzeug: HTML-Datei schreiben, dann veröffentlichen |
| claude.ai, Claude Desktop | ein Artifact direkt in der Antwort |
| ChatGPT | im Canvas, als HTML-Seite, die der Canvas als Vorschau rendert |
| Codex | im Canvas, wo es ihn gibt; sonst `.html` schreiben und den Pfad nennen — inhaltlich identisch |

**Das Handwerk steht in [references/craft.md](references/craft.md)** — Farbtokens für Hell und
Dunkel, Schriftwahl, der Aufbau einer Kennzahl-Kachel, Liniendiagramme in reinem SVG samt
Trefferflächen, Hover mit Tastatur-Entsprechung, und eine Prüfliste für den Schluss. Die Datei
setzt nichts voraus: keine Bibliothek, kein CDN, keinen weiteren Skill. Lies sie, bevor du die
Seite schreibst.

Was hier steht, ist nur, was dieses Dashboard **inhaltlich** braucht:

1. **Kopf**: Kontoname, Zeitraum und **der Beobachtungszeitpunkt** — wann du gemessen hast
   (`deliveryStatus` liefert ihn als `observedAt`, sonst die Uhrzeit deiner Aufrufe). Ein Dashboard
   ohne Datum wird Wochen später für aktuell gehalten.
2. **Kachelreihe**: erreichte Kontakte, Aussendungen im Zeitraum, Zustellrate, Öffnungsrate,
   Klickrate (`clickRateOfRecipients`), Klick-zu-Öffnung. Jede Kachel mit der absoluten Zahl
   **unter** der Prozentzahl — Prozente ohne Basis sind nicht prüfbar.
3. **Was lief gut, was nicht** — direkt unter den Kacheln, weil es die Frage ist, mit der jemand
   den Report öffnet: die **drei stärksten und drei schwächsten** Aussendungen nach Klickrate und
   Klick-zu-Öffnung, jede mit ihrer Abweichung vom Median, Betreff, Versandzeit, stärkstem Link und
   **einem Satz Vermutung**, als Vermutung beschriftet. Dazu jede Aussendung, deren Abmeldungen oder
   Beschwerden auffallen, auch wenn ihre Klicks gut sind. Siehe Abschnitt 4.
4. **Tabelle je Aussendung**, nach Versanddatum absteigend: Name, Datum, versendet, Öffnungsrate,
   Klickrate, Klick-zu-Öffnung, Bounces, Abmeldungen — jede Rate mit einer Markierung über oder
   unter dem Median, und „zu klein" oder „noch frisch", wo es zutrifft. Mit `statisticsUrl` aus der
   Antwort verlinkt, damit man von jeder Zeile in die App springen kann.
5. **Verlauf**, sobald es mehr als drei Aussendungen sind: Öffnungs- und Klickrate über der Zeit,
   mit dem Median als ruhige Bezugslinie. Ein Punkt je Aussendung, keine Interpolation zwischen
   Terminen, die nichts miteinander zu tun haben.
6. **Aktivität des Kontos**, wenn danach gefragt ist: Anmeldungen und Abmeldungen je Tag aus
   `activity`, ein Tag-Verlauf aus `get-tag-statistics`, die Mailanbieter aus `ispShares`.
7. **Fußzeile**: welche Werkzeuge gelesen wurden, dass die Zähler Lebenszeit-Summen sind, welche
   Faustregeln die Markierungen setzen, und was **nicht** enthalten ist.


### Erst die Zahlen, dann die Seite

Schreib die gemessenen Werte **zuerst** in eine kleine, getippte JSON-Struktur — Kopf, eine Zeile
je Newsletter, die abgeleiteten Quoten — und rendere die Seite daraus. Zwei Gründe, und beide
zahlen sich beim ersten Nachbessern aus:

- Die Zahlen sind prüfbar, **ohne HTML zu lesen**. Ein Streit über eine Kachel wird an der
  Datenstruktur entschieden, nicht im Markup.
- Ein Umbau der Gestaltung misst **nicht neu**. Ohne diese Trennung kostet jede Layout-Runde
  wieder 30 Werkzeugaufrufe, und die Zahlen ändern sich zwischendurch.

### Interaktion, die sich verdient hat, da zu sein

Nicht alles, was klickbar sein kann, hilft. Was bei einem Report trägt:

- **Hover auf einem Datenpunkt zeigt die exakten Zahlen** — absolut und in Prozent. Ein Diagramm,
  aus dem man den Wert nur schätzen kann, erzwingt die Tabelle daneben; mit Hover ergänzen sich
  beide.
- **Eine Zeile führt in die App.** `statisticsUrl` aus der Antwort ist der Sprung von der
  Beobachtung zur Ursache.
- **Ein Umschalter zwischen Öffnungs- und Klickrate** in derselben Achse, statt zweier Diagramme
  nebeneinander: so vergleicht man die beiden Kurven wirklich.
- **Tastatur und Fokus** funktionieren mit. Ein Report wird weitergereicht, auch an Leute, die
  nicht mit der Maus arbeiten.

Was **nicht** hilft: Animationen beim Laden, Tooltips, die nur wiederholen, was daneben steht, und
Filter, die Zahlen verändern, ohne dass die Kopfzeile es sagt.

### Die Seite muss halten, was sie zeigt

Vier Dinge, die eine hübsche Seite von einer belastbaren trennen — ausführlich in
[references/craft.md](references/craft.md):

1. **In sich geschlossen.** SVG inline, CSS und JS inline, **kein CDN**. Ein Report wird Wochen
   später geöffnet, oft ohne Netz — und ein nachgeladenes Diagrammpaket ist dann ein leerer Kasten.
2. **Hell und dunkel**, beides absichtlich gestaltet. Die Farben der Warnschwellen müssen in beiden
   lesbar bleiben; ein Rot, das auf Dunkel verschwindet, ist genau da unlesbar, wo es zählt.
3. **Kein horizontales Scrollen.** Prüf die fertige Seite bei **1440×900 und 1920×1080** und
   verlange `scrollWidth <= innerWidth`. Repariere Überlauf, indem du Inhalt wegnimmst oder
   Abstände straffst — **niemals** mit `overflow: hidden`, einem inneren Scroller oder kleinerer
   Schrift. Das versteckt den Fehler, statt ihn zu beheben. Breite Tabellen dürfen in einem eigenen
   `overflow-x: auto`-Container scrollen; die Seite selbst nicht.
4. **Exportierbar.** Ein Report wird weitergeschickt. Wenigstens „als PNG speichern" sollte gehen —
   und der Export darf keinen Bedienzustand mitnehmen, kein offenes Tooltip, keinen Hover.

**„Sieht gut aus" ist keine Prüfung.** Ein Blick auf die Seite ersetzt weder das Nachrechnen der
Quoten noch die Messung der Breite bei den beiden Fenstergrößen. Sag getrennt, was du geprüft hast
und was du nur gesehen hast.

### Wenn ein Ablauf gezeigt werden soll

Für den **Lebenszyklus** einer Aussendung — Entwurf, geplant, im Versand, versendet, samt Splittest
und seinem Gewinner — ist ein Dashboard das falsche Bild: das ist ein Zustandsdiagramm und gehört
nicht in Kacheln. Zeichne es als eigenes SVG daneben, nach denselben Regeln aus
[references/craft.md](references/craft.md), oder lass es weg. Ein Ablauf, den man aus fünf Kacheln
zusammenreimen muss, ist keiner.

### Drei Regeln, die dieses Dashboard ehrlich halten

**Jede Zahl trägt ihre Basis.** „42 % (1.208 von 2.876)" statt „42 %".

**Fehlendes wird benannt, nicht überbrückt.** Fehlt eine Kennzahl, steht dort „nicht verfügbar" mit
einem Halbsatz warum — nicht ein Strich, den man für eine Null hält.

**Ein Urteil nur mit Maßstab und Basis.** „Stark" heißt „über dem Median des Kontos", mit der Zahl
dazu — und nie bei weniger als 200 Versendeten oder bei einer Aussendung, die noch Zähler sammelt.
Die Tabelle bleibt nach Datum sortiert; das Urteil steht im eigenen Abschnitt, wo man sieht, worauf
es beruht.

## 6. Was dieser Skill nicht tut

- **Er schreibt nichts.** Kein Newsletter, kein Kontakt, kein Tag. Wenn aus einer Erkenntnis eine
  Handlung folgen soll, ist dafür der Skill `newsletter` zuständig.
- **Er kürt keinen Splittest-Gewinner.** Den meldet `get-newsletter-split-test-statistics`, oder es
  gibt noch keinen.
- **Er findet keine Automationen.** Ohne ID aus der App gibt es keine Automations-Zahlen.
- **Er zählt keine Kontakte durch.** Siehe Abschnitt 1.
- **Er beweist keine Ursachen.** „Der Betreff hat nicht gezogen" ist eine Vermutung, gestützt auf
  ein Muster aus Abschnitt 4 — schreib sie als solche hin, mit den Zahlen, auf denen sie beruht.
  Bewiesen ist nur, was ein entschiedener Splittest zeigt.
