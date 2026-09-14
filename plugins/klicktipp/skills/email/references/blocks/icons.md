# Icons (`icons`)

Bilder mit Beschriftung nebeneinander — Zahlungsarten, Siegel, App-Store-Badges, eine Merkmalsreihe.

Familie **Medien**. Modultyp im Dokument: `mailup-bee-newsletter-modules-icons`.

## Werkzeuge

| Anlegen | `email-icons-add` |
| --- | --- |
| Ändern | `email-icons-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Einträge

Der Inhalt ist eine **Liste** unter `descriptor.iconsList.icons`. Die Liste ersetzt die Liste: schick alle Einträge in der gewünschten Reihenfolge, eine leere Liste wird abgelehnt.

| Feld je Eintrag | gespeichert unter |
| --- | --- |
| `src` | `image` |
| `href` | `href` |
| `text` | `text` |

Alles, was du **nicht** nennst, bleibt aus dem Eintrag erhalten, den der Baustein schon hatte — der Server baut jeden neuen Eintrag aus einem vorhandenen.

## Worauf zu achten ist

Nicht dasselbe wie Social-Links: dieser Baustein trägt **irgendein** Bild mit Beschriftung. Größe (`width`, `height`) und Position der Beschriftung (`textPosition`) sind im Format Pflichtfelder — sie werden aus dem vorhandenen Eintrag kopiert, du musst sie weder kennen noch angeben.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als Bilder mit Links zurück; der bearbeitbare Baustein ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
