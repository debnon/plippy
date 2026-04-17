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


def detect_merchant_fraud_status_by_percentage(
    fraudulent_codes_csv: str,
    mcc_thresholds: list[str],
    merchants: list[str],
    transactions: list[str],
    minimum_total_transactions: int,
) -> list[str]:
    """Return sorted merchant fraud statuses for Stripe Fraud Detection Part 2.

    Each MCC threshold is a fraction in [0, 1]. A merchant becomes fraudulent when:
    fraud_count / total_count >= mcc_threshold, once total_count >= minimum_total_transactions.
    """
    if minimum_total_transactions <= 0:
        raise ValueError("minimum_total_transactions must be > 0")

    fraudulent_codes = {
        code.strip() for code in fraudulent_codes_csv.split(",") if code.strip()
    }

    mcc_to_threshold: dict[str, float] = {}
    for row in _parse_csv_table(mcc_thresholds):
        if len(row) != 2:
            continue

        mcc, threshold_raw = row
        try:
            threshold = float(threshold_raw)
        except ValueError:
            continue

        if 0.0 <= threshold <= 1.0:
            mcc_to_threshold[mcc] = threshold

    account_to_mcc: dict[str, str] = {}
    for row in _parse_csv_table(merchants):
        if len(row) != 2:
            continue
        account_id, mcc = row
        account_to_mcc[account_id] = mcc

    total_counts: dict[str, int] = defaultdict(int)
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

        total_counts[account_id] += 1
        if response_code in fraudulent_codes:
            fraudulent_counts[account_id] += 1

        if account_id in fraudulent_accounts:
            continue
        if total_counts[account_id] < minimum_total_transactions:
            continue

        mcc = account_to_mcc[account_id]
        threshold = mcc_to_threshold.get(mcc)
        if threshold is None:
            continue

        if (fraudulent_counts[account_id] / total_counts[account_id]) >= threshold:
            fraudulent_accounts.add(account_id)

    output: list[str] = []
    for account_id in sorted(account_to_mcc.keys()):
        status = "fraudulent" if account_id in fraudulent_accounts else "not_fraudulent"
        output.append(f"{account_id}:{status}")

    return output