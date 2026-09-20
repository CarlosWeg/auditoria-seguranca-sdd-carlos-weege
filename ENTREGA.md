# Entrega — Auditoria e Segurança de Sistemas

**Nome do Estudante:** Carlos H. A. Weeege  
**Projeto:** MiniRisk — Avaliação de risco de ativos de TI

## O que foi implementado
- Repositório GitHub com código e documentação.
- Sistema web simples em Flask.
- Engenharia SDD com requisitos, design, tarefas e specs `.sdd` versionadas junto ao código.
- Testes automatizados.
- Container Docker executado como usuário não-root.
- Pipeline no GitHub Actions.
- Scanner principal SonarQube Cloud integrado ao pipeline.
- Scanners adicionais Bandit e pip-audit.
- Deploy automatizado para AWS EC2 via SSH/SCP.
- Health check automático após o deploy.

## Fluxo do pipeline
```text
Push/PR
  -> Ruff
  -> Pytest + Coverage
  -> Bandit
  -> pip-audit
  -> SonarQube
  -> [somente se tudo passar]
  -> Docker Build
  -> Deploy EC2
  -> Health Check
```

## Evidências
Os prints necessários estão enumerados no arquivo `CHECKLIST_PRINTS.md`.
