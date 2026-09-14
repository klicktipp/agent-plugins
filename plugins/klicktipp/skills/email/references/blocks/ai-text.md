# KI-Text (`ai-text`)

Ein Add-on, das seinen Text beim Versand erzeugen lässt. Setzt voraus, dass das Konto das Add-on hat.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `smartcopywriter-handle`.

## Werkzeuge

| Anlegen | `email-ai-text-add` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Worauf zu achten ist

Kommt unkonfiguriert: die Anweisung wird im KlickTipp-Editor gesetzt. Anders als die personalisierte E-Mail, deren Anweisung du direkt mitgibst — und anders als sie setzt dieser Baustein voraus, dass das Konto das Add-on besitzt.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
