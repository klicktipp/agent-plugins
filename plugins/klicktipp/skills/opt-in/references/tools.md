# Opt-in tools — what for, what not, pitfalls

**This file does not repeat the tool descriptions.** The procedure is in `../SKILL.md`.

`R` reads only · `D` deletes or replaces without undo · `O` reaches a real recipient or an automation.

| Tool | | What for |
| --- | --- | --- |
| `search-opt-in-processes` · `get-opt-in-process` | R | Processes (= subscription lists); full configuration only in the detail. |
| `create-opt-in-process` | | A process; the confirmation email comes with it (`confirmationEmailId`). |
| `update-opt-in-process` · `delete-opt-in-process` | D | Write settings; deleting takes the confirmation email, the contacts stay. |
| `get-` / `update-opt-in-confirmation-email` | R / D | Subject, sender, reply-to, CC/BCC, domain, plus the permitted options. |
| `get-` / `update-opt-in-confirmation-email-content` | R / D | HTML and plain, each written whole. Not the block tools. |
| `preview-opt-in-confirmation-email` | R | The stored text, without signature, confirmation link or recipient data. |
| `send-opt-in-confirmation-email-test` | DO | A real mail; an unknown address becomes a tagged contact. |
| `get-opt-in-process-redirect-url` | R | One contact's pending or thank-you page. Personal data. |

### `search-opt-in-processes` · `get-opt-in-process`
Deleted processes are absent from the search.

### `create-opt-in-process`
The name is required. `copyFromOptInProcessId` copies an existing process including its email text;
arguments passed alongside win. `useForChangeEmail` does not exist here; two identical calls produce
two processes or fail on the duplicate name.

### `update-opt-in-process`
Writes only what it receives; a call without a field is rejected. `metaLabels` replaces the list.
`optInMode: "single"` subscribes later contacts without confirmation — ask. `useForChangeEmail: true`
takes the role from whichever process had it; there is one per account.

### `update-opt-in-confirmation-email`
An **empty stored** sender or reply-to means "the account's current address"; writing exactly that
address stores empty again — intended. Usually omit `senderDomain`; pass it only when
`senderDomainOptions` offers a choice.

### `get-` / `update-opt-in-confirmation-email-content`
Both bodies are written whole, not patched; writing only one leaves a mail that tells two recipients
two things. A rejected write returns `stored: false` and the mail still says what it said before.

### `get-opt-in-process-redirect-url`
Omitting `optInProcessId` takes the process the address subscribed through. Without an own page you
get KlickTipp's hosted one. `redirectPage: pending` means the contact has not confirmed yet, not a
misconfiguration — it also hits confirmed contacts when the process asks for confirmation on every
subscription. The URL carries ID, email, list, key and referral link — never into a log, a note or a
newsletter.
