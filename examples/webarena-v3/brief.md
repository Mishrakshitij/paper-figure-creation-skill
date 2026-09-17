# Figure brief

**Type:** benchmark/environment setup. The original WebArena paper introduces a substantive environment and benchmark; the conditional third mode therefore applies.

**Visual thesis:** an agent's web action changes a working website, and task success depends on the resulting URL and post content.

**Source invariant:** exactly the same task 601 source and scientific scope as `../webarena-setup/`: task definitions at `v0.2.0`, blob `91e88d7c3bce867b7f7608c8229c84b7be11ef1e`, interpreted with the WebArena v4 paper. No new experiment, target, observation interface, evaluator or success claim is introduced.

**Target placement:** 7 × 4.95 inches; 8.5–10.4 pt explanatory text, 14 pt title. The larger height accommodates a recognizable interface, visible state change and explicit evaluator boundary. A manuscript page was not supplied.

## Source contract

The public natural-language goal asks an appropriate forum whether a car is necessary in New York City. The exact required question is `is car necessary in NYC`. The depicted step starts after navigation and text entry; it is not the initial browser state or the full episode. The task starts with an authenticated Reddit-like website and has `require_reset: false`.

WebArena observations include URL and open tabs, plus screenshot, HTML or accessibility-tree content. The original baseline uses accessibility identifiers. The schematic `click [42]` refers to an invented accessibility target; screenshot-only observations are not implied to contain these IDs. Other supported actions include typing, hover, scrolling, key presses, navigation and tab operations. The baseline language supports `stop[answer]`; this drawing omits that action and any budget.

Task 601 evaluation uses `url_match` and `program_html`. The reference `/f/nyc` URL must be contained in the predicted URL (`GOLD in PRED`); the evaluator resolves the last post URL, reads `.submission__inner` text and requires the requested question. These are functional checks, not reference-trajectory matching. The source ledger retains the exact locator and post-URL resolver. Evaluation configuration is private; website content is not universally hidden from the agent. The evaluator sends no reward or policy-update arrow to the agent.

## Art direction

| Choice | Purpose | Scientific constraint |
|---|---|---|
| Large forum composer | Establish a recognizable task object at first glance | Original semantic UI; no claim of a real screenshot |
| Smaller foreground published page | Make the changed object explicit while retaining the same URL and question | Schematic consequence, not a logged execution |
| Restrained local shadow and overlap | Separate two snapshots and establish visual focus | No additional causal or physical meaning |
| Saturated Post target and cursor | Locate the illustrated action | Target 42 is invented and disclosed |
| Compact replaceable agent | Explain observation/action interfaces | No model architecture or learning mechanism implied |
| Teal returning arrow | Show the new observation | No evaluator feedback enters this edge |
| Separate ochre checks at the bottom | Explain what counts as task completion | Conditional success only; no measured result |

Three layouts were sketched first. The foreground-state composition was chosen because the same question remains identifiable across a visible interface change. The horizontal-strip alternative distributed emphasis evenly across the agent and both pages. Role lanes made the access boundary explicit but did not make the changing task object visually prominent.

The original source figure's four website categories and tools remain benchmark context in the caption; they are not drawn as a competing row of cards. A setup figure can illustrate one faithful task without pretending it is the entire benchmark's coverage. No website is represented as a physical city, and no decorative robot is introduced.

## Required reader reconstruction

The reader should recover: the user goal; a web agent's observation and click; the same question becoming a post; the changed page returning as observation; the final URL and DOM entering two private reference checks; and success being conditional on both checks. Reading the main figure alone should not imply an observed successful run.
