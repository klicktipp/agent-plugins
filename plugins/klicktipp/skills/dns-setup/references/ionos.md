## Provider: IONOS (1&1)

First distinguish ordinary **IONOS Hosting DNS** from **IONOS Cloud DNS**. Their credentials, zones and tools are unrelated.

Hosting DNS: prefer an already-connected official IONOS Hosting DNS MCP. If none is connected, offer to connect it through the client's settings/plugins; the user enters the IONOS API key there. Obtain approval before setting up the connection; obtain separate approval for the exact DNS changes after inspecting existing records. Never read an IONOS API key from the user's environment, shell profile or files, and keep it out of chat. The Hosting DNS API expects full record names.

If the user cannot or does not want to connect it, guide them through **Domains & SSL -> domain actions -> DNS -> Add record**.

Cloud DNS: this plugin handles no IONOS Cloud login or token. Use an already-connected IONOS Cloud integration if the user has one; otherwise guide them through the IONOS Cloud DCD's DNS section.

Sources: [Hosting DNS API](https://developer.hosting.ionos.de/docs/dns), [Hosting DNS MCP](https://developer.hosting.ionos.de/mcp/documentation/dns)

