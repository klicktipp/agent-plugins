# Personalisierte E-Mail (`personalized-email`)

Ein Baustein, der je Empfänger einen eigenen Text erzeugt — aus einer Anweisung, die du schreibst, und den Daten des Kontakts.

Familie **KlickTipp**. Im Dokument liegt er wie jedes Add-on als `mailup-bee-newsletter-modules-addon`; welches Add-on es ist, sagt `moduleInternal.uid`: `personalized-email`.

## Werkzeuge

| Anlegen | `email-personalized-email-add` |
| --- | --- |
| Ändern | `email-personalized-email-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `prompt` | `descriptor.` |
| `name` | `descriptor.` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

**Auf Production nicht freigeschaltet** — beide Werkzeuge. Anders als bei den übrigen Add-ons hilft hier kein Verweis auf den Editor: der bietet den Baustein im Einfügen-Menü gar nicht an. Auf Production ist die personalisierte E-Mail im Newsletter also schlicht nicht erreichbar; sag das, statt einen Umweg zu erfinden.

`prompt` ist beim Anlegen **Pflicht** — die Anweisung *ist* der Baustein. Ohne sie rendert er einen Platzhalter in einen fertig aussehenden Newsletter und erzeugt nichts.

Sag beim Hinzufügen dazu: der Newsletter-Editor bietet diesen Baustein im Einfügen-Menü **nicht** an, nur Automationen tun das. Eine Person kann ihn dort weder anlegen noch nach einem Entfernen zurückholen. Welche Datenfelder und Tags die Anweisung nutzen darf, wird im Editor gewählt.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als sein gerendertes Ergebnis zurück; das Add-on ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
