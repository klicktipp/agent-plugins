# Einen Baustein anlegen

Wann du hier landest: ein Baustein soll **neu** in einen Entwurf, der schon steht. Einen ganzen
Körper baust du nicht so (siehe „Einen Körper füllen" in `SKILL.md`), und zum Ändern eines
vorhandenen Bausteins brauchst du diese Datei nicht.

Zwei Dinge überraschen hier regelmäßig: manche Bausteine kommen leer und lassen sich von hier aus
nicht füllen, und ein neuer Baustein erbt sein Aussehen von einem Nachbarn, den du nicht ausgesucht
hast.

**Lies die `warnings` der Schreibantwort und gib sie weiter.** Ein Baustein wird auch dann
gespeichert, wenn er so nichts zeigt — das ist Absicht, weil es ein legitimer Zwischenstand auf dem
Weg zu einem Baustein ist, den ein Mensch im Editor fertigstellt. Gesagt wird es aber, und zwar in
der Antwort: ein Video ohne `thumbSrc`, eine Liste ohne `<ul>`/`<ol>`, ein unkonfiguriertes Add-on,
eine personalisierte E-Mail. Melde nie „hinzugefügt", wenn die Antwort dir sagt, dass der Baustein
leer bleibt — sag, was noch fehlt und wo es gesetzt wird.

**Countdown, Kontaktkarte und Wowing-Video kannst du nicht einfügen.** Ihr Inhalt entsteht in
einem Dialog des KlickTipp-Editors, und kein Werkzeug hier erreicht ihn. Es gab einmal Add-Werkzeuge
dafür; sie setzten eine leere Hülle, die beim Versand nichts anzeigte, und sind genau deshalb weg.
Wird einer dieser Bausteine gewünscht, ist die Antwort der Editor — nenne ihn, statt etwas
Ähnliches aus Text und Bild nachzubauen und es als Countdown auszugeben. Vorhandene Bausteine
dieser Art bleiben lesbar, verschiebbar und entfernbar.

**Der KI-Text-Baustein** kommt dagegen weiterhin leer und bleibt es, bis jemand ihn im Editor
einrichtet. Füge ihn nur ein, wenn der Nutzer ihn ausdrücklich will, und sag den Satz *vorher*:
„Ich kann den Baustein setzen, einrichten musst du ihn im Editor — willst du das?"

Der KI-Text-Baustein hat zusätzlich ein Tor: ohne die Freischaltung des Kontos wird sein Add mit
`kind_not_available` abgewiesen und es ändert sich nichts. Das ist keine Störung, sondern eine
Berechtigung — melde es als solche, statt es zu umgehen.

Ausgenommen ist die **personalisierte E-Mail**: die hat mit `email-personalized-email-write` ein
echtes Feld und lässt sich hier fertigstellen. Dafür gilt bei ihr das Umgekehrte: der
Newsletter-Editor bietet sie im Einfügen-Menü **nicht** an — nur Automationen tun das. Eine Person
kann sie dort also weder anlegen noch nach einem Entfernen zurückholen; nur dieser Werkzeugsatz
kann das. Füge sie deshalb nur auf ausdrücklichen Wunsch ein und sag diesen Punkt im selben Zug
dazu.

**Hinzufügen: der neue Baustein sieht aus wie ein Baustein derselben Art — aber nicht unbedingt wie
sein Nachbar.** Der Server kopiert beim Anlegen das `style`-Objekt und den Innenabstand vom
**ersten** Baustein derselben Art, den er findet: erst in derselben Spalte, dann in derselben Zeile,
dann irgendwo im Newsletter. *Erster*, nicht *nächstgelegener* — die Einfügeposition spielt dabei
keine Rolle. Was im
`html` steckt — Wrapper, `<p style=…>`, Schriftgrößen —, kopiert er **nicht**; das ist dein Teil:
nimm das `html` des Nachbarbausteins derselben Art (bevorzugt aus derselben Zeile oder dem
Abschnitt, in den der neue Block kommt — nicht die Vorschauzeile, nicht den Footer) als Vorlage und
ersetze nur die Wörter. Erfinde nichts: keine Werte, die nicht im Dokument stehen, keine
`font-family` aus dem Kopf, keine Größen, die du für passend hältst.

Zwei Dinge bleiben:

1. Hat der Newsletter **keinen** Baustein dieser Art, gibt es nichts abzulesen — dann trägt der neue
   Baustein die Werte seines Startzustands, und dein `html` kommt ohne Vorlage: dann schlichtes
   Markup (`<p>`, `<strong>`, `<a href>`), nichts erfunden. Sag das dem Nutzer, statt ein fertiges
   Ergebnis zu melden.
2. Mehrere neue Bausteine kosten mehrere Aufrufe: ein Add legt **einen** Baustein an und gibt die
   neue Revision zurück, mit der der nächste arbeitet. Da jedes Add seinen Inhalt mitnimmt, ist das
   ein Aufruf je Baustein — kein zweiter zum Füllen.
3. **Eine Reihe von Adds macht eine Reihe gleicher Bausteine.** Sobald der erste neue Absatz in der
   Spalte steht, ist *er* für den zweiten der erste seiner Art — und dessen Abstände wandern durch
   die ganze Reihe. Zehn so eingefügte Absätze tragen alle dasselbe Padding, während ein gestalteter
   Entwurf seine Abstände von Abschnitt zu Abschnitt variiert. Das ist als Design-Sprung sichtbar
   und war es in der Praxis schon.
