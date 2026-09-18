# Bild (`image`)

Ein Bild, wahlweise verlinkt. Die Breite, in der es gezeigt wird, gehört zum Baustein und nicht zum Bild.

Familie **Medien**. Modultyp im Dokument: `mailup-bee-newsletter-modules-image`.

## Werkzeuge

| Anlegen | `email-image-add` |
| --- | --- |
| Ändern | `email-image-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `src` | `descriptor.image.src` |
| `alt` | `descriptor.image.alt` |
| `href` | `descriptor.image.href` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Die URL muss eine dieses Kontos sein. Woher sie kommt, in dieser Reihenfolge: `email-image-search` (die Mediathek des Kontos — es **listet auf und sucht nicht**: eine Seite je Aufruf, weiter über `nextCursor`), sonst `email-image-stock-search` (Pexels und Pixabay) und das gewählte Foto mit `sourceUrl` und `fileName` durch `email-image-upload` — **die Provider-URL selbst gehört nie in den Newsletter**. Eigenes Material lädst du direkt mit `email-image-upload` hoch.

Vor dem Einsetzen lohnt ein Blick: `email-image-preview` zeigt eine dieser URLs als Bild im App-Fenster — Mediathek-CDN und Stock-Archive, mehr lässt die Sandbox nicht zu.

Der Grund: eine fremde URL lässt jedes Postfach einen Dritten kontaktieren und bricht an dem Tag, an dem das Foto dort verschwindet. Die Stock-Suche kommt außerdem **nie leer zurück** — ohne Treffer liefert sie unverwandte Fotos, also sag, was gekommen ist, statt es als Fund zu präsentieren. Die Breite, in der das Bild erscheint, ist kein Feld dieses Werkzeugs.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
