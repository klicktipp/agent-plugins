# Countdown (`countdown`)

Ein Add-on, das eine mitlaufende Restzeit als Bild rendert — für Angebote mit Frist.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `countdown-handle`.

## Werkzeuge

| Anlegen | `email-countdown-add` |
| --- | --- |
| Ändern | — (nichts zu ändern) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Worauf zu achten ist

Kommt unkonfiguriert: Zieldatum und Aussehen werden im KlickTipp-Editor gesetzt. Melde ihn nicht als fertigen Countdown — ohne Ziel zeigt er nichts Sinnvolles.

**Auf Production nicht freigeschaltet.** Dort antwortet der Aufruf mit „unknown tool". Das ist kein Defekt: ein Baustein, den nur der Editor fertig machen kann, geht erst heraus, wenn es ein Werkzeug gibt, das ihn konfiguriert. Nenne dem Nutzer den Editor.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
