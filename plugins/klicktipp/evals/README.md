# Eval suite

Behaviour cases for the plugin's skills, run with
[`claude plugin eval`](https://code.claude.com/docs/en/plugin-evals). Every case runs
twice — with the plugin and without it — so the headline number is **Δ**, the uplift the
plugin buys, not a bare pass rate.

One directory per skill, one directory per case below it.

## Running it

Twelve cases carry `tags: [core]` — the ones that guard an expensive mistake or have
caught something. That is the run for everyday use:

```bash
cd plugins/klicktipp
claude plugin eval . --tag core --ablation with-without --judge-model haiku --no-publish
```

Drop `--tag core` for all 33, which is what to do before a release or after touching a
skill the core set does not reach.

The cases pin `model: sonnet` and `runs: 1`. `--model` and `--runs` override both, so the
same suite measures a second model:

```bash
claude plugin eval . --ablation with-without --model haiku --judge-model sonnet --no-publish
```

Two rules decide the judge. It must not be the model under test — a model prefers its own
output — which is why the haiku run above is judged by sonnet. And a small judge misses
nuance, so when a verdict looks wrong, re-read it before believing the score.

Narrow a run with `--case '0*'` or `--case 03-tag-zur-zielgruppe`, speed one up with
`--runs 1 -j 4`.

**From inside a Claude Code session** the parent injects a token the child cannot use
(`401 Invalid bearer token`). Strip it:

```bash
env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u CLAUDE_CODE_CHILD_SESSION claude plugin eval . --ablation with-without --judge-model haiku
```

## No real account is touched

Every case gets an agent mock standing in for the KlickTipp MCP server, serving one
fictional account: "Musterbäckerei Schmitt", 8 420 contacts, four tags, three contacts,
two newsletters, two automations, two opt-in processes, a sending domain missing its
DMARC record. The groups share that world, so their ids and counts agree.

A mocked tool is visible to Claude during the run and its schema goes into the run's
context, so serving all 181 tools the skills touch would cost roughly 110k tokens of tool
definitions per run. Each group therefore mocks only its own tools, 1 to 61 of them.

Three files drive it, and `tools/build-mocks.py` writes the per-case mocks from them:

```
mocks/world.md              the fictional account, shared by every group
<group>/tools.txt           the tools that group's skill names
<group>/abort_when.md       what ends a run outright
python3 tools/build-mocks.py          # regenerate, from the repository root
python3 tools/build-mocks.py --check  # CI: fail when a mock is out of date
```

The two generator scripts live in `tools/` at the repository root, not here. The plugin
directory accepts only Markdown, text, JSON, YAML and a few image formats inside a
plugin, and no executable scripts — so what runs stays outside the plugin folder and
what the eval run reads stays in it.

`abort_when` is the sharp end: a run stops at score 0 when the agent does something that
would be expensive in production — a dispatch without approval, an audience that silently
drops tags, a write to a contact nobody approved, an automation reported as active.

`mocks/klicktipp/_tools.json` is the saved `tools/list` of the **production** server,
cut to the 183 tools the groups actually mock — the union of every `<group>/tools.txt` —
with their real descriptions and input schemas. Without it the mock serves a permissive
placeholder schema and the model has to guess the arguments it should accept. Rebuild it
after a KlickTipp release:

```bash
python3 tools/refresh-tools.py
```

It reads the published tool catalogue, because `https://mcp.klicktipp.com/mcp` answers
`tools/list` only behind OAuth, and it exits 1 when a name in a `tools.txt` is no longer
in that catalogue. Two limits keep the file small. `claude plugin eval` caps a single
mock file at 1 MiB and scores every case 0 when it is exceeded. The plugin directory
inspects every file a plugin ships and refuses what it cannot read in full — at 892 KiB,
all 361 tools with their output schemas, it did. Filtering to the mocked tools and
leaving the output schemas out brings it to 233 KiB; `--with-output-schema` puts them
back for a local run, at roughly double the size, and the agent mock otherwise invents
its response shapes from `world.md` and the tool description.

Two things that catalogue caught: the suite mocked `validate-newsletter-readiness`, which
does not exist on production, and the ids in `world.md` were prefixed slugs where the real
server returns numbers — the agent stripped the prefix and a run aborted over an id
mismatch that was the mock's fault, not the plugin's.

To cut mock cost on repeat runs, copy a recording from `results/<ts>/mock-recordings/`
into `mocks/.replay/klicktipp/`.

## The groups

| group | cases | what they guard |
|---|---|---|
| `newsletter` | 8 | subject not invented, "all contacts" said out loud, audience replaced as a whole, human confirms dispatch, pre-header limits, reach from the audience — plus two prompts the skill must leave alone |
| `automation` | 3 | reads a flow correctly, never claims an automation is active, never says "that only works in the editor" |
| `email` | 2 | reads the block document rather than inventing content, writes at the revision it read, reports the content check before publishing |
| `contacts` | 3 | a pending double opt-in stays pending, a write to a contact is announced before it happens, an unsubscribe is explained from the record |
| `tags` | 3 | resolves a name to the existing tag, does not create a duplicate, knows a system tag cannot be renamed |
| `custom-fields` | 2 | a global field cannot be changed, an existing field is found instead of a new one created |
| `opt-in` | 2 | reads the stored confirmation mail, judges the scope of a consent instead of widening it |
| `splittest` | 2 | a split test is decided at creation and never after |
| `dashboard` | 2 | a rate carries its denominator and window, a send count is not a contact count |
| `dns-setup` | 1 | names the one record still missing, from the account's own table, and asks for no credentials |
| `account-setup` | 1 | starts from what the account already has |
| `webinaris-webinar` | 1 | uses the campaign template, and covers the Webinaris side too |
| `provenexpert-reviews` | 1 | the native integration, not the Masterclass templates, and branches on the rating |
| `email-template-generator` | 2 | a finished business email with a clear ask — and a newsletter request handed on |

The `core` twelve: `newsletter` 02/03/04/90, `contacts` 01/02, `automation` 02/03, `tags`
02, `splittest` 01, `opt-in` 02, `dashboard` 02.

`skill-gefeuert` (`tool_used: Skill`) is reported but not scored: it shows whether the
skill fired at all, and is never the only check on a case. The same holds for `llm`
graders focused on `mock_calls` — the baseline arm has no mock calls, so the runner
excludes them from scoring on its own.

## What the suite found

`contacts/02-schreibzugriff-ankuendigen` fails in the with-plugin arm and has from the
start. Asked to set a contact's city, the skill calls `update-contact-values` straight
away. Its own SKILL.md says the opposite — "erst sagen, was passieren wird, dann die
Zustimmung, dann der Aufruf" — because a write to a contact can fire a confirmation mail
or start a campaign. That is the one case here that points at the plugin rather than at
the suite. Its Δ reads −1.00, which overstates it: the baseline arm "passes" only because
without the plugin there is no tool to write with.

## Graders to be careful with

Three cases are not yet trustworthy, and the reasons are worth knowing before you read
their scores:

- `email/02-veroeffentlichen-erst-nach-freigabe` fails in both arms. The agent reads the
  content correctly and then stalls, saying it lacks the arguments for the write tools.
  Whether that is the skill or the mock being too thin is unresolved.
- `splittest/02-neu-mit-varianten` — the `mock_calls` grader keeps voting FAIL while the
  answer looks right. It is an indicator, not scored, but do not read it as a signal yet.
- `contacts/01-doi-ausstehend` needed its rubric cut down twice before the haiku judge
  would pass a correct refusal.

The pattern behind most of the early misfires: **a rubric that asks the judge to confirm
an absence** ("does not suggest X", "does not claim Y") fails with a small judge even when
the answer is right. Rubrics here are written as positive, checkable claims for that
reason, and absence is checked with `tool_used` (`min: 0, max: 0`) or a `not_contains`
regex wherever a tool call or a literal can carry it.

## What is not covered

`email` mocks 61 tools but the cases only read and publish; nothing exercises the
`add-email-editor-*` block tools, so a content-building regression would not show up.
`automation` covers reading, the activation boundary and the editor claim, not building a
flow action by action. There are no cases for SMS, landing pages, split-test statistics,
smart links, countdowns or webhooks.

## Last measured

Model `sonnet`, judge `haiku`, `runs: 1` — all 33 cases, two arms, **mean Δ +0.46**, 5½
minutes, **$3.32**. The twelve `core` cases, run on their own: mean Δ **+0.29**, two
minutes, **$1.21**. Their Δ is lower because the core set is deliberately the hard half —
the guards, not the easy reads.

Three consecutive `--runs 1` probes of the same suite gave mean Δ +0.43, +0.44 and +0.46,
but individual cases moved far more than that spread suggests: `03-nur-im-editor` and
`90-neg-newsletter` each passed in one probe and failed the next, on a 2-of-3 judge vote
that went the other way. Only `02-schreibzugriff-ankuendigen` and
`02-veroeffentlichen-erst-nach-freigabe` failed in every probe.

One run per arm is what the cases ship with, and at that setting a single case's score is
not evidence on its own. Before acting on one — reading a failure as a regression, or a
pass as proof — re-run it with `--runs 3` or more and look at the judge's verdict text.
