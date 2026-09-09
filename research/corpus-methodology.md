# Research corpus: scope and provenance

This directory contains a **500-paper candidate corpus**, not a claim that 500 papers were selected as the best figures or visually reviewed. The records come from official ICML/PMLR, NeurIPS, and ECCV/ECVA proceedings. There are 100 papers per venue/year stratum: ICML 2021, 2022, 2023; ECCV 2024; NeurIPS 2023.

Selection used bounded proceedings windows followed by a broad title keyword preference for model, representation, architecture, generative, empirical, and learning papers. This is a convenience sample with author-order and availability bias, not a representative random sample or award-ranked sample. Acceptance in these venues does not itself establish figure quality. Award status is not checked in this broad corpus.

Evidence levels are kept separate:

- `metadata_catalogued`: title, authors, venue and year were available in the official proceedings.
- `pdf_text_retrieved`: a bounded PDF text window was read by the browser; this does not mean the full paper was read.
- `caption_candidates_extracted`: automated rules found caption-like text, figure numbers and PDF pages. Captions can contain extraction artifacts and false positives.
- `analyst_caption_reviewed`: an agent read the caption excerpts and considered their semantic role; this is still not visual inspection.
- `visual_reviewed`: rendered figure pixels were inspected. Broad-corpus records default to false; the separate curated visual study records its own actual visual coverage.

The manifest records observed coverage. Missing captions mean none were found in the retrieved windows, not that the paper contains no figures. The paper-title check is a token-overlap sanity check, not an identity proof.

Public files include bibliographic facts, original URLs, short caption excerpts (at most 22 words per paper), extraction status, and our own synthesis. Original paper PDFs and full extracted text are not redistributed. To reproduce the extraction in an environment with ordinary network access, use `screen_corpus.py`; keep its PDF cache outside version control.

The requested approximately 35% concept/example + 65% experimental-evidence teaser layout is an editorial default chosen for this skill. It is **not** an estimated frequency or a universal optimum inferred from the corpus.

Browser retrieval in this build encountered unsupported large PDFs and link-resolution limits in long proceedings indexes. Exact-title primary-site searches recovered canonical PDF URLs; PDF title tokens were checked against the catalogued title. The local script uses the canonical URLs directly and can retrieve more content than the browser windows.
