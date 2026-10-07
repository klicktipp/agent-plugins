# The tools of this skill — what for, what not, pitfalls

**This file does not repeat the tool descriptions.** The MCP server already sends you every
description and every parameter with its type and limits. What is here is what those cannot say:
the order between calls, the pitfalls, and what one tool means for another. The procedure is in
`../SKILL.md`. `R` reads only · `D` deletes
without undo · `I` a second identical call changes nothing.

**Released, but only from the next production release onwards.** All five are in the production
allowlist; until that release is out, production keeps answering "unknown tool" — the state of the
deployment, not a defect. On staging and locally they are there.

They were **not** released while `create-newsletter-draft` already published its `splitTest`
argument. That was a dead end: split test yes/no is irreversible in both directions, a fresh test has
**one** variant and needs two — and the second came from exactly one of these tools. Anyone meeting
that on an older deployment finds the newsletter only in the app; do not invent a detour.

| Tool | | What for |
| --- | --- | --- |
| `get-newsletter-split-test` | R I | Read the whole test — by `campaignId` **or** the `emailId` of a variant. |
| `add-newsletter-split-test-variant` | | Create a test variant, empty or as a copy (`copyFromEmailId`). |
| `update-newsletter-split-test-variant` | I | Name, subject, pre-header **of one variant** — the only place for it. |
| `remove-newsletter-split-test-variant` | D | Remove a variant; its email goes with it. |
| `configure-newsletter-split-test` | I | Test size, duration, winner criterion. Not: whether it is a split test. |

`send-newsletter-test` is a separate newsletter tool. The observed live contract describes
`messageId` with the split-test variant's `emailId` to target one variant; this path was not
exercised in the read-only retest. Read its current contract before use; it sends a real email to
the specified address and can create and tag a contact. Do not generalize earlier
unsupported-tool reports to every deployment.

The split test itself comes into being through `create-newsletter-draft` with `splitTest`
(skill `newsletter`); the four write tools take `campaignId`, and the ID decides the campaign kind —
`get-newsletter-split-test` optionally takes the `emailId` of a variant instead. Each takes an optional
`accountId` (a subaccount).

### `get-newsletter-split-test`
**What for:** inspecting the test without touching it — `testSizePercent`, `testDurationHours`,
`winnerBy`, `hasStarted`, plus every variant with `emailId`, `label`, `name`, `subject` and
`editorUrl`, as well as `variantCount`, `sharePerVariantPercent` and `needsMoreVariants`.

**Two ways in, exactly one per call.** `campaignId` is the test itself. `emailId` is **one variant** —
the number from the editor URL someone has open — and the response says which test it belongs to and
what siblings it has. That is the way from an email back to the test and therefore to `editorUrl` and
`campaignId`, with which both can be edited. Passing both is rejected: they can mean different tests,
and this tool does not choose.

**Not:** the results of a running test — those are in the app, `statisticsUrl` from
`get-newsletter` leads there. **Pitfall:** the four write tools return the same response;
whoever just called one does not need this call again. A campaign that is not a split test is
rejected rather than answered with an empty test.

### `add-newsletter-split-test-variant`
**What for:** the second and further variants. **Not:** the test settings. **Pitfall:** almost always
`copyFromEmailId` (the `emailId` of a variant from `splitTestVariants`) — a copy carries the
original's content and is the way to measure *one* change; an empty variant against a finished one
measures nothing. Locked once the test has started.

### `update-newsletter-split-test-variant`
**What for:** name, subject, pre-header (≤ 120 characters; empty removes, omitted keeps) **of one
variant**, addressed by `emailId` from `splitTestVariants`. **Not:** the body (block tools through
that variant's `editorUrl`, skill `email`). **Pitfall:** invalidates that variant's
`contentRevision`. Locked once started. An empty subject is rejected — and a subject comes from a
human, never invented.

### `remove-newsletter-split-test-variant`
**What for:** removing a variant. **Pitfall:** that variant's email goes with it, without undo. The
last variant stays. Locked once started. Show which variant is meant first — label and subject.

### `configure-newsletter-split-test`
**What for:** `testSizePercent` (2–98, the share of the audience going to the variants; the rest gets
the winner), `testDurationHours` (1–27777; the app offers the same range as hours, days or months),
`winnerBy` (`opens` = highest open rate, `clicks` = most unique clicks, `conversions`, `revenue`).
Omitted means keep. **Not:** whether it is a split test. **Pitfall:** `conversions`/`revenue` only
with the conversion pixel, otherwise rejected. Locked once started.
