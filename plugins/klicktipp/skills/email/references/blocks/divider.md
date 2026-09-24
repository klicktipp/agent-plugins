# Trennlinie (`divider`)

Eine waagerechte Linie, die zwei Abschnitte trennt.

Familie **Struktur**. Modultyp im Dokument: `mailup-bee-newsletter-modules-divider`.

## Werkzeuge

| Anlegen | `add-email-editor-divider` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-divider-style` (siehe unten) und `update-email-editor-block-style` |

## Inhalt

Hat kein Inhaltsfeld: er ist fertig, sobald er existiert.

## Worauf zu achten ist

Fertig, wie er ist. Wie er aussieht, ist die Gestaltungsebene (`update-email-editor-block-style` und die Zeile darüber).

## Gestaltung

`update-email-editor-divider-style` setzt die **Linie** (`1px solid #000000` — Dicke, Art, Farbe) und die **Breite** als Prozentwert der Zeile. Eine Dicke von `0` macht die Trennlinie zu einem unsichtbaren Abstandshalter; das ist ein echter Anwendungsfall, kein Versehen. Mehrere Linien in einem Aufruf.

`update-email-editor-block-style` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als gestaltete Linie zurück; der Trennlinien-Baustein ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
