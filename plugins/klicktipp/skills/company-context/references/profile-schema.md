# Portable company profile

Use this structure when a profile must be compared, persisted, migrated or returned as a portable `company-profile.md`. Omit empty optional values instead of inventing them. Keep personal preferences and task overrides outside `company_profile`.

```yaml
profile_version: 1
scope:
  company_key: ""
  public_brand: ""
  klicktipp_account_id: ""
  primary_domain: ""
  verified_sending_domains: []
  account_profile_business_relation: "same_business | partial_overlap | different_business | unknown | not_available"
  account_profile_usage: "approved | field_limited | declined | not_available"
  account_profile_approved_fields: []
profile_status: "candidate | confirmed | conflicted | stale"
confirmed_at: ""
sources:
  - type: "user | website | imprint | privacy_page | file | project_context | memory | klicktipp_account | klicktipp_user_profile"
    reference: ""
    retrieved_at: ""
    note: ""

company_profile:
  identity:
    public_name: ""
    legal_name: ""
    website: ""
    imprint_url: ""
    privacy_url: ""
    address: ""
    contact_options: []
  goals_with_klicktipp: ""
  audiences: []
  offers: []
  brand_voice: ""
  corporate_identity: ""
  email_design:
    status: "unset | candidate | confirmed | stale"
    source_type: "website | existing_email | klicktipp_template | external_example | user_description | delegated_proposal | mixed | unset"
    source_reference: ""
    applies_to_sending_domains: []
    template_reference: ""
    colors: []
    font_preferences: []
    layout_and_spacing: ""
    imagery: ""
    footer: ""
  default_language: ""
  default_addressing: "du | sie | situational | unset"
  writing_rules_and_boundaries: ""
  prohibited_or_sensitive_claims: []
  approved_proof_points: []

field_evidence:
  field_path:
    state: "candidate | confirmed | conflict | stale | missing | declined"
    source: ""
    retrieved_at: ""
    confirmed_at: ""

unknowns: []
conflicts: []
```

## KlickTipp field projection

Return these six user-facing fields whenever a reusable KlickTipp company profile is read, completed, compared, persisted or exported. These labels and paths describe the skill projection. Do not present them as verified API keys or enum values.

| KlickTipp profile field | Portable source | Projection rule |
| --- | --- | --- |
| Homepage or company domain | `company_profile.identity.website`, `scope.primary_domain` | Return the confirmed value selected for this field and keep any other mapping separately. A sending, technical or freemail domain is only a candidate. |
| Goals with KlickTipp | `company_profile.goals_with_klicktipp` | Keep the user's confirmed goals. Do not turn Trust-Economy guidance into a goal automatically. |
| Audiences, offers and brand voice | `company_profile.audiences`, `offers`, `brand_voice` | Combine the confirmed structured values into one clear long-text field without adding claims. |
| Assistant content language | `company_profile.default_language` | Preserve the account-language selection as a dynamic choice when selected. Report the resolved language separately when it is available. |
| Addressing in German content | `company_profile.default_addressing` | Use `du`, `sie` or `situational`. This field applies only to German content. Treat `du` as an editable candidate until confirmed or read from storage. |
| Writing rules and taboos | `company_profile.writing_rules_and_boundaries`, `prohibited_or_sensitive_claims` | Combine confirmed rules and prohibitions without weakening either one. |

For every field, return its value, evidence state, source and persistence status. Existing stored values take precedence over defaults. A default is not a confirmed answer. If reusable profile creation was skipped, return `skipped_by_user` instead of forcing values. If no verified company-profile write and readback path exists, use `persistenceStatus: write_unavailable`.

## Scope rules

1. `company_key` and `public_brand` distinguish agencies, legal entities and multiple brands.
2. `klicktipp_account_id` is required only when the profile is used for account-specific work.
3. `primary_domain` is the confirmed company-website domain, not an inferred sending domain.
4. One KlickTipp account may have several company profiles, and one profile may map to several `verified_sending_domains`.
5. A verified sending domain proves neither company identity nor website ownership. Store a domain mapping only after confirmation.
6. Use account-profile fields only when `account_profile_usage` permits them. When it is `field_limited`, list every approved field in `account_profile_approved_fields`.
7. `email_design` belongs to the company or brand profile. `applies_to_sending_domains` narrows reuse but does not make a sending domain the profile owner.
8. Website design signals and delegated proposals remain candidates until confirmed. A task-specific design is not persisted without separate approval.
9. Add a domain-specific design only when the customer confirms that the domain intentionally differs from the brand default.
10. A task override may replace audience, offer, language, addressing, tone, design and task-level writing rules.
11. A task override does not replace legal identity, sender identity, consent scope or unverified factual claims.
12. `default_language` may begin as a candidate from the product language.
13. `default_addressing` may be suggested as `du`, but stays `unset` or `candidate` until confirmed.
14. Trust-Economy principles belong in confirmed writing guidance, not automatically in `goals_with_klicktipp`.
15. The six-field KlickTipp projection is the storage and handback view. The structured portable fields remain the detailed source and must not contradict that projection.
