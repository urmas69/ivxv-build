#!/usr/bin/env python3
# rk23_parliament.py
#
# Deterministic reconstruction of the 101 elected members for RK elections
# from:
#  - VOTING_RESULT_IN_COUNTIES.xml  (district quotas, mandates, party & candidate votes incl. E-votes breakdown)
#  #
# Output modes:
#  --out print [default] -> console (grouped, reduced columns)
#  --out csv [file]      -> semicolon CSV with full columns (same regardless of file extension)

import argparse
import math
import csv
import xml.etree.ElementTree as ET
import os
import sys
from collections import defaultdict, namedtuple

Candidate = namedtuple("Candidate",
                       "candidate_id reg_no party_code party_name district forename surname")



def load_candidate_order_optional(path_candidates_xml: str):
    """Return candidateId -> sequenceNumberInAdminUnit if ELECTION_CANDIDATES.xml is available.
    Voting results XML does not include list order; without this, compensation mandate recipient selection
    can differ for low-vote edge cases.
    """
    try:
        tree = ET.parse(path_candidates_xml)
    except Exception:
        return {}
    root = tree.getroot()
    order = {}
    for cand_el in root.iter():
        if ns(cand_el.tag) != "candidate":
            continue
        cid = parse_int(child_text(cand_el, "candidateId", "0"), 0)
        if cid == 0:
            continue
        seqno = parse_int(child_text(cand_el, "sequenceNumberInAdminUnit", "0"), 0)
        if seqno > 0:
            order[cid] = seqno
    return order

def ns(tag):
    # ElementTree returns '{namespace}tag' names; we’ll compare by suffix.
    return tag.split('}', 1)[-1] if '}' in tag else tag


def child_text(el, name, default=""):
    for c in list(el):
        if ns(c.tag) == name:
            return (c.text or "").strip()
    return default


def parse_int(s, default=0):
    try:
        return int(str(s).strip())
    except:
        return default


def parse_float(s, default=0.0):
    try:
        return float(str(s).strip().replace(",", "."))
    except:
        return default


def dH_divisor(k: int) -> float:
    # Modified d’Hondt used in Estonia: divisor(1)=1, divisor(k)=k^0.9 for k>=2
    return 1.0 if k == 1 else (k ** 0.9)


def load_voting(path_voting_xml: str):
    tree = ET.parse(path_voting_xml)
    root = tree.getroot()

    districts = {}  # d -> dict(quota, mandates)
    party_votes_d = defaultdict(lambda: defaultdict(int))  # d -> party -> K votes
    party_votes_nat = defaultdict(int)

    # candidate votes: candidateId -> dict(total, e)
    cand_votes_total = defaultdict(int)
    cand_votes_e = defaultdict(int)

    cand_by_id = {}  # candidateId -> Candidate (metadata from voting XML)

    # Helper to read votesDistributionRow cells
    def cells_map(votes_row_el):
        m = {}
        for cell in votes_row_el:
            if ns(cell.tag) != "votesDistributionCell":
                continue
            name = child_text(cell, "name", "")
            val = parse_int(child_text(cell, "value", "0"), 0)
            if name:
                m[name] = val
        return m

    # Walk districts
    for dist_el in root.iter():
        if ns(dist_el.tag) != "district":
            continue

        dno = parse_int(child_text(dist_el, "districtNumber", "0"), 0)
        if dno == 0:
            continue

        quota = parse_float(child_text(dist_el, "districtSimpleQuota", "0"), 0.0)
        mandates = parse_int(child_text(dist_el, "districtNumberOfMandates", "0"), 0)
        if mandates == 0 and quota == 0:
            # not the right district node
            continue

        districts[dno] = {"quota": quota, "mandates": mandates}

        # Parties in this district
        votes_by_parties_el = None
        for c in list(dist_el):
            if ns(c.tag) == "votesDistributionByParties":
                votes_by_parties_el = c
                break
        if votes_by_parties_el is None:
            continue

        for party_el in list(votes_by_parties_el):
            if ns(party_el.tag) != "party":
                continue
            pname = child_text(party_el, "partyName", "")
            pcode = child_text(party_el, "partyCode", "")
            if not pcode:
                continue

            # Party total rows: rowName "Nimekiri kokku" contains district totals including E-hääled
            total_rows_el = None
            for cc in list(party_el):
                if ns(cc.tag) == "totalRows":
                    total_rows_el = cc
                    break

            if total_rows_el is not None:
                for tr in list(total_rows_el):
                    if ns(tr.tag) != "totalRow":
                        continue
                    if child_text(tr, "rowName", "") != "Nimekiri kokku":
                        continue
                    vr = None
                    for x in list(tr):
                        if ns(x.tag) == "votesDistributionRow":
                            vr = x
                            break
                    if vr is None:
                        continue
                    cm = cells_map(vr)
                    # In practice the keys are "Ringkond kokku" and "E-hääled"
                    k = cm.get("Ringkond kokku", cm.get("K", 0))
                    party_votes_d[dno][pcode] += k
                    party_votes_nat[pcode] += k
                    break

            # Candidate votes in this party in this district
            candidates_el = None
            for cc in list(party_el):
                if ns(cc.tag) == "candidates":
                    candidates_el = cc
                    break
            if candidates_el is None:
                continue

            for cand_el in list(candidates_el):
                if ns(cand_el.tag) != "candidate":
                    continue
                cid = parse_int(child_text(cand_el, "candidateId", "0"), 0)
                if cid == 0:
                    continue
                # Candidate metadata (names + reg number) are present in voting XML
                if cid not in cand_by_id:
                    forename = child_text(cand_el, "forename", "")
                    surname = child_text(cand_el, "surname", "")
                    reg_no = parse_int(child_text(cand_el, "candidateRegNumber", "0"), 0)
                    cand_by_id[cid] = Candidate(cid, reg_no, pcode, pname, dno, forename, surname)
                vr = None
                for x in list(cand_el):
                    if ns(x.tag) == "votesDistributionRow":
                        vr = x
                        break
                if vr is None:
                    continue
                cm = cells_map(vr)
                # Candidate row keys: often "Hääli kokku" + "E-hääled"
                total = cm.get("Hääli kokku", cm.get("K", 0))
                ev = cm.get("E-hääled", cm.get("E", 0))
                cand_votes_total[cid] += total
                cand_votes_e[cid] += ev

    total_valid_votes = sum(party_votes_nat.values())
    return cand_by_id, districts, party_votes_d, party_votes_nat, cand_votes_total, cand_votes_e, total_valid_votes


def eligible_parties(party_votes_nat, total_valid_votes):
    # 5% threshold
    return {p for p, v in party_votes_nat.items() if v / total_valid_votes >= 0.05}


def compute_entitlements(party_votes_nat, elig, seats=101):
    # Modified d’Hondt national entitlements
    # Returns total seats per party
    quotients = []
    for p in elig:
        v = party_votes_nat[p]
        # upper bound: seats
        for k in range(1, seats + 1):
            q = v / dH_divisor(k)
            quotients.append((q, p))
    quotients.sort(reverse=True, key=lambda x: x[0])
    res = defaultdict(int)
    for i in range(seats):
        _, p = quotients[i]
        res[p] += 1
    return res


def compute_elected(cand_by_id, districts, party_votes_d, party_votes_nat, cand_total, cand_e, cand_order, total_valid):
    elig = eligible_parties(party_votes_nat, total_valid)

    # --- Stage 1: personal mandates ---
    elected = {}  # cid -> mandateType
    party_seats_won = defaultdict(int)  # party -> seats already assigned (personal+district)
    party_seats_won_d = defaultdict(lambda: defaultdict(int))  # d -> party -> seats already assigned in district

    for cid, votes in cand_total.items():
        c = cand_by_id.get(cid)
        if not c:
            continue
        d = c.district
        if d not in districts:
            continue
        quota = districts[d]["quota"]
        if quota > 0 and votes >= quota:
            elected[cid] = "PERSONAL"
            party_seats_won[c.party_code] += 1
            party_seats_won_d[d][c.party_code] += 1

    # --- Stage 2: district mandates ---
    for d, info in districts.items():
        quota = info["quota"]
        if quota <= 0:
            continue

        min_cand = 0.10 * quota
        for p in elig:
            v = party_votes_d[d].get(p, 0)
            if v <= 0:
                continue

            base = int(v // quota)
            rem = v - base * quota
            extra = 1 if rem >= 0.75 * quota else 0
            mandates_for_party = base + extra

            mandates_for_party -= party_seats_won_d[d].get(p, 0)
            if mandates_for_party <= 0:
                continue

            candidates_in_party_d = [
                (cid, cand_total.get(cid, 0))
                for cid, c in cand_by_id.items()
                if c.party_code == p and c.district == d and cid in cand_total
            ]
            candidates_in_party_d.sort(key=lambda x: (-x[1], cand_order.get(x[0], 10**9), cand_by_id[x[0]].reg_no))

            for cid, vv in candidates_in_party_d:
                if mandates_for_party == 0:
                    break
                if cid in elected:
                    continue
                if vv < min_cand:
                    continue
                elected[cid] = "DISTRICT"
                party_seats_won[p] += 1
                party_seats_won_d[d][p] += 1
                mandates_for_party -= 1

    # --- Stage 3: compensation mandates ---
    entitlement = compute_entitlements(party_votes_nat, elig, seats=101)

    comp_needed = {p: entitlement[p] - party_seats_won.get(p, 0) for p in elig}

    for p, need in sorted(comp_needed.items()):
        if need <= 0:
            continue

        pool = []
        for cid, c in cand_by_id.items():
            if c.party_code != p:
                continue
            if cid in elected:
                continue
            d = c.district
            info = districts.get(d)
            if not info:
                continue
            quota = info["quota"]
            if quota <= 0:
                continue

            v = cand_total.get(cid, 0)
            if v < 0.05 * quota:
                continue

            order = cand_order.get(cid, 10**9)
            pool.append((order, -v, c.reg_no, cid))

        pool.sort()

        for _, _, _, cid in pool[:need]:
            elected[cid] = "COMPENSATION"
            party_seats_won[p] += 1

    # sanity
    if len(elected) != 101:
        raise SystemExit(f"ERROR: expected 101 elected, got {len(elected)}. Check parsing/keys in XML.")

    return elected


def fmt_pct(num: int, den: int) -> str:
    if den <= 0:
        return "0%"
    return f"{(num * 100.0 / den):.1f}%"


def build_rows(cand_by_id, elected, cand_total, cand_e, cand_order):
    rows = []
    for cid, mtype in elected.items():
        c = cand_by_id[cid]
        total = cand_total.get(cid, 0)
        ev = cand_e.get(cid, 0)
        paper = total - ev
        rows.append(
            {
                "partyCode": c.party_code,
                "partyName": c.party_name,
                "name": f"{c.forename} {c.surname}".strip(),
                "candidateRegNumber": c.reg_no,
                "votes_total": total,
                "votes_paper": paper,
                "votes_e": ev,
                "votes_e_pct": fmt_pct(ev, total),
                "district": c.district,
                "mandateType": mtype,
                "candidateId": cid,
                "nationalOrder": cand_order.get(cid, 0),
            }
        )
    return rows


def derive_party_votes_from_candidates(cand_by_id, cand_votes, districts):
    """Derive party votes per district and nationally by summing candidate votes.

    Used for hypothetical scenarios (paper-only / e-only) where we need party totals.
    """
    party_votes_d = defaultdict(lambda: defaultdict(int))
    party_votes_nat = defaultdict(int)
    for cid, v in cand_votes.items():
        if v <= 0:
            continue
        c = cand_by_id.get(cid)
        if not c:
            continue
        if c.district not in districts:
            continue
        party_votes_d[c.district][c.party_code] += v
        party_votes_nat[c.party_code] += v
    total_valid = sum(party_votes_nat.values())
    return party_votes_d, party_votes_nat, total_valid


def seats_by_party(elected, cand_by_id):
    res = defaultdict(int)
    for cid in elected.keys():
        res[cand_by_id[cid].party_code] += 1
    return dict(res)




def write_print(rows, party_votes_nat, cand_by_id, elected, cand_total, cand_e):
    by_party = defaultdict(list)
    party_name = {}
    for r in rows:
        by_party[r["partyCode"]].append(r)
        party_name[r["partyCode"]] = r.get("partyName", "")

    party_seats = {p: len(lst) for p, lst in by_party.items()}
    parties = sorted(by_party.keys(), key=lambda p: (-party_seats[p], p))

    cols = ["name", "Cand#", "Votes", "eVotes", "eVotes%", "district", "mandateType"]
    for p in parties:
        party_votes = party_votes_nat.get(p, 0)
        party_ev = 0
        for cid, c in cand_by_id.items():
            if c.party_code == p:
                party_ev += cand_e.get(cid, 0)
        party_paper = max(party_votes - party_ev, 0)
        party_ev_pct = fmt_pct(party_ev, party_votes)
        print(f"\n{p}  {party_name.get(p, '')}  seats={party_seats[p]}")
        lst = sorted(
            by_party[p],
            key=lambda r: (
                r["district"],
                0 if r["mandateType"] == "PERSONAL" else 1 if r["mandateType"] == "DISTRICT" else 2,
                r["candidateRegNumber"],
            ),
        )
        table_rows = []
        for r in lst:
            table_rows.append(
                [
                    r["name"],
                    str(r["candidateRegNumber"]),
                    str(r["votes_total"]),
                    str(r["votes_e"]),
                    r["votes_e_pct"],
                    str(r["district"]),
                    r["mandateType"],
                ]
            )

        # Build table (fixed-width) for this party section.
        widths = [len(c) for c in cols]
        for row in table_rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(cell))

        def fmt_row(row):
            return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))

        print(fmt_row(cols))
        print("  ".join("-" * widths[i] for i in range(len(widths))))
        for row in table_rows:
            print(fmt_row(row))

        total_votes = sum(r["votes_total"] for r in by_party[p])
        total_ev = sum(r["votes_e"] for r in by_party[p])
        total_ev_pct = fmt_pct(total_ev, total_votes)
        summary_row = [
            "TOTAL elected",
            "",
            str(total_votes),
            str(total_ev),
            total_ev_pct,
            "",
            "",
        ]
        print("  ".join("-" * widths[i] for i in range(len(widths))))
        print(fmt_row(summary_row))
        party_total_row = [
            "TOTAL",
            "",
            str(party_votes),
            str(party_ev),
            party_ev_pct,
            "",
            "",
        ]
        print(fmt_row(party_total_row))

    print("\nSUMMARY")
    grand_other = 0
    grand_votes = 0
    grand_seats = 0

    summary_rows = []
    for p in sorted(party_votes_nat.keys()):
        votes = party_votes_nat.get(p, 0)
        seats = party_seats.get(p, 0)
        grand_votes += votes
        grand_seats += seats

        other_votes = 0
        for cid, c in cand_by_id.items():
            if c.party_code != p:
                continue
            if cid in elected:
                continue
            other_votes += cand_total.get(cid, 0)
        grand_other += other_votes
        summary_rows.append([p, str(seats), str(votes), str(other_votes)])

    summary_rows.append(["ALL", str(grand_seats), str(grand_votes), str(grand_other)])

    sum_cols = ["party", "seats", "votes_total", "votes_without_mandate"]
    sum_widths = [len(c) for c in sum_cols]
    for row in summary_rows:
        for i, cell in enumerate(row):
            sum_widths[i] = max(sum_widths[i], len(cell))

    def fmt_sum_row(row):
        return "  ".join(cell.ljust(sum_widths[i]) for i, cell in enumerate(row))

    print(fmt_sum_row(sum_cols))
    print("  ".join("-" * sum_widths[i] for i in range(len(sum_widths))))
    for row in summary_rows:
        print(fmt_sum_row(row))

    ref_seats = party_seats.get("REF", 0)
    ee200_seats = party_seats.get("EE200", 0)
    print(f"\nREF+EE200 seats={ref_seats + ee200_seats}")


def write_csv(path_out, rows):
    with open(path_out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(
            [
                "partyCode",
                "name",
                "candidateRegNumber",
                "votes_total",
                "votes_paper",
                "votes_e",
                "partyName",
                "district",
                "mandateType",
                "candidateId",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r["partyCode"],
                    r["name"],
                    r["candidateRegNumber"],
                    r["votes_total"],
                    r["votes_paper"],
                    r["votes_e"],
                    r["partyName"],
                    r["district"],
                    r["mandateType"],
                    r["candidateId"],
                ]
            )


def main():
    ap = argparse.ArgumentParser(description="RK 2023 mandate reconstruction")
    ap.add_argument(
        "--voting",
        default="VOTING_RESULT_IN_COUNTIES.xml",
        help="Path to VOTING_RESULT_IN_COUNTIES.xml (default: %(default)s)",
    )
    ap.add_argument(
        "--candidates",
        default="ELECTION_CANDIDATES.xml",
        help="Path to ELECTION_CANDIDATES.xml (default: %(default)s)",
    )
    ap.add_argument(
        "--out",
        default="print",
        choices=["print", "csv"],
        help="Output mode (default: %(default)s)",
    )
    ap.add_argument(
        "--pie",
        nargs="?",
        const="seats_pies.png",
        default=None,
        help="Write 3 pie charts (paper/actual/e-votes) to PNG (default: %(const)s).",
    )
    ap.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Output file path for --out csv (default: elected_101.csv)",
    )

    args = ap.parse_args()

    if not os.path.exists(args.voting):
        print(f"ERROR: missing file: {args.voting}")
        sys.exit(1)
    if not os.path.exists(args.candidates):
        print(f"ERROR: missing file: {args.candidates}")
        sys.exit(1)

    cand_by_id, districts, party_votes_d, party_votes_nat, cand_total, cand_e, total_valid = load_voting(
        args.voting)

    cand_order = load_candidate_order_optional(args.candidates)

    elected = compute_elected(
        cand_by_id,
        districts,
        party_votes_d,
        party_votes_nat,
        cand_total,
        cand_e,
        cand_order,
        total_valid,
    )

    rows = build_rows(cand_by_id, elected, cand_total, cand_e, cand_order)

    party_mandates = defaultdict(int)
    for r in rows:
        party_mandates[r["partyCode"]] += 1
    party_order = {
        p: i for i, (p, _) in enumerate(sorted(party_mandates.items(), key=lambda kv: (-kv[1], kv[0])))
    }

    rows.sort(
        key=lambda r: (
            party_order.get(r["partyCode"], 10**9),
            -r["votes_total"],
            r["district"],
            r["candidateRegNumber"],
        )
    )

    if args.out == "print":
        write_print(rows, party_votes_nat, cand_by_id, elected, cand_total, cand_e)
    elif args.out == "csv":
        out = args.output or "elected_101.csv"
        write_csv(out, rows)
        print(f"OK: wrote {out} (101 rows)")

    if args.pie:
        try:
            from plot_utils import plot_seat_pies
        except ModuleNotFoundError:
            print("ERROR: matplotlib is required for --pie.")
            print("Install: pip install matplotlib")
            sys.exit(1)

        seats_actual = seats_by_party(elected, cand_by_id)

        # Paper-only scenario
        cand_paper = {cid: max(0, cand_total.get(cid, 0) - cand_e.get(cid, 0)) for cid in cand_by_id.keys()}
        pv_d_p, pv_n_p, tv_p = derive_party_votes_from_candidates(cand_by_id, cand_paper, districts)
        elected_paper = compute_elected(cand_by_id, districts, pv_d_p, pv_n_p, cand_paper, defaultdict(int), cand_order, tv_p)
        seats_paper = seats_by_party(elected_paper, cand_by_id)

        # E-votes-only scenario
        cand_ev = {cid: cand_e.get(cid, 0) for cid in cand_by_id.keys()}
        pv_d_e, pv_n_e, tv_e = derive_party_votes_from_candidates(cand_by_id, cand_ev, districts)
        elected_ev = compute_elected(cand_by_id, districts, pv_d_e, pv_n_e, cand_ev, cand_ev, cand_order, tv_e)
        seats_e = seats_by_party(elected_ev, cand_by_id)

        party_name_by_code = {}
        for c in cand_by_id.values():
            if c.party_code and c.party_name:
                party_name_by_code[c.party_code] = c.party_name

        try:
            plot_seat_pies(args.pie, party_name_by_code, seats_paper, seats_actual, seats_e)
        except ModuleNotFoundError as e:
            print("ERROR: matplotlib is required for --pie.")
            print("Install: pip install matplotlib")
            sys.exit(1)
        print(f"OK: wrote pie {args.pie}")


if __name__ == "__main__":
    main()
