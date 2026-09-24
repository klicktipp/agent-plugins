# Eigenes HTML (`html`)

Roher HTML-Code, den der Editor unverändert durchreicht. Der Ausweg für das, was kein anderer Baustein kann — und der Baustein, den ein Empfängerpostfach am ehesten anders darstellt, als du erwartest.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-html`.

## Werkzeuge

| Anlegen | `add-email-editor-html` |
| --- | --- |
| Ändern | `update-email-editor-text` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.html.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Der Inhalt ist Markup, das der Editor unverändert durchreicht. Beim HTML-Import überlebt der *gerenderte* Inhalt, der Code-Baustein selbst nicht.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Kommt als das Markup zurück, zu dem es rendert; der Code-Baustein ist weg.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
