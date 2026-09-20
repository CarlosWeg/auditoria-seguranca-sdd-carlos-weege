# SDD — 1. Requisitos

**Projeto:** MiniRisk  
**Estudante:** Carlos H. A. Weeege  
**Disciplina:** Auditoria e Segurança de Sistemas

## Objetivo
Construir um sistema web simples que permita avaliar o risco de um ativo de TI e, simultaneamente, demonstrar um fluxo de desenvolvimento orientado por especificação, testes, análise de segurança e implantação automatizada.

## Histórias de usuário
1. Como analista, quero informar fatores de risco de um ativo para receber uma classificação simples.
2. Como analista, quero visualizar recomendações relacionadas ao risco identificado.
3. Como responsável técnico, quero que entradas inválidas sejam rejeitadas no servidor.
4. Como responsável técnico, quero que o código seja testado e analisado por scanners antes de qualquer deploy.
5. Como avaliador da disciplina, quero visualizar evidências do pipeline, SonarQube e ambiente AWS.

## Requisitos funcionais
- RF01: coletar nome do ativo.
- RF02: coletar exposição (interna ou Internet).
- RF03: coletar presença de dados sensíveis.
- RF04: coletar presença de MFA administrativo.
- RF05: coletar criticidade (baixa, média ou alta).
- RF06: calcular pontuação de 0 a 11.
- RF07: classificar risco em Baixo, Médio ou Alto.
- RF08: exibir recomendações de mitigação.
- RF09: disponibilizar endpoint `/healthz` para monitoramento do deploy.

## Requisitos de segurança
- RS01: não persistir os dados informados.
- RS02: usar validação server-side.
- RS03: proteger POST contra CSRF.
- RS04: utilizar cabeçalhos HTTP de segurança.
- RS05: limitar tamanho das requisições.
- RS06: manter segredos fora do Git.
- RS07: executar o contêiner com usuário não-root.
- RS08: bloquear deploy quando testes/scanners falharem.

## Critérios de aceite
- Cenário de maior risco deve produzir 11 pontos e nível Alto.
- POST sem CSRF válido deve retornar HTTP 400.
- `/healthz` deve retornar HTTP 200 e `status=ok`.
- Pipeline deve executar testes, Ruff, Bandit, pip-audit e SonarQube.
- Job de deploy só pode iniciar após sucesso do job de qualidade/segurança.
