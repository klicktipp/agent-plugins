# Tests after activation

Use plus-addresses of the user, subscribed through a double opt-in process with the purchase tag
(tests the bridge) or directly with the action tag.
The user confirms the opt-in mails and fills the survey in a **private window** (the survey owner
cannot rate). Skip waits only with the user's consent: `get-contact-automation-status` →
`move-contact-past-automation-wait` (preview first, then `confirm`).

Give test contacts only the **purchase tag**; that tests the bridge too.

| Contact | Action | Expected |
|---|---|---|
| A | rate 5 stars right after the request (do not skip the wait) | goal fires inside the wait → thank-you → exit, no reminder |
| B | only open the survey; after the reminder rate 2 stars | reminder at once; goal fires inside the upper bound → improvement → exit |
| C | do nothing | reminder one day later → after the upper bound end without mail |
| A again | purchase tag again | no start, no mail |
| C again | purchase tag again (≥ 5 min after its end) | restart → new request |
| G | Gmail/Googlemail address (only if the Google branch stays): click "Jetzt auf Google bewerten" in the Google request | Google request, no ProvenExpert mail; after the 2-day wait exit, no reminder |
| G2 | second Gmail address: do nothing | Google reminder after 2 days → end 3 days later |

Check smart tags with `search-contacts` (`tagId` = smart tag) and the path with
`get-contact-history`. Ratings arrive within a minute; the campaign queue may take a few minutes.
Open one received mail's plain text: the survey link must be there (missing if it sits in a button
block). The survey link is a redirect, not a tracked mail link: opening it sets no "geklickt" tag —
judge by the smart tags, not by the mail's click statistics. The Google link is a normal tracked
link: its click sets the mail's "geklickt" smart tag, which the Google branch checks.
