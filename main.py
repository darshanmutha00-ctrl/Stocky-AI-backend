from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, requests, time
app = FastAPI(title='Stocky.AI Backend')

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

FINNHUB_KEY = os.environ.get('MARKET_API_KEY') or 'demo'  # replace with your key

@app.get('/health')
def health():
    return {'status':'ok'}

@app.get('/api/ohlc/{symbol}')
def get_ohlc(symbol: str, timeframe: str = '1d', limit: int = 200):
    # Use Finnhub candles endpoint as example: https://finnhub.io/docs/api/market-data
    # timeframe param mapping to resolution
    mapping = {'1m':'1','5m':'5','15m':'15','1h':'60','1d':'D'}
    resolution = mapping.get(timeframe, 'D')
    to_ts = int(time.time())
    from_ts = to_ts - (limit * 60)
    url = f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution={resolution}&from={from_ts}&to={to_ts}&token={FINNHUB_KEY}'
    r = requests.get(url, timeout=10)
    if r.status_code!=200:
        raise HTTPException(status_code=502, detail='Market API error')
    data = r.json()
    # Convert to lightweight-charts compatible format: {time, o, h, l, c, v}
    if data.get('s')!='ok':
        # fallback generate mock
        import random, time
        now = int(time.time())
        sample=[]
        for i in range(limit):
            base = 100 + random.random()*10
            sample.append({'t': now - i*60, 'o': base, 'h': base+random.random(), 'l': base-random.random(), 'c': base+random.random()-0.5, 'v': random.random()*1000})
        return list(reversed(sample))
    result=[]
    for i in range(len(data['t'])):
        result.append({'t': data['t'][i], 'o': data['o'][i], 'h': data['h'][i], 'l': data['l'][i], 'c': data['c'][i], 'v': data['v'][i] if 'v' in data else None})
    return result
