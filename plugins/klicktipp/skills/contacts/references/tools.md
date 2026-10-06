# Kontakt-Werkzeuge — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung. Der Ablauf steht in `../SKILL.md`.

`R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas außerhalb des Kontos (einen
echten Empfänger, eine Automation) · `I` ein zweiter gleicher Aufruf ändert nichts mehr. Jedes
Werkzeug nimmt optional `accountId`; weggelassen heißt das Konto des Zugangs.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `search-contacts` · `get-contact` | R | Kontakte finden (eine Zeile je Kanal, Cursor, ohne Gesamtzahl) und einen lesen. |
| `upsert-subscribed-contact` | DO | Einen Kontakt von Hand anlegen, sofort angemeldet — kein Opt-in, keine Bestätigungsmail. |
| `subscribe-contact-via-opt-in-process` · `unsubscribe-contact` | DO | Einen Kanal über einen Prozess an- / abmelden. Brauchen `approval`. |
| `update-contact-values` | DO | Feldwerte. Nicht: Adressen, Opt-in, Abos. |
| `tag-contact` · `untag-contact` | O | → Skill `tags`. |
| `get-account-settings` | R I | Die Einstellungen des Kontos, nur die, die es ändern darf. Zugangsdaten nur als eingerichtet oder nicht. |
| `update-account-settings` | I | Nur die genannten Einstellungen schreiben. Ein falscher Wert weist den ganzen Aufruf ab. |

### `search-contacts` · `get-contact`
**Wofür:** Kontakte finden (E-Mail-Fragment, Mobilnummer, Status, Kanal, **ein** manueller Tag) und
lesen (Adresse, Status, Feldwerte, manuelle Tags, Bearbeitungslink). **Nicht:** vollständige Kanal-
oder Referenzdaten — `get-contact` liest **eine** `referenceId` (Default `0`) und eine E-Mail.
**Stolperer:** Seiten à höchstens 100 ohne Gesamtzahl; ein Konto mit 80 000 Kontakten sind 800
Aufrufe. Der `cursor` kommt unverändert zurück, mit denselben Filtern.

### `upsert-subscribed-contact`
**Wofür:** einen Kontakt von Hand anlegen, wie der Bildschirm *Kontakt hinzufügen* — E-Mail-Adresse,
Mobilnummer oder beides, Feldwerte im selben Aufruf, optional ein manueller Tag. **Anders als
`subscribe-contact-via-opt-in-process`:** kein Opt-in-Prozess, **keine Bestätigungsmail**, der Kontakt
ist sofort `subscribed` und in der Zielgruppe des nächsten Mailings. **Stolperer:** Eine abgemeldete
Adresse wird abgewiesen, nicht wieder angemeldet. Eine bestehende Adresse wird *aktualisiert* — die
mitgegebenen Werte überschreiben die alten, `alreadyExisted` sagt es. Zählt gegen das
Tagesimportlimit. Unbekannte Feld-ID oder unbekannter Tag: Absage, nichts wird übersprungen.

### `subscribe-contact-via-opt-in-process` · `unsubscribe-contact`
**Wofür:** genau einen Kanal (E-Mail *oder* Telefon, nie beides) an- oder abmelden; Anmelden über
einen `optInProcessId`, optional mit `referenceId` und einem Tag, der sofort vergeben wird.
**Stolperer:** Ändert einen echten Empfänger, kann eine Bestätigungsmail auslösen und Automationen
starten — deshalb `approval` (`subscribe-contact` / `unsubscribe-contact`), erst nach Zustimmung. Der
mitgegebene Tag kann weitere Automationen starten. Andere Kanäle und Referenzen bleiben unberührt;
Abmelden entfernt keine Tags.

### `update-contact-values`
**Wofür:** Feldwerte (`fields`: je `fieldId` ein globaler Schlüssel oder eine numerische Feld-ID des
Kontos, `referenceId` Default 0). **Nicht:** Adressen, Opt-in, Abos, Listen. **Stolperer:** Das Feld
muss existieren (Skill `custom-fields`) — nichts wird nebenbei angelegt. Ein leerer Wert löscht das
Feld. Überschreibt ohne Undo.

### `get-account-settings`
**Wofür:** die Einstellungsseite des Kontos lesen — Funktionsschalter, Vorschau-Tag, Sperrliste.
**Nicht:** persönliche Daten, Datenschutz-Einstellungen, Auftragsverarbeitung, Absenderadressen.
**Stolperer:** Ein Schalter, den das Konto nicht ändern darf, fehlt in der Antwort, statt `false` zu
sein. Zugangsdaten angebundener Dienste kommen nur als eingerichtet oder nicht.

### `update-account-settings`
**Wofür:** einzelne Einstellungen ändern; die Antwort ist der Stand danach. **Nicht:** Zugangsdaten
— die bleiben in der App. **Stolperer:** Nur die genannten Einstellungen werden geschrieben. Ein
Schalter, den `get-account-settings` nicht zeigt, wird mit Namen abgewiesen; ein falscher oder
verbotener Wert weist den ganzen Aufruf ab, ohne zu schreiben. `refusals` listet nur, was die
Plattform erst beim Speichern ablehnte — die übrigen Änderungen sind dann gespeichert.
`emailBlacklist` ersetzt die ganze Liste, ein leerer String leert sie.
