"""
Original Author: mjpieters [https://gist.github.com/mjpieters/86b0d152bb51d5f5979346d11005588b]
Remastered by: Dragon of Shuu

Decode and encode Base64 VLQ encoded sequences

Base64 VLQ is used in source maps.

VLQ values consist of 6 bits (matching the 64 characters of the Base64
alphabet), with the most significant bit a *continuation* flag. If the
flag is set, then the next character in the input is part of the same
integer value. Multiple VLQ character sequences so form an unbounded
integer value, in little-endian order.

The *first* VLQ value consists of a continuation flag, 4 bits for the
value, and the last bit the *sign* of the integer:

  +-----+-----+-----+-----+-----+-----+
  |  c  |  b3 |  b2 |  b1 |  b0 |  s  |
  +-----+-----+-----+-----+-----+-----+

while subsequent VLQ characters contain 5 bits of value:

  +-----+-----+-----+-----+-----+-----+
  |  c  |  b4 |  b3 |  b2 |  b1 |  b0 |
  +-----+-----+-----+-----+-----+-----+

For source maps, Base64 VLQ sequences can contain 1, 4 or 5 elements.
"""

from typing import Callable, Final, List, Optional, Tuple

B64CHARS: Final[bytes] = (
    b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
)

B64TABLE: Final[list[Optional[int]]] = [None] * (max(B64CHARS) + 1)

for i, b in enumerate(B64CHARS):
    B64TABLE[b] = i

B64ENC: Callable[[int], str] = B64CHARS.decode().__getitem__
SHIFTSIZE: Final[int] = 5
FLAG: Final[int] = 1 << 5
MASK: Final[int] = (1 << 5) - 1


def vlq_decode(vlqval: str) -> Tuple[int, ...]:
    """Decode Base64 VLQ value"""
    results: List[int] = []
    add = results.append
    shiftsize, flag, mask = SHIFTSIZE, FLAG, MASK
    shift = value = 0
    # use byte values and a table to go from base64 characters to integers
    for v in map(B64TABLE.__getitem__, vlqval.encode("ascii")):
        value += (v & mask) << shift  # type: ignore  # v is always int
        if v & flag:  # type: ignore  # v is always int
            shift += shiftsize
            continue
        # determine sign and add to results
        add((value >> 1) * (-1 if value & 1 else 1))
        shift = value = 0
    return tuple(results)


def vlq_encode(*values: int) -> str:
    """Encode integers to a VLQ value"""
    results: List[str] = []
    add = results.append
    shiftsize, flag, mask = SHIFTSIZE, FLAG, MASK
    for v in values:
        # add sign bit
        v = (abs(v) << 1) | int(v < 0)
        while True:
            toencode, v = v & mask, v >> shiftsize
            add(B64ENC(toencode | (v and flag)))
            if not v:
                break
    return ''.join(results)