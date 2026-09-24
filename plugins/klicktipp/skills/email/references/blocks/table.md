# Tabelle (`table`)

Ein Raster aus Zellen: Preislisten, Vergleiche, Termine, alles Zeilenweise-Gegenüberstellende.

Familie **Tabelle**. Modultyp im Dokument: `mailup-bee-newsletter-modules-table`.

## Werkzeuge

| Anlegen | `add-email-editor-table` |
| --- | --- |
| Ändern | `update-email-editor-table` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Zeilen

Der Inhalt ist ein Raster unter `descriptor.table.content`: `rows[].cells[].html`. Du schickst Zeilen aus Zellen, jede Zelle ein Stück Markup.

## Worauf zu achten ist

Kein flaches Listenformat, sondern ein Raster: Zeilen aus Zellen, jede Zelle Markup. **Alle Zeilen brauchen gleich viele Zellen** — eine kurze Zeile ist ein Loch im Raster und wird abgelehnt.

**Die Kopfzeile schreibst du nicht.** Sie folgt automatisch der Breite der Datenzeilen und taucht deshalb im `entries`-Auszug nicht auf. Rahmen, Farben und Typografie bleiben ebenfalls.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als einfaches Markup zurück; die bearbeitbare Tabelle ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
