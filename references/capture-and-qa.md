# Complete capture and evidence checks

## Capture

Navigate the actual running app by clicking its visible controls, in the journey's real order. After every action, verify the reached UI before saving its screenshot and proceeding. Do not substitute generated HTML, a reconstructed page or an isolated component harness, and do not force state through response interception, DOM/component assignment, direct API calls or guessed deep links. Opening the app's normal entry URL is allowed; skipping required intermediate actions is not.

If the required screen or record does not exist, access is unavailable, or a step cannot pass, ask the user to help with that specific blocker. A screenshot request does not authorize changing business data/configuration to make the flow pass. Keep the last genuine state, continue unrelated captures, and resume only after the missing input or manual action is supplied. If a user handoff leaves intermediate steps uncaptured, identify that gap and ask for help capturing it; do not draw an unexplained success transition.

Use the available authorized browser tooling. If using Playwright, prefer an isolated context with consistent viewport, e.g. 430 × 932 CSS pixels and DPR 2. The approved reference used 860-pixel-wide output. Wait for fonts, images, async UI and transitions to settle. Set scroll to the top, then capture the complete document (`fullPage: true`, animations disabled where supported).

A fullPage flag is not proof of completeness: inspect document and nested-scroll heights. A fixed-height inner scroller may hide content from a document screenshot. Capture its complete contents or sequential overlapping views with clearly labeled same-screen continuations, ensuring no content is missing. Do not alter business UI layout to make it fit. Expand relevant accordion sections and capture differing states where mutually exclusive. Preserve the displayed footer and actions.

Store each screenshot with a manifest: unique ID, file, flow/step, UI state, capture method, viewport/DPR, document/content height, capture dimensions, visible-text assertions and whether data is illustrative. Record the preceding action and source step so the capture can be traced to an actual click or a disclosed user handoff. For ordinary full document captures, check pixels cover the content height at the capture DPR. For modal screenshots, record the exception and identify the paired full underlying screen.

An already implemented app test/mock mode may be used when authorized by the user and operated through its real UI. Preserve its visible mock notices and disclose illustrative values. Never add fixtures or intercept responses to fill missing screenshots. Follow the popup's real destination and distinguish displayed mock rewards from actual ticket/prize records; if they differ or the required record is absent, ask the user for help instead of inventing the next screen.

## Verify state before capture

- Wait for reactive watchers to settle; they may reset progress visibility, selection or validation.
- Trigger the actual form validation through its controls and inspect the visible message; never assign error strings or component state to manufacture the screenshot.
- Capture loading/retry/error states only when the real application reaches them. If the required state cannot be reached, ask the user for help rather than manufacturing it.
- Check amount units and totals. The reference app mixed cents in shared order state with RM amounts in quote state; this is a historical pitfall, not a rule for other projects.
- Trace button destinations. In the approved Pacific app, completion popup Continue returned to the receipt, then View status opened policy progress. Do not label a shortcut that the UI does not perform.
- Represent only implemented states. If external FIUU/bank pages are absent, explicitly mark that transition as external/not captured rather than generating a fake screen.

## Final acceptance

1. Each flow starts a new page and occupies no more than two consecutive pages; two-page continuations reference the correct page and step.
2. Every screenshot is legible, proportional and includes all scroll content. Compare top AND bottom and inspect long screens at enlarged scale. No frame covers pixels.
3. Step numbers, titles and captions agree with actual visible UI and available actions. Required-field and error screens visibly contain their error text.
4. Every next step has a red connector. Branches say what condition triggers them; retry routes have an unambiguous destination. Arrows do not cross UI text/screens or disappear behind labels.
5. Payment pending, payment confirmed, issuance pending and policy completed remain distinct. Check all document claims against the evidence.
6. Headings, captions, footnotes and arrow labels do not overlap or clip. No phone image touches the footer. Renderer bounds checks help but do not replace visual inspection.
7. Render all pages after the LAST change and inspect them. A contact sheet helps overview, but individual pages and enlarged long screens are necessary for completeness/readability.
8. Keep the source manifest, captures and build script accessible with the artifact. Deliver counts and genuine limitations, not an unsupported declaration of successful insurer UAT.
9. Every claimed transition is supported by an observed UI action or a disclosed user handoff. Missing or blocked steps require a concrete request for user help; a partial screenshot set must not be described as the complete flow.

Original reference provenance: user supplied MY CAR PLUS discussion PDF and then approved the Pacific Auto adaptation on 2026-10-01. The bundled approved PDF contains illustrative local UI scenarios; its historical placeholder text and prices are not new product requirements.
