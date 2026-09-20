# MiniRisk — SDD + DevSecOps + AWS

**Estudante:** Carlos H. A. Weeege  
**Disciplina:** Auditoria e Segurança de Sistemas

Projeto acadêmico de um sistema web simples de avaliação de risco, desenvolvido de forma **Spec-Driven Development (SDD)** e entregue com **CI/CD**, **scanner de segurança SonarQube Cloud**, scanners adicionais e **deploy automatizado em AWS EC2**.

## Requisitos da atividade atendidos

| Requisito | Implementação |
|---|---|
| Repositório GitHub | Estrutura pronta para push, incluindo `.github/workflows` |
| Sistema simples usando SDD | `minirisk.sdd`, specs locais e `docs/sdd/01..03` |
| Ambiente AWS | Docker em uma EC2 Ubuntu |
| Pipeline | GitHub Actions em `.github/workflows/ci-cd.yml` |
| Scanner de segurança | SonarQube Cloud + Bandit + pip-audit |
| Deploy automatizado | Docker build → SCP/SSH → EC2 → health check |

## O sistema
O MiniRisk recebe cinco fatores de um ativo de TI e calcula uma pontuação de 0 a 11. O resultado é classificado como risco Baixo, Médio ou Alto e inclui recomendações de mitigação.

Nenhum dado informado pelo usuário é persistido.

## Executar localmente

### Windows PowerShell
```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run-local.ps1
```

### Linux/macOS
```bash
./scripts/run-local.sh
```

Acesse: `http://127.0.0.1:8000`

## Testar manualmente sem script
```bash
python -m venv .venv
# Ative o ambiente virtual
pip install -r requirements-dev.txt
python -m pytest --cov=app
ruff check .
bandit -c pyproject.toml -r app
pip-audit -r requirements.txt
```

## Segurança implementada na aplicação
- Validação server-side de campos e valores enumerados.
- CSRF token em formulário POST.
- Limite de corpo de requisição.
- Autoescape do Jinja para conteúdo exibido.
- CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy` e `Permissions-Policy`.
- Segredos recebidos apenas por variável de ambiente.
- Container Docker executado com usuário não-root.
- Sem banco de dados nem persistência de informações do formulário.

## CI/CD
O job **Quality and Security** executa, nesta ordem:
1. Ruff.
2. Pytest + coverage.
3. Bandit SAST.
4. pip-audit.
5. SonarQube Cloud.

O job **Deploy to AWS EC2** depende do sucesso completo do primeiro job. Se qualquer teste ou scanner falhar, o deploy não acontece.

## Próximos passos
Siga exatamente `MANUAL_IMPLEMENTACAO.md` e depois `CHECKLIST_PRINTS.md`. A matriz `docs/sdd/04-rastreabilidade.md` relaciona requisitos, código e verificações.
