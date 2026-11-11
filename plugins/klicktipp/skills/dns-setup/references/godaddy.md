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

