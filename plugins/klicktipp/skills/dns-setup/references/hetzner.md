## Provider: Hetzner

This plugin brings no Hetzner integration and handles no Hetzner login or API token. If the user already has a connected Hetzner DNS integration, use it for reading and, with approval, for changes. Otherwise guide them through the **Hetzner Console -> DNS -> select zone -> Records** page.

Hetzner expects record names relative to the zone. Replacing a record set replaces all of its values, so have the user inspect the existing values first; adding a value must not create duplicate SPF or DMARC policies.

Source: [Hetzner DNS](https://www.hetzner.com/dns/)
