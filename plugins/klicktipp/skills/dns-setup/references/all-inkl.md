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

