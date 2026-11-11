# Tag tools — what for, what not, pitfalls

**This file does not repeat the tool descriptions.** The procedure is in `../SKILL.md`.

`R` reads only · `D` deletes without undo · `O` reaches an automation or a real recipient.

| Tool | | What for |
| --- | --- | --- |
| `search-tags` · `get-tag` | R | Manual and system tags alike; detail with description, holder count, auto-subscriptions. |
| `create-manual-tag` · `update-manual-tag` | | Manual tags only: name and description. No setting for multi-value. |
| `delete-manual-tag` | D | Takes the tag off every contact. |
| `tag-contact` · `untag-contact` | O | One manual tag on/off for one contact, per `referenceId`. `approval` required. |

### `create-manual-tag` · `update-manual-tag` · `delete-manual-tag`
Creating assigns nothing to anybody; the name is unique within the account and cannot be a number
alone; give a description. Renaming breaks nothing (references run by ID) but shows everywhere the
name is read — the result lists the users; auto-subscription configuration and single-value stay as
they are. Deleting is irreversible; a tag still in use is rejected with its users named. System tags
are untouchable.

### `tag-contact` · `untag-contact`
Can start or change campaigns, autoresponders and outbound events immediately. `referenceId`
defaults to 0; for a multidimensional tag establish the intended reference first. Removing a tag
unsubscribes nobody.
