# Menü (`menu`)

Eine Reihe von Links, meist als Navigation im Kopf der E-Mail.

Familie **Interaktiv**. Modultyp im Dokument: `mailup-bee-newsletter-modules-menu`.

## Werkzeuge

| Anlegen | `add-email-editor-menu` |
| --- | --- |
| Ändern | `update-email-editor-menu` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Einträge

Der Inhalt ist eine **Liste** unter `descriptor.menuItemsList.items`. Die Liste ersetzt die Liste: schick alle Einträge in der gewünschten Reihenfolge, eine leere Liste wird abgelehnt.

| Feld je Eintrag | gespeichert unter |
| --- | --- |
| `text` | `text` |
| `href` | `link.href` |

Alles, was du **nicht** nennst, bleibt aus dem Eintrag erhalten, den der Baustein schon hatte — der Server baut jeden neuen Eintrag aus einem vorhandenen.

## Worauf zu achten ist

Wie ein Link öffnet (`target`), der Trenner und die Abstände bleiben aus dem Eintrag erhalten, den das Menü schon hatte.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als Links zurück; das bearbeitbare Menü ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
