# Die veröffentlichten Verträge — Tags

Wort für Wort das, was der Server in `tools/list` für die 7 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Diese Datei spiegelt den Server, sie interpretiert ihn nicht: ändert sich eine
Werkzeugbeschreibung, wird sie hier wörtlich nachgezogen. Wofür ein Werkzeug da ist, was es nicht
tut und woran man sich stößt, steht in [tools.md](tools.md).

## Inhalt

`search-tags` · `get-tag` · `create-manual-tag` · `update-manual-tag` · `delete-manual-tag` · `tag-contact` · `untag-contact`

## `search-tags` · RI

**Search tags**

Lists the tags of a KlickTipp account with ID, name, type, whether they can be written and whether a contact can carry them more than once. Tags are either manual -- created and assigned deliberately -- or put on contacts by KlickTipp itself when something happens, for example a newsletter being sent, opened or clicked; the type says which. Can be narrowed by a text the name has to contain, by type, to the writable ones, by whether a contact can carry a tag once per subscription or only once overall, and to tags with a system role such as the test contact marker. The description of a tag is not part of the list -- use get-tag for that.

Parameter:

- `query` — null | string (maxLength 250): Text the name of a tag has to contain; omit to list them all
- `type` — null | string (maxLength 100): Only tags of this type, e.g. "tag" (manual), "campaign-sent", "email-opened"; omit for every type
- `onlyWritable` — null | boolean: Only manual tags the write tools may touch; omit to include the ones KlickTipp sets itself
- `multiValue` — null | boolean: true: tags a contact can carry once per subscription; false: once overall; omit for both
- `systemRole` — null | string (einer von `test-contact`): Only tags with this system role; "test-contact" marks contacts that receive test emails
- `limit` — null | integer (minimum 1; maximum 200): How many tags to return at most, 1 to 200, 50 by default
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `get-tag` · RI

**Get tag**

Returns one tag of a KlickTipp account with the context needed to tell what it means: its type, whether it can be written, what it stands for, the entity behind it for tags KlickTipp puts on contacts itself, the internal note and labels of the account, how many contacts carry it, and which tags a contact is subscribed to or unsubscribed from when this tag is assigned. Also says whether this is the tag the app marks test contacts with.

Parameter:

- `tagId`* — integer (minimum 1): ID of the tag, as shown in the KlickTipp app URL
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `create-manual-tag`

**Create manual tag**

Creates a manual tag in KlickTipp, one that is assigned deliberately rather than by KlickTipp itself. Creating a tag assigns it to nobody and changes no contact. Tags are never created as a side effect elsewhere, so a tag a contact should carry has to be created here first. The name has to be unique within the account. The description is what tells a later reader what the tag means.

Parameter:

- `name`* — string (minLength 1; maxLength 250): Name of the tag, which has to be unique within the account and cannot be a number alone
- `description` — null | string (maxLength 2000): What the tag stands for, so a person or a model reading it later knows when to assign it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `update-manual-tag` · I

**Update manual tag**

Changes the name or the description of a manual tag in KlickTipp. Only manual tags can be changed: a tag KlickTipp puts on contacts itself takes its name from the newsletter, automation or form behind it and is refused. Renaming a tag does not change who carries it and does not break the campaigns and automations that use it, since those refer to its ID -- but the result lists them, because a rename shows up wherever the name is read. Everything else about the tag, including its auto-subscribe configuration and whether it is single value, stays as it is.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to change
- `name` — null | string (maxLength 250): New name of the tag, which has to stay unique within the account; omit to keep the current one
- `description` — null | string (maxLength 2000): New description of what the tag stands for; omit to keep the current one
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `delete-manual-tag` · DOI

**Delete manual tag**

Deletes a manual tag in KlickTipp and takes it off every contact that carries it. Only manual tags can be deleted; a tag KlickTipp puts on contacts itself is refused. A tag that campaigns, automations or other entities still use is refused as well, and the refusal names them, so nothing that depends on the tag breaks silently. This cannot be undone, so only call it for a tag the user has explicitly asked to delete.

Parameter:

- `tagId`* — integer (minimum 1): ID of the manual tag to delete
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `tag-contact` · O

**Assign manual tag**

Assigns one existing writable manual tag to one contact. This may immediately start or alter campaigns, autoresponders, outbound events and automations. The caller must explicitly approve those effects. Unknown, foreign or non-manual tags are rejected and never created.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID; unknown tags are rejected and never created
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: tagging may start campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `untag-contact` · DOI

**Remove manual tag**

Removes one existing writable manual tag from one contact. This may immediately alter campaigns, autoresponder queues and automations, so the caller must explicitly approve those effects. Removing a tag does not unsubscribe-contact the contact and changes no subscription or channel state.

Parameter:

- `contactId`* — integer (minimum 1): Numeric contact ID returned by search-contacts
- `manualTagId`* — integer (minimum 1): Existing writable manual tag ID to remove
- `approval`* — string (einer von `I_ACCEPT_AUTOMATION_EFFECTS`): Exactly I_ACCEPT_AUTOMATION_EFFECTS: removal may alter campaigns and automations
- `referenceId` — integer (minimum 0; Default `0`): Reference for a multi-value manual tag; use 0 for contact-wide tags
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
