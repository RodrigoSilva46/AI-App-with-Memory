Aqui está um exemplo de texto para o arquivo `README.md` que descreve o conteúdo do seu projeto de forma clara e organizada:

---

# AI App with Memory

Este projeto é uma aplicação de inteligência artificial que utiliza a API da GROQ para criar um chatbot com memória de conversação. O chatbot é capaz de manter o contexto das interações com os usuários, gerenciar históricos de mensagens e responder de forma dinâmica e precisa.

## Funcionalidades Principais

- **Memória de Conversação:** O chatbot mantém um histórico de mensagens para cada sessão, permitindo interações contínuas e contextualizadas.
- **Integração com GROQ:** Utiliza a API da GROQ para gerar respostas precisas e eficientes.
- **Gerenciamento de Tokens:** Implementa um sistema de corte de mensagens antigas para otimizar o uso de tokens e manter a eficiência.
- **Prompts Dinâmicos:** Estrutura as entradas do modelo com templates de prompts personalizáveis.

## Bibliotecas Utilizadas

- **`os`:** Para interagir com o sistema operacional.
- **`dotenv`:** Para carregar variáveis de ambiente a partir de um arquivo `.env`.
- **`langchain_groq`:** Para criar e gerenciar o modelo de IA com a API da GROQ.
- **`langchain_community`:** Para manipular históricos de mensagens.
- **`langchain_core`:** Para criar prompts, mensagens e fluxos de execução reutilizáveis.
- **`operator`:** Para facilitar a extração de valores de dicionários.

## Configuração

1. **Instale as dependências:**

   Certifique-se de que todas as dependências estão instaladas. Você pode instalar as bibliotecas necessárias usando o arquivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente:**

   Crie um arquivo `.env` na raiz do projeto e adicione a chave da API da GROQ:

   ```env
   GROQ_API_KEY=sua_chave_da_api_aqui
   ```

3. **Execute o script:**

   Para rodar o chatbot, execute o arquivo `main.py`:

   ```bash
   python main.py
   ```

## Exemplos de Uso

### Exemplo 1: Histórico de Mensagens

O chatbot mantém um histórico de mensagens para cada sessão, permitindo interações contextualizadas. Por exemplo:

```python
response = with_message_history.invoke(
    [HumanMessage(content="Oi, meu nome é Eduardo e sou Filósofo.")],
    config={"configurable": {"session_id": "chat1"}}
)
```

### Exemplo 2: Gerenciamento de Tokens

O sistema de corte de mensagens antigas garante que o chatbot não exceda o limite de tokens:

```python
response = trimmer.invoke(messages)
```

### Exemplo 3: Pipeline de Execução

Um pipeline otimizado conecta o modelo ao template de prompt e ao gerenciador de tokens:

```python
response = chain.invoke(
    {'messages': messages + [HumanMessage(content="Qual é o meu sorvete favorito?")]}
)
```

## Estrutura do Projeto

- **`main.py`:** Contém a lógica principal do chatbot, incluindo a configuração do modelo, gerenciamento de histórico e exemplos de uso.
- **`requirements.txt`:** Lista todas as dependências necessárias para rodar o projeto.
- **`.env`:** Armazena as variáveis de ambiente, como a chave da API da GROQ.

## Como Contribuir

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

