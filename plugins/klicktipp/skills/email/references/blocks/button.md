# Button (`button`)

Der sichtbare Handlungsaufruf. Ein echter Baustein und kein verlinkter Text: er bleibt im Editor als Button bearbeitbar und wird in jedem Postfach als Fläche gerendert.

Familie **Interaktiv**. Modultyp im Dokument: `mailup-bee-newsletter-modules-button`.

## Werkzeuge

| Anlegen | `add-email-editor-button` |
| --- | --- |
| Ändern | `update-email-editor-button` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-button-style` (siehe unten) und `update-email-editor-block-style` |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `label` | `descriptor.button.label` |
| `href` | `descriptor.button.href` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

`label` ist Markup wie bei einem Textbaustein, nicht bloß Text: fang beim gelesenen Markup an und tausche nur die Wörter, sonst verliert der Button seine Typografie.

## Gestaltung

`update-email-editor-button-style` setzt den Button selbst: **Hintergrundfarbe**, **Textfarbe**, **Eckenradius**, **Rahmen** auf allen vier Seiten und den **Innenabstand** — der ist es, was einen Button groß oder klein macht.

Drei Ebenen nicht verwechseln: der Innenabstand *im* Button gehört hierher, der Abstand *um* den Button zu `update-email-editor-block-style`, und die Wörter zu `update-email-editor-button`.

`update-email-editor-block-style` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
