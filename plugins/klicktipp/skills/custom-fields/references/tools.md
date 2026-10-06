# Feld-Werkzeuge — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung. Der Ablauf steht in `../SKILL.md`.

`R` liest nur · `D` löscht oder ersetzt ohne Undo · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `search-custom-fields` · `get-custom-field` | R | Definitionen mit Platzhalter, API-Schlüssel, Gruppe, Labels, Mehrwertigkeit. Nicht die Werte eines Kontakts. |
| `create-custom-field` | | Eine Definition; speichert keinen Wert. Typ ist endgültig, `multiValue` weggelassen ist `true`. |
| `update-custom-field` | D I | Name, Beschreibung, Gruppe, Labels, Notiz, `requestName`, `copyToFieldId`, und `multiValue` nur true → false. |
| `delete-custom-field` | D | Die Definition und die Werte aller Kontakte darin. |

### `search-custom-fields` · `get-custom-field`
**Wofür:** Felddefinitionen; Filter `query`, `types` (z. B. `field-date`, `field-datetime`),
`onlyWritable`. Eigene Felder zuerst (neueste oben), dann die globalen. **Nicht:** die Werte eines
Kontakts (Skill `contacts`). **Stolperer:** Globale Felder tragen `isGlobal` und sind weder änderbar
noch löschbar. `customFieldId` ist eine Zahl für ein eigenes Feld, ein Name wie `FirstName` für ein
globales.

### `create-custom-field`
**Stolperer:** Der Datentyp ist endgültig. `multiValue` weggelassen heißt `true` (ein Wert je Abo) —
für einen kontaktweiten Wert ausdrücklich `false`. Anlegen speichert keinen Wert; gib eine
Beschreibung.

### `update-custom-field`
**Stolperer:** Nur was übergeben wird, wird geschrieben; ein leerer String leert eine
Texteinstellung. `metaLabels` ersetzt die ganze Liste. Eine Typänderung wird abgewiesen.
`multiValue: false` löscht die zusätzlichen Werte je Abo und geht nie zurück. `requestName` ist der
Schlüssel, den ein Kontakt in einer Anmelde-E-Mail als „Schlüssel = Wert" schreibt; teilen ihn zwei
Felder, gewinnt das erste. `copyToFieldId` braucht einen verträglichen Typ. Das Ergebnis listet, was
das Feld benutzt.

### `delete-custom-field`
**Stolperer:** Vernichtet die Werte aller Kontakte, ohne Undo. Ein noch benutztes Feld wird mit
Nennung der Nutzer abgewiesen. Der Platzhalter eines gelöschten Felds rendert leer.
