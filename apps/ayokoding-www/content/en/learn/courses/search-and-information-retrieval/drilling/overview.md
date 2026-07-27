---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Search and Information Retrieval topic: recall
first, then applied judgment, then a hands-on kata, then a self-check checklist, then
elaborative-interrogation prompts that ask _why_, not just _what_. Every answer is hidden in a
`<details>` block; try each item yourself before opening it.

Every kata below is self-contained and deterministic -- hand-constructed fixtures only, no live
network call, no dependency on this topic's own worked-example or capstone code.

## Recall Q&A

Thirty-six short-answer questions, one per concept (`co-01` through `co-36`). Answer from memory,
then check.

**Q1 (co-01 -- inverted index).** Why does building a `term -> documents` map once beat scanning
every document for every query?

<details>
<summary>Answer</summary>

Because a scan does O(N) work on every single query, while an inverted index does that work exactly
once at build time and turns each query into a cheap dictionary lookup into a posting list -- the
per-query cost stops scaling with corpus size. This is the whole "index-then-rank" idea the rest of
the topic builds on.

</details>

**Q2 (co-02 -- posting list).** What does a posting list store, and why does it stay sorted by
doc-id?

<details>
<summary>Answer</summary>

A posting list is the per-term list of doc-ids (optionally carrying term frequency or token
positions) that the index stores under that term. Keeping it sorted is what makes the two-pointer
merge (co-04) and skip pointers (co-05) possible -- an unsorted list would force a full scan to
intersect or union with another list.

</details>

**Q3 (co-03 -- boolean retrieval).** How do AND, OR, and NOT map onto set operations over posting
lists?

<details>
<summary>Answer</summary>

AND is intersection, OR is union, and NOT is set difference against the universe of all doc-ids --
boolean retrieval is nothing more than set algebra performed on the posting lists each query term
resolves to.

</details>

**Q4 (co-04 -- posting-list merge).** Why does the two-pointer merge run in one linear pass instead
of a nested loop?

<details>
<summary>Answer</summary>

Because both lists are already sorted, a single pointer per list can walk forward monotonically:
compare the two current entries, advance whichever pointer points at the smaller doc-id (or both, on
a match), and never backtrack. A nested loop would recompare pairs it has already ruled out; the
two-pointer walk touches each element at most once.

</details>

**Q5 (co-05 -- skip pointers).** Why do skip pointers speed up AND but not OR?

<details>
<summary>Answer</summary>

Skip pointers let the merge jump past a run of non-matching doc-ids without visiting each one --
useful only when the walk is actively trying to skip past positions it knows cannot match, which is
exactly what an AND (intersection) does when one list has a large gap the other list's next target
sits beyond. OR (union) must still visit every element of both lists because every element is part
of the answer, so there is nothing to skip.

</details>

**Q6 (co-06 -- tokenization).** What does tokenization do, and why does the split rule (whitespace
vs. regex) matter?

<details>
<summary>Answer</summary>

Tokenization splits raw text into the discrete indexable units ("terms") everything downstream
operates on. A whitespace split leaves trailing punctuation glued to words (`"end."` stays one
token, distinct from `"end"`), while a `\w+`-style regex split strips punctuation and normalizes the
two to the same term -- the choice made here silently decides what a later query can ever match.

</details>

**Q7 (co-07 -- case-folding).** Why does lowercasing tokens before indexing matter?

<details>
<summary>Answer</summary>

Without case-folding, `"The"` and `"the"` become two distinct index terms with disjoint posting
lists, splitting what should be one term's evidence across two entries and silently halving recall
for case-varied queries. Lowercasing conflates them into a single term.

</details>

**Q8 (co-08 -- stop-words).** What is the recall cost of dropping stop-words?

<details>
<summary>Answer</summary>

Stop-words (`the`, `of`, and similar high-frequency, low-signal terms) get dropped to shrink the
index and speed queries, but the cost is that any query that is itself only stop-words -- or that
depends on a stop-word for an exact phrase match -- can no longer be answered at all, because the
term was never indexed in the first place.

</details>

**Q9 (co-09 -- stemming).** What does a Porter-style stemmer do, and what does it trade away?

<details>
<summary>Answer</summary>

It strips common suffixes by rule (Porter, 1980) so that `running`/`runs`/`runner`-family variants
conflate to one shared stem, raising recall -- a query for `run` can now match a document that only
contains `running`. The trade is precision: the stem can also over-conflate unrelated words that
happen to share a suffix pattern.

</details>

**Q10 (co-10 -- lemmatization).** How does lemmatization differ from stemming, and why is it used
less often?

<details>
<summary>Answer</summary>

Lemmatization looks up a dictionary-correct base form (`better -> good`) rather than mechanically
stripping suffixes, so it never produces a non-word the way a stemmer occasionally can. It is used
less often because it needs a dictionary/vocabulary lookup (costlier) and, in most measured
information-retrieval settings, produces retrieval gains that are not meaningfully larger than a
cheap stemmer's.

</details>

**Q11 (co-11 -- normalization-recall tradeoff).** Why can aggressive normalization hurt as much as
it helps?

<details>
<summary>Answer</summary>

Every normalization step (stemming, stop-word removal, case-folding) conflates distinct surface
forms into fewer index terms, which raises recall (more documents become reachable by a given query)
but can lower precision (documents get pulled in that only match on the conflated, coarser term) --
the analyzer pipeline's choices decide what is EVER findable, in both directions.

</details>

**Q12 (co-12 -- term frequency).** What does `tf` measure, and why is it not enough on its own?

<details>
<summary>Answer</summary>

`tf` is the raw count of a term inside one document -- the base relevance signal, since a document
mentioning a query term more often is plausibly more about it. Used alone it rewards keyword
stuffing without limit and ignores how common the term is across the whole corpus, which is exactly
what idf (co-13) and BM25's saturation (co-17) correct for.

</details>

**Q13 (co-13 -- inverse document frequency).** What does `idf = log(N / df)` express?

<details>
<summary>Answer</summary>

It up-weights rare terms and discounts common ones: a term appearing in few documents (`df` small
relative to `N`) gets a high idf because matching it is more discriminating, while a term appearing
in nearly every document approaches `idf = 0` because matching it says almost nothing about
relevance.

</details>

**Q14 (co-14 -- tf-idf).** What does combining `tf x idf` give you, and why was it the first ranking
baseline?

<details>
<summary>Answer</summary>

Multiplying a term's raw frequency in a document by its corpus-wide rarity produces a single
per-(term, document) weight that rewards both "mentioned often here" and "rare across the corpus" --
summing it across a query's terms gives a ranking score with no training data and no saturation
correction, which is why it was the classical baseline before BM25 (co-16) refined it.

</details>

**Q15 (co-15 -- vector-space cosine).** What does treating documents as vectors let you compute that
a raw score sum cannot?

<details>
<summary>Answer</summary>

Representing a document (and a query) as a term-weight vector lets you rank by cosine similarity --
the length-normalized angle between the two vectors -- rather than a raw dot-product sum, so a very
long document's larger raw weights do not automatically win just from having more terms; cosine
compares direction (what the document is about), not magnitude (how much text it has).

</details>

**Q16 (co-16 -- BM25).** What does BM25 combine that plain tf-idf does not?

<details>
<summary>Answer</summary>

BM25 (Okapi BM25, Robertson & Zaragoza) combines a saturating version of term frequency (co-17), a
probabilistic RSJ idf, and document-length normalization (co-18) into one scoring function -- where
tf-idf grows a term's contribution linearly forever, BM25 caps it and also corrects for document
length, which is why it replaced tf-idf as the default lexical ranker.

</details>

**Q17 (co-17 -- BM25 saturation).** What does the `k1` parameter control?

<details>
<summary>Answer</summary>

`k1` controls how quickly a repeated term's contribution to the score saturates -- past a point set
by `k1`, additional occurrences of the same term add diminishing returns instead of growing the
score linearly the way plain tf-idf would, which is BM25's direct defense against keyword stuffing.

</details>

**Q18 (co-18 -- BM25 length normalization).** What does the `b` parameter and the `B = (1 - b) +
b*(dl/avdl)` term do?

<details>
<summary>Answer</summary>

It normalizes a document's term-frequency contribution by how its length compares to the corpus
average (`dl/avdl`) -- without it, a long document accumulates higher raw term counts purely from
having more text, not from being more relevant, and would unfairly outrank a short, tightly on-topic
document.

</details>

**Q19 (co-19 -- BM25 defaults).** Where do `k1 = 1.2, b = 0.75` come from, and what must you not
conflate them with?

<details>
<summary>Answer</summary>

They are the Lucene/Elasticsearch **software** defaults, not a universal law -- Robertson &
Zaragoza's own paper instead recommends an experimental range (`1.2 < k1 < 2`, `0.5 < b < 0.8`) to
tune per corpus. The software default's `k1 = 1.2` actually sits at the paper's lower boundary
rather than strictly inside its recommended open interval -- worth stating precisely rather than
treating the two numbers as interchangeable "the BM25 defaults."

</details>

**Q20 (co-20 -- top-k ranking).** Why does a size-k min-heap beat a full sort for returning the top
k results?

<details>
<summary>Answer</summary>

A full sort orders every scored document even though only the top k are ever shown; a size-k
min-heap only ever holds k candidates at a time and discards anything smaller than its current
minimum, so its cost scales with corpus size times `log(k)` rather than corpus size times
`log(corpus size)` -- the saving grows as the corpus grows and k stays small.

</details>

**Q21 (co-21 -- precision-recall).** What is the denominator difference between precision and
recall?

<details>
<summary>Answer</summary>

`precision = |relevant intersect retrieved| / |retrieved|` -- of what you returned, how much was
right; `recall = |relevant intersect retrieved| / |relevant|` -- of what was actually relevant, how
much did you find. Mixing up the denominator silently swaps which failure mode ("returning junk" vs.
"missing hits") a reported number is actually about.

</details>

**Q22 (co-22 -- precision at k).** Why does precision@k matter more than overall precision for a
search UI?

<details>
<summary>Answer</summary>

Users mostly look at the first page of results, not the entire retrieved set -- precision@5 or
precision@10 measures exactly the prefix a user actually sees, which is the number that predicts
whether the ranking "feels right," while overall precision (over every retrieved document) can look
fine while the visible top results are poor.

</details>

**Q23 (co-23 -- relevance judgments).** What does a qrels set turn "is this a good result" into?

<details>
<summary>Answer</summary>

A relevance-judgment (qrels) set is a labeled mapping from query to the documents actually judged
relevant to it -- without it, "is result A better than result B" is opinion; with it, precision,
recall, MAP, and nDCG all become computable, measurable quantities rather than guesses.

</details>

**Q24 (co-24 -- MAP and nDCG).** Why do MAP and nDCG matter when plain precision@k does not?

<details>
<summary>Answer</summary>

Precision@k does not care about the ORDER of the hits within the top k, or about graded relevance
(some hits being more relevant than others). MAP averages precision at each relevant hit's own rank
position (order-aware), and nDCG discounts a relevant hit's contribution the deeper it sits and can
weigh graded relevance levels -- both answer "is the best result actually near the top," which
precision@k alone cannot.

</details>

**Q25 (co-25 -- analyzer pipeline).** What is the fixed stage order of a Lucene-family analyzer?

<details>
<summary>Answer</summary>

Char filters, then exactly one tokenizer, then token filters, in that order -- char filters operate
on raw text before splitting (e.g. stripping HTML), the tokenizer does the actual split into terms,
and token filters (lowercasing, stop-word removal, stemming) then transform the token stream. The
same stages this topic builds by hand in the Beginner tier.

</details>

**Q26 (co-26 -- query DSL).** What does parsing a `must`/`should`/`must_not` query into a tree buy
you over a hand-written boolean expression?

<details>
<summary>Answer</summary>

A structured query DSL separates WHAT a user wants (the query's intent, expressed as a tree of
clauses) from HOW it executes (walking that tree against the index) -- the same tree can be
re-executed, cached, explained, or re-planned without re-parsing user input each time, and it
generalizes past a hand-written chain of if/else boolean checks.

</details>

**Q27 (co-27 -- segments and merge).** What does "near-real-time" mean for a Lucene-family engine,
and why not "real-time"?

<details>
<summary>Answer</summary>

The engine writes immutable segments and periodically merges them; a "refresh" opens a new segment
so recently indexed documents become searchable. It is NEAR-real-time, not real-time, because a
refresh happens on an interval (roughly every second by default) rather than instantly on every
write -- there is a small, bounded window where a just-indexed document is not yet visible to
queries.

</details>

**Q28 (co-28 -- positional and phrase queries).** What do postings need to carry to support a phrase
query, and why can't a plain (non-positional) index do it?

<details>
<summary>Answer</summary>

Postings need to carry each term's token POSITIONS within the document, not just presence. A
phrase query ("quick brown") must confirm the two terms occur at adjacent positions in the same
document, which a plain index -- knowing only that both terms appear SOMEWHERE in the document --
cannot distinguish from the two words appearing far apart and unrelated.

</details>

**Q29 (co-29 -- incremental indexing).** Why does adding a document without a full rebuild matter?

<details>
<summary>Answer</summary>

A full rebuild is O(corpus size) every time a single document changes, which does not scale as a
corpus and its update rate grow. Incremental indexing adds (or updates) just the new document's
postings, keeping the index consistent with a from-scratch build while paying a cost proportional to
the ONE document added, not the whole corpus.

</details>

**Q30 (co-30 -- postings persistence).** Why does an index need a serialization format at all?

<details>
<summary>Answer</summary>

An in-memory index vanishes when the process exits -- persistence (JSON, a compact binary encoding,
or delta-encoded doc-ids) lets the index survive a restart and be reloaded without re-indexing the
whole corpus from source documents again. The encoding choice trades human-readability (JSON)
against file size and load speed (binary/delta-encoded).

</details>

**Q31 (co-31 -- BM25F field weighting).** Why must BM25F combine per-term `tf` across fields BEFORE
saturating, not after?

<details>
<summary>Answer</summary>

BM25's saturation (co-17) is a non-linear function of `tf` -- summing two ALREADY-saturated per-field
scores is not the same as saturating the combined (weighted) `tf` once. A naive
per-field-score-then-add approach breaks the saturation curve's intended shape and can let a term
repeated across two fields contribute more than the formula's own cap intends; combining tf first,
then saturating once, is what keeps the cap meaningful.

</details>

**Q32 (co-32 -- fuzzy edit distance).** How does Damerau-Levenshtein differ from plain Levenshtein?

<details>
<summary>Answer</summary>

Plain Levenshtein counts single-character insert, delete, and replace operations. Damerau extends
it with a fourth operation, adjacent-character transposition, so a typo like `"teh"` for `"the"`
counts as distance 1 (one transposition) instead of distance 2 (two substitutions) under plain
Levenshtein -- a meaningfully different result for the common transposition-typo case.

</details>

**Q33 (co-33 -- n-gram autocomplete).** What is the difference between edge n-grams and character
n-grams, and what does each power?

<details>
<summary>Answer</summary>

Edge n-grams are anchored to the START of a word (`sea`, `sear`, `searc`, `search` for indexing
"search") and power prefix-based search-as-you-type/autocomplete. Character n-grams slide across the
WHOLE word (not just the start) and power substring matching anywhere inside a term, at the cost of
a much larger index.

</details>

**Q34 (co-34 -- query expansion / synonyms).** What problem does synonym expansion solve, and what
does it cost?

<details>
<summary>Answer</summary>

A lexical index only matches the literal terms present; expanding a query through a synonym map
(`car -> {car, automobile}`) lets a query for `car` also retrieve a document that only contains
`automobile`, raising recall for genuinely equivalent terms. The cost is that the synonym map must
be curated and kept accurate -- a wrong or overbroad synonym silently pulls in irrelevant documents.

</details>

**Q35 (co-35 -- semantic vector search).** What does dense-vector kNN retrieve that BM25 structurally
cannot?

<details>
<summary>Answer</summary>

BM25 matches TOKENS, not meaning -- a query for `"car"` will not match a document containing only
`"automobile"` unless a synonym map bridges them by hand. Dense embedding vectors place semantically
similar text near each other in vector space regardless of exact wording, so approximate-nearest-
neighbor search (HNSW in production engines) can retrieve a meaning-equivalent document even with
zero shared tokens -- at the cost of needing an embedding model, an ANN index, and more compute.

</details>

**Q36 (co-36 -- PageRank / link analysis).** Why is PageRank a content-independent ranking signal,
and why does it complement term-based scoring rather than replace it?

<details>
<summary>Answer</summary>

PageRank scores a document purely from the LINK GRAPH -- who points at it, and how important THOSE
pages are -- without reading the document's own text at all, which is why it is "content-independent"
and, unlike BM25, cannot tell whether a well-linked page is actually about the query's terms.
Combining it with a term-based score (BM25) lets the two signals correct each other's blind spot:
term relevance plus link authority together predict a better web-scale ranking than either alone.

</details>

## Applied problems

Ten scenarios spanning the whole topic. Each describes a realistic situation without naming the
specific concept -- decide what applies and why, then check your reasoning against the worked
solution. Every scenario below is invented for this drill and does not reuse any fixture, function,
or corpus from the 80 worked examples or the capstone.

**AP1.** A support team's internal tool searches ticket text with `WHERE body LIKE '%refund%'` and
it works fine on 500 tickets. A year later the table has 4 million rows and the same search now
takes eleven seconds. What structural change fixes this, and why doesn't just adding a database
index on the `body` column (as a plain B-tree) solve it the way it would for an equality lookup?

<details>
<summary>Worked solution</summary>

An inverted index (co-01), not a bigger B-tree -- a `LIKE '%refund%'` substring scan cannot use a
standard B-tree index (which is built for prefix/equality lookups, not "contains this substring
anywhere"), so the database still scans every row regardless of what column indexes exist. An
inverted index precomputes a `term -> ticket-ids` map once, turning the query into a direct lookup
whose cost does not grow with row count the way a per-row scan does.

</details>

**AP2.** A team strips all stop-words before indexing to shrink their index by 30%. Weeks later,
users searching for the exact phrase `"to be or not to be"` (a famous quote, entirely stop-words)
get zero results, and nobody can figure out why -- the phrase clearly appears in the indexed corpus.

<details>
<summary>Worked solution</summary>

This is the stop-word recall risk (co-08, co-11) in its sharpest form -- if every word in a phrase is
a stop-word and none of them were indexed, there is no term left in the index for the query to match
against, no matter how exactly the phrase appears in the source text. The fix is either not
stripping stop-words for phrase-heavy corpora, or keeping a separate un-stripped field just for
exact-phrase matching.

</details>

**AP3.** Two documents are compared for a query on "database": Doc A mentions "database" 40 times
in a short FAQ page; Doc B mentions "database" 4 times in a well-written, clearly on-topic article.
Under plain tf-idf, Doc A outranks Doc B by a wide margin. A team wants a ranking function where
that margin shrinks without discarding term frequency altogether.

<details>
<summary>Worked solution</summary>

This is exactly BM25's saturation (co-16, co-17) versus tf-idf's unbounded linear growth -- tf-idf
keeps rewarding every additional occurrence equally, so 40 mentions counts 10x as much as 4 with no
diminishing returns, rewarding keyword stuffing. BM25's `k1` term caps how much additional
occurrences can add past a point, shrinking (though not eliminating) Doc A's advantage while still
crediting Doc B's genuine, more moderate term frequency.

</details>

**AP4.** An engineer builds a correctly sorted inverted index and a correct two-pointer AND merge.
On a term appearing in 2 million documents intersected against a term appearing in 200 documents,
the query is still slower than expected -- profiling shows the merge is stepping through most of
the 2-million-entry list one doc-id at a time even though very few of those doc-ids can possibly
match. What's missing?

<details>
<summary>Worked solution</summary>

Skip pointers (co-05) -- a plain two-pointer merge (co-04) still visits every entry of the larger
list it cannot rule out one step at a time. Evenly-spaced skip pointers (roughly every sqrt(P)
entries) let the merge jump forward past a whole run of non-matching doc-ids in one step when the
shorter list's next target is far ahead, which is precisely the AND-query shape this scenario
describes -- and precisely the case skip pointers are built for (they would NOT help if this were an
OR query).

</details>

**AP5.** A team migrates their search index from one Lucene-family engine to another and is
surprised the raw relevance scores for the same query and corpus come out numerically different,
even though the RANKING ORDER of results looks unchanged. A stakeholder worries something is broken.

<details>
<summary>Worked solution</summary>

Likely nothing is broken -- different BM25 implementations can use slightly different idf variants
or default `k1`/`b` values (co-19), which changes the absolute SCORE magnitude without necessarily
changing the RELATIVE ordering of documents for a given query, since all documents are scored by the
same formula and constants that scale scores uniformly do not flip a ranking. The team should verify
ranking order and precision@k (co-22), not raw score equality, before concluding the migration is
broken.

</details>

**AP6.** A team turns on stemming and measures precision@10 for 50 queries: it rises for 38 queries,
falls for 7, and is unchanged for 5. A stakeholder asks for one number: "did stemming help?"

<details>
<summary>Worked solution</summary>

A single precision@k delta per query is not "one number" for the whole change -- this is exactly the
normalization-recall tradeoff (co-09, co-11) playing out unevenly across queries, and the honest
answer needs an aggregate, order-aware metric across ALL 50 queries (MAP, co-24) plus reporting how
many queries moved in each direction, not just an average that could hide a large regression on a
handful of queries behind a larger average gain on the rest.

</details>

**AP7.** A team's index is rebuilt from scratch every night via a full batch job. As the corpus grows
past a million documents, the nightly rebuild starts taking longer than the maintenance window
allows, and documents added mid-morning are not searchable until the following night.

<details>
<summary>Worked solution</summary>

The fix is incremental indexing (co-29) with a persisted index (co-30), not a faster full rebuild --
a full nightly rebuild's cost scales with the WHOLE corpus every single night regardless of how many
documents actually changed, while adding just the new documents to an already-persisted index scales
with the number of NEW documents, and (unlike the nightly batch) can run continuously rather than
once a day, closing the "not searchable until tomorrow" gap entirely.

</details>

**AP8.** A shopping search returns zero results for the query "auto insurance" even though the
catalog contains several documents about "car insurance" and one about "vehicle coverage." A
product manager wants "close enough" queries like this to work without a full ML project.

<details>
<summary>Worked solution</summary>

The cheapest fix here is query expansion through a curated synonym map (co-34) --
`auto -> {auto, car, vehicle}` -- which is far less costly to build and operate than a full semantic
embedding pipeline (co-35). Semantic/vector search is the more powerful, more general fix for
open-ended meaning-matching, but a hand-curated synonym list is the right first reach for a small,
known set of domain-specific equivalences like this one.

</details>

**AP9.** A search team adds PageRank-style link scoring on top of their existing BM25 ranking. A
week later, a heavily cross-linked "About Us" page starts outranking genuinely relevant product
pages for several product-name queries, even though "About Us" barely mentions those products.

<details>
<summary>Worked solution</summary>

This is PageRank's content-independence (co-36) overwhelming term relevance when weighted too
heavily -- a link-authority signal knows nothing about WHAT a page is about, only how well-linked it
is, so a page that is link-heavy but topically unrelated can win purely on link score if the combined
weighting gives PageRank too much influence relative to BM25's term-match signal. The fix is
rebalancing the combination weight (or gating the link signal by a minimum term-relevance floor), not
discarding either signal.

</details>

**AP10.** A team scores `title` and `body` fields separately with BM25, then sums the two per-field
scores to get a document's final score. They notice a document that repeats the query term heavily
in BOTH fields scores much higher than the formula's own saturation seems to allow -- almost as if
saturation weren't happening at all for that document.

<details>
<summary>Worked solution</summary>

This is exactly the naive per-field-score-then-sum failure BM25F is built to avoid (co-31) -- scoring
each field independently and adding the two ALREADY-saturated numbers effectively lets each field
"re-earn" its own saturation cap, so a term repeated across two fields can contribute close to double
what a single saturating formula intends. The fix is combining the per-term `tf` across fields
(weighted) FIRST, then saturating once over the combined value, exactly as BM25F specifies.

</details>

## Code katas

Five self-contained exercises. Every kata runs on hand-constructed, in-memory data using only the
Python 3 standard library -- no live model call, no network, and no dependency on this topic's own
worked-example or capstone files, so every kata is runnable anywhere Python 3 with `pytest` is
installed.

### Kata 1 -- Two-pointer posting-list intersection, from scratch

Write `intersect_sorted(a: list[int], b: list[int]) -> list[int]` that intersects two sorted
`list[int]` posting lists using a single two-pointer linear pass -- no `set` operations, no
`in`-checks against the other list. Construct three fixtures of your own: two lists with no overlap,
two lists that are identical, and two lists with a partial, non-trivial overlap. Confirm your
function's result matches Python's own `sorted(set(a) & set(b))` on all three, and that your
implementation never revisits an index in either list once advanced past it (co-02, co-04).

### Kata 2 -- BM25 term weight, from its formula

Write `bm25_term_weight(tf: int, df: int, n_docs: int, doc_len: int, avg_doc_len: float, k1: float =
1.2, b: float = 0.75) -> float` implementing `score = tf / (k1*B + tf) * idf_rsj` where
`B = (1 - b) + b * (doc_len / avg_doc_len)` and `idf_rsj = log((n_docs - df + 0.5) / (df + 0.5))`,
using only `math`. Construct three fixtures of your own: one where `doc_len` equals `avg_doc_len`
(so `B = 1`), one for a document twice the average length, and one for a term appearing in every
document (`df == n_docs`, confirm `idf_rsj` correctly goes negative rather than raising or returning
zero). Confirm the equal-length fixture's score is hand-computable by substituting `B = 1` directly
(co-16, co-17, co-18, co-19).

### Kata 3 -- Cosine similarity between two term-weight vectors, from scratch

Write `cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float` computing the
length-normalized dot product over the UNION of both vectors' keys (a missing key contributes 0),
using no external library. Construct three fixtures of your own: two identical vectors (confirm
similarity is 1.0), two vectors with disjoint keys (confirm similarity is 0.0), and two vectors that
share some but not all terms with different weights (confirm the result is strictly between 0 and 1
and matches a hand computation of the dot product and the two vector magnitudes) (co-14, co-15).

### Kata 4 -- Levenshtein edit distance, from its dynamic-programming definition

Write `levenshtein(a: str, b: str) -> int` computing the minimum number of single-character insert,
delete, and replace operations via the standard O(len(a) \* len(b)) dynamic-programming table, with no
library import. Construct three fixtures of your own: identical strings (confirm distance 0), one
insertion away (e.g. `"cat"` vs `"cats"`, confirm distance 1), and a transposition typo (e.g.
`"form"` vs `"from"`) -- confirm your PLAIN Levenshtein result on the transposition case is 2 (two
substitutions), and explain in one sentence why a Damerau-extended version would instead report 1
for that same pair (co-32).

### Kata 5 -- Precision@k and F1, from their definitions

Write `precision_at_k(ranked_ids: list[int], relevant_ids: set[int], k: int) -> float` and
`f1_score(precision: float, recall: float) -> float` (the harmonic mean, `0.0` when both inputs are
`0.0`), with no library import. Construct two fixtures of your own: a ranked list of 10 doc-ids
where exactly 3 of the top 5 are relevant (confirm `precision_at_k(..., k=5) == 0.6`), and a case
with `precision = 1.0, recall = 0.2` (confirm the F1 result sits much closer to the SMALLER of the
two inputs than their arithmetic mean would, demonstrating why the harmonic mean punishes a large
imbalance between precision and recall) (co-21, co-22).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can explain why building a `term -> documents` map once beats scanning every document per
      query. (co-01)
- [ ] I can state what a posting list stores and why it stays sorted by doc-id. (co-02)
- [ ] I can map AND/OR/NOT onto intersection/union/difference over posting lists. (co-03)
- [ ] I can explain why the two-pointer merge runs in one linear pass. (co-04)
- [ ] I can explain why skip pointers speed up AND but not OR. (co-05)
- [ ] I can explain what tokenization does and why the split rule matters. (co-06)
- [ ] I can explain why case-folding tokens before indexing matters. (co-07)
- [ ] I can explain the recall cost of dropping stop-words. (co-08)
- [ ] I can explain what a Porter-style stemmer does and what it trades away. (co-09)
- [ ] I can explain how lemmatization differs from stemming and why it is used less often. (co-10)
- [ ] I can explain why aggressive normalization can hurt as much as it helps. (co-11)
- [ ] I can state what `tf` measures and why it is not enough alone. (co-12)
- [ ] I can state what `idf = log(N / df)` expresses. (co-13)
- [ ] I can explain what combining `tf x idf` gives you and why it was the first ranking baseline.
      (co-14)
- [ ] I can explain what cosine similarity over term-weight vectors computes that a raw score sum
      cannot. (co-15)
- [ ] I can explain what BM25 combines that plain tf-idf does not. (co-16)
- [ ] I can explain what the `k1` parameter controls. (co-17)
- [ ] I can explain what the `b` parameter and the `B` length-normalization term do. (co-18)
- [ ] I can state where `k1 = 1.2, b = 0.75` come from and what not to conflate them with. (co-19)
- [ ] I can explain why a size-k min-heap beats a full sort for top-k results. (co-20)
- [ ] I can state the denominator difference between precision and recall. (co-21)
- [ ] I can explain why precision@k matters more than overall precision for a search UI. (co-22)
- [ ] I can explain what a qrels set turns "is this a good result" into. (co-23)
- [ ] I can explain why MAP and nDCG matter when plain precision@k does not. (co-24)
- [ ] I can state the fixed stage order of a Lucene-family analyzer. (co-25)
- [ ] I can explain what parsing a query into a DSL tree buys you over hand-written boolean checks.
      (co-26)
- [ ] I can explain what "near-real-time" means for a Lucene-family engine and why not "real-time."
      (co-27)
- [ ] I can explain what postings need to carry to support a phrase query. (co-28)
- [ ] I can explain why adding a document without a full rebuild matters. (co-29)
- [ ] I can explain why an index needs a serialization format at all. (co-30)
- [ ] I can explain why BM25F must combine per-term `tf` across fields before saturating, not after.
      (co-31)
- [ ] I can explain how Damerau-Levenshtein differs from plain Levenshtein. (co-32)
- [ ] I can explain the difference between edge n-grams and character n-grams and what each powers.
      (co-33)
- [ ] I can explain what problem synonym expansion solves and what it costs. (co-34)
- [ ] I can explain what dense-vector kNN retrieves that BM25 structurally cannot. (co-35)
- [ ] I can explain why PageRank is content-independent and why it complements term-based scoring
      rather than replacing it. (co-36)

## Elaborative interrogation & self-explanation

Six prompts that ask you to explain WHY, connecting two or more concepts, rather than recall a
single fact. Write your own answer before checking the discussion.

**E1.** Stemming and stop-word removal (co-09, co-11) trade precision for recall at the TEXT
NORMALIZATION stage, while BM25's saturation and length normalization (co-17, co-18) tame an
already-scored signal at the RANKING stage. Both "tune down" a naive signal -- what's the structural
difference between tuning at the normalization stage versus the ranking stage, and why does this
topic need both rather than one being enough?

<details>
<summary>Discussion</summary>

Normalization-stage tuning changes WHICH documents are reachable at all (what gets indexed as the
same term, decided once, before any query runs), while ranking-stage tuning changes ONLY THE ORDER
among documents that are already reachable (decided per-query, after retrieval). A generous stemmer
cannot fix a keyword-stuffed document ranking too high, and a well-tuned BM25 cannot recover a
document that stop-word stripping made permanently unreachable -- the two operate on different
failure modes at different points in the pipeline, so neither substitutes for the other.

</details>

**E2.** Skip pointers helping AND but not OR (co-05) and BM25F needing to combine per-term `tf`
across fields BEFORE saturating rather than after (co-31) are both "the order of operations
matters" lessons. Why does sequencing determine correctness in one case and efficiency in the other,
rather than both being the same kind of bug?

<details>
<summary>Discussion</summary>

Skip pointers are an EFFICIENCY concern -- doing the merge in a different order (with or without
skips) produces the exact same correct intersection result, just faster or slower; applying skips to
an OR query would not produce a WRONG answer, it simply would not help, because OR needs to visit
every element regardless. BM25F's field-combination order is a CORRECTNESS concern -- summing two
already-saturated per-field scores produces a mathematically different (and wrong, by the formula's
own intent) number than saturating the combined tf once; there is no "slower but still correct"
version of getting this one backwards.

</details>

**E3.** This topic computes nearly every named quantity (tf-idf co-14, BM25 co-16, cosine similarity
co-15) TWICE -- once from its definition in plain Python, once inside a larger example that exercises
it end-to-end -- and expects the two to agree. Why is that discipline worth the extra code rather
than simply trusting one implementation?

<details>
<summary>Discussion</summary>

Writing a quantity from its definition first forces genuine understanding of what it IS, not just
which function call produces it -- a reader who only ever calls a scoring function never sees why it
subtracts, saturates, or normalizes the way it does. Cross-checking the two also catches a real
class of error early: an off-by-one in the RSJ idf's `+0.5` terms, a swapped `k1`/`b` argument order,
or a length-normalization term applied to the wrong document -- errors that would otherwise silently
produce a plausible-looking but wrong ranking.

</details>

**E4.** Segments-and-merge / near-real-time refresh (co-27) and incremental indexing (co-29) both let
an index grow without a full rebuild. What is the structural difference between a production
engine's segment-merge approach and this topic's own typed incremental-add approach?

<details>
<summary>Discussion</summary>

A production engine's segments are IMMUTABLE once written -- new documents go into a brand-new
segment, and a background process periodically MERGES older segments together, trading a bounded
"near-real-time" visibility delay for write throughput and crash-safety. This topic's typed
incremental-add instead directly mutates the SAME in-memory posting-list structure a document
belongs in, which is simpler to reason about and verify (matching a from-scratch rebuild exactly,
co-29's own example) but does not, by itself, give you the segment-merge approach's immutability or
crash-recovery properties -- the two solve "grow without a full rebuild" at different points on the
simplicity-versus-production-robustness spectrum.

</details>

**E5.** Query expansion through synonyms (co-34) and semantic vector search (co-35) both aim to
retrieve `"automobile"` for a `"car"` query, yet this topic treats synonym expansion as the cheaper
first reach and semantic search as the more powerful, more expensive fallback. What makes one
"cheaper" and the other "more powerful" rather than one simply being a strictly better version of
the other?

<details>
<summary>Discussion</summary>

Synonym expansion is cheap because it is a small, hand-curated, deterministic lookup table -- it
covers exactly the equivalences someone thought to add, and nothing more, which is both its strength
(precise, auditable, no model to run) and its limit (it cannot generalize to a synonym relationship
nobody anticipated). Semantic vector search is more powerful because an embedding model captures
meaning relationships far beyond any hand-curated list -- but it needs an embedding model, an ANN
index, and materially more compute and operational complexity than a lookup table, so reaching for
it is justified only once the synonym list's coverage limit is genuinely the bottleneck.

</details>

**E6.** PageRank (co-36, a content-independent, query-independent signal) and BM25 (co-16, a
content-dependent, query-dependent signal) are combined in web-scale search rather than either being
used alone. Why does combining a content-independent signal with a content-dependent one improve
ranking, and what risk does AP9 above illustrate about weighting the two?

<details>
<summary>Discussion</summary>

The two signals answer genuinely different questions and fail in different, uncorrelated ways: BM25
can be gamed by keyword stuffing but knows nothing about a page's real-world authority, while
PageRank knows nothing about whether a page's TEXT actually matches the query at all. Combining them
lets each cover the other's blind spot -- but AP9 shows the failure mode of getting the combination
weight wrong: if the link signal is weighted too heavily relative to the term signal, a well-linked
but topically unrelated page (like an "About Us" page) can out-rank a genuinely relevant one purely
on link authority, which is precisely the content-independence that made PageRank useful in the
first place turning into a liability when it dominates the combined score.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
