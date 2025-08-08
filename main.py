from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(
    title="Stocky AI Backend",
    description="Backend API for Stocky.AI",
    version="1.0.0"
)

# -------------------------
# Health Check Endpoint
# -------------------------
@app.get("/")
@app.head("/")
def health_check():
    return {"status": "ok"}

# -------------------------
# Example Data Model
# -------------------------
class PredictionRequest(BaseModel):
    ticker: str
    days: int

# -------------------------
# Example Endpoint
# -------------------------
@app.post("/predict")
def predict_stock(data: PredictionRequest):
    # Placeholder prediction logic
    return {
        "ticker": data.ticker.upper(),
        "days": data.days,
        "prediction": "This is a sample prediction."
    }

# -------------------------
# Run server (for local dev)
# -------------------------
# On Render, you don't need this block — it's run by uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
