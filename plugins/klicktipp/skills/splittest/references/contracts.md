# Die veröffentlichten Verträge — Splittests

Wort für Wort das, was der Server in `tools/list` für die 5 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Generiert aus `build/tools-list.json` (Stand 2026-09-18) mit `build/contracts.py` — nicht von Hand
ändern, sondern den Dump erneuern und neu erzeugen. Wofür ein Werkzeug da ist, was es nicht tut
und woran man sich stößt, steht in [tools.md](tools.md).

## `email-split-test-get` · RI

**Read split test**

Reads a split test whole: the share of the audience the variants are sent to, the measuring period, the winner criterion, whether it has started, and every variant with its emailId, label ("A", "B"), name, subject and editorUrl. The test is named either by "campaignId" -- the newsletterId of email-newsletter-get -- or by the "emailId" of one variant, which answers with that variant`s test and its siblings; exactly one of the two, never both. "needsMoreVariants" is here -- a fresh test has one variant and cannot be sent until it has two -- and so is "hasStarted", which is what makes every further change refuse. Variants are changed by email-split-test-variant-add, -update and -remove, the settings by email-split-test-configure, the content of a variant by the email tools through its editorUrl. A campaign that is not a split test is refused, not answered with an empty test.

Parameter:

- `campaignId` — null | integer (minimum 1): ID of the split test campaign -- the newsletterId of email-newsletter-get; pass this or emailId, not both
- `emailId` — null | integer (minimum 1): Email ID of one variant, as splitTestVariants or an editor URL carries it; the answer is the whole test that variant belongs to. Either this or campaignId, never both
- `accountId` — null | integer (minimum 1): User ID of the account the campaign belongs to; omit for the account the access token belongs to, or pass the user ID of a subaccount the token owner may act for

## `email-split-test-variant-add`

**Add split test variant**

Adds a test variant to the split test of a campaign and returns the test with all its variants and their editorUrl. With "copyFromEmailId" the variant is a copy of an existing one, otherwise it is empty. A split test needs at least two variants before it can be sent; a fresh one has exactly one. Adding a variant redistributes the audience share evenly. Refused once the test has started. The contents of a variant are written through the tools that take its editorUrl, its subject and preheader through email-split-test-variant-update, the test settings through email-split-test-configure. Nothing is sent.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign (a newsletter ID)
- `copyFromEmailId` — null | integer (minimum 1): Email ID of the variant to copy, from splitTestVariants; omit for an empty variant
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-split-test-variant-remove` · D

**Remove split test variant**

Removes one test variant from the split test of a campaign and returns the remaining variants. The variant is its own email: removing it deletes that email with everything in it, and there is no undo. The last variant cannot be removed, and a test that has started refuses the change. Removing a variant redistributes the audience share evenly. Test settings are written through email-split-test-configure. Nothing is sent.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign the variant belongs to
- `emailId`* — integer (minimum 1): Email ID of the variant to remove, as email-newsletter-get returns it in splitTestVariants
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-split-test-variant-update` · I

**Write split test variant**

Writes internal name, subject and preheader of one test variant of a split test campaign, addressed by its email ID as email-newsletter-get lists it in splitTestVariants, and returns the test with all variants. This is the only place a variant's subject can be set; email-newsletter-draft-update refuses a split test. Writing subject or preheader invalidates every contentRevision read from this variant. Omitted arguments keep their value, a call without any change is refused, and a started test refuses the write. The body of a variant is written by the block tools through its editorUrl, the test settings through email-split-test-configure. Nothing is sent.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign the variant belongs to
- `emailId`* — integer (minimum 1): Email ID of the variant to write, as email-newsletter-get returns it in splitTestVariants
- `name` — null | string (maxLength 250): New internal name of this variant, never sent to a recipient; omit to keep the current one
- `subject` — null | string (maxLength 998): New subject line of this variant, without HTML; ask the user, never invent one. Invalidates the variant's contentRevision
- `preheader` — null | string (maxLength 120): New inbox preview line of this variant, at most 120 characters, without HTML; empty string removes it, omit keeps it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-split-test-configure` · I

**Configure split test**

Writes the settings of a split test -- the audience share sent to the test variants, the measuring period and the winner criterion -- and returns the test with its variants. Omitted arguments keep their value, a call without any change is refused, and a started test refuses the write. Whether a campaign is a split test at all is decided at creation and cannot be changed here. "conversions" and "revenue" require the conversion pixel and are refused without it; "opens" and "clicks" are always available. Variants are changed by email-split-test-variant-add, -update and -remove. Nothing is sent.

Parameter:

- `campaignId`* — integer (minimum 1): ID of the split test campaign whose settings to write
- `testSizePercent` — null | integer (minimum 2; maximum 98): Share of the audience the variants go to, 2 to 98; omit to keep
- `testDurationHours` — null | integer (minimum 1; maximum 27777): Measuring period before the winner goes to the rest, 1 to 27777 hours; omit to keep
- `winnerBy` — null | string (einer von `opens`, `clicks`, `conversions`, `revenue`): "opens" (open rate), "clicks" (unique clicks), "conversions" or "revenue" (both need the conversion pixel); omit to keep
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
