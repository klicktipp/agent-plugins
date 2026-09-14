# Liste (`list`)

Eine Aufzählung, geordnet oder ungeordnet. Für alles, was ein Empfänger überfliegen soll, statt es zu lesen.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-list`.

## Werkzeuge

| Anlegen | `email-list-add` |
| --- | --- |
| Ändern | `email-text-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.list.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Das `html` ist das vollständige `<ul>`- oder `<ol>`-Markup, nicht nur die Einträge.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
