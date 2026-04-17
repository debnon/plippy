from scratch.stripe_interview_problems.part2_percentage_fraud_detection import (
    detect_merchant_fraud_status_by_percentage,
)


def test_marks_fraudulent_when_ratio_meets_threshold_after_minimum() -> None:
    result = detect_merchant_fraud_status_by_percentage(
        fraudulent_codes_csv="stolen_card",
        mcc_thresholds=["5812,0.5"],
        merchants=["acct_a,5812"],
        transactions=[
            "CHARGE,ch_1,acct_a,stolen_card",
            "CHARGE,ch_2,acct_a,stolen_card",
            "CHARGE,ch_3,acct_a,approved",
        ],
        minimum_total_transactions=3,
    )

    assert result == ["acct_a:fraudulent"]


def test_status_is_sticky_even_if_ratio_later_drops() -> None:
    result = detect_merchant_fraud_status_by_percentage(
        fraudulent_codes_csv="do_not_honor",
        mcc_thresholds=["5411,0.8"],
        merchants=["merchant_x,5411"],
        transactions=[
            "CHARGE,ch_1,merchant_x,do_not_honor",
            "CHARGE,ch_2,merchant_x,do_not_honor",
            "CHARGE,ch_3,merchant_x,approved",
            "CHARGE,ch_4,merchant_x,approved",
            "CHARGE,ch_5,merchant_x,approved",
        ],
        minimum_total_transactions=2,
    )

    assert result == ["merchant_x:fraudulent"]


def test_does_not_evaluate_before_minimum_transaction_count() -> None:
    result = detect_merchant_fraud_status_by_percentage(
        fraudulent_codes_csv="lost_card",
        mcc_thresholds=["7999,0.5"],
        merchants=["merchant_a,7999", "merchant_b,7999"],
        transactions=[
            "CHARGE,ch_1,merchant_a,lost_card",
            "CHARGE,ch_2,merchant_a,approved",
            "CHARGE,ch_3,merchant_b,lost_card",
        ],
        minimum_total_transactions=3,
    )

    assert result == [
        "merchant_a:not_fraudulent",
        "merchant_b:not_fraudulent",
    ]