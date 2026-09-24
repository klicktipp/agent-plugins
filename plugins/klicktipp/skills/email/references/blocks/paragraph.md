# Absatz (`paragraph`)

Der übliche Fließtextbaustein. In gespeicherten Newslettern ist er die mit Abstand häufigste Bausteinart; nimm ihn, wenn du zwischen `paragraph` und `text` wählen kannst.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-paragraph`.

## Werkzeuge

| Anlegen | `add-email-editor-paragraph` |
| --- | --- |
| Ändern | `update-email-editor-text` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.paragraph.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Die Typografie steckt **im `html` selbst**: Wrapper-`div`, `<p style=…>`, `<span style=…>`. Ein nacktes `<p>Neuer Text</p>` wirft Schriftgröße, Zeilenhöhe und Farben weg. Nimm das gelesene Markup als Vorlage und tausche nur die Wörter.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
