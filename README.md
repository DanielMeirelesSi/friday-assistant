# Friday

O Friday é uma software engineering assistant platform baseada em evidências, contexto, autoridade explícita, execução limitada, verificação proporcional e convergência.

Sua única interface pública é `$friday`. O Core é modular e carrega capabilities sob demanda. Atualmente, Documentation é a única capability implementada. Architecture, Testing, Security e as demais capabilities futuras ainda não estão implementadas.

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

## Friday Core

O Core coordena, de forma universal e independente de domínio:

- interpretação da intent e bootstrap de contexto;
- roteamento de capabilities e progressive disclosure;
- aquisição e qualificação de evidência;
- avaliação de autoridade, risco e profundidade de execução;
- estratégia de execução e execução limitada;
- verificação, convergência e avaliação de completion.

Padrões e workflows específicos pertencem à capability correspondente, não ao Core.

## Fluxos e limites

Documentation é implementada pelos workflows:

- `plan`: analisa o repositório e propõe a documentação;
- `generate`: cria ou completa documentação e estado validados;
- `update`: reconcilia documentação com mudanças do repositório;
- `audit`: verifica a documentação sem modificá-la.

`plan` e `audit` são somente leitura em relação ao conteúdo do projeto. `generate` e `update` podem modificar documentação e o estado local do Friday, mas não devem modificar código-fonte, dependências, infraestrutura, migrações, deploys ou publicação de pacotes. `.friday/state.json` continua sendo estado específico de Documentation, não Platform State.

Cada fluxo deve reunir evidências antes de fazer afirmações técnicas, detectar conflitos entre código, configuração, testes e documentação, validar caminhos e comandos documentados quando isso for aplicável e separar problemas do projeto de problemas da documentação.

## Estrutura do repositório

| Caminho | Responsabilidade |
| --- | --- |
| `SKILL.md` | Entrypoint público da Friday Platform: bootstrap do Core, capability routing e acesso progressivo às referências necessárias. |
| `references/core/` | Contratos universais da Platform: `platform.md`, `operating-model.md`, `context-model.md`, `evidence.md` e `authority-and-verification.md`. |
| `references/documentation-standard.md` | Padrão de qualidade, dimensionamento e critérios de documentação. |
| `references/repository-analysis.md` | Procedimento para levantar perfis, escopos, entradas, interfaces e fontes canônicas. |
| `references/evidence-and-trust.md` | Aplicação do Evidence Model universal à capability Documentation. |
| `references/documentation-writing.md` | Estilo, arquitetura da informação, comandos, links e regras de redação. |
| `references/state-and-ownership.md` | Propriedade dos documentos e formato do estado persistente. |
| `references/workflows/` | Procedimentos específicos para `plan`, `generate`, `update` e `audit`. |
| `tests/evals/platform_cases.json` | Contratos semânticos/manuais da fronteira da Platform e do roteamento de capabilities. |
| `tests/evals/behavior_cases.json` | Contratos determinísticos atuais dos workflows de Documentation. |
| `tests/evals/routing_cases.json` | Contratos/specs de routing dos workflows de Documentation. |
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

A raiz do projeto não declara manifest de dependências, comando de build ou lint. Os manifests presentes nos fixtures pertencem aos repositórios de teste. A validação é feita por uma suite `unittest` que inclui:

Execução local:

```bash
python -m unittest discover -s tests -v
```

- testes dos state guards Python e PowerShell;
- specs dos behavior evals de Documentation;
- specs dos Platform evals;
- validação dos casos de roteamento e dos fixtures de estado.

O GitHub Actions Validation executa essa suite em Ubuntu com Python e em Windows com Python/PowerShell, incluindo a paridade dos state guards. Os evals protegem contratos determinísticos e specs. Assertions semânticas ou manuais, incluindo a execução do modelo/agente, não são provadas automaticamente pelo CI e permanecem sujeitas a revisão manual ou a um harness externo.

Ao alterar a skill, comece por `SKILL.md` e revalide as referências afetadas. Ao alterar o modelo de estado, mantenha `scripts/state_guard.ps1` e `scripts/state_guard.py` compatíveis e valide um candidato completo antes de instalá-lo. Não foi identificada uma regra de geração de código ou de sincronização obrigatória entre outros artefatos deste repositório.

## Fontes de referência

Para entender ou manter o comportamento do Friday, leia `SKILL.md` primeiro. Em seguida, consulte o workflow correspondente em `references/workflows/` e as referências de análise, evidência, escrita e estado necessárias para a mudança.
