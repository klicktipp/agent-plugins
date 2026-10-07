---
name: splittest
description: A/B tests of a KlickTipp newsletter — create, add, copy and remove variants, subject line per variant. Use it for split test, variant, winner or "test two subject lines", and when a tool reports `split_test_not_supported`. The lifecycle is `newsletter`.
---

# KlickTipp split tests

Several versions of the same send go to part of the audience, get measured, and the better one goes
to the rest.

Choose the intended connector and account before account-specific reads or writes; confirm them
from a tool response or account URL. Load the live contract for the next needed tool and reuse it.
Do not treat a staging label, an authorization error or a skill load as proof of account or version.

## The sentence everything follows from

**A split-test newsletter has no single email** — each variant *is* one.

Therefore: `emailId`, `contentUrl` and `metadata.subject` are `null`.
`update-newsletter-draft` rejects a subject. Each variant is addressed through its own
`editorUrl` from `splitTestVariants`. `deliveryConfiguration` is rejected without an `editorUrl`.

**`split_test_not_supported` is not an error** — it means "the request went to the newsletter but
belongs to a variant". The response carries an `appUrl`.

## Creating

Only `create-newsletter-draft` with a `splitTest` object. **All three fields are required and
none has a default:**

| field | |
|---|---|
| `testSizePercent` | 2–98. Share of the audience receiving a test variant. The app's slider starts at 20. |
| `testDurationHours` | 1–27777. |
| `winnerBy` | `opens` · `clicks` · `conversions` · `revenue` |

**Obtain all three before creating.** Ask for the missing values together: what share of real
recipients gets a test version, how long the wait is, and how the winner is chosen. Keep values
already supplied or confirmed across turns; do not ask for them again. Even a "just do it" request
needs these three decisions before creation. Never silently substitute the app's initial slider value
or call a suggestion a default.

**How to ask:** Prefer the client's native selection UI when it is actually available in this chat.
Offer short, understandable options for winner criterion and examples for test share and duration;
let the user enter a different valid value. A skipped question leaves that value missing, so ask
again before creation. If the client has no native selection UI or it fails to render, ask the
missing values in one clear text message with numbered choices. Do not describe plain text as
clickable. In either form, use everyday wording in user-facing questions (for example, “Öffnungen”
rather than `winnerBy: opens`); keep parameter keys and tool names for internal use unless the user
asks for them. A skill can request this interaction but cannot guarantee how every Claude client
renders it.

**Two gates apply first:**

- Split tests are **premium** — without `klicktipp premium` the refusal comes before anything is
  created.
- `conversions` and `revenue` need the **conversion pixel**; without it they are rejected. `opens`
  and `clicks` always work. Do not offer a criterion the account cannot measure.

**The decision is made at creation and never after, in both directions.** An ordinary newsletter
never becomes one, a split test never stops being one. Anyone wanting it later creates a new one —
say so early if the newsletter already exists.

**Afterwards exactly one variant exists** (with the subject from `create-newsletter-draft`). A test needs at
least two; the response says `needsMoreVariants: true`.

For a tiny audience, explain that the split can be checked technically but cannot provide a
meaningful comparison of open or click rates. Percentages describe the requested configuration;
do not claim a recipient distribution until the server has produced one, including its rounding.

When reusing another email, read its body with `get-email-editor-content` before describing its
wording or promising the variants will match. Newsletter metadata and subject are not the body.
If the source has not been read, say that content copying is planned but its text and fidelity are
not yet verified.

## Variants

The tools take **`campaignId`**, not the newsletter ID.

| What | With |
| --- | --- |
| Inspect the test (settings, variants, `hasStarted`) | `get-newsletter-split-test` |
| From a variant back to the test | `get-newsletter-split-test` with `emailId` |
| Change size, duration, criterion | `configure-newsletter-split-test` |
| Add a variant (empty or as a copy) | `add-newsletter-split-test-variant` |
| Subject, pre-header, name | `update-newsletter-split-test-variant` |
| Remove a variant | `remove-newsletter-split-test-variant` |
| Content of a variant | skill `email` through its `editorUrl` |

Every response contains the **whole** test — adding and removing redistribute the shares.

- **`copyFromEmailId` is almost always right.** An empty variant against a finished email only
  measures that people prefer emails with content. Create empty only when the variants are genuinely
  independent.
- **`copyFromEmailId` is the `emailId` of a variant of *this* test**, not of the template
  newsletter. Otherwise: "Email … is not a test variant of campaign …". The right IDs come from
  `get-newsletter-split-test`.
- **Write the content in one go**, not block by block: a block inserted individually takes its look
  from the **first block of the same kind in the column**, not from its neighbour — ten paragraphs
  all get the same padding, the template's rhythm is gone, and dividers and sub-headings never
  appear at all. Fill the body in a single call the way the skill `email` describes under "Filling a
  body": from a sibling variant with `replace-email-editor-content-from-email`, from an editor document with
  `replace-email-editor-content-from-document`, and only from HTML with `replace-email-editor-content-from-html`. Then adjust
  individual spots with `update-email-editor-text`. With split tests this shows twice over: every later run
  of block calls makes the variants differ in something the test never meant to measure.
- **One test tests one thing.** Variants differing in subject *and* content *and* timing produce a
  number without a cause. Say so and let the user decide. The common case: copy, then
  `update-newsletter-split-test-variant` with a new `subject`.

**`configure-newsletter-split-test`** writes only `testSizePercent`, `testDurationHours`, `winnerBy`;
omitted values stay, a call without a change is rejected. Only while the test has not started.

**Two locks:** a **started** test no longer lets its variants be changed, and the **last** variant
cannot be removed. `remove-newsletter-split-test-variant` deletes the email **with its content**, no undo — show label and
subject from `splitTestVariants` first.

## Reading

**Every variant brings its own `contentRevision`.** So do **not** read them individually before
writing — `get-newsletter` / `get-newsletter-split-test` deliver `editorUrl` and token together.
That saves one call per variant (15–30 s). Read a variant only when you need its **content**.

- **`get-newsletter-split-test`** — settings, `hasStarted`, all variants, `needsMoreVariants`. Takes
  `campaignId` **or** the `emailId` of a variant (the way back from an editor URL). The four write
  tools return the same response.
- **`get-newsletter`** — `splitTestVariants` with `emailId`, `label` ("A", "B"), `name`,
  `subject`, `editorUrl`. The test settings are not there.

## What does not work here

Turning an existing newsletter into a split test and changing a started test are unavailable. For
delivery configuration, activation and winner handling, inspect the current tool contracts and
state the supported path; use the `appUrl` where the available tools do not support the operation.
Do not claim that every split-test action is limited to the interface.

The observed `send-newsletter-test` contract describes `messageId` to select a split-test variant by
its `emailId`; this path was not exercised in the read-only retest. A test still needs that variant's
published content, an explicitly named recipient and disclosure of the real-mail/contact-tagging
effect. Never call it during a read-only plan.
Check the live contract before any action, because a skill cannot guarantee what a deployment offers.

## References

What the tool descriptions do not say → [references/tools.md](references/tools.md).
