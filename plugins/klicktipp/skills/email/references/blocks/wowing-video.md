# Wowing-Video (`wowing-video`)

Ein Add-on von KlickTipp, das ein Video als anklickbares Vorschaubild einbindet.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `wowing-handle`.

## Werkzeuge

| Anlegen | — (nur im KlickTipp-Editor) |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Worauf zu achten ist

Kommt unkonfiguriert: das Video wird im KlickTipp-Editor gewählt. Nicht zu verwechseln mit dem normalen Video-Baustein, der `src` und `thumbSrc` direkt nimmt — den gibt es weiterhin als `add-email-editor-video`.

**Es gibt kein Werkzeug, das diesen Baustein anlegt.** Es gab eines; es konnte nur eine leere Hülle setzen, weil das Video im Dialog des KlickTipp-Editors gewählt wird. Ein so eingefügter Baustein sah platziert aus und zeigte beim Versand nichts — deshalb ist das Werkzeug weg. Wird ein Wowing-Video gewünscht, nenne den Editor. Vorhandene Bausteine dieser Art bleiben lesbar, verschiebbar und entfernbar.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
