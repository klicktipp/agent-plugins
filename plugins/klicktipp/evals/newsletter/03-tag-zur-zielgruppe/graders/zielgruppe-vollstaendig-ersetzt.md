---
type: llm
focus: mock_calls
weight: 1
---
Die Zielgruppe wird als Ganzes ersetzt, nicht erweitert. Die Aufrufe bestehen nur, wenn
die bestehende Zielgruppe gelesen wurde (get-newsletter mit der Zielgruppe), bevor
update-newsletter-draft aufgerufen wird, und der Schreibaufruf die vollständige neue
Menge der Tag-IDs enthält — das bereits gesetzte Tag UND das neue. Sie fallen durch,
wenn ohne vorheriges Lesen geschrieben wird oder wenn update-newsletter-draft nur das
neue Tag übergibt und das alte dabei verloren geht.
