# Agno + LLM interna (OpenAI-compatible)

Este projeto usa o provider `OpenAILike` do Agno para conectar em uma LLM interna que exponha API no formato OpenAI.

## 1) Variaveis de ambiente

No PowerShell, configure:

```powershell
$env:INTERNAL_LLM_BASE_URL = "https://llm.interna.suaempresa/v1"
$env:INTERNAL_LLM_MODEL = "seu-modelo"
$env:INTERNAL_LLM_API_KEY = "seu-token"
```

Opcional (se seu gateway usa header custom em vez de Authorization Bearer):

```powershell
$env:INTERNAL_LLM_AUTH_HEADER = "X-API-Key"
```

## 2) Executar exemplo

```powershell
.\.venv\Scripts\python.exe .\0.llm_call.py
```

## Observacoes

- `INTERNAL_LLM_BASE_URL` deve apontar para a raiz com `/v1` quando aplicavel.
- Se o endpoint exigir certificado interno, ajuste confianca TLS no ambiente da empresa.
- O arquivo `0.llm_call.py` cria um `Agent` e executa `print_response` para testar conectividade.
