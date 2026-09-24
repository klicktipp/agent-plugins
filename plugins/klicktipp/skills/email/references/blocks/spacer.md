# Abstand (`spacer`)

Leerraum mit einer festen Höhe. Das Mittel, um Abschnitte atmen zu lassen — verlässlicher als Innenabstände, weil jeder E-Mail-Client ihn gleich rendert.

Familie **Struktur**. Modultyp im Dokument: `mailup-bee-newsletter-modules-spacer`.

## Werkzeuge

| Anlegen | `add-email-editor-spacer` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-spacer-style` (siehe unten) und `update-email-editor-block-style` |

## Inhalt

Hat kein Inhaltsfeld: er ist fertig, sobald er existiert.

## Worauf zu achten ist

Fertig, wie er ist. Seine Höhe ist Gestaltung, kein Inhalt.

## Gestaltung

`update-email-editor-spacer-style` setzt die **Höhe** in Pixeln — und damit den ganzen Baustein. Mehrere Abstände in einem Aufruf: das Werkzeug nimmt eine Liste von uuids, die alle denselben Wert bekommen.

`update-email-editor-block-style` setzt zusätzlich für **jeden** Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
