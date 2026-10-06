# Opt-in-Werkzeuge — Wofür, Nicht, Stolperer

Den vollständigen Wortlaut jeder Beschreibung und jedes Parameters, wie der Server ihn veröffentlicht,
trägt [contracts.md](contracts.md); hier steht die Deutung. Der Ablauf steht in `../SKILL.md`.

`R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht einen echten Empfänger oder eine
Automation · `I` ein zweiter gleicher Aufruf ändert nichts mehr. Jedes Werkzeug nimmt optional
`accountId`; weggelassen heißt das Konto des Zugangs.

| Werkzeug | | Wofür |
| --- | --- | --- |
| `search-opt-in-processes` · `get-opt-in-process` | R | Opt-in-Prozesse (= Abonnentenlisten); volle Konfiguration nur im Detail. |
| `create-opt-in-process` | | Einen Prozess anlegen, auf Wunsch als Kopie. Die Bestätigungsmail entsteht mit (`confirmationEmailId`). |
| `update-opt-in-process` | I | Einstellungen schreiben; nur was übergeben wird. |
| `delete-opt-in-process` | D | Löschen nimmt die Bestätigungsmail mit, die Kontakte bleiben. |
| `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email` | R / I | Betreff, Absender, Antwortadresse, CC/BCC, Domain — dazu `senderEmailOptions` und `senderDomainOptions`. |
| `get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content` | R / I | HTML und Plain, jeder ganz geschrieben. **Nicht die Baustein-Werkzeuge.** |
| `preview-opt-in-confirmation-email` | R | Der gespeicherte Text als Bild, ohne Signatur, Bestätigungslink und Empfängerdaten. |
| `send-opt-in-confirmation-email-test` | DO | Eine echte Testmail; eine unbekannte Adresse wird zum getaggten Kontakt. |
| `get-opt-in-process-redirect-url` | R | Die Pending- oder Danke-Seite eines Kontakts. Persönliche Daten. |

### `search-opt-in-processes` · `get-opt-in-process`
**Wofür:** ID, Name, Opt-in-Modus, Flags; das Detail zusätzlich Bestätigungsmail, Weiterleitungen,
Löschung ausstehender Abonnenten, Labels, Notizen. **Stolperer:** Gelöschte fehlen in der Suche.

### `create-opt-in-process`
**Wofür:** einen Prozess anlegen — der Name ist Pflicht, alles andere wie beim Ändern.
`copyFromOptInProcessId` kopiert einen bestehenden samt Mailtext; daneben übergebene Argumente
gewinnen. **Stolperer:** `useForChangeEmail` gibt es hier nicht; zwei gleiche Aufrufe erzeugen zwei
Prozesse oder scheitern am doppelten Namen.

### `update-opt-in-process`
**Wofür:** Name, Opt-in-Modus, Weiterleitungen samt Parametern, erneutes Senden der Bestätigung,
Löschung ausstehender Abonnenten, Labels, Notizen, die Rolle für E-Mail-Änderungen. **Stolperer:** Ein
Aufruf ohne Feld wird abgewiesen. `metaLabels` ersetzt die Liste. Seiten- und UTM-Parameter wirken nur
zusammen mit der URL ihrer Seite im selben Aufruf. `optInMode: "single"` meldet spätere Kontakte ohne
Bestätigung an — frag. `useForChangeEmail: true` nimmt die Rolle dem Prozess weg, der sie hatte.

### `delete-opt-in-process`
**Nicht:** die Kontakte — die bleiben angemeldet. **Stolperer:** Der Standard-Prozess lässt sich nicht
löschen, und ein Prozess, auf den Formulare, Kampagnen oder andere Entitäten zeigen, wird mit deren
Namen abgewiesen. `create-opt-in-process` legt einen neuen an, nicht *diesen* wieder.

### `get-opt-in-confirmation-email` · `update-opt-in-confirmation-email`
**Stolperer:** Eine **leer gespeicherte** Absender- oder Antwortadresse heißt „die aktuelle Adresse
des Kontos"; wer genau diese Adresse schreibt, speichert wieder leer — gewollt. Absender nur aus
`senderEmailOptions`. `senderDomain` meist weglassen; nur übergeben, wenn `senderDomainOptions` eine
Wahl anbietet.

### `get-opt-in-confirmation-email-content` · `update-opt-in-confirmation-email-content`
**Stolperer:** Beide Körper werden ganz geschrieben, nicht gepatcht; wer nur einen schreibt, lässt eine
Mail zurück, die zwei Empfängern zwei Dinge sagt. Eine abgewiesene Schreibung trägt `stored: false`,
und die Mail sagt weiter, was sie vorher sagte — bis auf dieses Flag verwechselbar mit einem Erfolg.

### `preview-opt-in-confirmation-email` · `send-opt-in-confirmation-email-test`
**Stolperer:** Die Vorschau zeigt den gespeicherten Text; Signatur, Bestätigungslink und Empfängerdaten
kommen erst beim Versand dazu. Der Testversand ändert das Konto: eine Adresse, die noch kein Kontakt
war, wird einer und bekommt einen Tag — und Taggen startet Automationen. Der Link im Test bestätigt
niemanden.

### `get-opt-in-process-redirect-url`
**Wofür:** die Seite eines Kontakts per E-Mail-Adresse; `optInProcessId` weggelassen nimmt den
Prozess, über den die Adresse sich angemeldet hat. Ohne eigene Seite kommt die von KlickTipp gehostete.
**Stolperer:** Die Adresse ist Pflicht und bestimmt, über wen die Antwort ist. `redirectPage: pending`
heißt „noch nicht bestätigt", nicht „falsch eingestellt" — auch bei bestätigten Kontakten, wenn der
Prozess bei jeder Anmeldung erneut fragt. Die URL trägt ID, E-Mail, Liste, Schlüssel und
Empfehlungslink — nie in ein Protokoll, eine Notiz oder einen Newsletter.
