# Video (`video`)

Ein Vorschaubild mit Link, das aussieht wie ein Videoplayer.

Familie **Medien**. Modultyp im Dokument: `mailup-bee-newsletter-modules-video`.

## Werkzeuge

| Anlegen | `add-email-editor-video` |
| --- | --- |
| Ändern | `update-email-editor-video` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `src` | `descriptor.video.src` |
| `thumbSrc` | `descriptor.video.thumbSrc` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Die zwei Felder gehören zusammen. Kein Mail-Client spielt ein Video im Postfach ab: `src` ist das Ziel des Klicks, `thumbSrc` das, was der Empfänger sieht. Ohne `thumbSrc` ist der Baustein im Editor ein leerer Kasten — das als „Video hinzugefügt" zu melden ist irreführend. Bei YouTube: `https://i.ytimg.com/vi/<ID>/hqdefault.jpg` gibt es immer, `maxresdefault.jpg` nur bei hochauflösenden Videos.

Wie der Baustein rendert (`video.mode`) ist **kein** Feld: dafür gibt es keinen belegten zweiten Wert, und ein geratener hat den Editor schon zum Absturz gebracht.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als Vorschaubild mit Link zurück; der Video-Baustein ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
