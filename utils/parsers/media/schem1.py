import time

import ta
import pandas as pd
import numpy as np
import asyncio
from utils.db_api.binance_pg import Database
from binance import AsyncClient


async def main():
    client = await AsyncClient.create()
    while True:
        await strategy('ANCUSDT', 50, client)
        time.sleep(0.5)


async def getminutedata(symbol, interval, lookback, client):
    dataf = await client.get_historical_klines(symbol, interval, lookback + ' m ago UTC')
    frame = pd.DataFrame(dataf)
    frame = frame.iloc[:, :6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.astype(float)
    return frame





def applytechnicals(df):
    df['%K'] = ta.momentum.stoch(df.Close, df.High, df.Low, window=14, smooth_window=3)
    df['%D'] = df['%K'].rolling(3).mean()
    df['rsi'] = ta.momentum.rsi(df.Close, window=14)
    df['macd'] = ta.trend.macd_diff(df.Close)
    df.dropna(inplace=True)


class Signals:
    def __init__(self, df, lags):
        self.df= df
        self.lags = lags

    def gettrigger(self):
        dfx = pd.DataFrame()
        for i in range(self.lags + 1):
            mask = (self.df['%K'].shift(i) < 20) & (self.df['%D'].shift(i) < 20)
            dfx = dfx.append (mask, ignore_index=True)
        return dfx.sum(axis=0)

    def decide(self):
        self.df['trigger'] = np.where(self.gettrigger(), 1, 0)
        self.df['Buy'] = np.where((self.df.trigger) &
                                  (self.df['%K'].between(20, 80)) & (self.df['%D'].between(20, 80))
                                  & (self.df.rsi > 50) & (self.df.macd > 0), 1, 0)


# inst = Signals(df, 5)
# inst.decide()



async def strategy(pair, qty, client, open_position = False):
    df = await getminutedata(pair, '1m', '100', client)
    applytechnicals(df)
    inst = Signals(df, 25)
    inst.decide()
    print(f"current Close is " +str(df.Close.iloc[-1]))
    if df.Buy.iloc[-1]:
        db = Database()
        await db.create()
        price = df.Close.iloc[-1]
        await db.insert_transaction(symbol=pair, type="BUY", price=price,
                                      sum=(qty*price)+(qty*price)*0.001, id_bill=1)
        # order = client.create_order(symbol=pair,
        #                             side='BUY',
        #                             type='MARKET',
        #                             quantity=qty)
        buyprice = price#float(order['fills'][0]['price'])
        open_position = True
    while open_position:
        time.sleep(0.5)
        df = await getminutedata(pair, '1m', '100', client)
        print(f'current Buy_price '+str(buyprice))
        print(f'current Close '+str(df.Close.iloc[-1]))
        print(f'current Target '+str(buyprice * 1.005))
        print(f'curre0nt Stop is ' + str(buyprice * 0.995))
        if df.Close[-1] > buyprice:
            buyprice = df.Close[-1]
        if df.Close[-1] <= buyprice *0.995 or df.Close[-1] >= 1.005*buyprice:
            price = df.Close[-1]
            order = await db.insert_transaction(symbol=pair, type="SELL",
                                                price=price, sum=(qty*price)-(qty*price)*0.001, id_bill=1)
            # order = client.create_order(symbol=pair,
            #                             side="SELL",
            #                             type="MARKET",
            #                             quantity=qty)
            break



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())