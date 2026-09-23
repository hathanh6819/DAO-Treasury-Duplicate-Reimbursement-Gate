#!/usr/bin/env python3
"""Prove that every newer relevant claim is included before consumption."""

import getpass
import time

from genlayer_py import create_account, create_client, studionet

from run_studionet_v2_reassessment import (
    AUTHORITY,
    CONTROLLER,
    TOKEN,
    as_int,
    checkpoint,
    read,
    sha,
    write,
)


def main():
    authority_key = getpass.getpass("Authority test private key: ").strip()
    controller_key = getpass.getpass("Controller test private key: ").strip()
    authority = create_account(authority_key)
    controller = create_account(controller_key)
    authority_key = controller_key = ""
    checkpoint(str(authority.address).lower() == AUTHORITY.lower(), "authority wallet matches")
    checkpoint(str(controller.address).lower() == CONTROLLER.lower(), "controller wallet matches")
    ca = create_client(chain=studionet, account=authority)
    cb = create_client(chain=studionet, account=controller)
    checkpoint(as_int(read(ca, "get_count")) == 2, "starts after reviewer lifecycle")

    now = int(time.time())
    action_c = sha("reviewer-v2-multi-action-c-2026-09-22")
    common = ["MULTI_DAO", "VENDOR_GREEN", authority.address, TOKEN]
    claim_c = common + [
        91000, now - 90 * 86400, now - 61 * 86400,
        sha("reviewer-v2-multi-invoice-c"),
        "Accessibility review of the DAO member portal for keyboard navigation and screen reader support during June 2026.",
        action_c, 604800,
    ]
    claim_d = common + [
        37000, now - 60 * 86400, now - 31 * 86400,
        sha("reviewer-v2-multi-invoice-d"),
        "Design and delivery of three community moderator training workshops during July 2026, excluding accessibility review work.",
        sha("reviewer-v2-multi-action-d"), 604800,
    ]
    claim_e = common + [
        52000, now - 30 * 86400, now - 1 * 86400,
        sha("reviewer-v2-multi-invoice-e"),
        "Preparation of the August 2026 treasury tax reconciliation workbook, excluding portal review and moderator training services.",
        sha("reviewer-v2-multi-action-e"), 604800,
    ]
    txs = {}
    txs["submit_c"] = write(ca, "submit_claim", claim_c)
    txs["assess_c_initial"] = write(ca, "assess_claim", [3, 1])
    c = read(ca, "get_claim", [3])
    checkpoint(c.get("status") == "CLEAR" and as_int(c.get("revision")) == 2, "claim C initially clear")

    txs["submit_d"] = write(ca, "submit_claim", claim_d)
    c = read(ca, "get_claim", [3])
    checkpoint(as_int(c.get("revision")) == 3 and c.get("reassessment_scope") == [4], "first arrival reopens C")

    txs["submit_e"] = write(ca, "submit_claim", claim_e)
    c = read(ca, "get_claim", [3])
    checkpoint(as_int(c.get("revision")) == 4, "second arrival invalidates in-flight revision")
    checkpoint(c.get("reassessment_scope") == [4, 5], "scope contains both newer claims")

    txs["stale_reassess_c"] = write(ca, "assess_claim", [3, 3])
    checkpoint(read(ca, "get_claim", [3]) == c, "stale reassessment leaves C unchanged")

    txs["reassess_c_all"] = write(ca, "assess_claim", [3, 4])
    c = read(ca, "get_claim", [3])
    checkpoint(c.get("status") == "CLEAR" and as_int(c.get("revision")) == 5, "C reassessed at current revision")
    checkpoint(c.get("compared_ids") == [4, 5], "both newer claims recorded as compared")
    checkpoint(c.get("reassessment_scope") == [], "multi-arrival scope completed")

    txs["consume_c"] = write(cb, "consume_authorization", [3, 5, action_c])
    checkpoint(read(ca, "get_claim", [3]).get("consumed") is True, "C consumes only after both comparisons")
    print("MULTI_ARRIVAL_COMPLETE", flush=True)
    print("transactions=" + __import__("json").dumps(txs, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
