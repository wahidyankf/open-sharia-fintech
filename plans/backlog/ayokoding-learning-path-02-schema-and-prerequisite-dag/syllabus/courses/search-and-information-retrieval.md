# Search and Information Retrieval (By Example, Python)

**Course ID**: `search-and-information-retrieval` · **Format**: By Example · **Language**: Python.

**Short summary**: Inverted indexes, ranking, full-text search

**Scope note**: making text findable, taught in three tiers — a raw inverted index by hand →
a real engine (tokenization, TF-IDF/BM25, ranking) → building a small index yourself — with the
relevance-vs-recall trade-off in the foreground. The vanilla tier grounds the intuition, the
practical tier shows what a production engine (Lucene/Elasticsearch/OpenSearch family) actually
does, and the build-your-own tier makes the machinery concrete. `†`: Python, fully type-annotated
(DD-39) — every snippet carries type hints in the pyright-clean spirit.

## Why this exists · the big idea

- **The problem before the solution**: a `LIKE '%term%'` scan finds substrings, not documents — it
  can't rank, can't handle "roughly this", and gets slower with every row. Users don't want the rows
  that _contain_ a word; they want the handful that are _about_ it, best-first, in milliseconds.
- **Keep-this-if-you-forget-everything**: search inverts the problem — instead of scanning documents
  for a query, you build a term → documents map once (the inverted index) and let the query do a
  cheap lookup, then _rank_ the hits by a relevance score. Index-then-rank is the whole game.
- **Big ideas touched**: `abstraction-and-its-cost` (a search engine hides tokenization, scoring, and
  merge logic behind one `search()` call — and the hidden analyzer choices leak straight into which
  documents you can ever find), `consistency-latency-throughput` (ranking quality, index freshness,
  and query latency trade against each other — a better score costs CPU, a fresher index costs write
  throughput).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./sql-essentials.md) (the row-scan baseline search
  improves on) and [topic 7 Data Structures & Algorithms Essentials](./data-structures-and-algorithms-essentials.md)
  (hash maps, sorted postings, heaps for top-k).
- **Tools & environment**: a macOS/Linux terminal; **Python** at a recent stable release with type
  hints and `pyright`; a small text corpus (a docs folder or a public dataset dump); optionally a local
  search engine from the Lucene family (Elasticsearch/OpenSearch) via a container for the practical
  tier; Neovim/VSCode with the Python LSP (DD-17).
- **Assumed knowledge**: writing and querying a table (topic 10); dictionaries, sets, and sorting
  by a key (topic 07); reading a file line by line from Python (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: BM25 (Okapi BM25) remains the default lexical ranking function across the
  Lucene family and is left correctly version-unpinned — the formula and its `k1`/`b` parameters are
  stable and standard. TF-IDF as the teaching stepping-stone to BM25 is unchanged.
- 2026-07-12 — verified (GAP for plan owner): the practical tier names the Lucene/Elasticsearch/
  OpenSearch family generically on purpose — pin a concrete engine + version only at drafting time,
  since the licensing split (Elastic vs the OpenSearch fork) and default analyzers shift between
  releases. The vanilla and build-your-own tiers are engine-independent and stable.

> DD-35 primary-source pass (2026-07-12). Every citation below traces to a source the author fetched
> and read; unverifiable specifics are flagged `[Needs Verification]`, never guessed. When authoring
> `learning/code/`, keep these exact.

- **Inverted index, boolean merge, postings** — term → dictionary + postings; postings sorted by
  docID; AND/OR/NOT = intersection/union/difference of sorted posting lists. Source: Manning,
  Raghavan & Schütze, _Introduction to Information Retrieval_ (Cambridge UP, 2008),
  [ch. 1 "A first take at building an inverted index"](https://nlp.stanford.edu/IR-book/html/htmledition/a-first-take-at-building-an-inverted-index-1.html).
- **Skip pointers** — √P evenly-spaced skips speed AND-intersection; "the presence of skip pointers
  only helps for AND queries, not for OR queries" (verbatim). Source: IR-book,
  [Faster postings list intersection via skip pointers](https://nlp.stanford.edu/IR-book/html/htmledition/faster-postings-list-intersection-via-skip-pointers-1.html).
- **Porter stemmer** — M.F. Porter, "An algorithm for suffix stripping," _Program_ 14(3):130–137,
  **1980** (algorithm written 1979/1980). Source: author's own page,
  <https://tartarus.org/martin/PorterStemmer/>. Teach it as **1980**. Stemming raises recall while
  harming precision (IR-book ch. 2, [02voc.pdf](https://nlp.stanford.edu/IR-book/pdf/02voc.pdf)).
- **idf / tf-idf** — exact forms `idf_t = log(N / df_t)` and `tf-idf = tf × idf` (IR-book,
  [tf-idf weighting](https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-weighting-1.html)).
- **BM25 exact formula** — Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and
  Beyond," _Foundations and Trends in IR_ 3(4):333–389, **2009**, DOI
  [10.1561/1500000019](https://doi.org/10.1561/1500000019). Term weight (eqs. 3.12–3.15, read from
  the PDF): `B = (1 − b) + b·(dl/avdl)`; `score_i = tf / (k1·B + tf) · idf_RSJ`, with RSJ idf
  `log((N − n_i + 0.5)/(n_i + 0.5))`. Saturation via `k1`, length-norm via `b`.
- **BM25 defaults — split fact `[Verified]`**: `k1 = 1.2, b = 0.75` are the **software** defaults
  (Lucene/Elasticsearch;
  [Lucene `BM25Similarity` Javadoc](https://lucene.apache.org/core/9_11_0/core/org/apache/lucene/search/similarities/BM25Similarity.html)),
  **distinct from** the paper's own recommended experimental range `1.2 < k1 < 2, 0.5 < b < 0.8`.
  Do not conflate. Lucene's idf is the `log(1 + (N − df + 0.5)/(df + 0.5))` variant (+1 inside the
  log avoids negative idf) — a real, small divergence from the paper's raw RSJ idf worth a footnote.
- **Precision / recall direction** — `Precision = |rel ∩ ret| / |ret|` (denominator = retrieved),
  `Recall = |rel ∩ ret| / |rel|` (denominator = relevant); F1 = harmonic mean. Source: IR-book
  ch. 8 (Evaluation), eqs. 8.1–8.4, read from the PDF. MAP and nDCG per the same chapter.
- **Vector space / cosine** — docs as term-weight vectors, cosine = length-normalized dot product
  (IR-book §6.3).
- **Analyzer pipeline** — char filters → **one** tokenizer → token filters, in order (Elastic docs,
  [Anatomy of an analyzer](https://www.elastic.co/docs/manage-data/data-store/text-analysis/anatomy-of-an-analyzer)).
- **BM25 as Lucene default since Lucene 6** — LUCENE-6789 changed `IndexSearcher`'s default
  similarity to `BM25Similarity` in **Lucene 6.0.0**; the "April 2016" calendar date is
  `[Needs Verification]` (Maven timestamp, not an Apache-authored dated changelog) — cite the
  version, not the day.
- **Segments + near-real-time** — Lucene writes immutable segments merged over time; a "refresh"
  opens a new segment (~1 s default), hence _near_-real-time (Elastic
  [Near real-time search](https://www.elastic.co/docs/manage-data/data-store/near-real-time-search)).
  The exact `MergePolicy`/segment-file wording is `[Needs Verification]` (reached via search summary,
  not a direct fetch) — the immutability + merge architecture is uncontroversial.
- **Positional index / phrase** — postings carry token positions; phrase/proximity match checks
  compatible positions; biword indexes cannot do proximity (IR-book,
  [Positional postings and phrase queries](https://nlp.stanford.edu/IR-book/html/htmledition/positional-postings-and-phrase-queries-1.html)).
- **BM25F** — combine per-term tf **across fields/streams first** (weighted), then saturate once;
  naive per-field-then-linear-combine breaks saturation. Source: Robertson & Zaragoza (2009) §3.6.
- **Fuzzy / edit distance** — Levenshtein = min insert/delete/replace; Elasticsearch's fuzzy query
  also allows adjacent-character transposition, which is the **Damerau**-Levenshtein extension (note
  the distinction). Sources: IR-book [Edit distance](https://nlp.stanford.edu/IR-book/html/htmledition/edit-distance-1.html);
  Elastic [Fuzzy query](https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-fuzzy-query).
- **Edge n-grams** — index-time n-grams anchored to word start power search-as-you-type/autocomplete
  (Elastic [Edge n-gram tokenizer](https://www.elastic.co/docs/reference/text-analysis/analysis-edgengram-tokenizer)).
- **Semantic / vector search** — dense-vector kNN with **HNSW** (Malkov & Yashunin, arXiv
  [1603.09320](https://arxiv.org/abs/1603.09320), 2016/2018); Lucene added HNSW-backed vector fields
  in **Lucene 9.0** (Dec 2021); Elasticsearch uses HNSW for kNN (Elastic
  [`dense_vector`](https://www.elastic.co/docs/reference/elasticsearch/mapping-reference/dense-vector)).
  The specific ES `dense_vector`-in-7.3 / native-kNN-in-8.0 versions are `[Needs Verification]`.
- **PageRank** — Brin & Page, "The Anatomy of a Large-Scale Hypertextual Web Search Engine,"
  _Computer Networks_ 30(1–7):107–117, **1998** (7th WWW Conf.); link graph as a content-independent
  ranking signal complementary to term stats. Source:
  [Google Research](https://research.google/pubs/the-anatomy-of-a-large-scale-hypertextual-web-search-engine/).
  The exact recursive PageRank formula was not re-verified from the fetched excerpt — teach the toy
  power-iteration form as illustrative and flag the constant/damping specifics `[Needs Verification]`.
- **Elastic / OpenSearch licensing (month-level only)** — Apache 2.0 → dual SSPL + Elastic License v2
  from Elasticsearch **7.11 (January 2021)** → AWS forks **OpenSearch** from ES 7.10.2 under Apache
  2.0 (**April 2021**) → Elastic adds **AGPLv3** as a third option (**September 2024**). Sources:
  [Elastic license update](https://www.elastic.co/blog/elastic-license-update),
  [AWS Introducing OpenSearch](https://aws.amazon.com/blogs/opensource/introducing-opensearch/). The
  exact January-2021 **day** is `[Needs Verification]` (sources disagree, Jan 14 vs 21) — cite the
  month only.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject topic). Each example below cites the co-NN it exercises. -->

- **co-01 · inverted-index** — a `term → documents` map built once so a query is a cheap lookup, not a per-query scan of every document.
- **co-02 · posting-list** — the per-term list of doc-ids (kept sorted, optionally carrying term-frequency or positions) that the index stores under each term.
- **co-03 · boolean-retrieval** — AND, OR, and NOT queries answered as set intersection, union, and difference over posting lists.
- **co-04 · posting-list-merge** — the linear two-pointer walk that intersects (or unions) two sorted posting lists in one pass.
- **co-05 · skip-pointers** — √P evenly-spaced shortcuts in a posting list that skip non-matching stretches during an AND intersection (they help AND, not OR).
- **co-06 · tokenization** — splitting raw text into indexable terms (whitespace vs regex `\w+`), the first stage every downstream choice depends on.
- **co-07 · case-folding** — lowercasing tokens so `The` and `the` conflate to one index term.
- **co-08 · stop-words** — dropping high-frequency low-signal terms (`the`, `of`) to shrink the index — at the cost of ever finding a stop-word-only phrase.
- **co-09 · stemming** — Porter suffix-stripping (Porter 1980) conflates `running`/`runs`/`ran`-family variants to one stem, raising recall.
- **co-10 · lemmatization** — dictionary-based reduction to a lemma (`better → good`); costlier than stemming with weaker measured gains.
- **co-11 · normalization-recall-tradeoff** — aggressive normalization (stemming, stop-words) raises recall but can lower precision; the analyzer choice decides what is _ever_ findable.
- **co-12 · term-frequency** — `tf`, the raw count of a term in a document, the base signal of relevance.
- **co-13 · inverse-document-frequency** — `idf = log(N / df)`, up-weighting rare terms and discounting common ones.
- **co-14 · tf-idf** — `tf × idf` weighting: the classic per-(term, doc) score and ranking baseline.
- **co-15 · vector-space-cosine** — documents and queries as term-weight vectors, ranked by cosine similarity (length-normalized dot product).
- **co-16 · bm25** — the Okapi BM25 ranking function: saturating `tf`, RSJ `idf`, and length normalization combined (Robertson & Zaragoza 2009).
- **co-17 · bm25-saturation** — the `k1` term caps any single term's contribution so repeated occurrences give diminishing returns (unlike linear tf-idf).
- **co-18 · bm25-length-normalization** — the `b` term normalizes by `dl/avdl` so long documents are not unfairly favoured.
- **co-19 · bm25-defaults** — `k1 = 1.2, b = 0.75` are the Lucene/Elasticsearch _software_ defaults, distinct from the paper's recommended `1.2 < k1 < 2, 0.5 < b < 0.8` range.
- **co-20 · top-k-ranking** — a size-k min-heap returns the k highest-scoring documents without fully sorting the corpus.
- **co-21 · precision-recall** — `precision = |rel ∩ ret| / |ret|` (over retrieved), `recall = |rel ∩ ret| / |rel|` (over relevant); F1 is their harmonic mean.
- **co-22 · precision-at-k** — precision measured over the top-k results, the metric users actually feel.
- **co-23 · relevance-judgments** — a labeled qrels set of (query → relevant docs) that turns "is this better?" from opinion into measurement.
- **co-24 · evaluation-map-ndcg** — Mean Average Precision and normalized Discounted Cumulative Gain for scoring _ranked_ (order- and grade-aware) results.
- **co-25 · analyzer-pipeline** — a Lucene-family analyzer = char filters → one tokenizer → token filters, in order; the same stages you built by hand.
- **co-26 · query-dsl** — a structured query language (must/should/must_not) parsed into a query tree and executed against the index.
- **co-27 · segments-and-merge** — an engine writes immutable segments merged over time; a refresh opens a new segment, giving _near_-real-time search.
- **co-28 · positional-and-phrase** — postings carrying token positions enable exact phrase and within-N-proximity queries.
- **co-29 · incremental-indexing** — adding a document to a built index without a full rebuild, keeping it consistent with a from-scratch index.
- **co-30 · postings-persistence** — serializing the index to disk (JSON, compact binary, delta-encoded doc-ids) and reloading it to query.
- **co-31 · field-weighting-bm25f** — BM25F scores multiple fields (title, body) by combining per-term `tf` across streams _first_, then saturating once.
- **co-32 · fuzzy-edit-distance** — Levenshtein (insert/delete/replace), extended to Damerau (transposition), for typo-tolerant matching and spelling correction.
- **co-33 · ngram-autocomplete** — edge n-grams (prefix) and character n-grams for search-as-you-type and substring matching.
- **co-34 · query-expansion-synonyms** — broadening a query with synonyms/thesaurus terms (`car → {car, automobile}`) to raise recall.
- **co-35 · semantic-vector-search** — dense embedding vectors + approximate nearest neighbour (HNSW), and hybrid lexical+vector ranking, to match meaning not just tokens.
- **co-36 · pagerank-link-analysis** — Brin & Page's link graph as a content-independent ranking signal complementary to term statistics (1998).

## Tensions & trade-offs — when NOT to reach for this

- **A dedicated search engine is a second source of truth**: it must be fed, kept in sync with the
  primary store, and reindexed when the schema or analyzer changes. For a small dataset, Postgres
  full-text search (or even a well-indexed `LIKE`) avoids a whole distributed system you'd otherwise
  operate and reconcile.
- **Lexical search doesn't understand meaning**: BM25 matches tokens, not concepts — "car" won't find
  "automobile". When semantic matching genuinely matters, vector/embedding search is the tool, but it
  adds model, index, and cost; hybrid (lexical + vector) is often right, pure-vector rarely is.
- **Relevance tuning is unbounded**: analyzers, boosts, and score functions can be tuned forever.
  Without a relevance-judgment set to measure against, tuning is guessing — reach for evaluation
  before reaching for another boost.

## Lineage — why it beat the alternative

- Search grew out of library and legal-database retrieval: the inverted index predates the web, and
  the probabilistic ranking work behind BM25 was hardened at the TREC evaluations in the early 1990s.
  Brin and Page's link-analysis (PageRank) then showed that _who points at a document_ ranks web
  pages better than term statistics alone. The lasting winner for text is index-then-rank with BM25,
  because it is cheap, explainable, and strong without training data — which is exactly why the Lucene
  family made it the default. This topic hands its scoring and indexing intuition to
  [topic 39 Backend at Scale](./backend-at-scale.md) (search as a service to operate) and its
  storage mechanics to [topic 91 Build Your Own Database](./build-your-own-database.md).

## Worked examples

Colocated under `search-and-information-retrieval/learning/code/`; each runnable from the CLI, every
Python snippet fully type-annotated and `pyright`-clean (DD-20/DD-30/DD-34/DD-39). Contiguous `ex-01..ex-80`.
Every example cites the `co-NN` it exercises; every concept above is exercised by ≥ 1 example.

### Beginner

- **ex-01 · tokenize-whitespace** — split a document string on whitespace into tokens — verify the token count equals the space-separated word count. (co-06)
- **ex-02 · tokenize-regex** — tokenize with a `\w+` regex that drops punctuation — verify `"end."` and `"end"` yield the same token. (co-06)
- **ex-03 · case-fold** — lowercase every token — verify `"The"` and `"the"` collapse to one index term. (co-07)
- **ex-04 · build-term-doc-map** — build a typed `dict[str, set[int]]` term → doc-id map over 3 docs — verify each term maps to exactly the docs containing it. (co-01)
- **ex-05 · posting-list-sorted** — store each posting list as a sorted `list[int]` — verify doc-ids are strictly ascending. (co-02)
- **ex-06 · boolean-and** — intersect two posting lists for an AND query — verify the result equals Python's `set &`. (co-03, co-04)
- **ex-07 · boolean-or** — union two posting lists for an OR query — verify the result equals `set |`. (co-03, co-04)
- **ex-08 · boolean-not** — compute all-docs minus a posting list for NOT — verify excluded docs are absent. (co-03)
- **ex-09 · merge-two-pointer** — implement a two-pointer linear intersection of sorted lists — verify it matches `set &` on random inputs and is single-pass. (co-04)
- **ex-10 · scan-vs-index-timing** — time a substring `in` scan across N docs vs an index lookup — verify the index lookup's time is flat as N grows while the scan's rises. (co-01)
- **ex-11 · term-frequency-count** — compute `tf` per (term, doc) into a typed dict — verify a repeated term's count is > 1. (co-12)
- **ex-12 · document-frequency** — compute `df`, the number of docs containing each term — verify a term in all docs has `df == N`. (co-13)
- **ex-13 · idf-formula** — compute `idf = log(N / df)` — verify a rare term's idf exceeds a common term's. (co-13)
- **ex-14 · tf-idf-weight** — combine `tf × idf` per (term, doc) — verify the weight matrix matches a hand computation on a 3-doc fixture. (co-14)
- **ex-15 · stop-word-drop** — remove a stop-word list before indexing — verify `"the"` is absent from the index and the term count drops. (co-08)
- **ex-16 · stop-word-recall-risk** — query a phrase of only stop-words after removal — verify it returns nothing, exposing the recall cost. (co-08, co-11)
- **ex-17 · porter-stem** — apply a Porter stemmer to `running`/`runs`/`runner` — verify they share one stem. (co-09)
- **ex-18 · stem-index-shrink** — build the index with stemming on — verify the distinct-term count falls and `"run"` retrieves the `"running"` doc. (co-09, co-11)
- **ex-19 · lemmatize-vs-stem** — lemmatize `"better" → "good"` and contrast with the stemmer's output — verify the lemma differs from the stem. (co-10)
- **ex-20 · normalization-recall-delta** — run the same query with and without stemming — verify hit count rises with stemming (recall up), noting the precision risk. (co-11)
- **ex-21 · posting-with-freq** — store postings as `list[tuple[int, int]]` of (doc-id, tf) — verify each tuple's tf matches the raw count. (co-02, co-12)
- **ex-22 · multi-term-and** — chain pairwise intersections for a 3-term AND — verify the result equals the intersection of all three sets. (co-04)
- **ex-23 · skip-pointer-build** — add √P evenly-spaced skip pointers to a posting-list structure — verify each skip target is ahead of its source. (co-05)
- **ex-24 · skip-pointer-merge** — intersect two lists using skips — verify the result is correct and the comparison count is below the plain merge's. (co-05)
- **ex-25 · rank-by-tfidf** — score docs for a query by summed tf-idf and sort descending — verify the top doc has the highest hand-computed sum. (co-14)
- **ex-26 · vector-space-vectors** — represent two docs as tf-idf vectors (`dict[str, float]`) — verify shared terms appear in both vectors. (co-15)
- **ex-27 · cosine-similarity** — rank docs by cosine of the query vector against each doc vector — verify the ranking matches a hand-computed cosine. (co-15)
- **ex-28 · analyzer-order** — chain tokenize → case-fold → stop-word → stem in one pass — verify the final term set matches the expected fixture. (co-06, co-07, co-08, co-09)

### Intermediate

- **ex-29 · bm25-idf-term** — compute BM25's RSJ idf `log((N − df + 0.5)/(df + 0.5))` — verify it differs from plain `log(N/df)` and stays finite for a term in every doc. (co-16)
- **ex-30 · bm25-score-one-term** — compute the full BM25 term weight with `k1`, `b` on a fixture — verify it matches a hand computation. (co-16)
- **ex-31 · bm25-saturation-curve** — print BM25 score vs `tf` for `k1 = 1.2` — verify each increment adds less, approaching an asymptote. (co-17)
- **ex-32 · tfidf-vs-bm25-saturation** — contrast linear tf-idf against saturating BM25 as `tf` grows — verify tf-idf grows without bound while BM25 flattens. (co-17)
- **ex-33 · bm25-length-norm** — score a short vs a long doc with the same term counts — verify `B = (1 − b) + b·dl/avdl` penalizes the long doc. (co-18)
- **ex-34 · bm25-b-sweep** — sweep `b ∈ {0, 0.5, 0.75, 1}` — verify the ranking of a short vs long doc flips as `b` rises. (co-18)
- **ex-35 · bm25-k1-sweep** — sweep `k1` — verify the saturation point (where extra tf stops helping) moves with `k1`. (co-17)
- **ex-36 · bm25-defaults** — run the ranker with `k1 = 1.2, b = 0.75` — verify the values match Lucene's defaults and note they differ from the paper's recommended range. (co-19)
- **ex-37 · bm25-full-ranker** — rank a corpus for a multi-term query with full BM25 — verify the top result matches a reference BM25 implementation on the fixture. (co-16)
- **ex-38 · topk-heap** — keep a size-k min-heap of scored docs — verify it returns the same top-k as a full sort. (co-20)
- **ex-39 · topk-vs-fullsort-timing** — compare heap top-k vs full sort on a large corpus — verify identical results and lower heap time for small k. (co-20)
- **ex-40 · precision-recall-compute** — from a retrieved set and a relevant set, compute precision and recall — verify against hand values. (co-21)
- **ex-41 · precision-recall-direction** — construct a high-precision/low-recall case and its inverse — verify each denominator (retrieved vs relevant) drives the right metric. (co-21)
- **ex-42 · f1-harmonic** — compute F1 as the harmonic mean of precision and recall — verify F1 lies between them and nears the smaller. (co-21)
- **ex-43 · precision-at-k** — compute precision@5 and precision@10 on a ranked list — verify against a hand count of relevant docs in each prefix. (co-22)
- **ex-44 · qrels-load** — load a tiny relevance-judgment set into `dict[str, set[int]]` — verify each query maps to its labeled relevant docs. (co-23)
- **ex-45 · evaluate-two-configs** — compute precision@k for tf-idf vs BM25 over the qrels — verify the reported winner matches a hand tally. (co-22, co-23)
- **ex-46 · average-precision** — compute Average Precision for one query — verify it matches the mean of precisions at each relevant hit. (co-24)
- **ex-47 · map-multi-query** — compute MAP across several queries — verify it equals the mean of per-query APs. (co-24)
- **ex-48 · ndcg-compute** — compute nDCG@k with graded relevance — verify a perfect ranking scores 1.0 and a shuffled one scores less. (co-24)
- **ex-49 · analyzer-pipeline-model** — model an analyzer as char-filter → tokenizer → token-filters in typed Python — verify the staged output matches a hand trace. (co-25)
- **ex-50 · analyzer-swap-filter** — insert a stemming token filter into the pipeline — verify the emitted index terms change accordingly. (co-25)
- **ex-51 · query-dsl-parse** — parse a small `must`/`should`/`must_not` bool DSL into a typed query tree — verify the tree shape matches the query. (co-26)
- **ex-52 · query-dsl-execute** — execute the parsed tree against the index — verify results equal the equivalent hand-written boolean merge. (co-26)
- **ex-53 · positional-index-build** — store positions as `dict[str, dict[int, list[int]]]` — verify a term's position list matches its offsets in the doc. (co-28)
- **ex-54 · phrase-query** — match a two-word phrase by checking adjacent positions — verify it hits only docs where the words are consecutive. (co-28)
- **ex-55 · proximity-query** — match terms within N positions — verify a doc with the terms N+1 apart is excluded. (co-28)
- **ex-56 · segment-merge-model** — model two immutable segments merged into one — verify the merged index answers a query identically to a single-segment build. (co-27)

### Advanced

- **ex-57 · nrt-refresh-model** — model near-real-time refresh: buffered docs become searchable only after a `refresh()` — verify a doc added pre-refresh is invisible until refresh runs. (co-27)
- **ex-58 · typed-index-class** — build an `InvertedIndex` class with typed `add`/`query` methods — verify `pyright` is clean and queries return correct sets. (co-01, co-29)
- **ex-59 · incremental-add** — add a document to a built index without a rebuild — verify it becomes findable immediately. (co-29)
- **ex-60 · incremental-equals-rebuild** — compare the incremental index to a from-scratch rebuild — verify identical postings for every term. (co-29)
- **ex-61 · persist-json** — serialize postings to JSON, reload, and query — verify results match the in-memory index. (co-30)
- **ex-62 · persist-binary** — serialize with a compact varint/binary encoding — verify the file is smaller than JSON and round-trips correctly. (co-30)
- **ex-63 · delta-encode-postings** — delta-encode sorted doc-ids before storing — verify decode reconstructs the exact posting list at a smaller size. (co-30)
- **ex-64 · avgdl-incremental** — update `avgdl` as docs are added so BM25 stays correct — verify the running `avgdl` matches a recomputed one. (co-18, co-29)
- **ex-65 · bm25f-fields** — score `title` + `body` as weighted streams, combining tf then saturating — verify a title match outranks an equal body match. (co-31)
- **ex-66 · bm25f-vs-naive** — contrast BM25F combine-first with a naive per-field-score-then-sum — verify the naive version breaks saturation on a repeated term. (co-31)
- **ex-67 · fuzzy-levenshtein** — compute Levenshtein distance and match terms within edit distance 1 — verify `"colour"` matches `"color"`. (co-32)
- **ex-68 · fuzzy-damerau** — add adjacent-transposition (Damerau) — verify `"teh"` matches `"the"` at distance 1. (co-32)
- **ex-69 · spelling-correct** — suggest the nearest dictionary term for a misspelled query token — verify the suggestion is the min-edit-distance term. (co-32)
- **ex-70 · edge-ngram-autocomplete** — build edge n-grams and match a prefix — verify typing `"sea"` retrieves `"search"`. (co-33)
- **ex-71 · char-ngram-substring** — build character n-grams for substring matching — verify an interior substring query finds the doc. (co-33)
- **ex-72 · synonym-expand** — expand a query through a synonym map (`car → {car, automobile}`) — verify the doc with only `"automobile"` is now retrieved. (co-34)
- **ex-73 · semantic-embedding-cosine** — represent docs as fixed toy dense vectors and cosine-rank a query vector — verify the nearest-meaning doc ranks first. (co-35)
- **ex-74 · ann-vs-exact-knn** — compare brute-force exact kNN with a toy approximate search — verify recall/speed trade-off and note HNSW is the production approach. (co-35)
- **ex-75 · hybrid-lexical-vector** — blend a normalized BM25 score with a vector score into one hybrid rank — verify the hybrid order differs from pure BM25. (co-35)
- **ex-76 · lexical-miss-semantic-win** — run a `"car"` query where BM25 misses an `"automobile"` doc that the vector search finds — verify the semantic hit. (co-35)
- **ex-77 · pagerank-toy** — power-iterate PageRank on a tiny link graph to convergence — verify scores sum to 1 and the most-linked node ranks highest. (co-36)
- **ex-78 · pagerank-plus-bm25** — combine a link score with a term score for a final web-style rank — verify a well-linked doc outranks a marginally more relevant orphan. (co-36)
- **ex-79 · evaluate-hybrid** — compute precision@k of lexical vs hybrid over the qrels on semantic queries — verify hybrid scores higher where synonyms matter. (co-22, co-35)
- **ex-80 · mini-search-engine** — assemble index + analyzer + BM25 + top-k + persistence behind one `search()` CLI — verify an end-to-end query returns correct ranked results after a reload. (co-01, co-16, co-20, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small typed search library over a real text corpus that indexes documents,
  ranks queries with BM25 top-k, supports incremental add, and reports a relevance metric against a
  judgment set — then contrast one query's results with a Lucene-family engine to prove the concepts
  transfer.
- **Concepts exercised**: [ ] inverted index + posting-list merge (co-01, co-04) [ ] tokenization/
  normalization (co-06, co-07, co-09) [ ] TF-IDF → BM25 scoring (co-14, co-16) [ ] top-k ranking
  (co-20) [ ] precision@k evaluation (co-22, co-23) [ ] incremental indexing + persistence (co-29,
  co-30).
- **Ordered steps**:
  1. `.../learning/capstone/code/index.py` — a typed inverted index with tokenization and persisted
     postings. Verify a boolean query returns the correct document set and `pyright` is clean.
  2. `.../learning/capstone/code/rank.py` — add TF-IDF then BM25 top-k scoring. Verify the ranked
     order matches a hand-computed BM25 score on a 3-document fixture.
  3. `.../learning/capstone/code/evaluate.py` — run precision@k over a small relevance-judgment set
     across two analyzer configs. Verify the metric changes as expected when a stemmer is toggled.
  4. `.../learning/capstone/code/incremental.py` — add a new document without a full rebuild. Verify
     it becomes findable and its BM25 score is consistent with a from-scratch rebuild.
- **Acceptance criteria**: boolean and ranked queries are correct; BM25 matches the hand computation;
  precision@k responds to analyzer changes; incremental add matches a rebuild; all Python is
  type-annotated and `pyright`-clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Introduction to Information Retrieval** — Christopher D. Manning, Prabhakar Raghavan, Hinrich
  Schütze (2008). Free, standard graduate textbook on indexing, ranking, and evaluation for search
  systems. <https://nlp.stanford.edu/IR-book/>
- **Relevant Search: With Applications for Solr and Elasticsearch** — Doug Turnbull, John Berryman
  (2016). Standard practitioner's guide to tuning ranking and relevance in Lucene-based search
  engines.
- **Lucene in Action** — Michael McCandless, Erik Hatcher, Otis Gospodnetić (2nd ed., 2010).
  Canonical implementation-level reference for building search applications on Apache Lucene.

**Papers & articles**

- **The Anatomy of a Large-Scale Hypertextual Web Search Engine** — Sergey Brin, Lawrence Page
  (1998). The original Google/PageRank paper defining link-based ranking for large-scale web search.
  <http://infolab.stanford.edu/pub/papers/google.pdf>
- **Okapi at TREC** — Stephen E. Robertson, Stephen Walker, Micheline Hancock-Beaulieu, A. Gull,
  M. Lau (1992). Origin of the probabilistic ranking work that produced BM25, the ranking function
  underlying most modern inverted-index search engines. <https://trec.nist.gov/pubs/trec1/papers/02.txt>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Data depth — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Data depth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 6 · Databases & data depth.

> _Content originated in the now-closed FS-SE plan (topic 38); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
