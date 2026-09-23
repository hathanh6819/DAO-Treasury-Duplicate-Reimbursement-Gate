#!/usr/bin/env python3
"""Reviewer-specific Studionet v2 reassessment lifecycle. Never deploys."""

import getpass
import hashlib
import json
import time

from genlayer_py import create_account, create_client, studionet
from genlayer_py.types.transactions import TransactionStatus


CONTRACT = "0xF6cF059A3bFa4e8F8B01Db976387f32324DBc477"
AUTHORITY = "0x1D283b45974B0be9630DFD1deC6A62a9B72B2760"
CONTROLLER = "0xf96Cf822F9f4e76956AB9fAAa22B3BdCD7b10aD6"
TOKEN = "0x0000000000000000000000000000000000001001"


def sha(label):
    return "sha256:" + hashlib.sha256(label.encode()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def checkpoint(condition, message):
    if not condition:
        raise RuntimeError("CHECKPOINT FAILED: " + message)
    print("CHECKPOINT OK: " + message, flush=True)


def as_int(value):
    return int(value)


def read(client, method, args=None):
    result = client.read_contract(
        address=CONTRACT, function_name=method, args=args or []
    )
    print("READ " + method + "=" + canonical(result), flush=True)
    return result


def write(client, method, args, timeout=1200):
    tx = None
    for attempt in range(1, 7):
        try:
            tx = client.write_contract(
                address=CONTRACT, function_name=method, args=args, value=0
            )
            break
        except Exception as exc:
            if attempt == 6:
                raise
            print("RPC RETRY send " + method + " attempt=" + str(attempt), flush=True)
            time.sleep(10)
    assert tx is not None
    print("WRITE " + method + " tx=" + str(tx), flush=True)
    receipt = None
    for attempt in range(1, 7):
        try:
            receipt = client.wait_for_transaction_receipt(
                tx,
                status=TransactionStatus.FINALIZED,
                interval=3000,
                retries=max(1, timeout // 3),
                full_transaction=False,
            )
            break
        except Exception:
            if attempt == 6:
                raise
            print("RPC RETRY receipt " + method + " attempt=" + str(attempt), flush=True)
            time.sleep(10)
    assert receipt is not None
    status = str(receipt.get("status_name", receipt.get("status", ""))).upper()
    execution = str(
        receipt.get(
            "result_name",
            receipt.get(
                "result",
                receipt.get("tx_execution_result_name", ""),
            ),
        )
    ).upper()
    print(
        "FINAL " + method + " status=" + status + " execution=" + execution,
        flush=True,
    )
    checkpoint("FAILED" not in status and "ERROR" not in execution, method + " finalized")
    return str(tx)


def main():
    authority_key = getpass.getpass("Authority test private key: ").strip()
    controller_key = getpass.getpass("Controller test private key: ").strip()
    authority = create_account(authority_key)
    controller = create_account(controller_key)
    authority_key = controller_key = ""

    checkpoint(str(authority.address).lower() == AUTHORITY.lower(), "authority wallet matches")
    checkpoint(str(controller.address).lower() == CONTROLLER.lower(), "controller wallet matches")

    authority_client = create_client(chain=studionet, account=authority)
    controller_client = create_client(chain=studionet, account=controller)
    protocol = read(authority_client, "get_protocol")
    checkpoint(protocol.get("version") == 2, "deployed protocol is version 2")
    checkpoint(protocol.get("authority", "").lower() == AUTHORITY.lower(), "authority bound")
    checkpoint(protocol.get("controller", "").lower() == CONTROLLER.lower(), "controller bound")
    checkpoint(as_int(read(authority_client, "get_count")) == 0, "fresh v2 deployment")

    now = int(time.time())
    action_a = sha("reviewer-v2-action-a-2026-09-22")
    common = ["REVIEWER_DAO", "VENDOR_BLUE", authority.address, TOKEN]
    claim_a = common + [
        125000,
        now - 60 * 86400,
        now - 30 * 86400,
        sha("reviewer-v2-invoice-a-2026-09-22"),
        "Independent security audit of treasury multisig configuration completed for July 2026, including signer and threshold review.",
        action_a,
        604800,
    ]
    claim_b = common + [
        46000,
        now - 29 * 86400,
        now - 1 * 86400,
        sha("reviewer-v2-invoice-b-2026-09-22"),
        "Vietnamese translation and localization of the community governance handbook for August 2026; no security audit services were included.",
        sha("reviewer-v2-action-b-2026-09-22"),
        604800,
    ]

    txs = {}
    txs["submit_a"] = write(authority_client, "submit_claim", claim_a)
    a = read(authority_client, "get_claim", [1])
    checkpoint(a.get("status") == "PENDING" and as_int(a.get("revision")) == 1, "claim A pending revision 1")

    txs["assess_a_initial"] = write(authority_client, "assess_claim", [1, 1])
    a = read(authority_client, "get_claim", [1])
    checkpoint(a.get("status") == "CLEAR" and as_int(a.get("revision")) == 2, "claim A initially clear")

    txs["submit_b"] = write(authority_client, "submit_claim", claim_b)
    a = read(authority_client, "get_claim", [1])
    checkpoint(a.get("status") == "PENDING", "new claim atomically reopens A")
    checkpoint(a.get("reason") == "NEW_RELEVANT_CLAIM_REQUIRES_REASSESSMENT", "reviewer reason recorded")
    checkpoint(a.get("assessment_mode") == "REASSESSMENT", "reassessment mode recorded")
    checkpoint(as_int(a.get("revision")) == 3 and 2 in [as_int(x) for x in a.get("reassessment_scope", [])], "revision and scope include B")

    txs["stale_consume_a"] = write(
        controller_client, "consume_authorization", [1, 2, action_a]
    )
    a_after_stale = read(authority_client, "get_claim", [1])
    checkpoint(a_after_stale == a and not a_after_stale.get("consumed"), "stale revision cannot consume A")

    txs["reassess_a"] = write(authority_client, "assess_claim", [1, 3])
    a = read(authority_client, "get_claim", [1])
    checkpoint(a.get("status") == "CLEAR", "reassessment restores A to clear")
    checkpoint(as_int(a.get("revision")) == 4, "reassessment publishes revision 4")
    checkpoint(2 in [as_int(x) for x in a.get("compared_ids", [])], "reassessment records comparison with B")
    checkpoint(a.get("assessment_mode") == "COMPLETE" and a.get("reassessment_scope") == [], "reassessment scope completed")

    txs["consume_a_current"] = write(
        controller_client, "consume_authorization", [1, 4, action_a]
    )
    consumed = read(authority_client, "get_claim", [1])
    checkpoint(consumed.get("consumed") is True, "current exact authorization consumed once")

    txs["replay_consume_a"] = write(
        controller_client, "consume_authorization", [1, 4, action_a]
    )
    checkpoint(read(authority_client, "get_claim", [1]) == consumed, "consume replay leaves state unchanged")

    print("LIFECYCLE_COMPLETE", flush=True)
    print("transactions=" + canonical(txs), flush=True)


if __name__ == "__main__":
    main()
