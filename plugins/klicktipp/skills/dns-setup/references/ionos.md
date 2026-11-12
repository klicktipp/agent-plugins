## Provider: IONOS (1&1)

First distinguish ordinary **IONOS Hosting DNS** from **IONOS Cloud DNS**. Their accounts, zones and tools are unrelated, so establish which one holds the zone before proposing a path.

Hosting DNS: prefer IONOS' own hosted MCP server for the Hosting DNS API where the client supports adding a remote MCP server — it authorizes against IONOS itself, so nothing has to be read from the user's machine or repeated in chat. Obtain approval for the connection, then separate approval for the exact records after inspecting what the zone already holds. The API expects full record names. Manual path: **Domains & SSL -> domain actions -> DNS -> Add record**.

Cloud DNS: authenticate interactively with `ionosctl config login`, inspect with `ionosctl dns zone list` and `ionosctl dns record list --zone example.com`, then consult `ionosctl dns record create --help` for an approved write. Never ask for an API key in chat and never read one from the user's environment or files; the CLI's own login keeps it where it belongs.

If `ionosctl` is missing, offer the official Cloud CLI installation instructions. On macOS/Linux with Homebrew the minimal commands are `brew tap ionos-cloud/homebrew-ionos-cloud` and `brew install ionosctl`. Ask before running either. For Hosting DNS, prefer its MCP server or the portal instead of installing the unrelated Cloud CLI.

Sources: [Hosting DNS API](https://developer.hosting.ionos.de/docs/dns), [Hosting DNS MCP](https://developer.hosting.ionos.de/mcp/documentation/dns), [IONOS Cloud DNS CLI](https://docs.ionos.com/cloud/tools-cli/subcommands/dns/record/create)
