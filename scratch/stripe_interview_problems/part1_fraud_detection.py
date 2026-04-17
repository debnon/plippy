from __future__ import annotations

from collections import defaultdict


def _parse_csv_table(lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        rows.append([segment.strip() for segment in stripped.split(",")])
    return rows


def detect_merchant_fraud_status(
    fraudulent_codes_csv: str,
    mcc_thresholds: list[str],
    merchants: list[str],
    transactions: list[str],
) -> list[str]:
    """Return sorted merchant fraud statuses for Stripe Fraud Detection Part 1.

    Output format: ["account_id:fraudulent", "account_id:not_fraudulent", ...]
    """
    fraudulent_codes = {
        code.strip() for code in fraudulent_codes_csv.split(",") if code.strip()
    }

    mcc_to_threshold: dict[str, int] = {}
    for row in _parse_csv_table(mcc_thresholds):
        if len(row) != 2:
            continue
        mcc, threshold = row
        try:
            mcc_to_threshold[mcc] = int(threshold)
        except ValueError:
            print(f"Invalid threshold for MCC, maybe be a header {mcc}: {threshold}")
            continue

    account_to_mcc: dict[str, str] = {}
    for row in _parse_csv_table(merchants):
        if len(row) != 2:
            continue
        account_id, mcc = row
        account_to_mcc[account_id] = mcc

    fraudulent_counts: dict[str, int] = defaultdict(int)
    fraudulent_accounts: set[str] = set()

    for row in _parse_csv_table(transactions):
        if len(row) != 4:
            continue

        event_type, _charge_id, account_id, response_code = row
        if event_type != "CHARGE":
            continue
        if account_id not in account_to_mcc:
            continue

        if response_code in fraudulent_codes:
            
            fraudulent_counts[account_id] += 1

            mcc = account_to_mcc[account_id]
            
            threshold = mcc_to_threshold.get(mcc)
            if threshold is not None and fraudulent_counts[account_id] >= threshold:
                fraudulent_accounts.add(account_id)

    output: list[str] = []
    for account_id in sorted(account_to_mcc.keys()):
        status = "fraudulent" if account_id in fraudulent_accounts else "not_fraudulent"
        output.append(f"{account_id}:{status}")

    return output