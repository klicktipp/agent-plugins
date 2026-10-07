# What the tool descriptions do not say

**This file does not repeat the tool descriptions.** The MCP server already sends you every
description and every parameter with its type and limits. Here is what those cannot say: the order
between calls, the pitfalls, and what one tool means for another. The procedure is in `../SKILL.md`.

`R` reads only · `D` replaces or deletes without undo · `O` reaches a real recipient · `I` a second
identical call changes nothing.

## Newsletter

| | |
|---|---|
| `search-newsletters` | A draft has **no send date** and falls into no `sendDate` window, even when a date was set and cancelled — count drafts by `status`. The way from an editor URL to the newsletter: compare the `emailId` in the URL against the results; neighbouring IDs belong to different newsletters. `nextCursor` goes back unchanged and with the same filters. |
| `get-newsletter` | Projections are all or nothing: one that cannot be served fails the whole call. `audienceReach` is a measurement, not a stored number. A split test has `emailId: null` and its variants in `splitTestVariants`. `conversionPixel` gives one `snippet` per sender domain — pass it on **verbatim** and name the domain; the wrong domain counts nothing. |
| `create-newsletter-draft` | Without a filter the audience is `all_contacts` — the widest set, not the narrowest. A `splitTest` object here is irreversible in both directions (skill `splittest`). |
| `update-newsletter-draft` | Writes six fields only; sender, signature and schedule are rejected rather than ignored. **Subject and pre-header invalidate a read `contentRevision`** — the response says `contentRevisionInvalidated`. The audience is **replaced, not extended**. |
| `delete-newsletter-draft` | No recycle bin. A name resembling the one asked for, found by your own search, is not consent. |
| `configure-newsletter-delivery` | Validates against the lists it returns itself (`availableSenderAddresses`, `availableSenderDomains`). **Address and domain belong together** — changing only the address leaves the old domain and is refused. An empty domain list means the account picks no domain. `linkTracking` cannot be switched off without an own sending domain. |
| `get-utm-tracking-settings` | `R` — what `utm_campaign` is filled with. With `email-name` the newsletter's internal name is the campaign name; any other value means `utmCampaignName` is not the only thing that decides. |
| `preview-email-editor` | `R` — the **draft**, unpublished edits included, placeholders unresolved. Proof of the look, not of a recipient's footer. |
| `search-signatures` | `R` — usable signatures only unless `includeUnusable`; the order is **not** the tag priority. `signatureId: 0` for "pick by tags" is not an entry of this list. |
| `send-newsletter-test` | Carries the **published** content — run `publish-newsletter-email-content` first, otherwise `newsletter_send_content_publish_required`. An address that is not yet a contact **becomes one and gets tagged**, and tagging starts automations. Newer draft changes produce a `warnings`: the test shows the older state. |
| `prepare-newsletter-dispatch` | Does not send. Never say "sent" afterwards. |
| `cancel-newsletter-dispatch` | Only while `canBeCancelled`. What is already out stays out. ⚠ not on production — there the way is the `scheduleUrl`. |

## Signatures — ⚠ not on production

`search-signatures` / `get-signature` deliver the candidates for `signatureId`. `create-signature`,
`update-signature`, `replace-signature-content` and `configure-signature-delivery` write them.

**The placeholder rules for signature content** apply to `create-signature` and `replace-signature-content` alike, and
the server rejects what breaks them:

| Body | Requires | Forbids |
|---|---|---|
| HTML | `%Link:Unsubscribe%` as a link `href`, plus `%User:FirstName%`, `%User:LastName%`, `%User:Street%`, `%User:Zip%`, `%User:City%`, `%User:Country%` | — |
| plain text | the same placeholders; the unsubscribe one may be plain text | — |
| transactional HTML | the address placeholders; `%Link:SubscriberInfo%` recommended | **`%Link:Unsubscribe%`** |

Accounts permitted to omit address details are exempt from the address placeholders, never from the
unsubscribe link.

Plain text is trimmed and **stored only if the account allows text editing**; otherwise it is
ignored — even when supplied — and regenerated from the HTML. So do not expect supplied text to come
back unchanged.

**The transactional version is the reason the field exists**, not an edge case: it goes to first
contacts (SOI confirmation), where an unsubscribe link would unsubscribe from a subscription that
was never confirmed. Offer it when a signature is created, instead of waiting to be asked — see
[SKILL.md](../SKILL.md), step 4.
