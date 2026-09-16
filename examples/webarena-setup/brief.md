# Representation contract

**Figure type:** benchmark / environment setup. WebArena introduces a benchmark and a self-hosted environment, so the third mode applies. A paper merely evaluating an agent on WebArena would not automatically warrant a separate environment figure; its manuscript would need a substantive setup explanation.

**Visual thesis:** a language goal is grounded in actions on working websites, and success is tested against the resulting website state. The environment is distinct from the tested agent and from the evaluator.

**Target size:** 7 × 4.75 inches. Main explanatory text is 8–9.4 pt; supplementary annotation is 7.5–8 pt. There is no target manuscript page, so final venue fit remains unverified.

## Source-backed task contract

- Version: WebArena task definitions at `v0.2.0`; task ID 601; repository file blob `91e88d7c3bce867b7f7608c8229c84b7be11ef1e`.
- Intent, paraphrased: ask an appropriate forum whether having a car is necessary in New York City. The exact question string is preserved in the schematic input and posted state.
- Initial configuration: the Reddit-like site, authenticated user storage state, and the site's start URL. The configuration says `require_reset: false`. The figure starts **after** navigation and typing; it does not depict the complete episode or its initial page.
- Observation interface: page URL, open tabs, and focused-page content represented as screenshot, HTML, or accessibility tree. The paper's original baseline uses accessibility identifiers. Our page rendering is a semantic sketch, with invented target `[42]` demonstrating an accessibility target. It is not evidence that the original site had that identifier or that screenshot-only agents receive accessibility IDs.
- Allowed actions include click, type, hover, scrolling, key presses, navigation, and tab operations. The single illustrated click is a teaching example, not the only supported action type or a reference path that agents must follow.
- Termination: the baseline action language has `stop[answer]`; a task can be answered or its requested website change completed. The figure depicts evaluation at completion. It omits the stop action for space. It does not impose the original baseline's 30-step budget as an environment property.
- Exact evaluator types for this task: `url_match` and `program_html`. The reference URL is the forum `/f/nyc`; `url_note` is `GOLD in PRED`. The HTML evaluator resolves the resulting post URL using `reddit_get_post_url('__last_url__')`, reads `.submission__inner` text, and requires the requested question to appear.
- Access boundary: the goal and observations belong to the agent's task context. Reference evaluation targets/checks belong to evaluation configuration. Website content itself is not globally hidden; some of the same content can also be visible through the browser. The figure does not expose the reference checks to the agent or connect success signals back into a policy update.
- General benchmark context: WebArena has four website categories plus utilities/reference sites. The figure uses one forum task, not a benchmark coverage analysis, task split, or aggregate score plot.

## Visual mapping

| Object / relationship | Encoding | Meaning |
|---|---|---|
| Hosted world | Four concise site cards with domain-specific line glyphs | Site inventory; highlighted forum is used by this example |
| User intent | Full-width blue goal strip | Public natural-language instruction |
| Observation at one moment | Forum composer with meaningful question text | The agent has already navigated and typed |
| Agent | One compact neutral agent block | A replaceable system under evaluation, no model internals |
| Action | `click [42]`, highlighted Post target and outgoing arrow | Illustrative permitted interaction |
| State transition | Same forum and text, now presented as a submission | A write action changes the website |
| Feedback | Teal perimeter return arrow | Updated observation returns to the same agent |
| Evaluator | Separate ochre lane with two explicit criteria | Functional task completion, not action-sequence imitation |
| Success | Conditional label, “if both checks pass” | Definition; no measured success outcome |

**Invariants:** same question, forum and agent across the illustrated transition. Colors communicate environment/interaction versus evaluation, with labels and layout providing redundant cues.

**What changes visibly:** an editable field and Post control become a published submission. This is the reason to draw the interface rather than write “environment” in a box.

**Reading path:** world → public goal → current page / agent / changed page → new observation → evaluator criteria. The explicit numbered panels distinguish context, one interaction, and scoring.

**Detail boundary:** browser chrome, body text, identity, site styling, intermediate navigation, login sequence and full evaluator code are omitted. No benchmark totals, train/test split, budget, random seed or learning algorithm is invented. The UI is intentionally a compact schematic and does not claim pixel fidelity to the actual application.

## Composition decision

Three distinct thumbnails are saved. A world strip plus a state transition was chosen because it retains both benchmark context and the action's visible consequence. A hub-and-spoke agent surrounded by websites better conveys breadth but hides what interaction changes. Three abstract role lanes clarify access boundaries but would either obscure the concrete page or demand more space. The final combines the first option's main composition with a separate evaluation lane.

## Reference inspection

The official `media/overview.png` was viewed at full resolution through its base64 image data. It clearly separates the hosted world, language intents, interaction cycle and functional evaluation, and uses recognizable website/tool objects. The new figure borrows those explanatory relationships while adding a concrete state transition and task-specific checks. The drawing, layout, icons and interface are original; no author image is embedded or redistributed.
