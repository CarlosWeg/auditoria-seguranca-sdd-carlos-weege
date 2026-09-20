from app.risk import RiskInput, evaluate_risk


def test_low_risk():
    result = evaluate_risk(RiskInput("Intranet", "internal", False, True, "low"))
    assert result.score == 0
    assert result.level == "Baixo"


def test_high_risk():
    result = evaluate_risk(RiskInput("Portal", "internet", True, False, "high"))
    assert result.score == 11
    assert result.level == "Alto"
    assert len(result.recommendations) >= 4


def test_medium_risk_boundary():
    result = evaluate_risk(RiskInput("API", "internet", False, False, "medium"))
    assert result.score == 6
    assert result.level == "Médio"
