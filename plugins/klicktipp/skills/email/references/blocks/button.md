# Button (`button`)

Der sichtbare Handlungsaufruf. Ein echter Baustein und kein verlinkter Text: er bleibt im Editor als Button bearbeitbar und wird in jedem Postfach als Fläche gerendert.

Familie **Interaktiv**. Modultyp im Dokument: `mailup-bee-newsletter-modules-button`.

## Werkzeuge

| Anlegen | `email-button-add` |
| --- | --- |
| Ändern | `email-button-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-button-style-write` (siehe unten) und `email-block-style-write` |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `label` | `descriptor.button.label` |
| `href` | `descriptor.button.href` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

`label` ist Markup wie bei einem Textbaustein, nicht bloß Text: fang beim gelesenen Markup an und tausche nur die Wörter, sonst verliert der Button seine Typografie.

## Gestaltung

`email-button-style-write` setzt den Button selbst: **Hintergrundfarbe**, **Textfarbe**, **Eckenradius**, **Rahmen** auf allen vier Seiten und den **Innenabstand** — der ist es, was einen Button groß oder klein macht.

Drei Ebenen nicht verwechseln: der Innenabstand *im* Button gehört hierher, der Abstand *um* den Button zu `email-block-style-write`, und die Wörter zu `email-button-write`.

`email-block-style-write` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
