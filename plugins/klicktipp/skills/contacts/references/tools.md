# Contact tools — what for, what not, pitfalls

**This file does not repeat the tool descriptions.** The MCP server already sends every description
and parameter. What is here is the order between calls, the pitfalls, and what one tool means for
another. The procedure is in `../SKILL.md`.

`R` reads only · `D` deletes or replaces without undo · `O` reaches something outside the account (a
real recipient, an automation). Every tool takes an optional `accountId`.

| Tool | | What for |
| --- | --- | --- |
| `search-contacts` · `get-contact` | R | Find contacts (one row per channel, cursor, no total) and read one. |
| `upsert-subscribed-contact` | DO | Add a contact by hand, subscribed at once — no opt-in, no confirmation. |
| `subscribe-contact-via-opt-in-process` · `unsubscribe-contact` | DO | One channel through a process / off. Need `approval`. |
| `update-contact-values` | DO | Field values. Not: addresses, opt-in, subscriptions. |
| `update-contact-email` | DO | Replace one email address; status stays, nothing is confirmed. |
| `delete-contact` | DO | The whole contact, both channels, history included. |
| `get-contact-history` · `add-contact-history-note` | R / D | Read the history; add a note that can never be removed. |
| `search-duplicate-contacts` | R | Detected duplicate pairs; merging only in the app. |
| `tag-contact` · `untag-contact` | O | → skill `tags`. |

### `search-contacts` · `get-contact`
**Pitfall:** pages of at most 100 without a total; an account with 80,000 contacts is 800 calls.
`get-contact` reads field values and manual tags **of one `referenceId`** (default `0`) and one email
— not the complete channel or reference record.

### `upsert-subscribed-contact`
**Unlike `subscribe-contact-via-opt-in-process`:** no opt-in process, **no confirmation email**, the
contact is `subscribed` at once and in the audience of the next mailing. **Pitfall:** an unsubscribed
address is rejected, not resubscribed. An existing address is *updated* — the values passed overwrite
the old ones, and `alreadyExisted` says so. Counts against the daily import limit. An unknown field
ID or tag is refused, nothing is skipped. **Before the first call in a conversation** name the
no-double-opt-in effect and link the [Import Policy](https://www.klicktipp.com/import-policy/) — see
"Import Policy before direct subscription" in the skill.

### `subscribe-contact-via-opt-in-process` · `unsubscribe-contact`
Exactly one channel, email *or* phone. Can send a confirmation email and start automations; the tag
passed along can start more. Other channels and references stay untouched; unsubscribing removes no
tags.

### `update-contact-values`
`fields`: per `fieldId` a global key or a numeric field ID of the account, `referenceId` defaults
to 0. The field must exist (skill `custom-fields`) — nothing is created on the side. An empty value
clears the field.

### `update-contact-email`
Without `currentEmail` the primary address is replaced. A contact merged from duplicates can have
more addresses; `get-contact` shows only the primary one, but every answer of this tool lists all of
them in `emailAddresses`. To replace another one, pass it as `currentEmail`; an address the contact
does not have is refused with the addresses it does have.

Refused for an unsubscribed address, an address another contact has, an invalid or blacklisted
address, or once the daily import limit is reached. The old address is gone afterwards; the change is
in the history. The mobile number is not changed here.
