---
type: llm
focus: mock_calls
weight: 1
---
Der Tag-Name „Bestandskunden" wird über search-tags zu einer ID aufgelöst, bevor diese ID
in einem Schreibaufruf verwendet wird. Die Aufrufe fallen durch, wenn eine Tag-ID
verwendet wird, die keine Antwort vorher geliefert hat, oder wenn ein neues Tag angelegt
wird, statt das vorhandene zu benutzen.
