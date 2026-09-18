---
name: dashboard
description: Die Zahlen der letzten Aussendungen eines KlickTipp-Kontos als Dashboard — Zustellung, Öffnungen, Klicks, Bounces, Abmeldungen. Nutze ihn bei Report, Auswertung, Öffnungs- oder Klickrate, Zustellbarkeit oder dem Vergleich mehrerer Aussendungen. Nur lesend.
---

# KlickTipp Dashboard

Ein Dashboard ist nur so gut wie die Zahlen darunter. Dieser Skill beschreibt, **welche Zahlen das
Konto überhaupt hergibt**, wie man sie günstig einsammelt, wie man sie richtig rechnet, und wie
daraus eine Seite wird, die jemand ohne Erklärung versteht.

Die Reihenfolge ist Absicht: erst messen, dann rechnen, dann gestalten. Ein hübsches Dashboard mit
einer falsch gerechneten Öffnungsrate ist schlechter als gar keins, weil ihm geglaubt wird.

## 1. Was es wirklich gibt — und was nicht

Das ist der wichtigste Abschnitt. Die häufigste Art, hier zu scheitern, ist eine Kennzahl zu
versprechen, die die Werkzeuge nicht hergeben, und sie dann zu schätzen, ohne es zu sagen.

| Frage | Antwort | Woher |
| --- | --- | --- |
| Wie lief eine Aussendung? | **vollständig** | `email-newsletter-get`, `include: ["deliveryStatus"]` |
| Wie viele erreicht ein Versand gerade? | **vollständig** | `email-newsletter-get`, `include: ["audienceReach"]` |
| Welche Newsletter gibt es, in welchem Zustand? | **vollständig** | `email-newsletter-search`, nach `status` gefiltert |
| Welche Tags hat das Konto? | **Liste, ohne Zahlen** | `search-tags` |
| **Wie viele Kontakte hat das Konto?** | **gibt es nicht** | siehe unten |

**Die Kontaktzahl ist die Lücke.** `search-contacts` ist Cursor-paginiert, maximal 100 pro Seite,
und liefert **keine Gesamtzahl**. Ein Konto mit 80.000 Kontakten zu zählen hieße 800 Aufrufe. Tu
das nicht.

Nimm stattdessen `audienceReach` eines Newsletters mit Zielgruppe `all_contacts`: das ist die Zahl
der aktiven Kontakte, die KlickTipp selbst berechnet, in einem Aufruf. Es kommen `minRecipients`
und `maxRecipients` zurück — sind sie verschieden, ist es eine Spanne, und dann zeig eine Spanne.
Gibt es keinen solchen Newsletter, **lass die Kachel weg**, statt eine Zahl zu erfinden.

## 2. Einsammeln, ohne das Konto leerzulesen

```
email-newsletter-search  status="sent"  limit=25     → die letzten Aussendungen
  └─ je Newsletter: email-newsletter-get  include=["deliveryStatus"]
email-newsletter-search  status="draft"  limit=1     → nur für die Zählung
email-newsletter-search  status="scheduled" limit=1  → dito
```

Das sind etwa 25 bis 30 Aufrufe für ein volles Dashboard. Zwei Regeln halten es dabei:

**Ein Zeitraum, nicht „alles".** Frag nach dem Zeitraum, oder nimm die letzten 90 Tage und schreib
es hin. `sendDateFrom` und `sendDateBefore` sind halboffen — „From" schließt ein, „Before" schließt
aus — und ISO 8601 mit explizitem Offset (`2026-09-01T10:00:00+02:00`).

**Entwürfe haben kein Versanddatum.** Ein Entwurf fällt in kein `sendDate`-Fenster, auch wenn ein
Termin gesetzt und wieder abgesagt wurde. Für „wie viele Entwürfe liegen herum" zählst du über
`status="draft"`, nicht über ein Zeitfenster.

Wird die Liste lang, kommt ein `nextCursor` zurück: unverändert zurückgeben, zusammen mit
**denselben** Filtern. Ein Cursor aus einer anderen Suche wird abgewiesen.

## 3. Rechnen — hier werden Dashboards falsch

`deliveryStatus` liefert die Zähler roh. Die Quoten rechnest du selbst, und jede hat einen Nenner,
den man falsch wählen kann.

| Kennzahl | Formel | Fallstrick |
| --- | --- | --- |
| Zustellrate | `sentCount / estimatedRecipients` | `estimatedRecipients` ist die Schätzung **vor** dem Versand, nicht die Wahrheit danach |
| Öffnungsrate | `uniqueOpenCount / sentCount` | **nicht** `totalOpenCount` — das zählt jedes Öffnen derselben Person |
| Klickrate | `uniqueClickCount / sentCount` | dito |
| Klick-zu-Öffnung (CTOR) | `uniqueClickCount / uniqueOpenCount` | die ehrlichste Inhaltskennzahl: misst den Inhalt, nicht die Betreffzeile |
| Bounce-Rate | `(hardBounceCount + softBounceCount) / sentCount` | hart und weich **getrennt** zeigen — hart ist eine tote Adresse, weich ein Moment |
| Abmelderate | `unsubscriptionCount / sentCount` | |
| Beschwerderate | `spamComplaintCount / sentCount` | die wichtigste Zahl im Dashboard, siehe unten |

**Teile nie durch null.** Ein Newsletter, dessen Versand noch läuft, hat `sentCount: 0` bei
gesetztem `sendDate`. Zeig „—", nicht „0 %" und nicht `NaN`.

**`totalOpenCount` gehört trotzdem hin**, aber als eigene Zahl: `totalOpenCount / uniqueOpenCount`
sagt, wie oft eine Öffnerin im Schnitt zurückkommt. Das ist interessant und wird selten gezeigt.

**Sag dazu, was eine Öffnung heute wert ist.** Apple Mail Privacy Protection lädt Bilder vorab, ohne
dass jemand die Mail gesehen hat. Öffnungsraten sind dadurch nach oben verzerrt und über die Zeit
nicht sauber vergleichbar. Ein Dashboard, das die Öffnungsrate groß und unkommentiert zeigt, führt
in die Irre — **Klicks sind das härtere Signal**, und der Skill stellt sie deshalb gleichberechtigt
daneben.

### Was hervorzuheben ist

Nicht alle Zahlen sind gleich wichtig. Zwei verdienen eine Warnfarbe, weil an ihnen die
Zustellbarkeit des ganzen Kontos hängt:

- **Beschwerden über 0,1 %** — das ist die Schwelle, an der große Anbieter anfangen, den Absender
  schlechter zuzustellen.
- **Harte Bounces über 2 %** — deutet auf eine gekaufte oder alte Liste hin und beschädigt die
  Reputation der Absenderdomain.

Diese beiden Grenzen sind Branchenübliches, keine KlickTipp-Einstellung; schreib sie als
Orientierung dazu, nicht als Urteil.

## 4. Die Seite

Bau sie als **ein** Artifact, eine einzelne, in sich geschlossene HTML-Seite — und zwar wirklich
als Artifact, nicht als Datei mit einem Pfad daneben. Ein Report soll sich öffnen und weiterreichen
lassen, ohne dass jemand erst etwas herunterlädt.

Wie das geht, hängt von der Umgebung ab, und das ist der einzige Unterschied:

| Umgebung | Weg |
| --- | --- |
| Claude Code | das `Artifact`-Werkzeug: HTML-Datei schreiben, dann veröffentlichen |
| claude.ai | ein Artifact direkt in der Antwort |
| ohne Artifacts (z. B. Codex) | `.html` schreiben und den Pfad nennen — inhaltlich identisch |

**Das Handwerk steht in [references/craft.md](references/craft.md)** — Farbtokens für Hell und
Dunkel, Schriftwahl, der Aufbau einer Kennzahl-Kachel, Liniendiagramme in reinem SVG samt
Trefferflächen, Hover mit Tastatur-Entsprechung, und eine Prüfliste für den Schluss. Die Datei
setzt nichts voraus: keine Bibliothek, kein CDN, keinen weiteren Skill. Lies sie, bevor du die
Seite schreibst.

Was hier steht, ist nur, was dieses Dashboard **inhaltlich** braucht:

1. **Kopf**: Kontoname, Zeitraum und **der Beobachtungszeitpunkt**. `deliveryStatus` liefert
   `observedAt` — schreib ihn hin. Ein Dashboard ohne Datum wird Wochen später für aktuell gehalten.
2. **Kachelreihe**: erreichte Kontakte, Aussendungen im Zeitraum, Zustellrate, Öffnungsrate,
   Klickrate. Jede Kachel mit der absoluten Zahl **unter** der Prozentzahl — Prozente ohne Basis
   sind nicht prüfbar.
3. **Tabelle je Newsletter**, nach Versanddatum absteigend: Name, Datum, versendet, Öffnungen,
   Klicks, Bounces, Abmeldungen. Mit `statisticsUrl` aus der Antwort verlinkt, damit man von jeder
   Zeile in die App springen kann.
4. **Verlauf**, sobald es mehr als drei Aussendungen sind: Öffnungs- und Klickrate über der Zeit.
   Ein Punkt je Aussendung, keine Interpolation zwischen Terminen, die nichts miteinander zu tun
   haben.
5. **Fußzeile**: welche Werkzeuge gelesen wurden und was **nicht** enthalten ist.


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

**Kein Vergleich ohne Vergleichbarkeit.** Zwei Aussendungen an verschiedene Zielgruppen haben
verschiedene Grundgesamtheiten. Sortier nach Datum, nicht nach Erfolg, und setz keine Rangliste
daneben, die einen Zufall zur Leistung erklärt.

## 5. Was dieser Skill nicht tut

- **Er schreibt nichts.** Kein Newsletter, kein Kontakt, kein Tag. Wenn aus einer Erkenntnis eine
  Handlung folgen soll, ist dafür der Skill `newsletter` zuständig.
- **Er zählt keine Kontakte durch.** Siehe Abschnitt 1.
- **Er erklärt keine Ursachen.** „Die Öffnungsrate ist gefallen" ist eine Beobachtung; warum, weiß
  das Dashboard nicht. Formulier Vermutungen als Vermutungen, wenn überhaupt.
