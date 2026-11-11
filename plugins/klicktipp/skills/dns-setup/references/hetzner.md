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

