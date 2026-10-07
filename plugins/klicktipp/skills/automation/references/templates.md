# Automationsvorlagen: finden, lesen, importieren

Zwei Arten von Vorlagen, ein Werkzeugpaar für beide:

| Quelle | Was der Nutzer hat | Was du als `templateLink` übergibst |
|---|---|---|
| **Katalog** — die fertigen Automationen der Business Automation Masterclass (BAM), die KlickTipp mitbringt | nichts, oder einen Anwendungsfall („Termin nachfassen") | die `uri` aus `search-automation-templates`, z. B. `klicktipp://automation-templates/teve` |
| **Geteilte Vorlage** — eine Vorlage, die ein anderes Konto veröffentlicht hat | einen Link `https://app.klicktipp.com/template/…` | den Link, wie er eingefügt wurde; Host, Schrägstrich am Ende und Zeilenumbrüche sind egal |

## Reihenfolge

1. **Finden.** `search-automation-templates` mit dem Ziel des Nutzers in seinen Worten als `query`
   (Deutsch trifft am besten — der Katalog ist deutsch). Ohne `query` kommt alles; `module`
   beschränkt auf ein Masterclass-Modul. Jeder Treffer trägt `description`, `startsWhenTagged`,
   `emailSubjects`, `tagNames`, `customFieldNames` und `includedAutomations`. Wähle danach, nicht
   nach dem Namen. Stell zwei oder drei Kandidaten mit je einem Satz vor, wenn die Wahl nicht
   offensichtlich ist.
2. **Lesen.** `get-automation-template` mit der uri oder dem Link. Die Antwort enthält:
   - `objects` — jeden Tag, jedes Feld, jede E-Mail und jeden Outbound, den der Import mitbringt,
     jeweils mit `suggestedExistingId`: dem gleichnamigen Objekt des Kontos, auf das der Import
     standardmäßig abbildet. `''` heißt: standardmäßig eine Kopie.
   - `smartImportAvailable` — ob dieses Konto Name, Präfix, Labels und Zuordnungen überhaupt wählen darf.
   - `importable` / `refusal` — ob ein Import jetzt abgelehnt würde (etwa am Outbound-Limit) und warum.
   - `notTransferable` — Bezüge, die der Import nicht übertragen kann, typischerweise eine
     Startbedingung auf ein Formular oder einen API-Key des Herkunftskontos. Sie müssen nach dem
     Import neu gesetzt werden; sag das vor dem Import.
3. **Mit dem Nutzer klären**, nur was das Konto wählen kann (`smartImportAvailable`):
   - den **Namen** der neuen Automation — fragen, nicht erfinden; Standard ist der Vorlagenname, und
     ein schon vergebener Name wird abgelehnt;
   - ein optionales **Präfix** für jedes angelegte Objekt, damit importierte Tags und E-Mails
     erkennbar bleiben;
   - **Zuordnungen**: für jeden Tag und jedes Feld ein bestehendes weiterverwenden oder eine Kopie
     anlegen. Weiterverwenden zählt bei Tags und Feldern, mit denen das Konto schon arbeitet
     (`per Du`, `Kunde`, Vorname).
4. **Importieren.** `import-automation-template`:

   ```json
   {
     "templateLink": "klicktipp://automation-templates/teve",
     "automationName": "Terminvereinbarung",
     "objectPrefix": "TEVE",
     "mappings": [
       {"type": "tag", "incomingId": "1234", "useExistingId": "987"},
       {"type": "custom-field", "incomingId": "5678"}
     ]
   }
   ```

   Eine Zuordnung mit `useExistingId` verwendet dieses Objekt weiter; ohne wird das Objekt kopiert.
   Nicht aufgeführte Objekte nehmen den Standard aus Schritt 2. **Ohne `mappings` wird alles
   kopiert** — das ist der Standard des Dialogs bei ausgeschaltetem Smart-Import.
5. **Berichten** aus der Antwort, nie aus dem Gedächtnis: `automationName` und `editUrl`, was
   `created`, was `mapped`, was `failed` ist, und `notTransferable`.
6. **Die Automation fertigstellen** mit den übrigen Werkzeugen dieses Skills — die importierte ist
   eine gewöhnliche Automation. Die Startbedingung setzen, wo `notTransferable` sagt, dass sie nicht
   übertragen werden konnte, Platzhaltertext in den E-Mails ersetzen (die Sales-Funnel-Vorlagen
   tragen `[Was ist das Thema deines Angebots]` und Ähnliches), dann `validate-automation`.

## Was der Import ist und was nicht

- **Er fügt hinzu, und es gibt kein Undo.** Jedes angelegte Objekt bleibt im Konto, in der Antwort
  aufgeführt. Ein zweiter Aufruf importiert ein zweites Mal.
- **Es wird nichts versendet.** Die Automationen werden **pausiert** angelegt — nicht gestartet.
  Starten ist `prepare-automation-activation`, das ein Mensch in KlickTipp bestätigt.
- **Abgelehnt, bevor etwas geschrieben wird**, wenn das Outbound-Limit überschritten würde, der Name
  vergeben ist, eine Zuordnung auf ein Objekt zeigt, das das Konto nicht hat, oder zwei
  Vorlagenobjekte auf dasselbe abgebildet werden. Die Ablehnung sagt, was; das beheben und erneut
  aufrufen.
- **Ohne Smart-Import** kann das Konto weder Name, Präfix, Labels noch Zuordnungen wählen; wer sie
  übergibt, wird abgelehnt. Jedes Objekt wird dann mit dem Präfix `Importiert` kopiert, wie im Dialog.
- Die E-Mails kommen mit ihrem Inhalt an: klassische E-Mails als HTML, Drag-and-Drop-E-Mails mit
  ihrem Editor-Dokument. Platzhalter kopierter Felder werden auf die neuen Felder umgeschrieben.
