# 1 - IMPORTS ===========================================================
import requests
import json
import streamlit as st

AGENT_ID = "Agent_PDF"
ENDPOINT = f"https://agno-agent-rag.onrender.com/agents/{AGENT_ID}/runs"

# 2 - Consexão com Agno ==================================================
def get_reponse_stream(message: str):
    response = requests.post(
        url=ENDPOINT, 
        data={
            "message": message,
            "stream": True
        },
        stream=True
    )

    # 2.1 - Streaming (processamento) ===================================
    for line in response.iter_lines():
        if line:
            # Parse Server-Sent Events
            if line.startswith(b"data:"):
                data = line[6:] # Remove "data: " prefix
                try:
                    event = json.loads(data)
                    yield event
                except json.JSONDecodeError:
                    continue

# 3 - Streamlit (processamento) =========================================
st.set_page_config(page_title="Agent Chat PDF")
st.title("Agent Chat PDF")

# 3.1 Histórico de mensagens ============================================
# O streamlit ao iterar sobre a página, refaz todo o código, 
# então precisamos armazenar o histórico de mensagens no session_state

if "history" not in st.session_state:
    st.session_state.history = []

# 3.2 Input de mensagem ================================================
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        if msg['role'] == 'assistant' and msg.get('process'):
            with st.expander(label='Process', expanded=False):
                st.json(msg["process"])
        st.markdown(msg["content"])

# 3.3 Envio de mensagem ================================================
if prompt := st.chat_input("Digite sua mensagem:"):
    # Adiciona mensagem do usuário ao histórico
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta do asssitente
    with st.chat_message("assistant"):
        process_placeholder = st.empty()
        response_placeholder = st.empty()
        full_response = ""

    # Processando streaming
    for event in get_reponse_stream(prompt):
        event_type = event.get("event", "")

        if event_type == "ToolCallStarted":
            tool_name = event.get("tool", {}).get("tool_name", "Unknown")
            with st.status(f"Executando: {tool_name}... ", expanded=True):
                st.json(event.get("tool", {}).get("tool_args", {}))


        elif event_type == "RunContent":
            content = event.get("content", "")
            if content:
                full_response += content
                response_placeholder.markdown(full_response)

    response_placeholder.markdown(full_response)

    # Salvar a resposta e histórico na session state
    st.session_state.history.append({
        "role": "assistant",
        "content": full_response
    })


# # 3 - Printa a resposta =================================================
# def print_streaming_response(message: str): 
#     for event in get_reponse_stream(message):
#         event_type = event.get("event","")

#         # Início da execução
#         if event_type == "RunStarted":
#             print("Execução iniciada")
#             print("-"*50)

#         # Conteúdo da resposta
#         elif event_type == "RunContent":
#             content = event.get("content", "")
#             if content:
#                 print(content, end="", flush=True)

#         # Tool call inicado
#         elif event_type == "ToolCallStarted":
#             tool = event.get("tool", {})
#             tool_name = tool.get("tool_name", "Unknown")
#             tool_args = tool.get("tool_args", {})
#             print(f"TOOL INICIADA: {tool_name}")
#             print(f"ARGUMENTOS: {json.dumps(tool_args, indent=2)}")
#             print("-"*50)

#         # Tool call finalizado
#         elif event_type == "ToolCallCompleted":
#             tool = event.get("tool", {}).get("tool_name")
#             print(f"TOOL FINALIZADA: {tool_name}")
#             print("-"*50)

#         # Execução finalizada
#         elif event_type == "RunCompleted":
#             print("Execução finalizada")
#             metrics = event.get("metrics", {})
#             if metrics:
#                 print(f"MÉTRICAS: {json.dumps(metrics, indent=2)}")
#             print("-"*50)

# # 5 - RUN (loop) ========================================================
# if __name__ == "__main__":
#     message = input("Digite sua mensagem: ")
#     print_streaming_response(message)
#     while True:
#         message = input("Digite sua mensagem: ")
#         print_streaming_response(message)