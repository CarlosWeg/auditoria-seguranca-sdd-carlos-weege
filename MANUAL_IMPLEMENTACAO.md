# Manual de implementação — MiniRisk

**Estudante:** Carlos H. A. Weeege  
**Disciplina:** Auditoria e Segurança de Sistemas

Este manual descreve somente as intervenções que dependem das suas contas no GitHub, SonarQube Cloud e AWS. O código, Dockerfile, SDD, testes e pipeline já estão prontos.

---

## 0. O que você vai precisar
- Conta no GitHub.
- Conta AWS com permissão para criar uma EC2, Security Group e Key Pair.
- Conta no SonarQube Cloud, preferencialmente entrando com GitHub.
- Git instalado no computador.

> Para esta atividade, recomendo criar o repositório GitHub como **Public**. Isso facilita a integração acadêmica e o uso do SonarQube Cloud.

---

## 1. Testar o projeto localmente (opcional, mas recomendado)

No Windows PowerShell, dentro da pasta do projeto:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\run-local.ps1
```

Depois abra:

```text
http://127.0.0.1:8000
```

Faça um teste com:
- Nome: `Portal do Cliente`
- Exposição: `Exposto à Internet`
- Criticidade: `Alta`
- Dados sensíveis: `Sim`
- MFA: `Não`

O resultado esperado é **Risco Alto — 11/11**.

---

## 2. Criar o repositório GitHub

No GitHub:
1. Clique em **New repository**.
2. Nome sugerido: `auditoria-seguranca-sdd-carlos-weege`.
3. Escolha **Public**.
4. NÃO marque criação automática de README, `.gitignore` ou licença.
5. Clique em **Create repository**.

No terminal, dentro desta pasta:

```bash
git init
git branch -M main
git add .
git commit -m "feat: projeto MiniRisk SDD com pipeline DevSecOps"
git remote add origin https://github.com/SEU_USUARIO/auditoria-seguranca-sdd-carlos-weege.git
git push -u origin main
```

Troque apenas `SEU_USUARIO`.

Neste momento o Actions ficará vermelho, pois ainda faltam SonarQube e AWS. Isso é esperado.

---

## 3. Configurar o SonarQube Cloud

1. Acesse o **SonarQube Cloud** e entre usando GitHub.
2. Importe/crie um projeto a partir do repositório `auditoria-seguranca-sdd-carlos-weege`. O repositório já contém `sonar-project.properties`, o que ajuda a indicar que a análise será feita pelo CI.
3. Em **Administration → Analysis Method**, confirme que **Automatic Analysis está OFF**, pois este projeto usa análise pelo GitHub Actions.
4. Anote:
   - **Organization Key**.
   - **Project Key**.
5. No SonarQube, gere um token pessoal para análise e copie o valor.

No GitHub, abra seu repositório:

### 3.1 Secret
`Settings` → `Secrets and variables` → `Actions` → aba **Secrets** → `New repository secret`

Crie:

```text
SONAR_TOKEN = <token copiado do SonarQube>
```

### 3.2 Variables
Na aba **Variables**, crie:

```text
SONAR_ORGANIZATION = <organization key>
SONAR_PROJECT_KEY   = <project key>
```

Não coloque o token em arquivo ou commit.

---

## 4. Criar a EC2 na AWS

No console AWS, abra **EC2** → **Launch instance**.

Use:
- Name: `minirisk-sdd`
- AMI: **Ubuntu Server 24.04 LTS**
- Architecture: `64-bit (x86)`
- Instance type: `t3.micro` (ou equivalente pequeno disponível na sua conta)
- Key pair: crie `auditoria-sdd-key` e baixe o arquivo `.pem`

### Network / Security Group
Crie um novo Security Group com:

| Porta | Protocolo | Origem | Objetivo |
|---|---|---|---|
| 22 | TCP | Anywhere IPv4 (`0.0.0.0/0`) **temporariamente** | GitHub Actions precisa alcançar a EC2 por SSH no primeiro deploy |
| 80 | TCP | Anywhere IPv4 (`0.0.0.0/0`) | Aplicação web |

Não abra outras portas para esta atividade. **Depois que o pipeline ficar verde, altere a porta 22 para `My IP` antes de tirar o print do Security Group.** Assim o deploy inicial funciona e a configuração final fica mais restritiva.

### Advanced details → User data
Cole integralmente o conteúdo do arquivo:

```text
infra/ec2-user-data.sh
```

Depois clique em **Launch instance**.

Aguarde o estado da instância ficar **Running** e os status checks ficarem aprovados. Copie o **Public IPv4 address** ou **Public IPv4 DNS**.

---

## 5. Cadastrar a AWS/EC2 no GitHub Actions

No seu PC, gere uma chave de aplicação aleatória:

### PowerShell
```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie a saída.

No GitHub:
`Settings` → `Secrets and variables` → `Actions` → **Secrets**.

Crie três secrets:

### `EC2_HOST`
O IPv4 público ou DNS público da EC2. Exemplo:
```text
18.123.45.67
```

### `EC2_SSH_KEY`
Abra o arquivo `auditoria-sdd-key.pem` no Bloco de Notas/VS Code e copie **todo o conteúdo**, incluindo:

```text
-----BEGIN ... PRIVATE KEY-----
...
-----END ... PRIVATE KEY-----
```

Cole como valor do secret.

### `APP_SECRET_KEY`
Cole a chave hexadecimal aleatória gerada anteriormente.

Ao final, os Secrets esperados são:

```text
SONAR_TOKEN
EC2_HOST
EC2_SSH_KEY
APP_SECRET_KEY
```

E as Variables:

```text
SONAR_ORGANIZATION
SONAR_PROJECT_KEY
```

---

## 6. Disparar o pipeline

Faça um commit pequeno para disparar o pipeline novamente:

```bash
git commit --allow-empty -m "ci: execute pipeline completo"
git push
```

Abra:

```text
GitHub repository → Actions → CI Security and Deploy
```

O fluxo esperado é:

```text
Quality and Security
  ✓ Ruff lint
  ✓ Tests and coverage
  ✓ Bandit SAST
  ✓ Dependency audit
  ✓ SonarQube Cloud scan

Deploy to AWS EC2
  ✓ Build Docker image
  ✓ Export image
  ✓ Configure SSH
  ✓ Copy artifact to EC2
  ✓ Deploy container
  ✓ Verify deployment
```

O segundo job só começa se o primeiro terminar com sucesso.

---

## 7. Validar a aplicação na AWS

No navegador, acesse:

```text
http://IP_PUBLICO_DA_EC2/
```

Faça o teste de risco alto sugerido no passo 1.

Para conferir o health check:

```text
http://IP_PUBLICO_DA_EC2/healthz
```

Você deve ver algo semelhante a:

```json
{"service":"minirisk","status":"ok"}
```

---

## 8. Se o pipeline falhar

### Erro no SonarQube
Confira se `SONAR_TOKEN`, `SONAR_ORGANIZATION` e `SONAR_PROJECT_KEY` correspondem exatamente ao projeto importado.

### `Permission denied (publickey)`
Confirme que:
- `EC2_SSH_KEY` contém o `.pem` inteiro;
- a EC2 foi criada com exatamente aquele Key Pair;
- o usuário é Ubuntu (o workflow utiliza `ubuntu`).

### Timeout no SSH
Durante o primeiro deploy, a regra inbound TCP/22 precisa aceitar os GitHub-hosted runners. Para esta versão simples da atividade, deixe temporariamente `0.0.0.0/0`, rode o pipeline e, assim que terminar, altere a origem para **My IP**. **Não deixe SSH aberto globalmente de forma permanente.**

### Aplicação não abre na porta 80
Confirme a regra TCP/80 `0.0.0.0/0` e veja o passo `Verify deployment` do GitHub Actions.

---

## 9. Depois da entrega
Para não continuar gerando custo, encerre a instância:

```text
EC2 → Instances → minirisk-sdd → Instance state → Terminate instance
```

Se você não for reutilizar, remova também recursos relacionados que tenham cobrança própria.
