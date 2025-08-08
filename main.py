from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI(
    title="Stocky AI Backend",
    description="Backend API for Stocky.AI - Stocks, Crypto, AI Chat, Portfolio",
    version="1.0.0"
)

# -------------------------
# Health Check
# -------------------------
@app.get("/")
@app.head("/")
def health_check():
    return {"status": "ok", "timestamp": datetime.datetime.utcnow()}

# -------------------------
# Request Models
# -------------------------
class StockRequest(BaseModel):
    ticker: str
    days: int

class CryptoRequest(BaseModel):
    symbol: str
    days: int

class ChatRequest(BaseModel):
    message: str

class PortfolioRequest(BaseModel):
    user_id: str
    assets: dict

# -------------------------
# Stock Prediction Endpoint
# -------------------------
@app.post("/stocks/predict")
def predict_stock(data: StockRequest):
    # TODO: Replace with real stock prediction logic
    return {
        "ticker": data.ticker.upper(),
        "days": data.days,
        "prediction": f"Predicted upward trend for {data.ticker.upper()} over {data.days} days."
    }

# -------------------------
# Crypto Prediction Endpoint
# -------------------------
@app.post("/crypto/predict")
def predict_crypto(data: CryptoRequest):
    # TODO: Replace with real crypto prediction logic
    return {
        "symbol": data.symbol.upper(),
        "days": data.days,
        "prediction": f"Expected price increase for {data.symbol.upper()} over {data.days} days."
    }

# -------------------------
# AI Chat Endpoint
# -------------------------
@app.post("/ai/chat")
def ai_chat(data: ChatRequest):
    # TODO: Connect with OpenAI or custom AI model
    return {
        "user_message": data.message,
        "ai_response": f"This is a sample AI reply to: '{data.message}'"
    }

# -------------------------
# Portfolio Update Endpoint
# -------------------------
@app.post("/portfolio/update")
def update_portfolio(data: PortfolioRequest):
    # TODO: Save portfolio to DB
    return {
        "user_id": data.user_id,
        "updated_assets": data.assets,
        "status": "Portfolio updated successfully"
    }

# -------------------------
# Run locally
# -------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
