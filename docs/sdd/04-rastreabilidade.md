# SDD — 4. Matriz de rastreabilidade

| Requisito | Implementação | Verificação |
|---|---|---|
| RF01-RF05 — coletar fatores | `app/templates/index.html`, `app/main.py` | `tests/test_web.py` |
| RF06-RF08 — calcular/classificar/recomendar | `app/risk.py` | `tests/test_risk.py` |
| RF09 — health check | `app/main.py:/healthz` | `tests/test_web.py` + etapa `Verify deployment` |
| RS01 — sem persistência | arquitetura sem banco/arquivo de dados | revisão de design |
| RS02 — validação server-side | `app/main.py` | testes web |
| RS03 — CSRF | `app/main.py` + token no formulário | `test_analysis_requires_csrf` |
| RS04 — headers de segurança | `add_security_headers()` | `test_home_and_security_headers` |
| RS05 — limite de requisição | `MAX_CONTENT_LENGTH` | revisão de código/SonarQube |
| RS06 — segredos fora do Git | GitHub Actions Secrets + `.gitignore` | revisão do repositório |
| RS07 — container não-root | `Dockerfile` (`USER appuser`) | revisão da imagem/Dockerfile |
| RS08 — deploy bloqueado | `deploy.needs: quality-security` + Quality Gate | GitHub Actions |
