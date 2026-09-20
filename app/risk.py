from dataclasses import dataclass
from typing import Literal

Exposure = Literal["internal", "internet"]
Criticality = Literal["low", "medium", "high"]


@dataclass(frozen=True)
class RiskInput:
    asset_name: str
    exposure: Exposure
    sensitive_data: bool
    mfa_enabled: bool
    criticality: Criticality


@dataclass(frozen=True)
class RiskResult:
    score: int
    level: str
    recommendations: tuple[str, ...]


def evaluate_risk(data: RiskInput) -> RiskResult:
    """Return a deterministic risk score and actionable recommendations."""
    score = 0
    recommendations: list[str] = []

    if data.exposure == "internet":
        score += 3
        recommendations.append("Restringir a superfície exposta e revisar regras de firewall/WAF.")

    if data.sensitive_data:
        score += 3
        recommendations.append(
            "Aplicar criptografia em trânsito e em repouso aos dados sensíveis."
        )

    if not data.mfa_enabled:
        score += 2
        recommendations.append("Habilitar MFA para contas administrativas e acessos privilegiados.")

    criticality_score = {"low": 0, "medium": 1, "high": 3}[data.criticality]
    score += criticality_score

    if data.criticality == "high":
        recommendations.append(
            "Definir backup, restauração testada e plano de resposta a incidentes."
        )

    if score <= 3:
        level = "Baixo"
    elif score <= 6:
        level = "Médio"
    else:
        level = "Alto"

    if not recommendations:
        recommendations.append("Manter controles atuais e revisar o risco periodicamente.")

    return RiskResult(score=score, level=level, recommendations=tuple(recommendations))
