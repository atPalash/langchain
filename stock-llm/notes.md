# code

gherkin = (
     "Given stocks from index nifty50\n"
     "When let ema10Change = rate in 20 samples of minute5 close ema 10\n"
     "* let vwap10Change = rate in 20 samples of minute5 close vwap 10\n"
     "* let vwapMax = maximum in 10 samples of minute5 close vwap 10\n"
     "* let vwapMin = minimum in 10 samples of minute5 close vwap 10\n"
     "* let emaMax = maximum in 10 samples of minute5 close ema 10\n"
     "* let emaMin = minimum in 10 samples of minute5 close ema 10\n"
     "* let ema10Day = oldest in 2 samples of day close ema 10\n"
     "* let close = latest in 1 samples of minute5 close\n"
     "* let dayClose = oldest in 2 samples of day close\n"
     "Then list bulls = tickers with ema10Change > 0 and vwap10Change > 0 and close > ema10Day * 0.99 and close < ema10Day * 1.01\n"
     "* list bears = tickers with ema10Change < 0 and vwap10Change < 0 and close > ema10Day * 0.99 and close < ema10Day * 1.01\n"
     "* list vwapMovers = tickers with ((ema10Change < 0 and vwap10Change < 0) or (ema10Change > 0 and vwap10Change > 0)) and abs(dayClose - close) / dayClose > 0.01\n* list movers = tickers with abs(dayClose - close) / dayClose > 0.01\n",
)