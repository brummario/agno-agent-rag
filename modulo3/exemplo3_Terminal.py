# 1 - IMPORTS ===========================================================
import requests # Comunica com o servidor Agno via HTTP
import json
from pprint import pprint

# Comunicação com o servidor AgentOS
AGENT_ID = "Agent_PDF" # ID do agente Agno que é usado para processar mensagens
ENDPOINT = f"http://localhost:7777/agents/{AGENT_ID}/runs"

# 2 - Conexão com Agno ==================================================
def get_reponse_stream(message: str):
    """Função que envia uma mensagem para o agente Agno e retorna um stream de eventos."""
    response = requests.post(
        url=ENDPOINT, 
        data={
            "message": message,
            "stream": True # Mostra em tempo real o que o agente está processando
        },
        stream=True
    )
    for line in response.iter_lines():
        if line:
            # Parse Server-Sent Events
            if line.startswith(b"data:"):
                data = line[6:] # Remove "data: " da resposta
                try:
                    event = json.loads(data)
                    yield event # Mantem o fluxo aberto para streaming
                except json.JSONDecodeError:
                    continue

# 3 - Streamlit (processamento) =========================================



# 3 - Printa a resposta =================================================
def print_streaming_response(message: str): 
    for event in get_reponse_stream(message):
        event_type = event.get("event","")

        # Início da execução
        if event_type == "RunStarted":
            print("Execução iniciada")
            print("-"*50)

        # Conteúdo da resposta
        elif event_type == "RunContent":
            content = event.get("content", "")
            if content:
                print(content, end="", flush=True) # Imprime o conteúdo em tempo real

        # Tool call inicado
        elif event_type == "ToolCallStarted":
            tool = event.get("tool", {})
            tool_name = tool.get("tool_name", "Unknown")
            tool_args = tool.get("tool_args", {})
            print(f"TOOL INICIADA: {tool_name}")
            print(f"ARGUMENTOS: {json.dumps(tool_args, indent=2)}")
            print("-"*50)

        # Tool call finalizado
        elif event_type == "ToolCallCompleted":
            tool = event.get("tool", {}).get("tool_name")
            print(f"TOOL FINALIZADA: {tool_name}")
            print("-"*50)

        # Execução finalizada
        elif event_type == "RunCompleted":
            print("Execução finalizada")
            metrics = event.get("metrics", {})
            if metrics:
                print(f"MÉTRICAS: {json.dumps(metrics, indent=2)}")
            print("-"*50)

# 5 - RUN (loop) ========================================================
if __name__ == "__main__":
    message = input("Digite sua mensagem: ")
    print_streaming_response(message)
    while True:
        message = input("Digite sua mensagem: ")
        print_streaming_response(message)

    