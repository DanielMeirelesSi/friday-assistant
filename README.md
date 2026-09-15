# Friday

Skill para analisar repositórios e criar, atualizar ou auditar documentação técnica baseada em evidências.

O Friday trata o repositório atual como fonte primária de verdade. Ele distingue o que está declarado em documentação e configuração do que foi observado no código ou confirmado por validação, e não altera o código da aplicação para fazê-lo coincidir com a documentação.

## Uso

Invoque a skill com `$friday` e descreva a tarefa. Quando necessário, indique explicitamente o fluxo:

```text
$friday plan          # analisa e propõe a documentação, sem escrever arquivos
$friday generate      # cria ou completa a documentação e o estado do Friday
$friday update        # sincroniza documentação existente com mudanças do repositório
$friday audit         # verifica a documentação sem modificá-la
```

Sem um fluxo explícito, a intenção é inferida do pedido. Um pedido para “documentar o projeto” usa `generate`; um pedido para apenas avaliar a documentação usa `audit`.

## Fluxos e limites

`plan` e `audit` são somente leitura em relação ao conteúdo do projeto. `generate` e `update` podem modificar documentação e o estado local do Friday, mas não devem modificar código-fonte, dependências, infraestrutura, migrações, deploys ou publicação de pacotes.

Cada fluxo deve reunir evidências antes de fazer afirmações técnicas, detectar conflitos entre código, configuração, testes e documentação, validar caminhos e comandos documentados quando isso for aplicável e separar problemas do projeto de problemas da documentação.

## Estrutura do repositório

| Caminho | Responsabilidade |
| --- | --- |
| `SKILL.md` | Contrato principal: roteamento de intenção, invariantes, modos, limites e estado. |
| `references/documentation-standard.md` | Padrão de qualidade, dimensionamento e critérios de documentação. |
| `references/repository-analysis.md` | Procedimento para levantar perfis, escopos, entradas, interfaces e fontes canônicas. |
| `references/evidence-and-trust.md` | Níveis de evidência, suporte de claims, conflitos e desconhecidos. |
| `references/documentation-writing.md` | Estilo, arquitetura da informação, comandos, links e regras de redação. |
| `references/state-and-ownership.md` | Propriedade dos documentos e formato do estado persistente. |
| `references/workflows/` | Procedimentos específicos para `plan`, `generate`, `update` e `audit`. |
| `agents/openai.yaml` | Metadados de apresentação da skill; a invocação implícita está desativada. |
| `scripts/state_guard.ps1` | Validação e instalação atômica do estado em PowerShell. |
| `scripts/state_guard.py` | Equivalente em Python 3 para validar e instalar o estado. |

## Estado local

Quando um fluxo de escrita é concluído com sucesso, o Friday pode manter conhecimento de manutenção em `.friday/`:

- `.friday/config.yaml` é configuração humana, quando existir;
- `.friday/state.json` é estado gerenciado pela skill;
- o estado deve ser criado como candidato e instalado pelo state guard;
- em um repositório Git, `.friday/` deve ficar em `.git/info/exclude`, sem alterar `.gitignore` apenas por esse motivo.

Exemplo de validação de um estado existente no Windows:

```powershell
powershell -File scripts/state_guard.ps1 -Command validate -State .friday/state.json -Repo .
```

O script em `scripts/state_guard.py` oferece o mesmo subcomando para ambientes com Python 3. Não há valores secretos no exemplo nem no estado documentado.

## Desenvolvimento e validação

Este repositório não declara manifest de dependências, comando de build, lint, testes automatizados, CI/CD ou infraestrutura de execução. A validação disponível no próprio projeto concentra-se na consistência documental e no formato do estado, usando os dois state guards.

Ao alterar a skill, comece por `SKILL.md` e revalide as referências afetadas. Ao alterar o modelo de estado, mantenha `scripts/state_guard.ps1` e `scripts/state_guard.py` compatíveis e valide um candidato completo antes de instalá-lo. Não foi identificada uma regra de geração de código ou de sincronização obrigatória entre outros artefatos deste repositório.

## Fontes de referência

Para entender ou manter o comportamento do Friday, leia `SKILL.md` primeiro. Em seguida, consulte o workflow correspondente em `references/workflows/` e as referências de análise, evidência, escrita e estado necessárias para a mudança.
