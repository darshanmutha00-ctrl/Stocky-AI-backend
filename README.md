@app.get("/")
def home():
    return {"message": "✅ Stocky.AI Backend is running successfully!"}
Backend (FastAPI) with Finnhub integration. Set MARKET_API_KEY env var to your Finnhub key.
