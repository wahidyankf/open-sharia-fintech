---
title: "Overview"
date: 2026-07-27T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Prior topics**: [SQL Essentials](../../sql-essentials/learning/overview.md) and [Data Structures
  and Algorithms Essentials](../../data-structures-and-algorithms-essentials/overview.md) -- see this
  topic's own [Overview](../overview.md) for the full prerequisite rationale.
- **Tools & environment**: a macOS/Linux terminal; Python at a recent stable release with type hints
  and `pyright`. Every example is pure-Python and stdlib-only.
- **Assumed knowledge**: dictionaries, sets, and sorting by a key; reading and writing a small file
  from Python.

## Why this exists -- the big idea

Index-then-rank: build a `term -> documents` map once, then let every query do a cheap lookup instead
of a per-query scan. This tier turns that one idea into 80 runnable, progressively deeper examples --
from a hand-rolled inverted index through BM25 ranking and evaluation to a typed, incremental,
persisted mini search engine.

## How this topic is organized

- **Beginner** (Examples 1-28) -- tokenization (whitespace vs regex), case-folding, building an
  inverted index and posting lists, boolean AND/OR/NOT, the two-pointer posting-list merge and why
  scanning loses to indexing, term frequency and idf, stop-words and their recall risk, a from-scratch
  Porter (1980) stemmer, skip pointers, ranking by tf-idf, and the vector-space model's cosine
  similarity.
- **Intermediate** (Examples 29-56) -- BM25's own RSJ idf, saturating tf, and length normalization,
  sweeping `k1`/`b` to see them genuinely change (and even flip) a ranking, the Lucene/Elasticsearch
  software defaults versus the paper's own recommended range, top-k selection with a size-k heap, the
  full precision/recall/F1/precision@k/MAP/nDCG evaluation family over a relevance-judgment set, a
  typed analyzer pipeline model, a small boolean query DSL parsed and executed, positional indexes and
  the phrase/proximity queries they enable, and a segment-merge model.
- **Advanced** (Examples 57-80) -- near-real-time refresh semantics, a typed `InvertedIndex` class with
  incremental add proven identical to a from-scratch rebuild, JSON/binary/delta-encoded persistence, an
  incrementally-maintained `avgdl`, BM25F field weighting versus a broken naive alternative, fuzzy
  matching (Levenshtein, Damerau-Levenshtein, spelling correction), edge and character n-grams for
  autocomplete and substring search, synonym expansion, toy semantic embeddings and cosine ranking,
  approximate versus exact k-NN, hybrid lexical+vector search, PageRank's power iteration alone and
  combined with BM25, and a final mini search engine assembling the whole pipeline.
- **[Capstone](./capstone/overview.md)** -- a typed inverted index, BM25 top-k ranking, precision@k
  evaluation across two analyzer configs, and incremental indexing, assembled behind one small library
  over a real 8-document text corpus.

Every code example is real, runnable, fully type-annotated, colocated under
`learning/code/ex-NN-<slug>/`, actually executed to capture its documented output -- every printed
number on these pages is a genuine, captured transcript, never a fabricated one -- and `pyright`-clean
under `# pyright: strict`. Run each example with `python3 <file>.py` from its own
`learning/code/ex-NN-<slug>/` directory. Where a Lucene-family engine (Elasticsearch/OpenSearch) is
discussed, the code remains a pure-Python model of its behavior, never a live dependency.

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Tokenize Whitespace](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-1-tokenize-whitespace)
- [Example 2: Tokenize Regex](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-2-tokenize-regex)
- [Example 3: Case Fold](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-3-case-fold)
- [Example 4: Build Term-Doc Map](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-4-build-term-doc-map)
- [Example 5: Posting List Sorted](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-5-posting-list-sorted)
- [Example 6: Boolean AND](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-6-boolean-and)
- [Example 7: Boolean OR](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-7-boolean-or)
- [Example 8: Boolean NOT](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-8-boolean-not)
- [Example 9: Merge Two Pointer](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-9-merge-two-pointer)
- [Example 10: Scan vs Index Timing](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-10-scan-vs-index-timing)
- [Example 11: Term Frequency Count](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-11-term-frequency-count)
- [Example 12: Document Frequency](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-12-document-frequency)
- [Example 13: IDF Formula](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-13-idf-formula)
- [Example 14: TF-IDF Weight](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-14-tf-idf-weight)
- [Example 15: Stop-Word Drop](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-15-stop-word-drop)
- [Example 16: Stop-Word Recall Risk](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-16-stop-word-recall-risk)
- [Example 17: Porter Stem](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-17-porter-stem)
- [Example 18: Stem Index Shrink](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-18-stem-index-shrink)
- [Example 19: Lemmatize vs Stem](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-19-lemmatize-vs-stem)
- [Example 20: Normalization Recall Delta](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-20-normalization-recall-delta)
- [Example 21: Posting with Frequency](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-21-posting-with-frequency)
- [Example 22: Multi-Term AND](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-22-multi-term-and)
- [Example 23: Skip-Pointer Build](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-23-skip-pointer-build)
- [Example 24: Skip-Pointer Merge](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-24-skip-pointer-merge)
- [Example 25: Rank by TF-IDF](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-25-rank-by-tf-idf)
- [Example 26: Vector-Space Vectors](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-26-vector-space-vectors)
- [Example 27: Cosine Similarity](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-27-cosine-similarity)
- [Example 28: Analyzer Order](/en/learn/courses/search-and-information-retrieval/learning/beginner#example-28-analyzer-order)

### Intermediate (Examples 29–56)

- [Example 29: BM25 IDF Term](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-29-bm25-idf-term)
- [Example 30: BM25 Score: One Term](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-30-bm25-score-one-term)
- [Example 31: BM25 Saturation Curve](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-31-bm25-saturation-curve)
- [Example 32: TF-IDF vs BM25 Saturation](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-32-tf-idf-vs-bm25-saturation)
- [Example 33: BM25 Length Normalization](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-33-bm25-length-normalization)
- [Example 34: BM25 b Sweep](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-34-bm25-b-sweep)
- [Example 35: BM25 k1 Sweep](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-35-bm25-k1-sweep)
- [Example 36: BM25 Defaults](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-36-bm25-defaults)
- [Example 37: BM25 Full Ranker](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-37-bm25-full-ranker)
- [Example 38: Top-K Heap](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-38-top-k-heap)
- [Example 39: Top-K vs Full Sort Timing](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-39-top-k-vs-full-sort-timing)
- [Example 40: Precision/Recall Compute](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-40-precisionrecall-compute)
- [Example 41: Precision/Recall Direction](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-41-precisionrecall-direction)
- [Example 42: F1 Harmonic Mean](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-42-f1-harmonic-mean)
- [Example 43: Precision at K](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-43-precision-at-k)
- [Example 44: Qrels Load](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-44-qrels-load)
- [Example 45: Evaluate Two Configs](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-45-evaluate-two-configs)
- [Example 46: Average Precision](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-46-average-precision)
- [Example 47: MAP: Multi-Query](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-47-map-multi-query)
- [Example 48: nDCG Compute](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-48-ndcg-compute)
- [Example 49: Analyzer Pipeline Model](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-49-analyzer-pipeline-model)
- [Example 50: Analyzer Swap Filter](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-50-analyzer-swap-filter)
- [Example 51: Query DSL Parse](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-51-query-dsl-parse)
- [Example 52: Query DSL Execute](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-52-query-dsl-execute)
- [Example 53: Positional Index Build](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-53-positional-index-build)
- [Example 54: Phrase Query](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-54-phrase-query)
- [Example 55: Proximity Query](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-55-proximity-query)
- [Example 56: Segment Merge Model](/en/learn/courses/search-and-information-retrieval/learning/intermediate#example-56-segment-merge-model)

### Advanced (Examples 57–80)

- [Example 57: NRT Refresh Model](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-57-nrt-refresh-model)
- [Example 58: Typed Index Class](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-58-typed-index-class)
- [Example 59: Incremental Add](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-59-incremental-add)
- [Example 60: Incremental Equals Rebuild](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-60-incremental-equals-rebuild)
- [Example 61: Persist JSON](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-61-persist-json)
- [Example 62: Persist Binary](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-62-persist-binary)
- [Example 63: Delta-Encode Postings](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-63-delta-encode-postings)
- [Example 64: avgdl Incremental](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-64-avgdl-incremental)
- [Example 65: BM25F: Fields](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-65-bm25f-fields)
- [Example 66: BM25F vs Naive](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-66-bm25f-vs-naive)
- [Example 67: Fuzzy: Levenshtein](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-67-fuzzy-levenshtein)
- [Example 68: Fuzzy: Damerau](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-68-fuzzy-damerau)
- [Example 69: Spelling Correct](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-69-spelling-correct)
- [Example 70: Edge N-Gram Autocomplete](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-70-edge-n-gram-autocomplete)
- [Example 71: Char N-Gram Substring](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-71-char-n-gram-substring)
- [Example 72: Synonym Expand](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-72-synonym-expand)
- [Example 73: Semantic Embedding Cosine](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-73-semantic-embedding-cosine)
- [Example 74: ANN vs Exact kNN](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-74-ann-vs-exact-knn)
- [Example 75: Hybrid Lexical + Vector](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-75-hybrid-lexical--vector)
- [Example 76: Lexical Miss, Semantic Win](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-76-lexical-miss-semantic-win)
- [Example 77: PageRank Toy](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-77-pagerank-toy)
- [Example 78: PageRank + BM25](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-78-pagerank--bm25)
- [Example 79: Evaluate Hybrid](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-79-evaluate-hybrid)
- [Example 80: Mini Search Engine](/en/learn/courses/search-and-information-retrieval/learning/advanced#example-80-mini-search-engine)

---

← Previous: [Overview](../overview.md) · Next: [Beginner Examples](./beginner.md) →
