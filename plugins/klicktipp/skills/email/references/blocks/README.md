# Die Bausteine, einer je Datei

Eine Datei je Bausteinart: welche Werkzeuge sie anlegen und ändern, welche Felder sie hat, wo das
Dokument sie speichert, worauf zu achten ist, und was ein HTML-Import sie kostet. Lies die eine,
die du brauchst — nicht alle.

| Familie | Bausteine |
| --- | --- |
| Text | [Überschrift](heading.md) · [Text](text.md) · [Absatz](paragraph.md) · [Liste](list.md) · [Eigenes HTML](html.md) |
| Medien | [Bild](image.md) · [Video](video.md) · [Icons](icons.md) |
| Interaktiv | [Button](button.md) · [Menü](menu.md) · [Social-Links](social.md) |
| Struktur | [Trennlinie](divider.md) · [Abstand](spacer.md) |
| Tabelle | [Tabelle](table.md) |
| KlickTipp | [Countdown](countdown.md) · [Kontaktkarte](contact-card.md) · [Wowing-Video](wowing-video.md) · [Personalisierte E-Mail](personalized-email.md) |

Vier Arten gibt es im Editor, aber nicht hier: **Formular, Karussell, Merge-Inhalt und
Leerbaustein**. Sie haben kein Werkzeug, weil kein echtes Exemplar gefunden wurde, aus dem sich ein
neutraler Startzustand ableiten ließe. Sie bleiben beim Editor.

## Was für alle gilt

- **Anlegen bringt den Inhalt mit.** Jedes `email-<art>-add` nimmt die Felder seiner Art. Lege nie
  leer an, um danach zu schreiben.
- **Der neue Baustein sieht aus wie der erste seiner Art** — der Server kopiert `style` und
  Innenabstand vom *ersten* Baustein derselben Art (Spalte, dann Zeile, dann Newsletter), nicht vom
  Nachbarn über der Einfügestelle. Das **Markup** kopiert er nicht: das ist dein Teil. Eine Reihe
  von Adds erzeugt deshalb eine Reihe gleich aussehender Bausteine — einen ganzen Körper baut
  `replace-email-editor-content-from-html`, nicht eine Kette von Adds.
- **Entfernen und neu anlegen ist kein Ändern.** Dabei gehen Typografie, Add-on-Konfiguration und
  die `uuid` verloren. Siehe SKILL.md.
- **Aussehen ist die Gestaltungsebene**, nicht der Inhalt: `update-email-editor-block-style` und die drei
  Ebenen darüber.
