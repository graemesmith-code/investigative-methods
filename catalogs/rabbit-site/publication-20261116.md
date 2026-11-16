# Rabbit on graemesmith.com

Rabbit is published at [graemesmith.com/rabbit/](https://graemesmith.com/rabbit/), linked from a new “Recent projects” section of Graeme’s bio. The bio uses the supplied two-sentence text, with only “sources” linked, and reuses the Selected work heading and hairline styling.

The page embeds the existing live Rabbit application. It does not copy the catalog: approved changes continue to appear in one shared source of truth. A small link returns to the bio; another opens Rabbit on its own.

Visitors can browse and download the approved catalog and change log without signing in. Submitting suggestions, reading private submissions and saving reviews still require authenticated identity. Only the curator can approve changes.

The practical point is that a public catalog needs to open when someone follows the link. Private notes and pending submissions do not need to open with it.

## Technical annex

The bio site remains on GitHub Pages. Its new `rabbit/index.html` loads the existing Sites origin in a full-height frame and advertises public catalog JSON and agent documentation. Authentication links use top-level navigation, as required by Sites. No domain or DNS change is required.

Rabbit’s public GET routes expose only the catalog and published changes. Anonymous contribution-list reads return an empty list with `authenticated: false`; they do not query private submissions. Workspace requests still require a signed-in user. Contribution POST and curator approval checks remain unchanged. Model Context Protocol calls continue to require authentication; public machine readers can use the documented catalog JSON and change-log URLs.

The development-only preview identity remains gated by the build’s DEV flag. No runtime identity bypass, embedded token, anonymous writer or new approval tool has been added. Existing workflow, caller-isolation, agent and patent-release tests passed (56 checks). The following checks were completed after publication.

## Publication and verification

- Bio repository: `graemesmith-code/graemesmith.github.io`, main branch. Rabbit page commit `071ddd11be60c2912bb2d0c7fb362ff4afc14466`; bio section commit `8fe6b8c2e90909e890372854c3adfe108033711e`.
- Rabbit public-reading implementation: `5750cdd2fc5fa7c01ca0bb630489ef27ad564d8b`. Public-access documentation revision: `b8141420ad5d86168b685635e1bcf879d813f9fd`.
- The Sites access policy was changed from owner-only to public for this requested publication. Application-level private workspace and curator checks remain enforced.
- Live browser verification confirmed the new section and its exact text at https://graemesmith.com/, then followed “sources” to https://graemesmith.com/rabbit/ and observed the fully loaded Rabbit catalog without sign-in.
- Computed styles for both headings match: 22.4px, weight 600, same serif family. Both dividers are 1px solid rgba(0,0,0,0.15), with matching spacing. The body contains exactly one link, on “sources”.
- A 390-pixel preview frame confirmed the bio layout without horizontal overflow (375 pixels of usable content after the scrollbar). The embedded catalog also loaded at that width. This is a responsive-layout check, not a physical-phone test.
- Public search returned the approved EPO source. The contribution page showed the sign-in link and no editable submission form. An anonymous browser request to /api/contributions returned `{"authenticated":false,"can_review":false,"proposals":[]}`; /api/workspace returned `{"error":"Sign in to load your saved reviews."}`.
- The command-line HTTP client received HTTP 403 with error code 1010 from the hosting edge. Its attempted endpoint checks did not reach the application and are not counted as passed. Anonymous browser checks succeeded. No test submission was added to production.
- Type checking, production build and 56 existing workflow, caller-isolation, agent and patent-release checks passed. The existing weekly curator email schedule was not changed.

The bio and Rabbit are now connected without maintaining a second catalog. The remaining integration limit is the embedded app’s dependency on its existing Sites host; its direct-open link provides an alternative to the embedded view, not an independent fallback host.
