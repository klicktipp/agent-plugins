---
name: dns-setup
description: Use for KlickTipp sending-domain setup, DNS verification, DKIM, DMARC, SPF, CNAME, TXT, MX, A records, and provider-specific DNS changes through the provider's DNS connectors, APIs, CLIs, or guided portal steps.
---

# KlickTipp DNS setup

Help the user publish and verify the DNS records KlickTipp requires for a sending domain. Use the connected KlickTipp and DNS-provider tools when available; otherwise offer to set up a suitable provider integration or CLI if the environment permits it. Guide the user through the provider's website when direct access is unavailable or declined. KlickTipp's current record table, not the examples below, determines what to publish.

## Choose a route

1. Identify the sending domain and obtain its current DNS record table from `get-sender-domain-dns-setup`. If KlickTipp tools are unavailable, ask the user to copy the record table from KlickTipp; do not infer values from the examples in this skill. Never ask for credentials.
2. Identify who hosts the authoritative DNS zone. With shell access, inspect the domain's NS records (for example, `dig +short NS example.com`); otherwise use an available DNS lookup tool or ask the user where they manage DNS. Nameservers can differ from the registrar, and nameservers alone may not identify the account the user can edit. Confirm the editable zone before proceeding.
3. Check for an already-connected provider integration or CLI. Prefer it for inspecting existing records and, with approval, making changes. If none is available and installation/configuration is possible, offer a suitable provider MCP server, official CLI, or API client; explain its source, access scope, credential handling, and what will be installed. Obtain explicit approval before installing or configuring it. Installing a tool does not authorize DNS changes.
4. If no provider integration is connected and the user needs the optional KlickTipp mailserver service for this domain, also offer the KlickTipp-assisted mailserver setup form as a choice alongside setting up a provider tool or managing DNS themselves. Use this route only when the service is available to the account and domain; `dkimOnly` alone does not establish eligibility. If availability is not exposed by a KlickTipp tool, ask the user to confirm it in their KlickTipp domain settings rather than assume it. Link to `https://www.klicktipp.com/de/mailserver-domain-einrichten?domain=DOMAIN_NAME`, replacing `DOMAIN_NAME` with the selected domain from KlickTipp, URL-encoded. Prefer a domain-specific link returned by KlickTipp if one becomes available. The user logs in and enters any hoster credentials directly in the form; the agent does not collect or submit them. This requests assisted mailserver setup, not generic DNS setup, and does not replace the remaining DNS steps.
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
- A valid existing DMARC policy can differ from the suggested value. Never create a second DMARC policy merely to match the suggestion.

## Workflow

1. If KlickTipp tools are available, use `list-sender-domains` before adding anything. Use `create-sender-domain` only when the user asked to add a new KlickTipp sending domain. Obtain its exact record table from `get-sender-domain-dns-setup`; otherwise use the table the user provides from KlickTipp. Show type, host, chosen value, TTL, and priority to the user.
2. Inspect existing records at every requested host through the provider integration or DNS page before proposing changes. Check the full record set where a change could affect other values.
3. Explain the minimal create/update operations and get explicit approval for the exact DNS changes. If guiding in the portal, have the user confirm the values before they save them.
4. Apply only approved changes, or guide the user through them. Do not alter nameservers, web records, MX records, or mail routing unless KlickTipp's record table calls for them and the user approves.
5. Verify against public DNS when a lookup tool is available (for example, `dig +short <TYPE> <host>`). Otherwise ask the user to check in KlickTipp or a public DNS lookup page. Do not treat a saved provider entry as proof that it has propagated.
6. When KlickTipp tools are available, use `request-sender-domain-dns-check` after propagation is visible. The check is asynchronous and has a 60-second cooldown; during the cooldown the tool returns the stored request with `cooldownActive: true` instead of queueing another check. Poll `get-sender-domain` and `get-sender-domain-dns-setup` until the stored check result changes. Without these tools, guide the user through KlickTipp's verification page. Report propagation as pending rather than creating duplicates.

Safety rules:

- Never ask the user to paste an API token, password, or recovery code into chat. Prefer interactive login; if a tool requires credentials in environment variables or local configuration, have the user set them privately and explain where they will be stored. Do not put secrets in example commands, shell history, chat, or project files.
- Never install or configure a CLI, package manager, plugin, MCP server, or credential helper without explicit approval. State what will be installed, its source (and whether it is third-party), its access scope, and why it is needed.
- Existing read-only access needs no repeated approval. Creating, replacing, or deleting DNS records always requires approval of the proposed changes.
- Stop when a requested CNAME owner already has another record type; a CNAME cannot coexist with it.
- When `_dmarc` already exists, validate and preserve the existing policy if valid; do not add another policy.
- Never create two `v=spf1` policies at one owner. Modify the existing policy only with explicit approval and a clear merged value.
- Determine whether the provider expects relative names (`_dmarc`) or full names (`_dmarc.example.com`) before writing.
- Provider-hosted/proxied CNAME features must be disabled unless the provider and KlickTipp explicitly support them.

## Provider: ALL-INKL

In KAS, record names are relative to the zone (for example, `_dmarc` rather than `_dmarc.example.com`); the API's `zone_host` is the full domain with a trailing dot. ALL-INKL's CNAME guide requires a trailing dot on the target hostname. Check the actual field conventions before writing.
KAS API credentials can control services beyond DNS, so use a restricted account when available.

Sources:
- [KAS DNS API](https://kasapi.kasserver.com/dokumentation/phpdoc/packages/API%20Funktionen.dns.html)
- [CNAME guide](https://all-inkl.com/wichtig/anleitungen/kas/tools/dns-werkzeuge/cname_178.html)
- [TXT guide](https://all-inkl.com/wichtig/anleitungen/kas/tools/dns-werkzeuge/txt-record_157.html)

### Local MCP (npx)

Third-party MCP server: https://github.com/hl9020/mcp-all-inkl. It exposes DNS **and** other KAS administration actions; review its permissions and source with the user before offering it. It requires Node.js 22+, KAS API access, and local KAS credentials. `npx -y mcp-all-inkl` downloads and runs the package if it is not already cached; obtain installation approval first.

For Claude Code or Codex, follow the server's linked setup instructions for the host in use. Have the user provide `KAS_LOGIN` and `KAS_PASSWORD` privately through their local configuration; do not ask them to type secrets into a command you execute or paste a credential-bearing configuration into chat. Check how the host stores MCP credentials before configuring it.

### SOAP/PHP API

ALL-INKL supports DNS writes through its KAS SOAP API when the customer's plan permits it.

SOAP API:
- Auth WSDL: https://kasapi.kasserver.com/soap/wsdl/KasAuth.wsdl
- API WSDL: https://kasapi.kasserver.com/soap/wsdl/KasApi.wsdl
- Functions: https://kasapi.kasserver.com/dokumentation/phpdoc/

### Python/Go libraries

Python: fetzerch/kasserver
Go: https://go-acme.github.io/lego/dns/allinkl/

### Manual website guidance

If no direct integration is available or the user prefers the website, have them log in at https://kas.all-inkl.com/login themselves.

- Open **Tools > DNS-Settings** and select the zone to edit. **Domain** in the main menu lists domains; it is not the DNS editor.
- Review entries at each requested host before adding anything. Use the pencil icon to edit an existing entry, or **Add a new DNS record** for a missing one.
- Enter **Name** relative to the zone: for example, `_dmarc` for `_dmarc.example.com`. Select the **Type** and fill **Data/Value** from KlickTipp's table. Enter **Prio** separately for records that require it (such as MX); for a CNAME, use the target hostname with a trailing dot as instructed by ALL-INKL. Use KlickTipp's TTL if the portal offers that setting.
- Have the user review the full proposed entry before saving it. Then verify the result using the workflow above.

Tutorials at: https://all-inkl.com/en/support/tutorials/kas#kas_domain (DNS Tools section)

## Provider: IONOS (1&1)

First distinguish ordinary **IONOS Hosting DNS** from **IONOS Cloud DNS**. Their credentials, zones and tools are unrelated.

Hosting DNS:

```bash
curl -sS https://api.hosting.ionos.com/dns/v1/zones -H "X-API-Key: $IONOS_API_KEY"
curl -sS "https://api.hosting.ionos.com/dns/v1/zones/$ZONE_ID" -H "X-API-Key: $IONOS_API_KEY"
```

Use the official Hosting DNS API or hosted MCP for approved CRUD. The API expects full record names. Manual path: **Domains & SSL -> domain actions -> DNS -> Add record**.

Cloud DNS: authenticate with `ionosctl config login`, inspect with `ionosctl dns zone list` and `ionosctl dns record list --zone example.com`, then consult `ionosctl dns record create --help` for an approved write.

If `ionosctl` is missing, offer the official Cloud CLI installation instructions. On macOS/Linux with Homebrew the minimal commands are `brew tap ionos-cloud/homebrew-ionos-cloud` and `brew install ionosctl`. Ask before running either. For Hosting DNS, prefer its API/MCP or portal instead of installing the unrelated Cloud CLI.

Sources: [Hosting DNS API](https://developer.hosting.ionos.de/docs/dns), [Hosting DNS MCP](https://developer.hosting.ionos.de/mcp/documentation/dns), [IONOS Cloud DNS CLI](https://docs.ionos.com/cloud/tools-cli/subcommands/dns/record/create)

## Provider: Cloudflare

Prefer an already-connected official Cloudflare integration. If none is connected, offer to connect Cloudflare through the client's settings/plugins and have the user authorize access to the intended zone. Obtain approval before setting up the connection; obtain separate approval for the exact DNS changes after inspecting existing records.

Where the client supports adding a remote MCP server instead, Cloudflare's official API MCP server is at `https://mcp.cloudflare.com/mcp`. It uses Cloudflare OAuth and supports DNS record management. Use the API MCP server for record changes; the separate DNS Analytics server is for analysis, not DNS record management.

Set KlickTipp CNAME records to DNS-only (`proxied: false`). Follow the record inspection, approval, and verification workflow above. If the user cannot or does not want to connect Cloudflare, guide them through **Cloudflare dashboard > select zone > DNS > Records**.

Source: [Cloudflare's own MCP servers](https://developers.cloudflare.com/agents/model-context-protocol/cloudflare/servers-for-cloudflare/)

## Provider: STRATO

STRATO has no supported general DNS CRUD API or CLI. Guide the user through **Domains -> Domain management -> gear -> DNS**.

- TXT: open TXT management and enter a relative prefix such as `_dmarc`.
- CNAME: create/select the required subdomain, then open its CNAME management.

STRATO appends the zone automatically. Its DynDNS endpoint cannot create KlickTipp TXT or CNAME records. Do not use tools that scrape the portal with account credentials.

Source: [STRATO DNS records](https://www.strato.de/faq/domains/wie-kann-ich-bei-strato-meine-dns-eintraege-verwalten/)

## Provider: GoDaddy

The plugin has no GoDaddy server. The official `gddy` CLI supports browser login and DNS CRUD, though GoDaddy labels it beta.

```bash
gddy auth login
gddy dns list example.com
gddy dns add --help
```

If `gddy` is missing, offer GoDaddy's official installer for the current operating system and ask before running it. Disclose that the macOS/Linux installer downloads and executes GoDaddy's installation script; provide the linked setup page so the user can choose manual installation instead.

Use `--dry-run` where offered before approved changes. `set` and `delete` can affect every record matching a name/type pair, so inspect the complete RRSet first. The domain must use GoDaddy authoritative DNS.

Sources: [`gddy` setup](https://developer.godaddy.com/en/docs/api-users/cli/set-up), [DNS workflow](https://developer.godaddy.com/en/docs/api-users/domains/manage/dns)

## Provider: Hetzner

Hetzner DNS is managed through the official `hcloud` CLI/API. Authenticate interactively and keep credentials out of chat.

```bash
command -v hcloud
hcloud context create klicktipp-dns
hcloud zone list
hcloud zone rrset list example.com
hcloud zone rrset create --help
```

If `hcloud` is missing, offer the matching official package and wait for approval:

- macOS/Linux with Homebrew: `brew install hcloud`
- Windows: `winget install --id HetznerCloud.CLI --exact`

If the user declines, use the Hetzner Console or official API instead.

`hcloud` expects names relative to the zone. Inspect an RRSet with `hcloud zone rrset describe <zone> <name> <type>`. `set-records` replaces the complete RRSet; use it only after displaying the existing values and receiving approval. `add-records` preserves existing values but must not create duplicate SPF or DMARC policies.

Sources: [Hetzner DNS](https://www.hetzner.com/dns/), [`hcloud zone` reference](https://github.com/hetznercloud/cli/blob/main/docs/reference/manual/hcloud_zone.md)

## Other providers

Prefer an official scoped API, CLI, Terraform provider, or guided portal workflow. Inspect first, show the exact proposed records, obtain approval, and apply the generic workflow above. Do not attempt undocumented endpoints or portal automation; fall back to manual guidance.
