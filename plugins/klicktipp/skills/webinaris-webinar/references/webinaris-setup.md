# Webinaris setup

Values for the template. `<P>` is the prefix chosen at import plus the template's own prefix, e.g. `Webinar Masterclass | Webinaris |`. Use the
names the import actually created — read them back from the import answer, never from memory.

## Two ways to run it

**Guided (default).** Tell the user plainly that you cannot open Webinaris. One screen per message:
where to click, what to set, then ask for an "ok" or a screenshot (in the user's language). Check the
screenshot against the table below before moving on.

**Browser extension.** Read every screen first. Then present one list:

| Screen | Setting | now | new |
|---|---|---|---|
| Webinar-Details | Webinarraum schließen | 10 | 15 |
| … | … | … | … |

After the user's "ok", apply exactly that list, save each screen, read it back, report. Changes not
on the list need a new "ok". The user types the KlickTipp password in the plugin dialog themself.

## Steps (in this order)

1. **Webinar** — Auto Webinare → "Neues Auto-Webinar" → *Von vorne beginnen* / *Bestehendes Webinar
   klonen* / *Webinar aus anderem Account kopieren*. A clone already has plugin, tags and fields:
   go through the steps anyway and compare.
2. **Termine** — 3/5/7 automatic or "Ich lege die Termine selbst an" (own dates only on a 15-minute
   grid, optional spontaneous slots). Any choice works with the campaign.
3. **E-Mails** — every mail comes from KlickTipp.
   - E-Mails → Einstellungen → Double Opt-In: **Nein** (default in a new webinar: "Ja, immer").
     After switching it off, the Webinaris DOI mail disappears from the list.
   - E-Mails → E-Mails: a new webinar brings its own mails (access data, reminders, re-invite,
     sales). Webinaris has **no "deactivate"** — only edit, clone, delete. Deleting is irreversible:
     list them and get an explicit ok before deleting each.
4. **Experten-Einstellungen → Webinar-Details**
   - Teilnahme-Status: **10 %** (who watched ≥ 10 % counts as attended)
   - Startverzögerung: **Nein**
   - Webinarraum schließen: **15** minutes (rule 3 in SKILL.md)
5. **Experten-Einstellungen → Aufzeichnung** — availability fits question 4 (3 or 7 days).
6. **Experten-Einstellungen → Schnittstellen**
   - Double Opt-In (other platform): **Nein** (KlickTipp's opt-in process does the DOI)
   - Erneute Registrierung: **"Schnittstellen-Aufrufe sollen immer nur für die letzte Registrierung
     gesendet werden"** — mandatory
   - Plugin: if a KlickTipp plugin for this account exists, *Plugin auswählen* it. Plugin names do
     not show the account; after selecting, the plugin editor's opt-in list shows that account's
     processes — that confirms the right account. Otherwise
     "Plugin hinzufügen" → "+ Neues Plugin erstellen" → "Klick-Tipp" → name, KlickTipp user name,
     password (user types it) → "Plugin erstellen".
7. **Plugin bearbeiten** (three-dot menu → Bearbeiten)
   - Opt-in-Prozess: the one from question 6.
   - The KlickTipp field dropdown has no search and loads lazily: newly created fields appear only
     after scrolling to the **end** of the list. Do not ask the user to re-save the plugin.
   - Data fields (KlickTipp field ← Webinaris content):

     | KlickTipp field | Webinaris content | type |
     |---|---|---|
     | `<P> Webinar Datum` | Webinaris_Webinardatum | Zeile |
     | `<P> Webinar Uhrzeit` | Webinaris_Webinarzeit | Zeile |
     | `<P> Webinar Link` | Webinaris_Webinarlink | Zeile |
     | `<P> Webinar Termin` | Webinaris_UNIXTimestamp | **Datum & Zeit** |
     | `<P> Webinar Aufzeichnung Link` | Webinaris_7-Tage-Aufzeichnung-mit-Pausieren-und-Spulen (or the variant from question 4) | Zeile |
     | Vorname / Nachname | first / last name | — |

   - Tags (tag · time · audience):

     | Tag | Zeit und Einstellungen | Für wen |
     |---|---|---|
     | `<P> Angemeldet` | Sofort bei der Registrierung | Alle Personen |
     | `<P> Nicht im Raum nach Start` | Nach dem Webinar-Start · 00:05:00 (= N) | Nur Personen, die zum gewählten Zeitpunkt nicht im Webinarraum online sind |
     | `<P> Teilgenommen` | Nach dem Webinar-Ende · 00:01:00 | Nur Teilnehmer |
     | `<P> Nicht teilgenommen` | Nach dem Webinar-Ende · 00:01:00 | Nur Nicht-Teilnehmer |

     No reminder tags: the campaign computes reminders from the date field.
8. **Speichern**, then read the plugin back.
9. **Test date** — own dates only on a 15-minute grid; choose one ≥ 30 min ahead so the
   15-min reminder is testable. The form also lists spontaneous slots: tell the user to pick the
   test date explicitly.

## After the setup

- Compare N and R with the campaign (SKILL.md alignment rules). If the user picked other values,
  change the campaign's LIVE-CHECK wait and the "ZU SPÄT FÜR LIVE" decision accordingly.
- Several webinars at the same time → one set of tags and one campaign per webinar (own prefix).
