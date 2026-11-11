# Custom-field tools — what for, what not, pitfalls

**This file does not repeat the tool descriptions.** The procedure is in `../SKILL.md`.

`R` reads only · `D` deletes or replaces without undo.

| Tool | | What for |
| --- | --- | --- |
| `search-custom-fields` · `get-custom-field` | R | Definitions with placeholder, API key, group, labels, multi-value. Not a contact's values. |
| `create-custom-field` | | A definition; stores no value. Type is final, `multiValue` defaults to `true`. |
| `update-custom-field` | D | Name, description, group, labels, note, `requestName`, `copyToFieldId`, and `multiValue` true→false only. |
| `delete-custom-field` | D | The definition and every contact's value in it. |

### `search-custom-fields` · `get-custom-field`
Filters `query`, `types` (e.g. `field-date`, `field-datetime`), `onlyWritable`. Custom fields first
(newest on top), then the global ones. Global fields carry `isGlobal` and can be neither changed nor
deleted.

### `update-custom-field`
Only what is passed is written; an empty string clears a text setting. `metaLabels` replaces the
whole list. The data type is refused. `multiValue: false` deletes the extra per-subscription values
and can never go back. `requestName` is the key a contact writes as "key = value" in a subscription
email; two fields sharing one means the first wins. `copyToFieldId` needs a compatible type.

### `delete-custom-field`
Destroys the values of all contacts, without undo. A field still used by forms or automations is
refused with its users named. A deleted field's placeholder renders empty.
