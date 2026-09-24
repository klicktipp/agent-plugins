# Kontaktkarte (`contact-card`)

Ein Add-on mit den Kontaktdaten des Absenders als gestaltete Karte.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `vcard-handle`.

## Werkzeuge

| Anlegen | — (nur im KlickTipp-Editor) |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Worauf zu achten ist

Kommt unkonfiguriert: die Kontaktdaten werden im KlickTipp-Editor eingetragen.

**Es gibt kein Werkzeug, das diesen Baustein anlegt.** Es gab eines; es konnte nur eine leere Hülle setzen, weil die Kontaktdaten im Dialog des KlickTipp-Editors gewählt werden. Ein so eingefügter Baustein sah platziert aus und zeigte beim Versand nichts — deshalb ist das Werkzeug weg. Wird eine Kontaktkarte gewünscht, nenne den Editor. Vorhandene Bausteine dieser Art bleiben lesbar, verschiebbar und entfernbar.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
