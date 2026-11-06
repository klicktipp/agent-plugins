# ProvenExpert: connection and survey

Click paths change; read the current steps in the KlickTipp article
https://www.klicktipp.com/de/support/wissensdatenbank/provenexpert/ and the ProvenExpert help
https://help.provenexpert.com/de before you guide the user. The ProvenExpert API cannot create the
connection or run the sync — this is UI work.

## Connection

- Started from KlickTipp ("Neues Marketing Tool" → ProvenExpert) or from ProvenExpert
  ("Integrationen" → KlickTipp → "Verbinden"). The user signs in and authorises.
- One ProvenExpert account is connected to **one** KlickTipp account — the one the browser is
  signed in to when the user authorises. Make sure that is the intended account.
- Existing ProvenExpert placeholders or smart tags in KlickTipp only show that a connection existed
  once, not that it points here now. Do not report "already connected" on that basis; say that the
  sync check (Order step 3) will prove it.

## Survey

- One survey per product or service: each email address can rate a survey once.
- Create the survey with a clear name (it becomes the name of the smart tags), then use the survey's
  edit menu → "KlickTipp Sync". Changing the questions needs a paid plan; the free plan works.
- A new survey shows "KlickTipp Sync" only after the survey list is reloaded.
- "Integrationen" → KlickTipp shows "Verbunden" (free plan too) but not which KlickTipp account;
  only the sync check (Order step 3) proves that.
- The free plan holds five surveys; when all are used, the user deletes one they no longer need.
- Do not use an internal survey unless the user wants one.

## Sync does not arrive

"KlickTipp Sync" shows no result, a clock icon may stay. Wait up to two minutes, then check
`search-tags` for the survey name.

1. Nothing in KlickTipp → the connection points to another KlickTipp account. The user disconnects
   and reconnects while signed in to the right account.
2. Still nothing for a survey created **before** the reconnect → create a new survey and sync that
   one; older surveys stay bound to the previous account.
