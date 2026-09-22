# Personalisierte E-Mail (`personalized-email`)

Ein Baustein, der je Empfänger einen eigenen Text erzeugt — aus einer Anweisung, die du schreibst, und den Daten des Kontakts.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `personalized-email`.

## Werkzeuge

| Anlegen | — (siehe unten) |
| --- | --- |
| Ändern | — (siehe unten) |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `prompt` | `descriptor.` |
| `name` | `descriptor.` |

Diese Felder nahmen die beiden entfallenen Werkzeuge.

**Seit dem 18.09.2026 gibt es für diesen Baustein kein Werkzeug mehr.** `email-personalized-email-add` und `email-personalized-email-write` sind entfernt: das Add-on ist kostenpflichtig und die Arbeit daran vertagt. Das Schreib-Werkzeug ging zudem mit einem gemeldeten Fehler heraus — ein Update nur des Namens wurde mit „carries no prompt" abgewiesen, ein weggelassenes optionales Feld galt also als geleert.

**Der Editor ist hier kein Ersatz fürs Anlegen.** Sein Einfügen-Menü führt diesen Baustein nicht; nur Automationen setzen einen. In einem Newsletter ist er damit derzeit nicht anzulegen. Ein vorhandener Baustein bleibt lesbar, verschiebbar und entfernbar, und seine Anweisung ändert man im Editor.

## Worauf zu achten ist

**Nirgends mehr anzulegen, auch nicht auf Staging** — die beiden Werkzeuge sind entfernt, nicht nur auf Production gesperrt. Anders als bei den übrigen Add-ons hilft hier auch kein Verweis auf den Editor: der bietet den Baustein im Einfügen-Menü gar nicht an, nur Automationen setzen einen. In einem Newsletter ist die personalisierte E-Mail damit schlicht nicht erreichbar; sag das, statt einen Umweg zu erfinden.

Was mit einem **vorhandenen** Baustein geht: lesen, verschieben, entfernen, sein Aussehen ändern. Seine Anweisung — der `prompt`, der *der* Baustein ist — wird im Editor geändert, ebenso die Datenfelder und Tags, die sie nutzen darf.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
