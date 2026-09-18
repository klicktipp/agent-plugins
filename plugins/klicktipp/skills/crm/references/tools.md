# Die Werkzeuge dieses Skills — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung.

Die Werkzeugbeschreibungen, die der Server ausliefert, sind **Verträge, keine Handbücher**. Hier
steht, woran man sich stößt, wenn man eines einzeln in die Hand nimmt; der Ablauf steht in
`../SKILL.md`.

`R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas außerhalb des Kontos (einen
echten Empfänger, eine Automation) · `I` ein zweiter gleicher Aufruf ändert nichts mehr. Jedes
Werkzeug nimmt optional `accountId` (ein Unterkonto); weggelassen heißt das Konto des Zugangs.

**Auf Production freigegeben** sind die dreizehn Tag-, Kontakt- und Feld-Werkzeuge plus die zwei
Opt-in-Leser — ab dem nächsten Release dort, vorher „unknown tool". **Nicht** freigegeben, jedes
aus eigenem Grund: die beiden Löscher (`delete-manual-tag`, `delete-custom-field`), die drei
Anmelde-Werkzeuge (`subscribe`, `unsubscribe`, `get-subscription-redirect-url`) und alles am
Einwilligungsnachweis. Die Aufschlüsselung mit Begründung steht in `../SKILL.md` unter
„Verfügbarkeit".

| Werkzeug | | Wofür |
| --- | --- | --- |
| `search-opt-in-processes` · `get-opt-in-process` | R | Opt-in-Prozesse (= Abonnentenlisten). **Auf Production verfügbar.** |
| `create-opt-in-process` | | Prozess anlegen, optional als Kopie eines bestehenden. Die Bestätigungsmail entsteht mit. |
| `update-opt-in-process` · `delete-opt-in-process` | I / D | Einstellungen schreiben; löschen nimmt die Bestätigungsmail mit, die Kontakte bleiben. |
| `get-opt-in-confirmation-email` | R | Absenderseite der Bestätigungsmail: Betreff, Absender, Reply-To, CC/BCC. |
| `update-opt-in-confirmation-email` | I | Dieselben Einstellungen schreiben. Rechtlicher Einwilligungsnachweis — nur auf ausdrücklichen Wunsch ändern. |
| `get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` | R / I | Der Text: HTML und Klartext. **Nicht mit den Baustein-Werkzeugen** — `bodyIsEditable` bleibt `false`. |
| `preview-opt-in-confirmation-email` | ROI | Die Mail als Bild. Zeigt den gespeicherten Text, ohne Signatur und Bestätigungslink. |
| `send-opt-in-confirmation-email-test` | DO | Testversand an eine Adresse. Macht aus ihr einen vertaggten Kontakt. |
| `get-subscription-redirect-url` | R | Die Weiterleitungs-URL eines Abonnenten (Pending- oder Danke-Seite). |
| `search-contacts` · `get-contact` | R | Kontakte suchen (Cursor, ohne Gesamtzahl) und Detail lesen. |
| `subscribe` · `unsubscribe` | DO | Ein Kanal eines Kontakts an-/abmelden. Ändert einen echten Empfänger, kann Automationen starten. Brauchen `approval`. |
| `update-contact` | DO | Feldwerte eines Kontakts setzen. Nicht: Adressen, Opt-in, Abos. |
| `assign-manual-tag` · `remove-manual-tag` | O | Tag an/ab — kann Kampagnen starten. Brauchen `approval`. |
| `search-tags` · `get-tag` | R | Tags, manuell wie systemvergeben. |
| `create-manual-tag` · `update-manual-tag` · `delete-manual-tag` | / I / D | Nur manuelle Tags. Löschen nimmt den Tag von allen Kontakten. |
| `search-custom-fields` · `get-custom-field` | R | Felddefinitionen samt Platzhalter für den Inhalt. |
| `create-custom-field` · `update-custom-field` · `delete-custom-field` | / I / D | Datentyp ist endgültig. Löschen vernichtet die Werte aller Kontakte. |

## Opt-in

### `search-opt-in-processes` · `get-opt-in-process`
**Wofür:** Opt-in-Prozesse — in der App auch „Abonnentenlisten": ID, Name, Opt-in-Modus, Flags; das
Detail zusätzlich Bestätigungsmail, Weiterleitungen, Löschung ausstehender Abonnenten, Labels,
Notizen. **Stolperer:** Gelöschte fehlen in der Suche; die volle Konfiguration nur im Detail.

### `create-opt-in-process`
**Wofür:** einen Prozess anlegen — Name ist Pflicht, alles Weitere wie beim Ändern.
`copyFromOptInProcessId` kopiert einen bestehenden samt dem Text seiner Bestätigungsmail.
**Stolperer:** `useForChangeEmail` gibt es hier nicht (es würde einem anderen Prozess eine Rolle
wegnehmen); zwei gleiche Aufrufe erzeugen zwei Prozesse oder scheitern am doppelten Namen.

### `get-/update-opt-in-confirmation-email-content`
**Wofür:** den Text der Bestätigungsmail lesen und schreiben — HTML und Klartext, dazu der Betreff.
**Stolperer:** Beide Körper werden ganz geschrieben, nicht gepatcht; wer nur einen schreibt,
hinterlässt eine Mail, die zwei Empfängern zwei Dinge sagt. Ein Fehler der Inhaltsprüfung hält den
Schreibvorgang an — dann steht `stored: false` in der Antwort, und die Mail sagt weiter, was sie
vorher sagte.

### `preview-opt-in-confirmation-email` · `send-opt-in-confirmation-email-test`
**Wofür:** die Mail prüfen, bevor ein Kontakt sie bekommt — als Bild oder als echte Mail an eine
Adresse. **Stolperer:** Die Vorschau zeigt den **gespeicherten** Text; Signatur, Bestätigungslink
und Empfängerdaten kommen erst beim Versand dazu, ihr Fehlen ist kein Fehler. Der Testversand
dagegen ändert das Konto: eine Adresse, die noch kein Kontakt war, wird einer und wird vertaggt —
und Vertaggen startet Automationen.

### `get-subscription-redirect-url`
**Wofür:** die Pending- (Bestätigung offen) oder Danke-Seite (bestätigt) eines Abonnenten, per
E-Mail-Adresse; `optInProcessId` weggelassen nimmt den Prozess, über den die Adresse sich angemeldet
hat. Ohne eigene Seite kommt die von KlickTipp gehostete. **Stolperer:** Die Adresse ist Pflicht und
bestimmt, über wen die Antwort ist — such dir keine aus. `redirectPage` sagt, welche der beiden
Seiten kam; `pending` heißt „dieser Kontakt hat noch nicht bestätigt", nicht „falsch eingestellt".
Die URL trägt identifizierende Parameter (Abonnenten-ID, E-Mail, Liste, Schlüssel,
Empfehlungslink) — nicht weiterreichen, wo sie nicht hingehört.

## Kontakte

### `search-contacts` · `get-contact`
**Wofür:** Kontakte finden (E-Mail-Fragment, Status, **ein** manueller Tag) und lesen (Adresse,
Status, Feldwerte der `referenceId` — `0` sind die kontaktweiten —, manuelle Tags,
Bearbeitungslink). **Nicht:** vollständige Kanal- oder Referenzdaten. **Stolperer:** Cursor-Seiten à
höchstens 100 ohne Gesamtzahl; ein Konto mit 80 000 Kontakten sind 800 Aufrufe. Der `cursor` kommt
unverändert zurück, mit denselben Filtern.

### `subscribe` · `unsubscribe`
**Wofür:** genau einen Kanal (E-Mail *oder* Telefon, nie beides) an- oder abmelden; `subscribe`
über einen `optInProcessId`, optional mit `referenceId` und einem Tag, der sofort vergeben wird.
**Stolperer:** Ändert einen echten Empfänger, kann eine Bestätigungsmail auslösen und Automationen
starten — deshalb `approval` Pflicht (`subscribe-contact` / `unsubscribe-contact`) und erst nach
ausdrücklicher Zustimmung. Der mitgegebene Tag kann weitere Automationen starten. Andere Kanäle und
Referenzen bleiben unberührt; Abmelden entfernt keine Tags.

### `update-contact`
**Wofür:** Feldwerte (`fields`: je `fieldId` ein globaler Schlüssel oder eine numerische Feld-ID des
Kontos, `referenceId` Default 0). **Nicht:** Adressen, Opt-in, Abos, Listen. **Stolperer:** Jede
Feld-ID muss zum Konto gehören; das Feld muss existieren (`create-custom-field`) — nichts wird
nebenbei angelegt. Überschreibt ohne Undo.

### `assign-manual-tag` · `remove-manual-tag`
**Wofür:** ein manueller Tag an/ab, optional je `referenceId`. **Stolperer:** Kann sofort Kampagnen,
Autoresponder, Outbound-Events starten oder ändern — `approval: I_ACCEPT_AUTOMATION_EFFECTS`
Pflicht, nach Zustimmung. Entfernen meldet niemanden ab. Nur manuelle, existierende Tags des
Kontos; unbekannte werden abgewiesen, nie angelegt.

## Tags

### `search-tags` · `get-tag`
**Wofür:** Tags mit Typ — manuell oder von KlickTipp gesetzt (gesendet, geöffnet, geklickt); Filter
`query`, `type` (`tag`, `campaign-sent`, `email-opened` …), `onlyWritable`, `multiValue` (einmal je
Abo oder einmal überhaupt), `systemRole` (`test-contact` markiert Testempfänger). **Stolperer:** Die
Beschreibung steht nur im Detail. `get-tag` sagt, wie viele Kontakte den Tag tragen, wofür er steht,
welche Entität hinter einem Systemtag steckt und welche Abos ein Zuweisen auslöst.

### `create-manual-tag` · `update-manual-tag` · `delete-manual-tag`
**Stolperer:** Anlegen weist niemandem etwas zu; der Name ist eindeutig im Konto; gib eine
Beschreibung. Umbenennen bricht nichts (Referenz per ID), zeigt sich aber überall, wo der Name
gelesen wird — das Ergebnis listet die Nutzer; Auto-Abo-Konfiguration und Einmaligkeit bleiben.
Löschen nimmt den Tag von allen Kontakten und ist unumkehrbar; ein noch benutzter Tag wird mit
Nennung der Nutzer abgewiesen. Systemtags sind unantastbar.

## Felder

### `search-custom-fields` · `get-custom-field`
**Wofür:** Felddefinitionen mit dem Platzhalter für den Inhalt, dem Schlüssel der öffentlichen API,
Gruppe, Labels, Mehrwertigkeit; Filter `query`, `types` (z. B. `field-date`, `field-datetime`),
`onlyWritable`. Eigene Felder zuerst (neueste oben), dann die globalen. **Nicht:** die Werte eines
Kontakts (Kontakt-Werkzeuge). **Stolperer:** Globale Felder (Vorname, Stadt) tragen `isGlobal` und
sind weder änderbar noch löschbar. `customFieldId` ist eine Zahl für ein eigenes Feld, ein Name wie
`FirstName` für ein globales.

### `create-custom-field` · `update-custom-field` · `delete-custom-field`
**Stolperer:** Der **Datentyp ist endgültig** — einmal gewählt, nie änderbar; ein Datum ist ein
Datumsfeld. Anlegen speichert keinen Wert; gib eine Beschreibung. Ändern nimmt Name, Beschreibung,
Gruppe (`category`; leer sortiert in keine) und Labels — Typ und Mehrwertigkeit werden abgewiesen;
das Ergebnis listet, was das Feld benutzt. Löschen vernichtet die Werte aller Kontakte in diesem
Feld, ohne Undo; ein noch benutztes Feld wird mit Nennung abgewiesen. Der Platzhalter eines
gelöschten Felds rendert leer.
