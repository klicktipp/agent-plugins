# Icons (`icons`)

Bilder mit Beschriftung nebeneinander — Zahlungsarten, Siegel, App-Store-Badges, eine Merkmalsreihe.

Familie **Medien**. Modultyp im Dokument: `mailup-bee-newsletter-modules-icons`.

## Werkzeuge

| Anlegen | `add-email-editor-icons` |
| --- | --- |
| Ändern | `update-email-editor-icons` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

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

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als Bilder mit Links zurück; der bearbeitbare Baustein ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
