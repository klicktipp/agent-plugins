# Tag-Werkzeuge — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung. Der Ablauf steht in `../SKILL.md`.

`R` liest nur · `D` löscht ohne Undo · `O` erreicht eine Automation oder einen echten Empfänger · `I`
ein zweiter gleicher Aufruf ändert nichts mehr.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `search-tags` · `get-tag` | R | Manuelle und Systemtags; das Detail mit Beschreibung, Trägerzahl, Auto-Abos. |
| `create-manual-tag` · `update-manual-tag` | / I | Nur manuelle Tags: Name und Beschreibung. Keine Einstellung für Mehrdimensionalität. |
| `delete-manual-tag` | D | Nimmt den Tag von allen Kontakten. |
| `tag-contact` · `untag-contact` | O | Einen manuellen Tag an einem Kontakt an / ab, je `referenceId`. `approval` Pflicht. |

### `search-tags` · `get-tag`
**Wofür:** Tags mit Typ — manuell oder von KlickTipp gesetzt; Filter `query`, `type` (`tag`,
`campaign-sent`, `email-opened` …), `onlyWritable`, `multiValue` (einmal je Abo oder einmal
überhaupt), `systemRole` (`test-contact` markiert Testempfänger). **Stolperer:** Die Beschreibung
steht nur im Detail. `get-tag` sagt, wie viele Kontakte den Tag tragen, wofür er steht, welche Entität
hinter einem Systemtag steckt und welche Abos ein Zuweisen auslöst.

### `create-manual-tag` · `update-manual-tag` · `delete-manual-tag`
**Stolperer:** Anlegen weist niemandem etwas zu; der Name ist eindeutig im Konto und darf keine reine
Zahl sein; gib eine Beschreibung. Umbenennen bricht nichts (Referenz per ID), zeigt sich aber überall,
wo der Name gelesen wird — das Ergebnis listet die Nutzer; Auto-Abo-Konfiguration und
Mehrdimensionalität bleiben, wie sie sind. Löschen ist unumkehrbar; ein noch benutzter Tag wird mit
Nennung der Nutzer abgewiesen. Systemtags sind unantastbar.

### `tag-contact` · `untag-contact`
**Stolperer:** Kann sofort Kampagnen, Autoresponder und Outbound-Events starten oder ändern —
`approval: I_ACCEPT_AUTOMATION_EFFECTS`, nach Zustimmung. `referenceId` ist Default 0; bei einem
mehrdimensionalen Tag die gemeinte Referenz vorher klären. Nur manuelle, existierende Tags des
Kontos; unbekannte werden abgewiesen, nie angelegt. Entfernen meldet niemanden ab.
