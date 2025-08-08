from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import time
import os

# Create FastAPI app
app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend domain for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Securely get API key from environment or fallback
API_KEY = os.getenv("FINNHUB_API_KEY", "your_api_key_here")  # Replace if needed

# Root route (check if backend works)
@app.get("/")
def home():
    return {"message": "Stocky.AI Backend is running"}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Stock price data route
@app.get("/api/ohlcv/{symbol}")
def get_ohlcv(symbol: str, resolution: str = "1d", limit: int = 200):
    try:
        # Map resolution
        mapping = {"1d": "D", "1h": "60", "30m": "30", "15m": "15", "5m": "5"}
        res = mapping.get(resolution, "D")

        to_ts = int(time.time())
        from_ts = to_ts - (limit * 86400)

        url = (
            f"https://finnhub.io/api/v1/stock/candle?"
            f"symbol={symbol}&resolution={res}&from={from_ts}&to={to_ts}&token={API_KEY}"
        )

        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        if data.get("s") != "ok":
            raise HTTPException(status_code=500, detail="Market API error")

        # Convert to lightweight chart format
        result = [
            {
                "t": data["t"][i],
                "o": data["o"][i],
                "h": data["h"][i],
                "l": data["l"][i],
                "c": data["c"][i],
                "v": data["v"][i],
            }
            for i in range(len(data["t"]))
        ]
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

