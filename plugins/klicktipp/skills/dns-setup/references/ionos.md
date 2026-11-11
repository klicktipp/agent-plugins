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

