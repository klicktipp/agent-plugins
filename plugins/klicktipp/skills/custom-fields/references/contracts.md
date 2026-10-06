# Die veröffentlichten Verträge — Eigene Felder

Wort für Wort das, was der Server in `tools/list` für die 5 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-custom-fields` · `get-custom-field` · `create-custom-field` · `update-custom-field` · `delete-custom-field`

## `search-custom-fields` · RI

**Search custom fields**

Lists the custom field definitions of a KlickTipp account with ID, name, data type, the placeholder that renders the value of the receiving contact in newsletter content, and the group the account sorted the field into. Fields the account created itself come first, newest first, followed by the global fields every KlickTipp account has, such as first name or city; the global ones are marked with isGlobal and cannot be changed or deleted. Can be narrowed by a text the name has to contain, by data type, and to the fields the write tools may touch. This lists definitions -- what a contact has stored in a field is read through the contact tools.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a field has to contain; omit to list them all
- `types` — array | null: Only fields of these data types, for example ["field-date", "field-datetime"]; omit for every type
- `onlyWritable` — null | boolean: Only the account's own fields, the ones the write tools may touch; omit to include the global fields
- `limit` — null | integer (minimum 1; maximum 200): How many fields to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-custom-field` · RI

**Get custom field**

Returns one custom field definition of a KlickTipp account: its name and data type, the placeholder that renders the value of the receiving contact in newsletter content, the key the public API addresses it with, what the account wrote about what the field holds, its internal note, group and labels, the field its values are copied to, and whether a contact can hold more than one value in it. This returns the definition -- what a contact has stored in the field is read through the contact tools.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): Field ID: a number for the account's own field, a name such as "FirstName" for a global one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-custom-field`

**Create custom field**

Creates a custom field definition in KlickTipp and returns its ID and the placeholder that renders it in newsletter content. Creating a field stores no value and changes no contact. Fields are never created as a side effect elsewhere, so a field a contact should have a value in has to be created here first. The data type is picked once and for good: it cannot be changed afterwards, so pick the one that matches what will be stored -- a date field for a date, a number field for an amount. multiValue decides whether a contact holds one value PER SUBSCRIPTION (true, the default when omitted) or one value overall (false); it is worth deciding here, because an existing field can only go from true to false and never back. The name has to be unique within the account. The description is what tells a later reader what belongs in the field.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the field, which has to be unique within the account
- `type`* — string (einer von `field-single`, `field-paragraph`, `field-email`, `field-number`, `field-url`, `field-date`, `field-time`, `field-datetime`, `field-html`, `field-decimal`): Data type of the field, which decides what can be stored in it and cannot be changed afterwards
- `description` — null | string (maxLength 2000): What the field holds, so a person or a model reading it later knows what to write into it
- `multiValue` — null | boolean: True: one value per subscription; false: one value overall; omit for true
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-custom-field` · I

**Update custom field**

Changes the name, description, group, labels, cardinality, subscription-email key, note or copy target of a custom field. Only what is passed is written; an empty string clears a text setting. The data type cannot be changed and is refused: an existing field keeps the type its stored values were written in. multiValue false collapses the field to ONE value per contact and DELETES the extra values contacts hold per subscription -- ask the person first, it cannot be undone and true is then refused for good. requestName is the key a contact writes as "key = value" in the body of a subscription email to fill this field; it addresses the field, so two fields sharing one means the first wins. copyToFieldId must name a field of a compatible type or the change is refused. Only fields the account created itself can be changed; the global ones are refused.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to change
- `name` — null | string (maxLength 250): New name of the field, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the field holds; omit to keep the current one
- `category` — null | string (maxLength 250): Group in the app; empty string sorts into none; omit to keep
- `metaLabels` — array | null (maxItems 50): New set of labels of the field, which replaces the current one; omit to keep the current labels
- `multiValue` — null | boolean: False collapses the field to one value per contact and DELETES the others; true is refused on a field that is already false; omit to keep
- `requestName` — null | string (maxLength 250): Key this field is addressed by in a subscription email body; empty string removes it; omit to keep
- `copyToFieldId` — null | string (maxLength 100; Muster `^[A-Za-z0-9_]*$`): ID of the field every value written here is also copied into; empty string stops the copying; omit to keep
- `notes` — null | string (maxLength 1000): Internal note on the field, which nobody outside the account sees; empty string removes it; omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-custom-field` · DI

**Delete custom field**

Deletes a custom field definition in KlickTipp and with it every value the contacts of the account hold in that field. This destroys contact data and cannot be undone, so only call it for a field the user has explicitly asked to delete. Only fields the account created itself can be deleted; the global fields every KlickTipp account has are refused. A field that opt-in forms, automations or other entities still use is refused as well, and the refusal names them, so nothing that reads the field breaks silently. The placeholder of a deleted field renders an empty value wherever content still carries it.

Parameter:

- `customFieldId`* — string (minLength 1; maxLength 100; Muster `^[A-Za-z0-9_]+$`): ID of the field to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
