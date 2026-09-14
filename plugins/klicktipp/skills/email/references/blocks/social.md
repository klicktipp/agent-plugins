# Social-Links (`social`)

Die Icon-Reihe zu den Profilen des Absenders, meist im Fuß.

Familie **Interaktiv**. Modultyp im Dokument: `mailup-bee-newsletter-modules-social`.

## Werkzeuge

| Icons finden | `email-social-icon-search` |
| --- | --- |
| Anlegen | `email-social-add` |
| Ändern | `email-social-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Einträge

Der Inhalt ist eine **Liste** unter `descriptor.iconsList.icons`. Die Liste ersetzt die Liste: schick alle Einträge in der gewünschten Reihenfolge, eine leere Liste wird abgelehnt.

| Feld je Eintrag | gespeichert unter |
| --- | --- |
| `name` | `name` |
| `src` | `image.src` |
| `href` | `image.href` |
| `alt` | `image.alt` |
| `title` | `image.title` |

Alles, was du **nicht** nennst, bleibt aus dem Eintrag erhalten, den der Baustein schon hatte — der Server baut jeden neuen Eintrag aus einem vorhandenen.

## Worauf zu achten ist

**Rate niemals eine `src`.** Die Icon-Bilder kommen aus den Icon-Sätzen des Editors, und die liegen in dessen Browser-SDK — der Server kann sie nicht auflisten. Frag darum vor jedem Anlegen oder Ändern `email-social-icon-search`: es gibt die Bilder heraus, die dieser Newsletter schon verwendet, das meistgenutzte zuerst, mit Netzwerk, Alt-Text und Tooltip.

Eine Bild-URL aus der eigenen Bibliothek (`email-image-search`, das die Bibliothek seitenweise auflistet) geht ebenso, und das ist kein Behelf: der Editor führt für genau diesen Fall den Icon-Typ **„Custom"** mit eigenem Bild und den Feldern Titel, Alternativer Text und URL. Setz `name` auf `Custom`, wenn das Bild zu keinem Netzwerk gehört.

Kommt die Suche leer zurück und die Bibliothek gibt nichts her, **sag das und bitte den Nutzer, einen Social-Block im Editor zu setzen.** Eine erfundene URL wird angenommen — der Empfänger sieht dann ein Loch in der Reihe, und das bemerkt vor dem Versand niemand.

`alt` und `title` sind nicht dasselbe: `alt` bekommt, wer das Bild nicht sieht — weil es nicht lädt oder weil ein Screenreader vorliest —, `title` nur, wer schon darauf zeigt. Schreib den Tooltip nie statt des Alt-Textes.

Was ein Icon ist (`type: follow`) und wie sein Link öffnet, bleibt aus dem Eintrag erhalten, den der Baustein schon hatte.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als Bilder mit Links zurück; der bearbeitbare Baustein ist weg.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.
