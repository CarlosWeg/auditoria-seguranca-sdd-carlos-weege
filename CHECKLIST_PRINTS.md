# Checklist de prints para a entrega

A atividade será entregue por printscreens. A sequência abaixo foi pensada para provar cada requisito com o menor número possível de imagens.

## Print 1 — Repositório GitHub
**Tela:** página inicial do repositório.  
**Deve aparecer:**
- nome do repositório;
- seu usuário GitHub;
- pastas `app`, `docs`, `infra`, `tests` e `.github`;
- arquivos `README.md`, `minirisk.sdd` e `Dockerfile`.

**Prova:** repositório criado e projeto versionado.

---

## Print 2 — Evidência do SDD
**Tela:** GitHub abrindo `docs/sdd/01-requisitos.md`.  
**Deve aparecer:** título, estudante, requisitos e critérios de aceite.

Se puder mandar um print adicional, abra também `docs/sdd/02-design.md` mostrando o diagrama e o modelo de ameaça.

**Prova:** desenvolvimento orientado por especificação/SDD antes da implementação.

---

## Print 3 — Pipeline inteiro verde
**Tela:** GitHub → Actions → execução mais recente do workflow `CI Security and Deploy`.  
**Deve aparecer:**
- `Quality and Security` verde;
- `Deploy to AWS EC2` verde.

**Prova:** pipeline CI/CD e bloqueio por dependência entre jobs.

---

## Print 4 — Scanners dentro do pipeline
**Tela:** abra o job `Quality and Security`.  
**Deve aparecer na mesma tela, se possível:**
- `Bandit SAST`;
- `Dependency audit`;
- `SonarQube Cloud scan`;
- `Tests and coverage`.

**Prova:** segurança integrada ao processo de deploy.

---

## Print 5 — Dashboard do SonarQube
**Tela:** SonarQube Cloud → projeto MiniRisk → Overview/Summary.  
**Deve aparecer:**
- nome do projeto;
- status do Quality Gate;
- métricas de segurança/qualidade, como vulnerabilities, security hotspots, bugs/code smells e coverage.

**Prova:** scanner SonarQube executado e analisando o repositório.

---

## Print 6 — EC2 executando
**Tela:** AWS Console → EC2 → Instances.  
**Deve aparecer:**
- instância `minirisk-sdd`;
- estado `Running`;
- tipo da instância;
- Public IPv4/DNS.

**Prova:** ambiente hospedado na AWS.

---

## Print 7 — Security Group
**Tela:** AWS → Security Group da instância → Inbound rules.  
**Deve aparecer:**
- TCP/22 com origem **My IP** (faça essa restrição depois do deploy);
- TCP/80 com origem `0.0.0.0/0`.

**Prova:** configuração básica de acesso ao servidor e aplicação.

> Não precisa mostrar nenhum segredo, chave `.pem` ou token.

---

## Print 8 — Sistema funcionando na AWS
**Tela:** navegador em `http://IP_DA_EC2/`.  
Preencha:
- Portal do Cliente;
- Internet;
- Alta;
- Dados sensíveis = Sim;
- MFA = Não.

Tire o print depois de clicar em **Calcular risco**.

**Deve aparecer:**
- URL/IP da AWS no navegador;
- `MiniRisk`;
- `Risco Alto`;
- `11/11`;
- recomendações.

**Prova:** sistema efetivamente implantado e funcional.

---

## Print 9 — Health check do deploy (opcional, excelente evidência)
**Tela:** navegador em `http://IP_DA_EC2/healthz` ou passo `Verify deployment` aberto no GitHub Actions.  
**Deve aparecer:** `status: ok` ou o comando `curl` concluindo com sucesso.

**Prova:** pipeline validou a implantação automaticamente.

---

# Ordem recomendada de entrega
Se o professor limitar a quantidade de prints, use estes **6 essenciais**:
1. GitHub/repositório.
2. SDD/requisitos.
3. GitHub Actions com dois jobs verdes.
4. Job de segurança mostrando SonarQube/Bandit/pip-audit.
5. SonarQube Dashboard.
6. Aplicação na AWS com resultado 11/11.

Se não houver limite, envie os 8 ou 9 prints.
