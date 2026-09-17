# Die veröffentlichten Verträge — E-Mail-Inhalt, Bausteine, Gestaltung, Bilder

Wort für Wort das, was der Server in `tools/list` für die 48 Werkzeuge dieses Skills
ausliefert: Beschreibung, Annotationen, jeder Parameter mit Typ, Grenzen und Beschreibung. Ein `*`
markiert Pflichtparameter. `R` liest nur · `D` löscht oder ersetzt ohne Undo · `O` erreicht etwas
außerhalb des Kontos · `I` ein zweiter gleicher Aufruf ändert nichts mehr.

Generiert aus `build/tools-list.json` (Stand 2026-09-17) mit `build/contracts.py` — nicht von Hand
ändern, sondern den Dump erneuern und neu erzeugen. Wofür ein Werkzeug da ist, was es nicht tut
und woran man sich stößt, steht in [tools.md](tools.md).

## `email-content-import` · DO

**Import email content from HTML**

Converts HTML into the drag-and-drop editor document of one KlickTipp email newsletter, addressed by its editor URL -- the entry path for a design that exists only as HTML; changes afterwards belong to the block tools. Replaces the stored draft entirely, has no undo, and does not publish: the dispatch content changes only through email-content-publish, named in nextAction. Bound to the content revision of the preceding read. A newsletter that already has content is refused on the first call with a list of what it holds; a second call with replaceExistingContent set to true converts. Non-HTML blocks (add-ons, decisions, AI blocks) are rendered or dropped; the warnings record what it cost. The body has to carry the %User:Signature%placeholder or spell out postal details and unsubscribe link, else it is refused. Returns content status, new revision and editor URL.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, exactly as returned by email-get
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the read this HTML is based on; a stale one refuses the import
- `contentHtml`* — string (minLength 1; maxLength 10000000): The complete HTML body; replaces the stored document entirely
- `replaceExistingContent` — null | boolean: true to replace content the email already has; omit on the first attempt, so the answer lists what would be lost
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-content-publish` · DO

**Publish email content**

Publishes the drag-and-drop editor draft of one KlickTipp email newsletter: from then on that body is what a dispatch sends, replacing the previously published one. This changes what real recipients would receive and has no undo. It takes no HTML -- only the stored draft is published -- and is bound to the content revision of the preceding read or write; if the newsletter changed in between, nothing is published. Only a draft can be published, and a body using editor features the server must not publish on a person's behalf is refused with the editor URL. Sending is separate: email-newsletter-send. Returns content status before and after, the new revision and the editor URL.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, exactly as returned by email-get
- `contentRevision`* — string (minLength 7; maxLength 100): contentRevision of the state to publish, from the read or the last write; a stale one refuses
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-spacer-style-write` · I

**Write email spacer height**

Sets how tall spacers are, SEVERAL IN ONE CALL. A spacer is nothing but its height, so this is the whole block: the gap it makes between two sections. Named values only -- a whole number of pixels. Everything not named stays as it is. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `height` — null | integer (minimum 0; maximum 400): Height of the gap in pixels
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-divider-style-write` · I

**Write email divider line**

Sets the line of dividers, SEVERAL IN ONE CALL: how thick it is, whether it is solid, dashed or dotted, its colour, and how far it reaches across the row. Named values only -- no CSS -- so a line is "1px solid #000000" and a width is a whole percentage. A thickness of 0 makes the divider an invisible spacer, which is a real use and not a mistake. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `line` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): The line as "1px solid #000000"
- `width` — null | integer (minimum 10; maximum 100): How far the line reaches across the row, as a whole percentage
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-button-style-write` · I

**Write email button look**

Sets the look of buttons, SEVERAL IN ONE CALL: the colour behind the label, the colour of the label, how round the corners are, a border on any of the four sides, and the space between the label and the edge -- which is what makes a button large or small. Named values only -- no CSS. This is the button itself; the space AROUND it is email-block-style-write, and the words are email-button-write. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the label, "#RRGGBB" or "transparent"
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour of the label
- `borderRadius` — null | integer (minimum 0; maximum 400): How round the corners are, in pixels; 0 is a rectangle
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above, as "2px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left, same shape
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the label, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the label
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the label
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the label
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-get` · RI

**Get email**

Reads one email body by email ID or editor URL and says what the email is used for: email ID, usage type, editor, content state and the editor URL every write of the body takes. Everything else is a projection requested through "include": "content" (the editable document), "contentOutline" (uuid, kind and value of every writable field), "styleOutline" (what the style tools set) and "publishedContent" (the HTML a dispatch would send). The outlines carry the contentRevision a write has to give back. The newsletter around the email -- name, audience, dispatch state, split-test arms -- is email-newsletter-get. Reads only. The three document projections exist for the drag-and-drop editor and are answered whole or refused; publishedContent is readable in every state and editor.

Parameter:

- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it; omit when the email ID is given
- `include` — array<string> (maxItems 4): Projections to add: "content" (the editable document), "contentOutline" (uuid, kind and value of every writable field -- for a content change), "styleOutline" (what the style tools set -- for a style change), "publishedContent" (the HTML a dispatch would send); omit for identity only
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-preview` · ROI

**Preview email**

Renders the current drag-and-drop email draft through Bee and displays its HTML in an MCP App. Takes the editor URL from email-get or a content write. Includes unpublished edits; does not save, publish or send. Recipient placeholders remain unresolved. The result carries contentHtml for hosts without MCP Apps support.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-content-check` · RI

**Check email content**

Checks the body of one drag-and-drop email and returns findings, each naming the uuid to fix and the tool that fixes it: an image without source or alt text, a button without target, an empty text block, an add-on block (countdown, contact card, wowing video) that was added but never configured, text contrast below WCAG 4.5:1, and a missing KlickTipp footer placeholder. A source-less image and an unconfigured add-on are errors -- what would reach the inbox is broken -- and everything else is a warning, the same weight the platform gives them at dispatch. Reads only; nothing is written, published or leaves the account, and a contrast is measured only where both colours are in the document. An email of the previous editor is refused. Findings come as data and, for a host that renders MCP Apps, as a page.

Parameter:

- `emailId` — null | integer (minimum 1): ID of the email; omit when the editor URL is given
- `editorUrl` — null | string (minLength 12; maxLength 500): Editor URL of the email, as a previous read returned it; omit when the email ID is given
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-block-move`

**Move email block**

Moves one block to another place in its column, or into the column whose uuid it names. The same block moves, so its styling, its uuid and an add-on`s configuration survive -- removing it and adding it again would not. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the block to move
- `position` — null | integer (minimum 0): Where it goes, counted from zero; omit to append
- `toColumnUuid` — null | string: The uuid of the column to move it into; omit to move inside its own column
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-block-remove` · D

**Remove email block**

Removes one block, of any kind -- removing needs to know nothing about it. There is no undo and the block cannot be brought back through these tools, so ask the user before removing one. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the block to remove
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-block-style-write` · I

**Write email block style**

Writes the space around one block and how its content sits -- left, centred, right or justified. Works for a block of any kind, an image and a divider included. THE TYPOGRAPHY OF A TEXT BLOCK IS NOT HERE: its font, size, line height and colour live in the markup of that block, so they are changed with email-text-write, and the size an image is shown at belongs to the image. Everything not named stays as it is. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the blocks to write; the same values land on each
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the block, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the block, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the block, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the block, in pixels
- `textAlign` — null | string (einer von `left`, `center`, `right`, `justify`): How its content sits: "left", "center", "right" or "justify"
- `hideOnMobile` — null | boolean: Whether the block is hidden on a phone
- `hideOnDesktop` — null | boolean: Whether the block is hidden on a desktop
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-button-add`

**Add email button**

Puts a button into the column whose uuid it names and answers with the uuid of the new block. It takes label, href straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest button block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `label` — null | string (maxLength 2000): The visible text of the button, as markup
- `href` — null | string (maxLength 2000): Where the button leads
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-button-write` · I

**Write email button**

Writes the visible text of one button block and where it leads. The label is markup like a text block: start from what you read and swap only the words, or the button loses its typography. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the button block
- `label` — null | string: The visible text of the button, as markup
- `href` — null | string: The link target of the button
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-column-style-write` · I

**Write email column style**

Writes the look of columns -- SEVERAL IN ONE CALL, the same values on each: the colour behind it, the space between its edges and its blocks, and a border on any of its four sides. Named values only -- no CSS -- so a padding is a number of pixels and a border is "1px solid #000000", with solid, dashed, dotted or none. Everything not named stays as it is. THE WIDTH OF A COLUMN IS NOT HERE: columns of a row are equally wide, and an uneven split is made in the KlickTipp editor. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the columns to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the column, "#RRGGBB" or "transparent"
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the content of the column, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the content of the column, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the content of the column, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the content of the column, in pixels
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above the column, as "1px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right of the column, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below the column, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left of the column, same shape
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-divider-add`

**Add email divider**

Puts a divider into the column whose uuid it names and answers with the uuid of the new block. It has nothing to write: it is finished the moment it exists. What it looks like -- its thickness, its colour, the space around it -- is the style level, email-block-style-write and the row above it. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-heading-add`

**Add email heading**

Puts a heading into the column whose uuid it names and answers with the uuid of the new block. It takes text and level straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest heading block of this email; its markup does not come with it, so start from a neighbour`s. THE LEVEL IS PART OF THE STRUCTURE, not of the look: h1 is the one headline of the mail, h2 a section, h3 a subsection. A newsletter with several sections wants h2 -- that is what real ones use most. Size and colour are the markup, not the level. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `text` — null | string (maxLength 100000): The words of the heading, as markup
- `level` — null | string (einer von `h1`, `h2`, `h3`): The heading level: "h1", "h2" or "h3"; omit for h1
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-html-add`

**Add email custom HTML**

Puts a custom HTML block into the column whose uuid it names and answers with the uuid of the new block. It takes html straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest html block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The markup of the block
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-icons-add`

**Add email icons**

Puts an icon block into the column whose uuid it names, with its icons, and answers with the uuid of the new block. The size of an icon and where its words sit come from the block this email already has -- they are required by the format, so they are copied rather than asked for. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the picture, from email-image-search or email-image-upload.
  - `href` — string: Where it leads.
  - `text` — string: The words beside the icon.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-icons-write` · I

**Write email icons**

Writes the entries of one icon block: the picture of each, the words beside it and where it leads. THE LIST REPLACES THE LIST -- send every icon the block should have, in order. The size of the icons and where the words sit are kept from the entry that was there. Not the same block as social links: this one carries any picture with a caption. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the icon block
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the picture, from email-image-search or email-image-upload.
  - `href` — string: Where it leads.
  - `text` — string: The words beside the icon.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-add`

**Add email image**

Puts an image into the column whose uuid it names and answers with the uuid of the new block. It takes src, alt, href straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest image block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `src` — null | string (maxLength 2000): URL of the image, from email-image-search or email-image-upload
- `alt` — null | string (maxLength 1000): Alternative text of the image
- `href` — null | string (maxLength 2000): Link target of the image
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-write` · I

**Write email image**

Points image blocks at other images and sets their alternative text or their link, SEVERAL IN ONE CALL -- swapping the pictures of a newsletter is one call and one revision, not one per picture. THE URL HAS TO BE ONE OF THIS ACCOUNT: take it from email-image-search or from what email-image-upload returned -- a provider or stock URL makes every recipient`s mail client contact a third party and breaks the day the picture disappears there. The width the image is shown at belongs to the block and is not changed here. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `images`* — array<object> (minItems 1; maxItems 60): The image blocks to write, each by uuid; a field left out keeps its value, an empty href removes the link
  - `uuid`* — string: The uuid of the image block.
  - `src` — string: URL of the image, from email-image-search or email-image-upload.
  - `alt` — string: Alternative text of the image.
  - `href` — string: Link target; an empty string removes the link.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-list-add`

**Add email list**

Puts a list into the column whose uuid it names and answers with the uuid of the new block. It takes html straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest list block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The list, as complete <ul> or <ol> markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-menu-add`

**Add email menu**

Puts a menu into the column whose uuid it names, with its entries, and answers with the uuid of the new block. One call and one revision rather than two. What the entries do not name -- how a link opens, the separator, the spacing -- comes from the menu this email already has. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `items`* — array<object> (minItems 1; maxItems 30): The menu entries, left to right
  - `text`* — string: The words of the entry.
  - `href` — string: Where it leads.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-menu-write` · I

**Write email menu**

Writes the entries of one menu block: their words and where each one leads. THE LIST REPLACES THE LIST -- send every entry the menu should have, in order, because a menu has no stable handle to address one entry by. Everything the entries do not name is kept: how a link opens, the separator, the spacing and the typography of the block. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the menu block
- `items`* — array<object> (minItems 1; maxItems 30): The menu entries, left to right
  - `text`* — string: The words of the entry.
  - `href` — string: Where it leads.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-page-style-write` · I

**Write email page style**

Writes what the whole email starts out with: the colour around the message, the colour behind it, the default text colour, the colour of every link, the default font, how wide the message is and where it sits. THIS IS THE PLACE FOR "ALL LINKS GREEN", "A WIDER EMAIL", "ONE FONT FOR THE WHOLE MAIL" OR "ALIGN THE EMAIL LEFT": these are defaults of the document, so one call reaches every row -- but a block whose own markup names a value keeps it. It addresses no uuid: an email has one page. Named values only -- no CSS. The font is named, not a stack, and only fonts every mail client has are offered; a web font works only if the KlickTipp editor sets it. Everything not named stays as it is. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour around the message, "#RRGGBB" or "transparent"
- `contentBackgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the message itself
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default text colour of the whole email
- `linkColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default colour of every link of the email
- `contentWidth` — null | integer (minimum 320; maximum 1440): Width of the message in pixels
- `fontFamily` — null | string (einer von `Arial`, `Courier`, `Georgia`, `Helvetica Neue`, `Lucida Sans`, `Tahoma`, `Times New Roman`, `Trebuchet MS`, `Verdana`, `ヒラギノ角ゴ Pro W3`, `メイリオ`): Default font of the whole email, by name; see the schema for the names
- `contentAlign` — null | string (einer von `left`, `center`, `right`): Where the message sits when the window is wider than it is
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-paragraph-add`

**Add email paragraph**

Puts a paragraph into the column whose uuid it names and answers with the uuid of the new block. It takes html straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest paragraph block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The words of the paragraph, as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-personalized-email-add`

**Add email personalized email block**

Puts a personalized email block into the column whose uuid it names, with the instruction that IS the block: without it the block renders a placeholder into a newsletter that looks finished and generates nothing, which is why the instruction is required here. SAY ONE THING WHEN YOU ADD IT: the newsletter editor does not offer this block in its insert menu -- only automations do -- so a person cannot create it there and cannot bring it back after a removal. Which data fields and tags the instruction may use is chosen in the KlickTipp editor. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `prompt`* — string (minLength 1; maxLength 10000): The instruction a dispatch turns into a text per recipient
- `name` — null | string (maxLength 200): A name for the block, for the editor
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-personalized-email-write` · I

**Write personalized email block**

Writes the instruction a personalized email block generates its text from, per recipient. THAT INSTRUCTION IS THE BLOCK: the block itself stays the same block, and one without an instruction renders a placeholder into an email that looks finished. Which data fields and tags the instruction may use is chosen in the KlickTipp editor, not here. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the personalized email block
- `prompt` — null | string (maxLength 10000): The instruction a dispatch generates the text from, per recipient
- `name` — null | string (maxLength 250): The name of the block as a person sees it in the KlickTipp editor
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-row-add`

**Add email row**

Adds a row of equally wide, empty columns -- START HERE ON AN EMPTY DRAFT, because a block needs a column to go into. The answer names the uuids of the new columns and the revision for the next write, so no read is needed before filling them. The row takes its background and width from a row the email already has. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columns` — null | integer (minimum 1; maximum 6): How many equally wide columns the row gets; 1, 2, 3, 4 or 6, one by default
- `position` — null | integer (minimum 0): Where the row goes among the rows, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-row-style-write` · I

**Write email row style**

Writes the look of rows -- SEVERAL IN ONE CALL, the same values on each: the colour behind the whole band, the colour behind its content area, the default text colour, the width of the content, how the columns line up, whether the row stacks or is hidden, its padding, and a border on any of its four sides. TO FRAME A ROW, BORDER THE ROW, not its columns -- one border per column draws a box per column, with seams. Named values only -- no CSS -- so a colour is "#RRGGBB" or "transparent", a width or padding is a number of pixels, and a border is "1px solid #000000". Everything not named stays as it is. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuids`* — array<string> (minItems 1; maxItems 60): The uuids of the rows to write; the same values land on each
- `backgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the whole row, "#RRGGBB" or "transparent"
- `contentBackgroundColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Colour behind the content area inside the row
- `textColor` — null | string (Muster `^(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Default text colour of the row
- `contentWidth` — null | integer (minimum 320; maximum 1440): Width of the content area in pixels
- `verticalAlign` — null | string (einer von `top`, `middle`, `bottom`): How the columns line up: "top", "middle" or "bottom"
- `stackOnMobile` — null | boolean: Whether the columns stack under each other on a phone
- `hideOnMobile` — null | boolean: Whether the row is hidden on a phone
- `hideOnDesktop` — null | boolean: Whether the row is hidden on a desktop
- `paddingTop` — null | integer (minimum 0; maximum 400): Space above the content of the row, in pixels
- `paddingRight` — null | integer (minimum 0; maximum 400): Space right of the content of the row, in pixels
- `paddingBottom` — null | integer (minimum 0; maximum 400): Space below the content of the row, in pixels
- `paddingLeft` — null | integer (minimum 0; maximum 400): Space left of the content of the row, in pixels
- `borderTop` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border above the row, as "1px solid #000000"
- `borderRight` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border right of the row, same shape
- `borderBottom` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border below the row, same shape
- `borderLeft` — null | string (Muster `^(0|[1-9][0-9]{0,2})px (solid|dashed|dotted|none) (#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|transparent)$`): Border left of the row, same shape
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-social-add`

**Add email social links**

Puts a social block into the column whose uuid it names, with its icons, and answers with the uuid of the new block. ASK email-social-icon-search FOR THE ICON PICTURES FIRST: it hands back the ones this account already uses, and any URL from the account`s own image library works too. Never invent a src -- an icon URL that resolves to nothing is a hole in the row that no one sees until the mail is out. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the icon picture. Take one from email-social-icon-search, or any URL from the account`s own image library -- an uploaded picture is a usable icon. Never invent one: an icon URL that resolves to nothing is a hole in the row, in every recipient`s mail program.
  - `href`* — string: Where the icon leads.
  - `name` — string: The network, e.g. "facebook".
  - `alt` — string: Alternative text: what a reader gets instead of the picture when it does not load, and what a screen reader says.
  - `title` — string: Tooltip of the icon, shown on hover. Not a replacement for alt: a reader who never sees the picture never sees this either.
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-social-icon-search` · RI

**Search email social icons**

Lists the ICON PICTURES this email already uses, with the network, the alternative text and the tooltip each carries, most used first. ASK THIS BEFORE email-social-add OR email-social-write: the pictures come from the editor`s own icon sets, which this server cannot enumerate, so reusing one from here is the only way to stay inside the set a person picked in the editor. NEVER INVENT A src -- a URL that resolves to nothing is a hole in the row that nobody sees until the mail is out at every recipient. An account`s own picture works as an icon too: search it with email-image-search and pass that URL. If this comes back empty and the library has no suitable picture, say so and ask the user to place one social block in the editor rather than guessing a URL.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as a read returned it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-social-write` · I

**Write email social links**

Writes the icons of one social block: the picture of each, where it leads, its name and its alternative text. THE LIST REPLACES THE LIST -- send every icon the block should have, in order. The icon pictures come from the editor`s own icon sets, so take a src from what the read returned rather than inventing a URL; what an icon is (follow, share) and how its link opens are kept from the icon that was there. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the social block
- `icons`* — array<object> (minItems 1; maxItems 20): The icons, left to right
  - `src`* — string: URL of the icon picture. Take one from email-social-icon-search, or any URL from the account`s own image library -- an uploaded picture is a usable icon. Never invent one: an icon URL that resolves to nothing is a hole in the row, in every recipient`s mail program.
  - `href`* — string: Where the icon leads.
  - `name` — string: The network, e.g. "facebook".
  - `alt` — string: Alternative text: what a reader gets instead of the picture when it does not load, and what a screen reader says.
  - `title` — string: Tooltip of the icon, shown on hover. Not a replacement for alt: a reader who never sees the picture never sees this either.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-spacer-add`

**Add email spacer**

Puts a spacer into the column whose uuid it names and answers with the uuid of the new block. It has nothing to write: it is finished the moment it exists. What it looks like -- its thickness, its colour, the space around it -- is the style level, email-block-style-write and the row above it. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-table-add`

**Add email table**

Puts a table into the column whose uuid it names, with its rows, and answers with the uuid of the new block. Give every row the same number of cells: a table renders as a grid and a short row is a hole in it. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `rows`* — array<array> (minItems 1; maxItems 60): The rows, each a list of cells as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-table-write` · I

**Write email table**

Writes the cells of one table block, row by row, each cell a piece of markup. THE ROWS REPLACE THE ROWS -- send the whole table, and give every row the same number of cells, because a table renders as a grid and a short row is a hole in it. The header row, the borders, the colours and the typography of the table are kept. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the table block
- `rows`* — array<array> (minItems 1; maxItems 60): The rows, each a list of cells as markup
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-text-add`

**Add email text**

Puts a text block into the column whose uuid it names and answers with the uuid of the new block. It takes html straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest text block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `html` — null | string (maxLength 100000): The words of the block, as markup
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-text-write` · I

**Write email text**

Writes the words of text blocks -- heading, text, paragraph, list and custom HTML -- each named by its uuid. START FROM THE MARKUP YOU READ for that block, keep its wrapper div and its style attributes and swap only the words: the typography of a text block lives in its own markup, so a bare <p>new text</p> throws the font size, line height and colours away. Several blocks in one call, and nothing else in the email is touched. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `blocks`* — array<object> (minItems 1; maxItems 100): The blocks to write, each by uuid and its complete markup; a heading may add its level
  - `uuid`* — string: The uuid of the text block to write.
  - `html`* — string: Its complete markup, the read markup with the words replaced.
  - `level` — string (einer von `h1`, `h2`, `h3`): The heading level, for a heading block only. Refused on any other kind, which has none.
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-video-add`

**Add email video**

Puts a video into the column whose uuid it names and answers with the uuid of the new block. It takes src, thumbSrc straight away, so a filled block is one call and one revision rather than two. The block copies the look of the nearest video block of this email; its markup does not come with it, so start from a neighbour`s. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `columnUuid`* — string: The uuid of the column the block goes into
- `src` — null | string (maxLength 2000): URL of the video, which is where the click leads
- `thumbSrc` — null | string (maxLength 2000): URL of the preview image, which is what the recipient sees
- `position` — null | integer (minimum 0): Where it goes inside the column, counted from zero; omit to append
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-video-write` · I

**Write email video**

Writes the video URL of one video block and the preview image it shows. NO MAIL CLIENT PLAYS A VIDEO in the inbox, so the block shows the preview image with a play icon and links to the video -- a block without a preview image stays empty. For a YouTube video the thumbnail of that video is the obvious choice. Bound to the contentRevision of the read and refused whole if anything in it fails, so nothing half-written is stored. Drafts only. Saves the draft; publishing is email-content-publish.

Parameter:

- `editorUrl`* — string (minLength 12; maxLength 500): Editor URL of the email, as the read returned it
- `contentRevision`* — string (minLength 7; maxLength 100): The contentRevision of the read this change is based on
- `uuid`* — string: The uuid of the video block
- `src` — null | string (maxLength 2000): The video URL, for example a YouTube or Vimeo page
- `thumbSrc` — null | string (maxLength 2000): The preview image the block shows instead of the video
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-search` · RI

**Search images**

Lists the images in a KlickTipp account's image library -- the files the email editor's file manager shows -- sorted by path, with the public URL, path, file name, MIME type, size and upload time of each. The URL is what an image block takes in email-image-write (field src): put a URL from this list there, never a placeholder. The search matches file names and folder paths, not what a picture shows; dimensions are not part of a listing. Paged by cursor. Reads the account the access token belongs to, or one of its subaccounts when an account ID is given. To add a picture that is not in the library: email-image-upload opens a form the user picks a file in, email-image-upload-from-url adds one from a public URL.

Parameter:

- `limit` — null | integer (minimum 1; maximum 100): Images per page, 1 to 100; default 20
- `cursor` — null | string (maxLength 1000): nextCursor of the previous page; omit for the first page
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-stock-search` · ROI

**Search stock images**

Searches the free stock photo archives behind the KlickTipp email editor (Pexels, Pixabay) and returns candidates with preview URL, provider, licence and pixel size -- three by default, up to twelve. The search never comes back empty: a query without a match is answered with unrelated photos. Neither URL in the answer may go into a newsletter; pass sourceUrl and fileName of the chosen photo to email-image-upload-from-url and use the URL it returns. The licence needs no attribution but restricts identifiable people. A host that renders MCP Apps shows the candidates as pictures. The account's own library (logo, product photos) is searched with email-image-search.

Parameter:

- `query`* — string (minLength 1; maxLength 100): What the picture shows, one or two words, in English (the archives are indexed in English)
- `limit` — null | integer (minimum 1; maximum 12): How many candidates, 1 to 12; default 3
- `orientation` — null | string (einer von `landscape`, `portrait`, `square`): Only photos of this shape: landscape, portrait or square; omit for any shape
- `minWidth` — null | integer (minimum 1; maximum 10000): Only photos at least this wide, in pixels; 1200 for a full-width image
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-folder-search` · RI

**List image folders**

Lists the folders of a KlickTipp account's image library -- the folders the email editor's file manager shows -- as paths relative to the library, e.g. "Logos" and "Kampagnen/Herbst". These are the values email-image-upload-file and email-image-upload-from-url take as "folder"; a library without folders keeps everything in its root, which is what omitting the field means. Does not list pictures -- that is email-image-search, whose path field says which folder each one sits in. A very large tree is cut off and says so in "truncated".

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-folder-create`

**Create image folder**

Creates one folder in a KlickTipp account's image library and returns the folders of the library afterwards. The folder appears in the email editor's file manager, and pictures go into it by passing its path as "folder" to email-image-upload-file or email-image-upload-from-url. A path with slashes creates the levels above it as well. The name is cleaned the way a file name is -- letters, digits, dots, dashes and underscores survive, a space becomes a dash -- so read "changed" for the name it actually got. A folder that is already there is refused rather than merged into. Nothing is moved and no picture is touched.

Parameter:

- `path`* — string (minLength 1; maxLength 250): Name of the new folder, or a path for one inside another ("Kampagnen/Herbst"); letters, digits, dots, dashes and underscores survive, everything else becomes a dash
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-folder-delete` · DI

**Remove empty image folder**

Removes one EMPTY folder from a KlickTipp account's image library and returns the folders that remain. A folder that still holds anything is refused and says how much -- these tools never delete a picture, because a newsletter that was already sent keeps loading it from the library. Emptying a folder is done by the person in the KlickTipp file manager, and the appUrl of a newsletter answer leads there. Removing a folder that has folders inside it is refused for the same reason; remove those first. Nothing else in the library changes.

Parameter:

- `path`* — string (minLength 1; maxLength 250): Path of the folder to remove, as email-image-folder-search lists it
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-upload` · I

**Upload image**

Opens the upload form for a KlickTipp account's image library -- the files the email editor's file manager shows. Takes nothing and stores nothing: a host with MCP Apps support shows a file picker, the person picks a file from their own disk, and it goes into the library without passing through the conversation. Use this whenever a picture has to come from the user -- never ask them to paste base64. The answer says the form was opened; the URL of the stored file appears in the window and in a later email-image-search. A picture that already exists at a public URL does not need the form: email-image-upload-from-url adds it directly. Check email-image-search first -- a logo or product picture is usually already there.

Parameter:

- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-upload-file`

**Store picked image file**

Stores the file a person picked in the upload form of email-image-upload, in a KlickTipp account's image library, and returns its public URL for an image block in email-image-write (field src). JPEG, PNG, GIF or WebP up to 5 MB. Never overwrites: a taken name is numbered, and the result says under which name the file was stored. This tool belongs to the upload form and is published for it alone -- a model has no file of its own to send, and base64 through a conversation is what the form exists to avoid. To let the user add a picture, call email-image-upload; to add one from a public URL, email-image-upload-from-url.

Parameter:

- `fileName`* — string (minLength 1; maxLength 250): Name of the picked file, as the browser reports it; sanitised, extension set from the bytes, a taken name is numbered, never overwritten -- see storedAs
- `contentBase64`* — string (minLength 1; maxLength 6990508): The file's bytes as plain base64, no data: prefix
- `folder` — null | string (maxLength 250): Folder of the library to store it in, as email-image-folder-search lists it; omit for the library's root
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in

## `email-image-upload-from-url` · O

**Add image from URL**

Adds one image that exists at a public URL to a KlickTipp account's image library -- the files the email editor's file manager shows -- and returns its public URL, ready for an image block in email-image-write (field src). The server fetches the URL itself; it has to be reachable from the internet, without login, and may not point at a private host. Accepts JPEG, PNG, GIF and WebP up to 5 MB. Never overwrites: a taken name is numbered, and the result says under which name the file was stored. This is the way a stock photo from email-image-stock-search enters the library: pass its sourceUrl and fileName. Adds to the account the access token belongs to, or to one of its subaccounts when an account ID is given. A file on the user's own disk goes through the form email-image-upload opens.

Parameter:

- `fileName`* — string (minLength 1; maxLength 250): Name for the file, extension optional; sanitised, extension set from the bytes, a taken name is numbered, never overwritten -- see storedAs
- `sourceUrl`* — string (minLength 12; maxLength 2000): Public http(s) URL the server fetches the image from; reachable from the internet, no login, no private host
- `folder` — null | string (maxLength 250): Folder of the library to store it in, as email-image-folder-search lists it; omit for the library's root
- `accountId` — null | integer (minimum 1): User ID of the account; omit for the account the access token works in
