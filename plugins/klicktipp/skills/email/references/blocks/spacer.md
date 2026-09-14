# Abstand (`spacer`)

Leerraum mit einer festen Höhe. Das Mittel, um Abschnitte atmen zu lassen — verlässlicher als Innenabstände, weil jeder E-Mail-Client ihn gleich rendert.

Familie **Struktur**. Modultyp im Dokument: `mailup-bee-newsletter-modules-spacer`.

## Werkzeuge

| Anlegen | `email-spacer-add` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-spacer-style-write` (siehe unten) und `email-block-style-write` |

## Inhalt

Hat kein Inhaltsfeld: er ist fertig, sobald er existiert.

## Worauf zu achten ist

Fertig, wie er ist. Seine Höhe ist Gestaltung, kein Inhalt.

## Gestaltung

`email-spacer-style-write` setzt die **Höhe** in Pixeln — und damit den ganzen Baustein. Mehrere Abstände in einem Aufruf: das Werkzeug nimmt eine Liste von uuids, die alle denselben Wert bekommen.

`email-block-style-write` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
