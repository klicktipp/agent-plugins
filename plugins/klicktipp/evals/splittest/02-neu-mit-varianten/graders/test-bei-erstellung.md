---
type: llm
focus: mock_calls
weight: 1
---
Der Aufruf von create-newsletter-draft trägt bereits ein splitTest-Objekt — der Test wird
bei der Erstellung entschieden. Die Aufrufe fallen durch, wenn der Newsletter erst ohne
Splittest angelegt und der Test danach konfiguriert wird.
