# SDD — 2. Design

## Arquitetura

```text
Usuário
  |
  v
HTTP :80
  |
AWS EC2 (Ubuntu)
  |
Docker container: MiniRisk / Gunicorn / Flask
  |                      |
  |                      +--> /healthz
  +--> formulário --> motor de risco (sem banco de dados)

GitHub Push
  |
  v
GitHub Actions
  +--> Ruff
  +--> Pytest + Coverage
  +--> Bandit (SAST)
  +--> pip-audit (dependências)
  +--> SonarQube Cloud (qualidade + segurança)
  |
  +-- somente se aprovado --> Docker build --> SCP/SSH --> EC2 --> health check
```

## Componentes
- `app/main.py`: rotas HTTP, validação, CSRF e cabeçalhos de segurança.
- `app/risk.py`: regras puras do cálculo de risco.
- `tests/`: testes unitários e de integração da camada web.
- `Dockerfile`: imagem de execução não-root.
- `.github/workflows/ci-cd.yml`: pipeline CI/CD e scanner SonarQube.

## Modelo de ameaça resumido
| Ameaça | Controle adotado |
|---|---|
| Entrada malformada | listas permitidas, limites de tamanho e autoescape do template |
| CSRF | token de sessão comparado com `compare_digest` |
| Clickjacking | `X-Frame-Options: DENY` + `frame-ancestors 'none'` |
| MIME sniffing | `X-Content-Type-Options: nosniff` |
| Execução de código vulnerável | Bandit + SonarQube |
| Dependência vulnerável | pip-audit |
| Segredo exposto no Git | segredos somente em GitHub Actions Secrets |
| Deploy de build reprovado | dependência explícita entre jobs `quality-security` e `deploy` |

## Decisões de design
- Não há banco de dados: o objetivo acadêmico é demonstrar SDD, segurança e CI/CD sem aumentar desnecessariamente a superfície de ataque.
- O deploy usa uma única EC2 para manter o exercício reproduzível e barato.
- O SonarQube Cloud é usado no pipeline para evitar manter um servidor SonarQube adicional apenas para a atividade.
