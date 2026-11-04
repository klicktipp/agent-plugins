---
name: dns-setup
description: Use for KlickTipp sending-domain setup, DNS verification, DKIM, DMARC, SPF, CNAME, TXT, MX, A records, and provider-specific DNS changes through the provider's connected DNS integration or guided portal steps.
---

# KlickTipp DNS setup

Help the user publish and verify the DNS records KlickTipp requires for a sending domain. Use the connected KlickTipp and DNS-provider tools when available; otherwise offer to connect the provider's official integration through the client's settings where one exists. Guide the user through the provider's website when direct access is unavailable or declined. KlickTipp's current record table, not the examples below, determines what to publish.

## Choose a route

1. Identify the sending domain and obtain its current DNS record table from `get-sender-domain-dns-setup`. If KlickTipp tools are unavailable, ask the user to copy the record table from KlickTipp; do not infer values from the examples in this skill. Never ask for credentials.
2. Identify who hosts the authoritative DNS zone. With shell access, inspect the domain's NS records (for example, `dig +short NS example.com`); otherwise use an available DNS lookup tool or ask the user where they manage DNS. Nameservers can differ from the registrar, and nameservers alone may not identify the account the user can edit. Confirm the editable zone before proceeding.
3. Check for an already-connected provider integration. Prefer it for inspecting existing records and, with approval, making changes. If none is connected and the provider offers an official integration the client can connect (the user signs in or enters keys there, never in chat), offer it; explain its source and access scope and obtain explicit approval before connecting it. Connecting an integration does not authorize DNS changes. This skill does not run provider CLIs or API clients and never reads provider credentials from the environment or local files.
4. If no provider integration is connected and the user needs the optional KlickTipp mailserver service for this domain, also offer the KlickTipp-assisted mailserver setup form as a choice alongside connecting a provider integration or managing DNS themselves. Use this route only when the service is available to the account and domain; `dkimOnly` alone does not establish eligibility. If availability is not exposed by a KlickTipp tool, ask the user to confirm it in their KlickTipp domain settings rather than assume it. Link to `https://www.klicktipp.com/mailserver-domain-einrichten?mailserver_domain=DOMAIN_NAME`, replacing `DOMAIN_NAME` with the selected domain from KlickTipp, URL-encoded. Prefer a domain-specific link returned by KlickTipp if one becomes available. Do not put hoster credentials in URL parameters; the user logs in and enters them directly in the form, and the agent does not collect or submit them. This requests assisted mailserver setup, not generic DNS setup, and does not replace the remaining DNS steps.
5. If direct access is unavailable or the user declines setup, guide them through the provider's DNS page using the exact host, type, value, TTL, and priority from KlickTipp. Have them inspect existing entries first and confirm the proposed changes before saving. Ask them to report back with non-secret record details or the verification result.

## Sources

KlickTipp documentation:

- [Create a sending address: Standard, Premium and Deluxe](https://www.klicktipp.com/de/support/wissensdatenbank/versandadresse-anlegen/)
- [Configure an Enterprise/Whitelabel domain and mail server](https://www.klicktipp.com/de/support/wissensdatenbank/whitelabel-versand-domains-und-logo-upload/)
- [Configure DMARC](https://www.klicktipp.com/de/support/wissensdatenbank/dmarc-fuer-bessere-e-mail-zustellung-einrichten/)
- [SPF guidance](https://www.klicktipp.com/de/support/wissensdatenbank/spf-definition-in-klicktipp/)

The articles explain the product workflow. The authoritative names and values for one domain come from its current KlickTipp DNS record table (via `get-sender-domain-dns-setup` when available), not examples from an article or this skill.

## Record sets

### Standard sender domain

Standard, Premium and Deluxe accounts normally create a `dkimOnly` domain. The MCP output should contain:

- Click-host `CNAME`, usually `www<number>.<domain>`.
- Two DKIM `CNAME` records at `ktdkim1._domainkey.<domain>` and `ktdkim2._domainkey.<domain>`.
- DMARC `TXT` at `_dmarc.<domain>`.

This is the three-CNAME-plus-DMARC setup described by the knowledge base. A separate SPF `TXT` is not normally needed unless the MCP output explicitly includes one.

### Enterprise/Whitelabel mail server

Full Whitelabel configuration can add these records when the domain's mail-server data contains them:

- Whitelabel alias `CNAME`.
- SPF `TXT` for the bounce/MX host.
- `MX` records for configured sending hosts.
- `A` records for configured sending hosts or bounce host.
- Informational landing-page `CNAME` records when linked landing pages exist.

The exact list is data-driven. Enterprise access only unlocks mail-server configuration; it does not prove that a domain already has the full record set. Trust `dkimOnly`, `optional`, `informational`, and the records returned by the tool.

## Interpret MCP output

- `expectedTypes` lists accepted record types. Use the first type for a new record unless an existing accepted alternative should be preserved.
- `expectedValues` lists accepted alternatives, not values that must all be created. For a new record, use the first value for the selected type. Preserve an existing value when the tool already reports it valid.
- `expectedTtl` is the requested TTL. A provider may enforce another supported TTL.
- `expectedPriority` applies to records such as `MX`.
- `optional: true` means absence does not block the domain in its current lifecycle state.
- `informational: true` means the record is checked and displayed but excluded from sending-domain validity.
- `status` and `actual*` describe the last persisted check. `get-sender-domain-dns-setup` does not perform live DNS resolution.
- `checkedAt` later than `lastDnsCheckRequestedAt` shows that the saved result is newer than the last requested check; it does not reveal whether a scheduler, manual action or another mechanism triggered it. Report the timestamp and mark the cause as unknown.
- A valid existing DMARC policy can differ from the suggested value. Never create a second DMARC policy merely to match the suggestion.

## Workflow

1. If KlickTipp tools are available, use `list-sender-domains` before adding anything. Use `create-sender-domain` only when the user asked to add a new KlickTipp sending domain. Obtain its exact record table from `get-sender-domain-dns-setup`; otherwise use the table the user provides from KlickTipp. Show type, host, chosen value, TTL, and priority to the user.
2. Inspect existing records at every requested host through the provider integration or DNS page before proposing changes. Check the full record set where a change could affect other values.
3. Explain the minimal create/update operations and get explicit approval for the exact DNS changes. If guiding in the portal, have the user confirm the values before they save them.
4. Apply only approved changes, or guide the user through them. Do not alter nameservers, web records, MX records, or mail routing unless KlickTipp's record table calls for them and the user approves.
5. Verify against public DNS when a lookup tool is available (for example, `dig +short <TYPE> <host>`). Otherwise ask the user to check in KlickTipp or a public DNS lookup page. Do not treat a saved provider entry as proof that it has propagated.
6. When KlickTipp tools are available, use `request-sender-domain-dns-check` after propagation is visible. The check is asynchronous and has a 60-second cooldown; during the cooldown the tool returns the stored request with `cooldownActive: true` instead of queueing another check. Poll `get-sender-domain` and `get-sender-domain-dns-setup` until the stored check result changes. Without these tools, guide the user through KlickTipp's verification page. Report propagation as pending rather than creating duplicates.

Safety rules:

- Never ask the user to paste an API token, password, or recovery code into chat. Provider access goes only through an integration the user connects in the client, with its own sign-in; this skill never reads, stores or passes on provider credentials. Do not put secrets in example commands, shell history, chat, or project files.
- Never install or configure a plugin or MCP server without explicit approval. State what will be installed, its source (and whether it is third-party), its access scope, and why it is needed.
- Existing read-only access needs no repeated approval. Creating, replacing, or deleting DNS records always requires approval of the proposed changes.
- Stop when a requested CNAME owner already has another record type; a CNAME cannot coexist with it.
- When `_dmarc` already exists, validate and preserve the existing policy if valid; do not add another policy.
- Never create two `v=spf1` policies at one owner. Modify the existing policy only with explicit approval and a clear merged value.
- Determine whether the provider expects relative names (`_dmarc`) or full names (`_dmarc.example.com`) before writing.
- Provider-hosted/proxied CNAME features must be disabled unless the provider and KlickTipp explicitly support them.

## Provider-specific guidance

When the provider is known and the task requires its DNS portal or integration details, read only its matching reference: [ALL-INKL](references/all-inkl.md), [IONOS (1&1)](references/ionos.md), [Cloudflare](references/cloudflare.md), [STRATO](references/strato.md), [GoDaddy](references/godaddy.md), [Hetzner](references/hetzner.md). For a read-only KlickTipp status check, do not load provider references.

## Other providers

Prefer an already-connected official integration, otherwise the guided portal workflow. Inspect first, show the exact proposed records, obtain approval, and apply the generic workflow above. Do not attempt undocumented endpoints or portal automation; fall back to manual guidance.
