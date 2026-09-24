# Changelog

One entry per released version. Both manifests — `.claude-plugin/plugin.json` and
`.codex-plugin/plugin.json` — carry the same version, and every version is a tag in this
repository.

The plugin is generated from the internal `agent-plugin` repository, and the version numbers are
that repository's tags: only its production build is published here, so a version that changed
nothing in the production plugin leaves no entry of its own.

## 0.16.1 — 2026-09-24

Datumsangaben aus den Skills entfernt. Eine Referenz, die „Stand 2026-09-24" trägt oder erklärt,
seit wann ein Baustein fehlt und wie viele Werkzeuge es „vorher" waren, erzählt dem Agenten
Geschichte statt Gegenwart — und altert bei jeder Server-Änderung, auch wenn die Aussage darunter
noch stimmt. Betroffen sind neun Dateien in allen fünf Skills; der Inhalt bleibt, nur der Zeitbezug
fällt weg.

## 0.16.0 — 2026-09-24

Die Werkzeugnamen des Servers sind umbenannt worden, und die Skills ziehen nach. Der Name beginnt
jetzt mit dem Verb und nennt die Sache so, wie der Katalog sie führt:

- `email-get` → `get-email-editor-content`
- `email-content-import` → `replace-email-editor-content-from-html`
- `email-block-style-write` → `update-email-editor-block-style`
- `email-newsletter-get` → `get-newsletter`
- `email-content-publish` → `publish-newsletter-email-content`
- `email-newsletter-send` → `prepare-newsletter-dispatch`

Der letzte ist mehr als eine Umbenennung: der Aufruf bereitet den Versand vor, die Bestätigung ist
ein zweiter Schritt, und der alte Name behauptete das Gegenteil.

Jeder Name in dieser Fassung wurde gegen den Server geprüft, nicht aus der Umbenennung übernommen.
Alte Namen funktionieren nicht weiter — eine Sitzung mit einem Skill dieser Fassung gegen einen
älteren Server findet die Werkzeuge nicht, und umgekehrt.

## 0.15.0 — 2026-09-24

Die Skills beschreiben ab hier genau die Werkzeuge, die Produktion veröffentlicht — nicht die, die
auf dem Server existieren.

- **Die Signaturen sind raus.** Sechs Verträge von `email-signature-search` bis
  `email-signature-delivery-configure` standen in den Newsletter-Verträgen, aber `SignatureTool`
  steht auf keiner Freigabeliste. Wer dem Skill folgte, rief ein Werkzeug auf, das seine Sitzung
  nicht kennt.

- **Opt-in-Prozesse anlegen und ändern ebenfalls**, zusammen mit der ganzen Familie um die
  Bestätigungsmail — lesen, schreiben, Inhalt, Testversand, Vorschau. Lesen und Löschen eines
  Prozesses bleiben dokumentiert, denn die sind freigegeben; Anlegen und Ändern sitzen in eigenen
  Klassen, die es nicht sind.

- **Der Designkatalog kam dafür dazu.** `email-template-search` liefert den Katalog, den auch der
  Vorlagen-Browser des Editors zeigt, `email-template-apply` legt eines davon in den Körper — für
  jede E-Mail, die der Editor öffnet, nicht nur für Newsletter. Mit dem Stolperer, an dem sonst
  jeder hängenbleibt: die `templateId` ist ein Wort wie `monthly-marketing-dispatch`, keine Zahl.
  Die Nummer in der Miniaturbild-URL gehört dem Bildarchiv.

- **Die eigene Referenzdatei des KI-Textes ist weg.** Der Baustein hat seit 0.14.1 kein Werkzeug
  mehr und gehört damit zu denen, die im Editor entstehen und über die Werkzeuge nur lesbar,
  verschiebbar und entfernbar sind — dieselbe Gruppe wie Countdown, Kontaktkarte und Wowing-Video,
  und dort steht er jetzt auch.

## 0.14.1 — 2026-09-22

Five places where a skill told the agent something the server does not say. Each was measured
against the server rather than taken from the review that reported it, and each made an agent act
wrongly.

- **A fresh draft is not audience-less.** It was described as inert and unable to reach anybody. It
  has no audience *filter*, and unfiltered means `all_contacts` — every active contact of the
  account, the widest audience there is rather than the narrowest. An agent reading the old wording
  skipped the audience decision because the state looked harmless. The same paragraph called
  `subject` optional; the tool requires it.

- **A missing unsubscribe link is a blocker, not a matter of taste.** It sat beside pale text as a
  finding the user might want. The check calls it an error, `publish-newsletter-email-content` refuses without
  the placeholder, and nothing is dispatched without publishing.

- **`email-ai-text-add` is gone**, so it is no longer documented as a tool. The block itself
  remains, so the AI text now sits with the countdown, the contact card and the Wowing video: made
  in the editor, readable, movable and removable through the tools.

- **The font can be set.** `update-email-editor-page-style` takes `fontFamily`, while the styling guide
  listed the font among the things that cannot be set — so an agent refused work it could do.

- **A tool count in prose** said 51 where the contract said 54. Removed rather than corrected: a
  number kept by hand in a second place is a promise to be wrong again.

## 0.14.0 — 2026-09-22

The production release caught up with what production actually serves. Several notes in this
plugin still said "arrives with the next deployment" for tools that had long since arrived, and
that is the larger half of this entry.

- **Dynamic content.** Four tools write and read what the editor calls display conditions:
  `get-email-editor-display-condition-capabilities` for the vocabulary of one account,
  `update-email-editor-display-condition` for a named condition, `configure-email-editor-row-display-condition` to bind a row to it,
  and `list-email-editor-display-conditions` to see which rows a condition governs. The binding sits as a marker
  inside the row and shows up in no other projection, so the last one is the only way to find out
  that a row is conditional at all. The full catalogue of condition kinds is a new reference,
  [display-conditions.md](plugins/klicktipp/skills/email/references/display-conditions.md).

- **`preview-email-editor`** renders the current draft, unpublished changes included, and shows it. The
  `email` skill now says plainly that "show me the preview" is this tool and not `get-email-editor-content` —
  describing an email in words is an answer to a question nobody asked.

- **`upsert-subscribed-contact`** adds a contact by hand, subscribed at once and with its field values, the
  way the Add Contact screen does. An address the account already has is updated rather than added
  twice, and `alreadyExisted` says which of the two happened.

- **Set the page style before the first block.** The text and link colour of a block are written
  into it when it is made, not inherited at send time. A block added to an email that has no other
  block of its kind used to keep the colours of whatever newsletter its start state came from, and
  a page colour set afterwards never reached it. The order is now part of the authoring guidance.

- **The personalized email block lost its two tools.** They are gone rather than held back: the
  add-on behind it is paid for separately and the work on it is deferred. The editor offers the
  block only inside an automation, so a newsletter cannot get one at all — this is the one add-on
  where pointing at the editor is not an answer.

- **Availability, corrected throughout.** The image tools, the split tests, the contact, tag and
  field tools, `cancel-newsletter-dispatch` and the subscription tools are on production and are no
  longer described as pending. What genuinely is not there: the `email-signature-*` family,
  everything that writes an opt-in process or its confirmation email, and the two deletions.

- **Contracts follow the server word for word**, as always: `search-email-editor-templates` takes category
  and collection as free text now — the enum could refuse a value the same tool had answered with
  — and `update-email-editor-page-style` writes a default link colour instead of a separate content
  background.

## 0.11.6 — 2026-09-23

- **The Codex marketplace was rejected on one word.** `policy.authentication` said `ON_FIRST_USE`;
  Codex accepts `ON_USE` or `ON_INSTALL`, and refused to add the marketplace at all. The OAuth
  sign-in happens at the first tool call, so `ON_USE` is the value that was meant.

## 0.11.5 — 2026-09-21

- **Langdock is documented.** [SETUP_LANGDOCK.md](plugins/klicktipp/SETUP_LANGDOCK.md) walks a
  workspace through connecting to the same MCP server as a remote integration. The one thing that
  trips people up is named first: dynamic client registration is closed on the KlickTipp side, so
  the manual Authorization Code + PKCE option is the route, and the empty client secret is correct
  rather than a missing value.

## 0.11.4 — 2026-09-18

- **The last two vendor mentions are gone**, at the source. `replace-email-editor-content-from-document` and
  `preview-email-editor` name the editor document as what it is — JSON — rather than by brand, and the
  contract reference follows the server word for word as it always does.

## 0.11.3 — 2026-09-18

- **The editor is named by what it is.** The bundled schema folder is `references/simple-schema/`,
  and the prose around it says editor rather than vendor. Its README keeps the source URL and the
  Apache-2.0 copyright line, which is the condition for shipping those files at all. The module
  types inside a stored document are literal values and unchanged.

## 0.11.2 — 2026-09-18

- **The skill descriptions are terse.** 2761 characters down to 1748 across the six — and they were
  4743 two versions ago. Each now leads with the job in one clause, names the words a user would
  actually say, and hands off to its neighbouring skill. This is the text that decides which skill
  is consulted, and all of it sits in context before any of them is.

## 0.11.1 — 2026-09-18

- **The skills follow Anthropic's authoring checklist now.** Every reference longer than 100 lines
  carries a table of contents, so a partial read still shows what else is in the file. The
  `prerequisites` key is gone — the format defines `name` and `description`, and `prerequisites:
  None` said nothing six times over. And the contract references stopped describing a generator that
  no longer exists.

## 0.11.0 — 2026-09-18

- **Codex finds the marketplace where it looks for it.** `.agents/plugins/marketplace.json` is the
  location Codex documents; the Claude file it accepts only as a fallback, and that fallback cannot
  carry a policy. This one says the OAuth sign-in happens at the first tool call rather than on
  install.
- **The skill descriptions are half as long** — 4743 characters down to 2761 across the six. Every
  one of them is loaded before a single skill is chosen. Nothing that routes a request was dropped;
  what went is a trigger phrased twice and enumerations repeating their own first clause. Four of
  them also stopped writing `aendern` and `Oeffnungen`.
- **A description can no longer break its own frontmatter.** Two of the six contained `": "`, which
  in an unquoted YAML scalar is a mapping and not a string.
- **Seven tools are newly documented in the contract references** — `create-opt-in-process`, the
  four opt-in confirmation-email tools, `search-email-editor-templates` and `cancel-newsletter-dispatch`. The
  references mirror what the MCP server publishes; of these only `cancel-newsletter-dispatch` is marked
  as not being on production yet.
- The GitHub Pages site is gone. The documentation is at
  [developers.klicktipp.com](https://developers.klicktipp.com/guides/mcp-server-plugins), split into
  a guide for the server and one for the plugins.

## 0.10.4 — 2026-09-18

- **The documentation moved to developers.klicktipp.com and is now two guides** — one for the MCP
  server itself, one for the plugins. Both READMEs and the `homepage` of both manifests point there.
  The tool and skill listing stays in the README, because it changes with every release while the
  guides do not, and the guides link back here for it.

## 0.10.3 — 2026-09-18

- **An orphaned README no longer ships with the `email` skill.** It was linked from nowhere, predated
  the rebuild of the skill, and still opened by describing the skill as an HTML generator — the one
  framing 0.10.0 removed. A reader who found it in the plugin would have believed it.
- **The schema catalogue stops sending a reader upstream for files that are already there.** It
  claimed only `definitions.schema.json` was mirrored; all fifteen are, and it now names the three
  that genuinely are not.

## 0.10.2 — 2026-09-18

- **The editor is named by what it is, not by its vendor.** Six places in the `email` skill called
  the stored document a "Bee-Dokument" or its CDN "Bees Ressourcen-Host"; they now read
  Editor-Dokument and "Ressourcen-Host des Editors" — the term someone reading the KlickTipp UI
  would recognise. The module types in a stored document (`mailup-bee-newsletter-modules-*`) are
  literal values and unchanged, and the vendored simple-schema files keep their upstream origin,
  which their Apache-2.0 licence requires.

## 0.10.1 — 2026-09-18

- **Two things that made the plugin directory reject the submission.** The `email` skill's
  `description` was 1198 characters against a limit of 1024 — it now keeps every trigger that is not
  covered elsewhere and drops the two that were. And the release archive held the plugin directory
  as a folder, so `.claude-plugin/plugin.json` sat one level down; it now holds the contents of that
  directory, with the manifest at the top level.

## 0.10.0 — 2026-09-18

- **Three ways into a newsletter body, and the skill says which one you are in.** The `email` skill
  described the HTML conversion as the only route, which is what sent a run through it and cost the
  dividers, the box and some images. The form the design is already in decides now: another email of
  the account is `replace-email-editor-content-from-email`, a finished editor document is `replace-email-editor-content-from-document`,
  and only markup that exists nowhere else is worth a conversion. Both new routes replace the body in
  one call and convert nothing.
- **A body is not assembled from single block calls when it is new.** The skill said both things in
  two places for the same case; the slow reading took over ten minutes. Authoring now writes the
  document and stores it in one call, and the cost of the other road is named with the measured
  number rather than left as a preference.
- **The email skill loads a third of what it did** — 50k characters down to 31k. What only applies in
  one situation moved into `references/`: styling, adding blocks, the HTML case and authoring from
  nothing. Each site keeps a pointer that names the decision, so the choice of whether to go look
  stays in the skill.
- **A split test asks for its three settings** instead of filling them in as "defaults". Test size,
  duration and winner criterion settle what share of real recipients gets a test version — the one
  thing in that flow that is not a design decision. They are asked in one question, and an own choice
  is named as one.
- **A variant already carries its content revision**, so reading one just to learn its token is a
  round trip that can go.
- **Rules the tool descriptions had to give up now live in the skills** — among them: ask before
  removing a block, and ask for the subject rather than inventing it.

## 0.9.0 — 2026-09-17

- **Thirteen contact, tag and field tools go to production** — the four tag tools, the five
  contact tools, the four custom-field tools — arriving with the next production deployment.
- **And a list of what deliberately stays behind, each with its reason** rather than as one
  bucket: the two deletions, because deleting a field takes the value out of every contact of the
  account; `subscribe-contact-via-opt-in-process`, `unsubscribe-contact` and `get-opt-in-process-redirect-url`, because a subscription
  sends the confirmation mail, can start automations and changes who really gets post; and
  everything writing an opt-in process or its confirmation email, because that is the record of
  consent.
- `enrich-contact` is now **`update-contact-values`** — it never enriched, it wrote contact fields, and it
  now reads like `update-manual-tag` and `update-custom-field`.
- **A dispatch can be taken back.** `cancel-newsletter-dispatch` exists, so `canBeCancelled` no longer
  names a state with no way out of it. It does not unsend what already left, it takes the same
  permission as handing a newsletter over, it is not on production yet — and the skill says to ask
  the person before calling it.
- **A missing unsubscribe link is a blocker, not a warning.** The publish refuses without the
  token, and nothing is sent unpublished, so the old wording sent an agent to tell people the
  dispatch would decide it. The skill names which footer placeholder blocks and which does not.

## 0.8.19 — 2026-09-17

- **The split-test tools are released.** They are in the production allowlist, so what was "not on
  production, release pending" is now "released, and there from the next production deployment on"
  — an "unknown tool" until then is the state of the deployment, not a defect. The skill also says
  what the release does *not* change: delivery configuration, test send and activation refuse a
  split test everywhere, because none of them can pick an arm.
- It also records the dead end in between, because someone will still meet it: the `splitTest`
  argument was published while the five tools were not, and a test created that way cannot be
  given its second arm from here at all — that newsletter is finished in the app.
- `email`: block alignment, and the editor's own font names rather than approximations of them.

## 0.8.16 — 2026-09-16

- **No tool adds a block only the editor can fill.** Countdown, contact card and Wowing video had
  add tools that could set an empty shell and nothing else — their content is chosen in a dialog
  of the KlickTipp editor, so what came out looked placed and rendered nothing at send time. Those
  three add tools are gone; the skills name the editor as the answer, and existing blocks of those
  kinds stay readable, movable and removable.
- **A tool called without an account works in the account the app would open** — the user's own
  where they have KlickTipp access, the one linked account where they have none, and a choice
  where there are several. The skills describe that, and the refusals a texter or a disconnected
  account gets, so the agent asks the person instead of guessing.
- **The six output schemas are published again.** A client that wants to validate an answer needs
  a machine-readable schema; deriving the shape from Markdown is not that. The references say so
  rather than claiming there is none, and stay the fuller source — a schema names fields, it does
  not explain them.
- `newsletter`: the tracking settings the screen has and the tools did not — the UTM campaign name
  through draft-update, link tracking and the KlickTipp header line through delivery-configure.
- `email`: the HTML import answer says what the conversion cost, and since the conversion is Bee's,
  only the report after it is binding.

## 0.8.14 — 2026-09-16

- **The test send takes any address now — and writes one.** It runs through the app's own test
  dialog, so the restriction to the account's own addresses is gone and the side effect is real:
  the recipient becomes a tagged contact, which can start an automation. The skill says so before
  the step rather than after it, and the published tool table follows.
- **Publish before testing.** A test send shows the published body, so an unpublished change is
  not what arrives; the skill reads the warning that says so instead of passing it over.
- `newsletter`: the sender lists are binding and the domain comes with them; and three things the
  server allows without prompting — excluding long-inactive contacts when an audience is set (with
  the limit said out loud, because tag conditions have no time axis), the imprint, and the
  transactional signature.
- `crm`: contact date fields are read the way the interface writes them — `16.09.2026`, not a
  second notation beside it. ISO 8601 still goes in on the write side, for a date that was
  computed rather than read.

## 0.8.12 — 2026-09-16

- Three add-on blocks are held back on production: **countdown**, **contact card** and
  **personalized email**. The first two add a block only the editor can finish; the personalized
  email has no fallback at all, because the editor does not offer it in its insert menu either, so
  on production it cannot be placed. The `email` skill says so where an agent actually stands when
  it reaches for one — in the tool table, in the list of add tools and in each block's own file.

## 0.8.11 — 2026-09-16

- **Corrected what production actually offers.** 0.8.3 and 0.8.10 listed the split-test tools and
  the contact, tag and field tools as if they were available; they are not released on production
  yet, and neither are the image tools nor the `email-signature-*` family. The tool table marks
  each of them, and the plugin description is back to what production does: newsletters, and
  reading the opt-in processes.
- `crm`: on production the opt-in processes are read, not written — `update-opt-in-process` and
  `delete-opt-in-process` are missing there too, so the skill points at the web interface for
  changing and deleting one instead of enumerating which writer is out this week.

## 0.8.10 — 2026-09-16

- **Every skill carries its own tool reference.** A `references/` folder per skill holds the tools
  that skill uses, the answer shapes they publish and the pitfalls they have — generated from the
  tool list rather than remembered. Tools not released on production are marked as such instead of
  by environment. (0.8.4 – 0.8.6)
- **New skill `crm`** — the contact data of the account: find, read, subscribe and unsubscribe
  contacts, set field values, manage manual tags and custom field definitions, and read the opt-in
  processes behind them. The published tool table and the plugin description follow. (0.8.6)
- Opt-in: changing and deleting a process is described, along with the redirect parameters, the
  confirmation email and the tracking pixel. (0.8.9, 0.8.10)
- `email`: the image folders and the two upload tools (the file with its form, the URL on its
  own), the page font versus the row frame, and the content check now reporting unconfigured
  add-ons. (0.8.7 – 0.8.10)
- `splittest`: the read tool, which also takes an arm's email ID, plus what a test run turned up.
  (0.8.8)
- Signatures are documented as the `email-signature-*` family with their placeholder rules, but
  they are **not released on production** — an "unknown tool" there is the pending release, not a
  defect. (0.8.5)

## 0.8.3 — 2026-09-14

- **Split tests.** `configure-newsletter-split-test` makes a newsletter a split test and says how the
  winner is found; `add-newsletter-split-test-variant`, `-update` and `-remove` manage the arms, with
  the subject line per arm. The new `splittest` skill explains what changes once a newsletter is
  one — a tool refusing with `split_test_not_supported` is almost never a defect, it is the wrong
  address. (0.7.x)
- **A newsletter's preheader** is documented, and name, subject and preheader are read out of the
  HTML before it is imported. (0.7.x)
- **New skill `dashboard`** — reads an account's numbers (reach, delivery, opens, clicks, bounces,
  unsubscribes of the last dispatches) and builds a readable dashboard from them. Read-only: it
  creates, changes and sends nothing. (0.8.0 – 0.8.2)
- **New skill `email-template-generator`** — the plain business emails that are not newsletters:
  cold outreach, support replies, follow-ups, declines. No HTML, no layout. (0.8.3)
- Upstream the plugin is built one per environment, installable by either host, and production is
  plainly `KlickTipp`. Nothing changes for this repository, which only ever ships production.
  (0.7.x)

## 0.6.3 — 2026-09-11

- **The content of an email is edited block by block.** `email-newsletter-content-edit` is gone;
  in its place a tool per block kind — `add-email-editor-paragraph`, `update-email-editor-button`,
  `add-email-editor-image-block`, `update-email-editor-row-style`, `move-email-editor-block`, `remove-email-editor-block` and the
  rest — each addressing blocks by their `uuid`. Reading is `get-email-editor-content`, importing HTML
  `replace-email-editor-content-from-html`, publishing `publish-newsletter-email-content`, and `validate-email-editor-content` reviews
  the assembled email before it goes out. (0.6.0)
- **Two skills instead of one.** `email-erstellung` is split: `email` carries the content of one
  email — what each block is, which fields it takes, how to assemble a finished email from a
  starting point and how to change an existing one — and the new `newsletter` carries the hull
  around it: draft, audience, sender and reply address, test send, dispatch confirmation. (0.6.0,
  0.6.1)
- The `email` skill ships a design brief and a parts bin rather than more templates, with the
  per-kind styles documented per block, and it says what each block *is*, not only which fields it
  has. (0.6.0)
- The skill no longer makes the agent re-read after every write, and it says what fits into one
  call. (0.6.0)
- The Codex manifest follows: its listing text describes the block tools and names both skills,
  and CI now checks that the skills declaration does not drift between the two manifests.
- Fixes: no add-on blocks nobody asked for, the content check is performed rather than merely
  offered, the image library lists rather than searches, and the block-tool corrections reached
  the files the agent actually reads. (0.6.2, 0.6.3)

## 0.5.0 — 2026-09-09

- Every environment gets its own MCP server name upstream; production keeps the unsuffixed one, so
  the tool names in this plugin stay as they are.
- `email-erstellung`: changing the words of a text block keeps the block's **stored markup**. A
  block carries most of its look inside its own `html` — the wrapper, `<p style=…>`, `<span
  style=…>` — so a bare `<p>New text</p>` would throw away font size, line height and colours. The
  skill now takes the block's own `html` as the template and replaces the words only. (0.4.5,
  0.4.6)
- `email-erstellung`: corrected what `addModule` copies. The server takes the `style` object and
  the padding from the nearest block of the same kind, but not what sits inside the `html` — that
  part is the caller's, taken from a neighbouring block rather than invented. (0.4.4)

## 0.4.3 — 2026-09-08

- `email-erstellung`: the two structure operations are described, together with the way to build a
  newsletter out of them. (0.4.2, 0.4.3)

## 0.4.1 — 2026-09-08

- `email-erstellung`: states that the personalized email is written complete, and what it costs to
  add one.

## 0.4.0 — 2026-09-08

- DEV-10830: import once, edit afterwards — no full replacement any more.
- The skill ships a professional template to generate from, with its reference files.
- The two fields a video block takes are named.
- `replaceWarnings` is described as it behaves today.

## 0.3.1 — 2026-09-08

- `email-erstellung`: what a text replacement may and may not touch.

## 0.3.0 — 2026-09-07

- `email-erstellung`: the tools hand out the stored block document, not HTML — and the skill reads
  it that way. `content` is the editable draft with its revision, `publishedContent` the active
  dispatch template.

## 0.2.7 — 2026-09-07

- Fixes.

## 0.2.6 — 2026-08-31

- The skill is named `email-erstellung` — the plugin already says KlickTipp.

## 0.2.5 — 2026-08-31

- The plugin source is named `klicktipp` rather than `kt-app`.

## 0.2.4 — 2026-08-31

- Plugin, connector and skill are named after KlickTipp, not after the tooling.

## 0.2.3 — 2026-08-28

- The login instructions are split by install path.

## 0.2.2 — 2026-08-28

- The one-time MCP login is documented, with the prefixed server name.

## 0.2.0 — 2026-08-28

- Archives are named after the tag; the icon comes from the official logo. (0.2.0, 0.2.1)

## 0.1.0 — 2026-08-28

- First public release: the KlickTipp plugin for Claude Code and Codex, as a one-plugin
  marketplace, pointing at the production MCP server (`https://mcp.klicktipp.com/mcp`).
- Scope is newsletters and opt-in processes: drafts, drag-and-drop content, audience, sender, test
  sends and the dispatch confirmation, plus reading the account's opt-in processes.
- Ships the `email-erstellung` skill with its reference files, a `SETUP.md`, and the documentation
  page published through GitHub Pages. (0.1.0 – 0.1.2)
