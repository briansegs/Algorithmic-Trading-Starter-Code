import ccxt, json
import pandas as pd
import numpy as np
import xconfig as ds
from datetime import date, datetime, timezone, tzinfo
import time, schedule
import nice_funcs as n
import datetime as dt
import warnings
warnings.filterwarnings('ignore')

#: connect to the exchange of your choice. for algo
# trading live, we use ccxt in order to connect to
# the exchange and it’s pretty easy to do this.
phemex = ccxt.phemex({
    'enableRateLimit': True,
    'apiKey': 'YOUR KEY HERE',
    'secret': 'YOUR SECRET HERE',
})

#: params
symbol = 'BTCUSD'
trade_symbol = 'uBTCUSD'
pos_size = 3
target = 12


#: making sure that any algo trade that we import
# only submits as a limit order or else it cancels
# the order. we do this by creating a parameter called
# PostOnly which essentially tells the exchange: if
# this does not submit as a limit order, then cancel it.
# this saves us so much in fees.
params =  {'timeInForce': 'PostOnly',}

#: when algorithmic trading, we are continuously
# grabbing our open positions so the code below helps
# us easily do that whenever we need it. in all of
# our trading bots we are looking to see if we have an
# open position, what the size of that position is,
# and is the position long or short. we use pandas
# data frame in order to save this information neatly
def open_positions(trade_symbol=trade_symbol):

    params = {'type':'swap', 'code':'USD'}
    phe_bal = phemex.fetch_balance(params=params)
    open_positions = phe_bal['info']['data']['positions']
    #print(open_positions)

    # print('made 38')

    openpos_df = pd.DataFrame()
    openpos_df_temp = pd.DataFrame()
    for x in open_positions:
        sym = x['symbol']
        openpos_df_temp['symbol'] = [sym]

        openpos_df = openpos_df.append(openpos_df_temp)
    #print(openpos_df)

    active_symbols_list = openpos_df['symbol'].values.tolist()
    #print(active_symbols_list)
    active_sym_df = pd.DataFrame()
    active_sym_df_temp = pd.DataFrame()
    for symb in active_symbols_list:
        #print(symb)
        indexx = active_symbols_list.index(symb, 0, 100)
        active_sym_df_temp['symbol'] = [symb]
        active_sym_df_temp['index'] = [indexx]
        active_sym_df = active_sym_df.append\
                        (active_sym_df_temp)

    active_sym_df.to_csv('active_symbols.csv', index=False)
    # time.sleep(744)

    # if the symbol is showing in the df then store
    # the index position as index_pos

    #print(active_sym_df)
    # print('made 67')

    # active_symbols_list & active_sym_df
    active_sym_df_t = pd.DataFrame()
    active_sym_df2 = pd.DataFrame()
    for x in active_symbols_list:
        index_pos = active_sym_df.loc[active_sym_df['symbol'] \
        == x, 'index']
        index_pos = int(index_pos[0])
        #print(f'***** {x} THIS SHOULD BE INDEX: {index_pos}')
        #time.sleep(7836)
        openpos_side = open_positions[index_pos]['side'] # btc [3] [0] = doge, [1] ape
        openpos_size = open_positions[index_pos]['size']
        #print(open_positions)
        active_sym_df_t['symbol'] = [x]
        active_sym_df_t['open_side'] = [openpos_side]
        active_sym_df_t['open_size'] = [openpos_size]
        active_sym_df_t['index_pos'] = [index_pos]

        if openpos_side == ('Buy'):
            openpos_bool = True
            long = True
            active_sym_df_t['open_bool'] = True
            active_sym_df_t['long'] = True
        elif openpos_side == ('Sell'):
            openpos_bool = True
            long = False
            active_sym_df_t['open_bool'] = True
            active_sym_df_t['long'] = False
        else:
            openpos_bool = False
            long = None
            active_sym_df_t['open_bool'] = False
            active_sym_df_t['long'] = None

        active_sym_df2 = active_sym_df2.append(active_sym_df_t)
        #print(active_sym_df2)
        #print('made 108, done')

        #print(f'open_position for {x}... | openpos_bool {openpos_bool} | openpos_size {openpos_size} | long {long} | index_pos {index_pos}')

    return active_symbols_list, active_sym_df2

#: start building out the strategy. this is where
# we start building the strategy out and then
# let our bot execute every 30 seconds or so.
# there are many ways you can go from here, but
# below shows how we execute the bot. the rest
# is up to you. we will make sure to put a bunch
# of different strategies here on our blog but
# below is where we put the actual strategy &
# how we execute every 30 seconds.
def bot():
    # PUT THE STRATEGY HERE



# RUN THIS EVERY 30 seconds
schedule.every(30).seconds.do(bot)

while True:
    try:
        schedule.run_pending()
    except:
        print('+++ maybe an internet problem... code failed, sleeping 10')
        time.sleep(10)