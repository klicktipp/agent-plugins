# KI-Text (`ai-text`)

Ein Add-on, das seinen Text beim Versand erzeugen lässt. Setzt voraus, dass das Konto das Add-on hat.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `smartcopywriter-handle`.

## Werkzeuge

| Anlegen | — (siehe unten) |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Worauf zu achten ist

**Es gibt kein Anlege-Werkzeug mehr.** `email-ai-text-add` ist entfernt. Damit gilt für den KI-Text dasselbe wie für Countdown, Kontaktkarte und Wowing-Video: der Baustein entsteht im KlickTipp-Editor, weil seine Anweisung ohnehin dort gesetzt wird — ein Werkzeug hätte nur eine leere Hülle platzieren können, die beim Versand nichts rendert. Verweise auf den Editor, statt einen Umweg zu suchen.

Ein vorhandener Baustein bleibt lesbar, verschiebbar und entfernbar, und sein Aussehen lässt sich ändern. Der Baustein setzt außerdem voraus, dass das Konto das Add-on besitzt.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
