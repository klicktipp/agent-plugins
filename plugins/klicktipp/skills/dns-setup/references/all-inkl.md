## Provider: ALL-INKL

In KAS, record names are relative to the zone (for example, `_dmarc` rather than `_dmarc.example.com`); the API's `zone_host` is the full domain with a trailing dot. ALL-INKL's CNAME guide requires a trailing dot on the target hostname. Check the actual field conventions before writing.

Sources:
- [KAS DNS API](https://kasapi.kasserver.com/dokumentation/phpdoc/packages/API%20Funktionen.dns.html)
- [CNAME guide](https://all-inkl.com/wichtig/anleitungen/kas/tools/dns-werkzeuge/cname_178.html)
- [TXT guide](https://all-inkl.com/wichtig/anleitungen/kas/tools/dns-werkzeuge/txt-record_157.html)

### Direct access

This plugin brings no ALL-INKL integration and handles no KAS login. If the user already has a
connected ALL-INKL integration, use it for reading and, with approval, for changes. Otherwise guide
them through the website.

### Manual website guidance

If no direct integration is available or the user prefers the website, have them log in at https://kas.all-inkl.com/login themselves.

- Open **Tools > DNS-Settings** and select the zone to edit. **Domain** in the main menu lists domains; it is not the DNS editor.
- Review entries at each requested host before adding anything. Use the pencil icon to edit an existing entry, or **Add a new DNS record** for a missing one.
- Enter **Name** relative to the zone: for example, `_dmarc` for `_dmarc.example.com`. Select the **Type** and fill **Data/Value** from KlickTipp's table. Enter **Prio** separately for records that require it (such as MX); for a CNAME, use the target hostname with a trailing dot as instructed by ALL-INKL. Use KlickTipp's TTL if the portal offers that setting.
- Have the user review the full proposed entry before saving it. Then verify the result using the workflow above.

Tutorials at: https://all-inkl.com/en/support/tutorials/kas#kas_domain (DNS Tools section)

