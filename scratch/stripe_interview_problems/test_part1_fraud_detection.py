from scratch.stripe_interview_problems.part1_fraud_detection import (
    detect_merchant_fraud_status,
)


def test_marks_merchants_fraudulent_at_threshold() -> None:
    result = detect_merchant_fraud_status(
        fraudulent_codes_csv="do_not_honor,stolen_card,lost_card",
        mcc_thresholds=["5812,2", "5411,3"],
        merchants=["acct_a,5812", "acct_b,5411"],
        transactions=[
            "CHARGE,ch_1,acct_a,approved",
            "CHARGE,ch_2,acct_a,stolen_card",
            "CHARGE,ch_3,acct_a,lost_card",
            "CHARGE,ch_4,acct_b,approved",
        ],
    )

    assert result == [
        "acct_a:fraudulent",
        "acct_b:not_fraudulent",
    ]


def test_fraud_status_is_sticky_and_sorted() -> None:
    result = detect_merchant_fraud_status(
        fraudulent_codes_csv="do_not_honor",
        mcc_thresholds=["1111,1", "2222,2"],
        merchants=["merchant_z,1111", "merchant_a,2222"],
        transactions=[
            "CHARGE,ch_1,merchant_z,do_not_honor",
            "CHARGE,ch_2,merchant_z,approved",
            "CHARGE,ch_3,merchant_a,do_not_honor",
            "CHARGE,ch_4,merchant_a,approved",
        ],
    )

    assert result == [
        "merchant_a:not_fraudulent",
        "merchant_z:fraudulent",
    ]