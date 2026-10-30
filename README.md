# Test E2E Playwright

Uma skill multiplataforma para agentes de programação inspecionarem aplicações web no navegador, inventariarem suas rotas navegáveis e implementarem testes E2E estáveis com Playwright.

## Agentes compatíveis

O conteúdo canônico fica em `skills/test-e2e-playwright/SKILL.md`. Os manifests integram o pacote com:

- Codex: `.codex-plugin/` e `.agents/plugins/`
- Claude Code: `.claude-plugin/`
- Antigravity: `plugin.json` na raiz
- Cursor: `.cursor-plugin/`
- GitHub Copilot: `plugin.json` e `.github/plugin/`
- Outros agentes que aceitam skills: diretório `skills/`

Os comandos ficam em `commands/`. Cada host pode ter requisitos próprios de instalação e ativação de plugins; consulte a documentação atual do agente.

## Uso

Ative `test-e2e-playwright` ou use o comando `/test-e2e-playwright` no host compatível. Você escolhe o modo em cada execução. Se não informar a opção no pedido, o agente perguntará antes de iniciar a exploração.

### Modo automático

O agente percorre as rotas identificadas, registra o inventário, implementa os testes e executa a verificação sem parar para aprovação tela por tela. O navegador continua visível para acompanhamento; a diferença é que o agente não aguarda confirmação entre as telas.

Exemplo de pedido: `Use test-e2e-playwright no modo automático para cobrir as telas do projeto.`

### Modo acompanhado

O agente trabalha uma tela por vez: abre a rota no navegador visível, informa qual tela está exibindo e o que observou, e aguarda você revisar e confirmar/corrigir antes de avançar para a próxima. Você também pode pedir uma interação específica nessa tela. Depois da exploração, o agente implementa e executa os testes por tela, apresenta o teste e o resultado, e espera sua revisão para prosseguir.

Exemplo de pedido: `Use test-e2e-playwright no modo acompanhado e espere minha confirmação a cada tela.`

Nesse modo, a aprovação é uma pausa real: se o agente não puder aguardar uma resposta no host, ele deve parar no ponto de revisão e não continuar silenciosamente. Você pode trocar de modo durante uma pausa.

`8931` é a porta SSE do servidor MCP, não a porta da aplicação. O navegador aberto é uma sessão Playwright visível e isolada, sem reutilizar o perfil ou as credenciais do navegador habitual do usuário. Cobertura de telas significa rotas navegáveis inventariadas com testes passando; não significa 100% de cobertura de código.

## Instalação via skills.sh

Depois de publicar o repositório, instale a skill com:

```bash
npx skills add <owner>/skill-test-e2e-playwright
```

Substitua `<owner>` pelo proprietário GitHub do repositório publicado. Instalações via marketplace/plugin devem usar a documentação atual do agente correspondente.

## Desenvolvimento e validação

Requisitos: Python 3.10+; não há dependências Python adicionais.

```bash
make test
make validate
make check
```

O validador verifica os manifests, os arquivos obrigatórios e os elementos essenciais do contrato da skill. Consulte `skills/test-e2e-playwright/references/` para regras de browser, inventário, estabilidade e triagem.
