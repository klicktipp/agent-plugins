# Trennlinie (`divider`)

Eine waagerechte Linie, die zwei Abschnitte trennt.

Familie **Struktur**. Modultyp im Dokument: `mailup-bee-newsletter-modules-divider`.

## Werkzeuge

| Anlegen | `email-divider-add` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-divider-style-write` (siehe unten) und `email-block-style-write` |

## Inhalt

Hat kein Inhaltsfeld: er ist fertig, sobald er existiert.

## Worauf zu achten ist

Fertig, wie er ist. Wie er aussieht, ist die Gestaltungsebene (`email-block-style-write` und die Zeile darüber).

## Gestaltung

`email-divider-style-write` setzt die **Linie** (`1px solid #000000` — Dicke, Art, Farbe) und die **Breite** als Prozentwert der Zeile. Eine Dicke von `0` macht die Trennlinie zu einem unsichtbaren Abstandshalter; das ist ein echter Anwendungsfall, kein Versehen. Mehrere Linien in einem Aufruf.

`email-block-style-write` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als gestaltete Linie zurück; der Trennlinien-Baustein ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
