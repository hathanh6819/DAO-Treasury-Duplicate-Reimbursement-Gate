#!/usr/bin/env python3
"""Prove that reassessment can revoke a formerly clear authorization."""

import getpass
import time

from genlayer_py import create_account, create_client, studionet

from run_studionet_v2_reassessment import (
    AUTHORITY, CONTROLLER, TOKEN, as_int, checkpoint, read, sha, write,
)


def main():
    ka = getpass.getpass("Authority test private key: ").strip()
    kb = getpass.getpass("Controller test private key: ").strip()
    a = create_account(ka); b = create_account(kb); ka = kb = ""
    checkpoint(str(a.address).lower() == AUTHORITY.lower(), "authority wallet matches")
    checkpoint(str(b.address).lower() == CONTROLLER.lower(), "controller wallet matches")
    ca = create_client(chain=studionet, account=a)
    cb = create_client(chain=studionet, account=b)
    checkpoint(as_int(read(ca, "get_count")) == 5, "starts after multi-arrival lifecycle")
    now = int(time.time())
    action = sha("reviewer-v2-duplicate-action-f")
    common = ["DUPLICATE_DAO", "VENDOR_RED", a.address, TOKEN]
    original = common + [
        88000, now - 45 * 86400, now - 15 * 86400,
        sha("reviewer-v2-duplicate-invoice-f"),
        "Complete migration of the DAO treasury reporting database from the legacy schema to version two during August 2026.",
        action, 604800,
    ]
    rebill = common + [
        91000, now - 43 * 86400, now - 13 * 86400,
        sha("reviewer-v2-duplicate-invoice-g"),
        "Final delivery for migrating the treasury reporting database from its legacy schema to version two, rebilled under a new invoice.",
        sha("reviewer-v2-duplicate-action-g"), 604800,
    ]
    txs = {}
    txs["submit_f"] = write(ca, "submit_claim", original)
    txs["assess_f_initial"] = write(ca, "assess_claim", [6, 1])
    f = read(ca, "get_claim", [6])
    checkpoint(f.get("status") == "CLEAR" and as_int(f.get("revision")) == 2, "claim F initially clear")
    txs["submit_g_rebill"] = write(ca, "submit_claim", rebill)
    f = read(ca, "get_claim", [6])
    checkpoint(f.get("status") == "PENDING" and as_int(f.get("revision")) == 3, "rebill reopens F")
    txs["reassess_f"] = write(ca, "assess_claim", [6, 3])
    f = read(ca, "get_claim", [6])
    checkpoint(f.get("status") == "DUPLICATE" and as_int(f.get("revision")) == 4, "reassessment revokes F as duplicate")
    checkpoint(f.get("compared_ids") == [7], "duplicate decision records new claim G")
    txs["blocked_consume_f"] = write(cb, "consume_authorization", [6, 4, action])
    checkpoint(read(ca, "get_claim", [6]) == f and not f.get("consumed"), "duplicate authorization cannot be consumed")
    print("DUPLICATE_REASSESSMENT_COMPLETE", flush=True)
    print("transactions=" + __import__("json").dumps(txs, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
