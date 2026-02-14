#!/usr/bin/env python3
# ev_delta_utils.py
#
# Party-level e-vote delta application for rk23_parliament.py
#
# File format (one per line, # comments allowed):
#   REF+1
#   EE200-10
#
# Applies deltas neutrally: proportional to current candidate e-votes within that party
# (fallback to total votes), without any "maximize outcome impact" logic.

import math
import re
from collections import defaultdict

_DELTA_RE = re.compile(r"^\s*([A-Z0-9_]+)\s*([+-])\s*(\d+)\s*$")


def load_ev_deltas(path: Path) -> dict[str, int]:
    deltas: dict[str, int] = defaultdict(int)
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            s = line.split("#", 1)[0].strip()
            if not s:
                continue
            m = _DELTA_RE.match(s)
            if not m:
                raise ValueError(f"{path}:{ln}: invalid line: {line.rstrip()!r}")
            p, sign, num = m.group(1), m.group(2), int(m.group(3))
            deltas[p] += num if sign == "+" else -num
    return dict(deltas)


def _distribute_proportional(ids, weights, target: int) -> dict[int, int]:
    """
    Distribute positive integer target across ids proportionally to weights.
    Deterministic: ties by id.
    Returns allocations summing to target.
    """
    total_w = sum(weights)
    if target <= 0 or not ids:
        return {}

    if total_w <= 0:
        # deterministic 1-by-1
        alloc = {cid: 0 for cid in ids}
        for i in range(target):
            alloc[ids[i % len(ids)]] += 1
        return alloc

    raw = [(ids[i], target * weights[i] / total_w) for i in range(len(ids))]
    floor = {cid: int(math.floor(x)) for cid, x in raw}
    used = sum(floor.values())
    remain = target - used

    remainders = sorted(((cid, x - floor[cid]) for cid, x in raw), key=lambda t: (-t[1], t[0]))
    for cid, _ in remainders[:remain]:
        floor[cid] += 1

    return {cid: v for cid, v in floor.items() if v != 0}


def apply_ev_party_deltas(
    deltas: dict[str, int],
    cand_by_id,
    party_votes_d,
    party_votes_nat,
    cand_total,
    cand_e,
):
    """
    Mutates cand_total/cand_e and party_votes_d/party_votes_nat in-place.

    - Positive delta: adds e-votes (and total votes) to candidates of that party proportionally.
    - Negative delta: removes e-votes (and total votes) from candidates with highest e-votes first (deterministic).
    """
    party_cids = defaultdict(list)
    for cid, c in cand_by_id.items():
        party_cids[c.party_code].append(cid)
    for p in party_cids:
        party_cids[p].sort()

    for p, delta in deltas.items():
        if delta == 0:
            continue
        cids = party_cids.get(p, [])
        if not cids:
            raise ValueError(f"Unknown or empty party code in delta: {p}")

        if delta < 0:
            avail = sum(cand_e.get(cid, 0) for cid in cids)
            if -delta > avail:
                raise ValueError(f"Party {p}: cannot remove {-delta} e-votes; only {avail} available.")

            need = -delta
            donors = sorted(cids, key=lambda cid: (-cand_e.get(cid, 0), cid))
            alloc = {}
            for cid in donors:
                if need <= 0:
                    break
                take = min(need, cand_e.get(cid, 0))
                if take:
                    alloc[cid] = -take
                    need -= take
            if need:
                raise RuntimeError("Internal error: failed to allocate negative delta fully.")
        else:
            weights = [cand_e.get(cid, 0) for cid in cids]
            if sum(weights) == 0:
                weights = [cand_total.get(cid, 0) for cid in cids]
            alloc_pos = _distribute_proportional(cids, weights, delta)
            alloc = alloc_pos

        for cid, d in alloc.items():
            if d == 0:
                continue
            c = cand_by_id[cid]
            dno = c.district

            cand_e[cid] = cand_e.get(cid, 0) + d
            cand_total[cid] = cand_total.get(cid, 0) + d

            party_votes_d[dno][p] += d
            party_votes_nat[p] += d
