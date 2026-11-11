---
name: "signatures"
description: "Find, inspect, create, copy and update KlickTipp email signatures, including content, sender profile, selection tags and digital business-card data. Use for reusable email footers or signature readiness; newsletter selection belongs to newsletter."
---

# KlickTipp signatures

Manage reusable account signatures through the current connector contract. Resolve the account once and keep it consistent. Verify that the signature tool family exists before promising a read or write.

Read-only inspection may happen during sending-readiness checks. Before proposing, selecting, copying, creating or changing visible sender identity, sign-off, business card or footer, require the confirmed `company-context` handback or task-only brief. Treat website and imprint data as candidates until confirmed.

After context is confirmed, propose sender presentations only when a real choice exists. Base them on the confirmed brand voice, addressing, sender identity and recipient relationship. “René von KlickTipp” and “Dein René” are examples, not defaults. Never invent a personal sender.

## Workflow

1. Search before creating. Include unusable signatures when diagnosing readiness.
2. Read the selected signature with its complete content even when the user only changes the sender address or reuses it. Check the visible content for a complete postal address and at least two direct contact paths, such as email plus phone or a contact form. Identity and address placeholders prove structure, not populated account data. Verify their resolved values through a personalized rendered preview or test email. If the connector cannot read the source fields and no rendered result is available, mark them unverified and name the required app check. Confirmed website or imprint facts may show what the account information should contain, but they do not populate those fields. Report missing items and ask for them. A separately approved sender change may proceed, but the signature remains not ready until those items are resolved.
3. Preserve existing content and markup unless replacement was requested. A full content write has no MCP undo; show material removals first.
4. Before a persistent write, show the complete proposed signature or every changed field and its wider effect in the same response. A confirmation without that visible proposal is invalid. Do not use option labels that refer only to unseen numbered items. Obtain confirmation only after the proposal is visible.
5. Read back the signature. Report usability, blockers, effective sender identity, tag assignment and content state. A stored placeholder is not proof that its resolved value is present; do not report the signature as ready while required source values remain unreadable or render empty.

This is a signature-readiness check. Do not present it as proof of legal compliance, CSA conformity, inbox placement or improved deliverability.

## Creation and content

Prefer a suitable existing signature. Copy one when its structure is a better starting point. Names must be unique. Required selection tags must already exist and must not be reassigned as a hidden side effect.

Do not call an inherited sender address usable until readback confirms the effective identity and verified domain. If the required address is missing or unconfirmed, return that blocker to `account-setup`; do not register one silently.

Normal marketing content needs the current contract's unsubscribe, identity and permitted postal-address placeholders. Plain text needs the same identity. Transactional content must follow its separate placeholder contract and must not contain the unsubscribe placeholder. `User:` placeholders resolve to the account owner's imprint data, the sender, not the recipient; label that block as sender or imprint, never as recipient. Do not invent placeholder spelling. Read back stored content before claiming that supplied HTML, plain text or transactional content was preserved.

Offer a transactional version when confirmation or other transactional emails need the same identity. A missing subscriber-information placeholder can produce a warning, but that warning alone does not prove that publication, testing or dispatch is blocked.

## Boundaries

Newsletter delivery selection belongs to `newsletter`. Email-body placement belongs to `email`. Missing tags belong to `tags`. Sending-domain setup belongs to `dns-setup`. Obtain separate approval for any handoff write, then resume this workflow.

There is no current signature-delete tool. Do not claim deletion or offer an undocumented workaround.

When returning to `account-setup`, report the verified signature state, remaining blocker, required customer action and recommended next setup step. Preserve its active assessment or guided mode.