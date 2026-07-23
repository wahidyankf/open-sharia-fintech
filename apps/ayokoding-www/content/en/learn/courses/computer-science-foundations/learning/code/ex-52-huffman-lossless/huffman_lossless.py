# learning/code/ex-52-huffman-lossless/huffman_lossless.py
"""Example 52: Building Huffman Codes -- Compress Then Decompress, Losslessly."""  # => co-27: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import heapq  # => co-27: a min-heap is the standard way to repeatedly merge the two least-frequent nodes
from collections import Counter  # => co-27: character-frequency table -- Huffman's own input
from typing import Union  # => co-27: the recursive tree-node type needs Union for DD-39-clean typing

HuffmanTree = Union[str, tuple["HuffmanTree", "HuffmanTree"]]  # => co-27: a leaf (single char) or an internal (left, right) pair


def build_tree(text: str) -> HuffmanTree:  # => co-27: the classic greedy Huffman construction
    """Build a Huffman tree from text's character frequencies: repeatedly merge the two rarest nodes."""  # => co-27: documents build_tree's contract -- no runtime output, just sets its __doc__
    counts = Counter(text)  # => co-27: how often each character appears -- rarer characters get LONGER codes
    heap: list[tuple[int, int, HuffmanTree]] = [  # => co-27: (frequency, tie-breaker, node) -- heapq needs a total order
        (freq, i, char)
        for i, (char, freq) in enumerate(counts.items())  # => co-27: one leaf per distinct character
    ]  # => co-27: closes the multi-line construct opened above
    heapq.heapify(heap)  # => co-27: O(n) heap construction from the initial leaf list
    next_id = len(heap)  # => co-27: unique tie-breaker ids for freshly merged internal nodes
    while len(heap) > 1:  # => co-27: merge until exactly one node (the root) remains
        freq_a, _, node_a = heapq.heappop(heap)  # => co-27: the CURRENT least-frequent node
        freq_b, _, node_b = heapq.heappop(heap)  # => co-27: the CURRENT second-least-frequent node
        merged: HuffmanTree = (node_a, node_b)  # => co-27: a new internal node combining the two rarest subtrees
        heapq.heappush(heap, (freq_a + freq_b, next_id, merged))  # => co-27: reinsert with the SUMMED frequency
        next_id += 1  # => co-27: keeps every heap entry's tie-breaker unique
    return heap[0][2]  # => co-27: the single remaining node is the tree's root


def build_codes(tree: HuffmanTree, prefix: str = "") -> dict[str, str]:  # => co-27: root-to-leaf paths become codes
    """Walk the tree, assigning each leaf character the bit-string of the path from the root."""  # => co-27: documents build_codes's contract -- no runtime output, just sets its __doc__
    if isinstance(tree, str):  # => co-27: a LEAF -- this path (however long) IS this character's code
        return {tree: prefix or "0"}  # => co-27: a single-character alphabet still needs a valid 1-bit code
    left, right = tree  # => co-27: an INTERNAL node -- recurse into both children
    codes: dict[str, str] = {}  # => co-27: accumulates every leaf's code across both subtrees
    codes.update(build_codes(left, prefix + "0"))  # => co-27: "go left" appends a 0 to every code below this node
    codes.update(build_codes(right, prefix + "1"))  # => co-27: "go right" appends a 1 to every code below this node
    return codes  # => co-27: returns this computed value to the caller


def encode(text: str, codes: dict[str, str]) -> str:  # => co-27: text -> a single bitstring, via the code table
    return "".join(codes[c] for c in text)  # => co-27: one variable-length code per character, concatenated


def decode(bits: str, tree: HuffmanTree) -> str:  # => co-27: bitstring -> text, walking the SAME tree bit by bit
    """Decode a Huffman-encoded bitstring by walking the tree from the root for every character."""  # => co-27: documents decode's contract -- no runtime output, just sets its __doc__
    result: list[str] = []  # => co-27: accumulates decoded characters, one per completed root-to-leaf walk
    node = tree  # => co-27: current position in the tree -- resets to the root after every decoded character
    for bit in bits:  # => co-27: consume the bitstream one bit at a time
        node = node[0] if bit == "0" else node[1]  # type: ignore[index]  # => co-27: follow left (0) or right (1)
        if isinstance(node, str):  # => co-27: reached a LEAF -- one character fully decoded
            result.append(node)  # => co-27: record the decoded character
            node = tree  # => co-27: restart the walk from the root for the NEXT character
    return "".join(result)  # => co-27: the fully reconstructed text


if __name__ == "__main__":  # => co-27: entry point -- this block runs only when the file executes directly, not on import
    text = "abracadabra"  # => co-27: a classic small example with a genuinely skewed letter frequency
    tree = build_tree(text)  # => co-27: the Huffman tree built from this text's own frequencies
    codes = build_codes(tree)  # => co-27: the resulting variable-length code table
    for char, code in sorted(codes.items()):  # => co-27: prints every character's assigned code, alphabetically
        print(f"{char!r}: {code}")  # => co-27: rarer characters should get visibly LONGER codes
    encoded = encode(text, codes)  # => co-27: the full text, compressed into one bitstring
    decoded = decode(encoded, tree)  # => co-27: the SAME bitstring, decompressed back to text
    fixed_width_bits = len(text) * 8  # => co-27: the naive baseline -- 8 bits/char, no compression at all
    print(f"original:  {text!r} ({fixed_width_bits} bits at 8 bits/char)")  # => co-27: the uncompressed baseline
    print(f"encoded:   {len(encoded)} bits")  # => co-27: the Huffman-compressed size
    print(f"decoded:   {decoded!r}")  # => co-27: the reconstructed text, for a direct visual comparison
    assert decoded == text, "Huffman decoding must reconstruct the EXACT original text -- lossless"  # => co-27
    assert len(encoded) < fixed_width_bits, "Huffman coding must compress below the naive 8-bits/char baseline"  # => co-27
    print(f"Exact reconstruction and a real size reduction: True")  # => co-27: both asserts above passed
    # => co-27: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
