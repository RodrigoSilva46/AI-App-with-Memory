# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
import os                                                                                   # Permite interagir com o sistema operacional
from dotenv import load_dotenv, find_dotenv                                                 # Permite carregar as variáveis de ambiente do arquivo .env
from langchain_groq import ChatGroq                                                         # Permite criar um modelo de AI com a API da GROQ
from langchain_community.chat_message_histories import ChatMessageHistory                   # Permite criar Históricos de mensagens
from langchain_core.chat_history import BaseChatMessageHistory                              # Classe base para histórico de mensagens
from langchain_core.runnables.history import RunnableWithMessageHistory                     # Permite gerenciar o histórico de mensagens
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder                  # Permite criar prompts / mensagens
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, trim_messages   # Mensagens humanas, do sistema e do AI
from langchain_core.runnables import RunnablePassthrough                                    # Permite criar fluxos de execução e reutilizaveis
from operator import itemgetter                                                             # Facilita a extração de valores de dicionários


# Carregar as variáveis de ambiente do arquvo .env (para proteger as credenciais)
load_dotenv(find_dotenv())

# Obter a chave da API do GROQ armazenada no arquivo .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Inicializar o modelo de AI utilizando a API da GROQ
model = ChatGroq(
    model = "gemma2-9b-it",
    groq_api_key = GROQ_API_KEY
)

#EXEMPLO 01 ---------------------------------------------------------------------------------------------------------------------------------
# Dicionário para armazenar o histórico de mensagens
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Recura ou cria um histórico de mansagens para uma determinada sesão.
    Isso permite manter o contexto contínuo para diferentes usuários e interações.
    """
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Criar um gerenciador de histórico que conecta o modelo ao armazenamento de mensagens
with_message_history = RunnableWithMessageHistory(model, get_session_history)

# Configuração da sessão (Identificador único para cada chat/usuário)
config = {"configurable":{"session_id":"chat1"}}

# Exemplo de interação inicial do usuário
response = with_message_history.invoke(
    [HumanMessage(content="Oi, meu nome é Eduardo e sou Filósofo.")],
    config=config
)




#EXEMPLO 02 ---------------------------------------------------------------------------------------------------------------------------------
#Criação de um prompt template para estruturar a entrada do modelo
prompt = ChatPromptTemplate(
    [
        ('system', 'Você é um assistente útil. Responda todas as perguntas com precisão no idioma.'),
        MessagesPlaceholder(variable_name= 'messages') #Permitir adicionar mensagens de forma dinâmica
    ]
)

#Conectar o modelo ao template de prompt
chain = prompt | model #Usando LCEL para conectar o prompt ao modelo

#Exemplo de interação com o modelo usando o template 
response = chain.invoke(
    {'messages': [HumanMessage(content="Oi meu nome é Rodrigo!")]}
    )

# gerenciamento da memória do chatbot
trimmer = trim_messages(
    max_tokens = 45, #Limitar o número de tokens por mensagem
    strategy = 'last', #Define a estrtégia de corte para remover mensagens antigas
    token_counter = model, # Usa o modelo para contar os tokens
    include_system = True, #Inclui mensagens do sistema no histórico
    allow_partial = True, # Evita que as mensagens sejam cortadas parcialmente
    start_on = 'human' # Começa a contagem com a mensagem humana
) 

#Exemplo de histórico de mensagens 
messages = [
    SystemMessage(content="Você é um assistente. Responda todas as perguntas com precisão no idioma."),
    HumanMessage(content="Oi meu nome é Rodrigo!"),
    AIMessage(content="Oi Rodrigo, como posso te ajudar?"),
    HumanMessage(content="Meu sorvete favorito é de Doce de leite.")
]


#Aplicar o limitador de memória ao histórico 
response = trimmer.invoke(messages)

#Criando um pipeline de execução para otimizar a passagem de informações entre os componentes
chain = (
    RunnablePassthrough.assign(messages = itemgetter('messages') | trimmer) #Atribuir mensagens ao limitador de memória
    | prompt #Adicionar o prompt ao pipeline
    | model #Adicionar o modelo ao pipeline
)


#exemplo de interação utilizando o pipeline otimizado
response = chain.invoke(
    {'messages': messages + [HumanMessage(content="Qual é o meu sorvete favorito?")]
    }
)

#Exibir a reposta final do modelo
print("Resposta final do modelo: ", response.content)