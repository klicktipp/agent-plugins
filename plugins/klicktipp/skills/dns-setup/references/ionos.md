## Provider: IONOS (1&1)

First distinguish ordinary **IONOS Hosting DNS** from **IONOS Cloud DNS**. Their credentials, zones and tools are unrelated.

Hosting DNS: prefer an already-connected official IONOS Hosting DNS MCP. If none is connected, offer to connect it through the client's settings/plugins; the user enters the IONOS API key there. Obtain approval before setting up the connection; obtain separate approval for the exact DNS changes after inspecting existing records. Never read an IONOS API key from the user's environment, shell profile or files, and keep it out of chat. The Hosting DNS API expects full record names.

If the user cannot or does not want to connect it, guide them through **Domains & SSL -> domain actions -> DNS -> Add record**.

Cloud DNS: authenticate with `ionosctl config login`, inspect with `ionosctl dns zone list` and `ionosctl dns record list --zone example.com`, then consult `ionosctl dns record create --help` for an approved write.

If `ionosctl` is missing, offer the official Cloud CLI installation instructions. On macOS/Linux with Homebrew the minimal commands are `brew tap ionos-cloud/homebrew-ionos-cloud` and `brew install ionosctl`. Ask before running either. For Hosting DNS, prefer its API/MCP or portal instead of installing the unrelated Cloud CLI.

Sources: [Hosting DNS API](https://developer.hosting.ionos.de/docs/dns), [Hosting DNS MCP](https://developer.hosting.ionos.de/mcp/documentation/dns), [IONOS Cloud DNS CLI](https://docs.ionos.com/cloud/tools-cli/subcommands/dns/record/create)

