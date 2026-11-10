# --------------------------------------------------------------------------
# Conta corrente Bancária - FastAPI
# Gerenciar saques e depósitos de clientes
# --------------------------------------------------------------------------

# IMPORTS =================================================================
from pydantic import BaseModel, Field
import uvicorn
from fastapi import FastAPI

# INICIALIZAÇÃO DO APP =====================================================
app = FastAPI()

# Adicionar clientes (simula um banco de dados)
db_clientes = {
    "Joao": 0,
    "Maria": 0,
    "Pedro": 0,
}
    
# Criar uma classe para as movimentações (saques e depósitos) OBS.: usar pydantic (para não acontecer erros de validação)
class Movimentacao(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    valor: float = Field(..., gt=0, description="Valor da movimentação") # gt=0 limita valores positivos, não permitindo valores negativos

# Criar um endpoint HOME (raiz)
@app.get("/")
def home():
    return {"message": "Conta Bancária - Conta Corrente"}

# Criar um endpoint para consultar os saldos dos clientes
@app.post("/saldo")
def saldo(cliente: str):
    return {"message": f"Saldo do cliente {cliente}: {db_clientes.get(cliente, 'Cliente não encontrado')}"}

# Criar um endpoint para realizar saques
@app.post("/saque")
def saque(mov: Movimentacao):
    db_clientes[mov.cliente] -= mov.valor
    return {"message": {"cliente": mov.cliente, 
                        "valor_movimentacao": -mov.valor,
                        "saldo": db_clientes[mov.cliente]}}


# Criar um endpoint para realizar depósitos
@app.post("/deposito")
def deposito(mov: Movimentacao):
    db_clientes[mov.cliente] += mov.valor
    return {"message": {"cliente": mov.cliente, 
                        "valor_movimentacao": mov.valor,
                        "saldo": db_clientes[mov.cliente]}}

# RUN ===================================================================
if __name__ == "__main__":
    uvicorn.run("exemplo2:app", host="localhost", port=8000, reload=True)