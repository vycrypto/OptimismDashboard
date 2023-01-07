import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import requests
import time

# ============================ FUNCTIONS ===============================
# -------- Update chart layout -------------
def chart_update_layout(figure, x_axis, y_axis):
    figure.update_layout(
        font_size=12,
        #width=450,
        height=300,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(14,17,23,255)',
        margin=dict(l=20, r=20, t=20, b=20),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor="rgba(100,100,100,0.3)",
            font_size=14,
            #font_family="Rockwell"
        ),

        legend_title_text='',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.2,
            xanchor='left',
            x=0.01,
            font=dict(
                size=12,
                color="white"
            ),
            bgcolor="rgba(0,0,0,0)",
            bordercolor="rgba(0,0,0,0)",
            borderwidth=2
        ),
        legend_font=dict(size=12),  # legend location


        xaxis=dict(
            title=x_axis,
            title_font=dict(size=14, color='rgba(170,170,170,0.7)'), #, family='Arial Black'
            gridcolor='rgba(100,100,100,0.3)',
            linecolor='rgba(100,100,100,0.7)',
            tickfont=dict(color='rgba(100,100,100,1)')
            # rangeslider=dict(bgcolor='rgba(0,0,0,0)',yaxis_rangemode='auto')
        ),

        yaxis=dict(
            title=y_axis,
            title_font=dict(size=14, color='rgba(171,171,171,0.7)'), #, family='Arial Black'
            title_standoff=3,
            gridcolor='rgba(100,100,100,0.3)',
            linecolor='rgba(100,100,100,0.7)',
            tickfont=dict(color='rgba(100,100,100,1)')
        )
    )


# ============================ HISTORICAL DAILY TIME SERIES ===============================
## ------ DATA ----------
OptimismHist1Yr = 'https://node-api.flipsidecrypto.com/api/v2/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5/data/latest'
df_hist_1yr = pd.read_json(OptimismHist1Yr).iloc[1: , :]

OpBridgeTx = 'https://node-api.flipsidecrypto.com/api/v2/queries/a6767ad0-2bd3-48b1-a132-6e7bc732ac27/data/latest'
df_hist_brg = pd.read_json(OpBridgeTx).iloc[1: , :]

OpDev = 'https://node-api.flipsidecrypto.com/api/v2/queries/5e0853a7-17d0-4a43-92fc-f4fac754e073/data/latest'
df_Dev = pd.read_json(OpDev).iloc[1:, :] #data limited to 90 days

OpDevBrkDwn = 'https://node-api.flipsidecrypto.com/api/v2/queries/72be8fec-cca7-44a0-8e3d-34767bd71b86/data/latest'
df_Dev_BrkDwn = pd.read_json(OpDevBrkDwn).iloc[1:, :] #data limited to 90 days

ma_p = 7  # Moving Average Period
df_Dev['NUM_CONTRACTS_ACTIVE_MA'] = df_Dev['NUM_CONTRACTS_ACTIVE'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist_1yr['NUM_TXS_MA'] = df_hist_1yr['NUM_TXS'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['NUM_USERS_MA'] = df_hist_1yr['NUM_USERS'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist_1yr['TX_FEE_MA'] = df_hist_1yr['TX_FEE'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['TX_FEE_USD'] = df_hist_1yr['L1_GAS_FEES_USD'] + df_hist_1yr['L2_GAS_FEES_USD']
df_hist_1yr['TX_FEE_USD_MA'] = df_hist_1yr['TX_FEE_USD'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist_1yr['L1_FEES_MA'] = df_hist_1yr['L1_GAS_FEES'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['L2_FEES_MA'] = df_hist_1yr['L2_GAS_FEES'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['L1_FEES_USD_MA'] = df_hist_1yr['L1_GAS_FEES_USD'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['L2_FEES_USD_MA'] = df_hist_1yr['L2_GAS_FEES_USD'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist_1yr['EST_FEES_SAVED'] = df_hist_1yr['EQUIVALENT_L1_TX_FEE'] - df_hist_1yr['L2_GAS_FEES']
df_hist_1yr['EST_FEES_SAVED_MA'] = df_hist_1yr['EST_FEES_SAVED'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist_1yr['EST_FEES_SAVED_USD'] = df_hist_1yr['EST_FEES_SAVED'] * df_hist_1yr['ETH_PRICE']
df_hist_1yr['EST_FEES_SAVED_USD_MA'] = df_hist_1yr['EST_FEES_SAVED_USD'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist=df_hist_1yr.set_index('DT').join(df_hist_brg.set_index('DT'))
df_hist['Date']=df_hist.index
df_hist['NUM_BGUSERS_MA'] = df_hist['NUM_BGUSERS'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist['NUM_BGTX_MA'] = df_hist['NUM_BGTX'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist['L1_GAS_PRC_GWEI'] = df_hist['AVG_L1_GAS_PRICE'].round(decimals=12)*1e9
df_hist['L1_GAS_PRC_GWEI_MA'] = df_hist['L1_GAS_PRC_GWEI'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist['L2_GAS_PRC_GWEI'] = df_hist['AVG_L2_GAS_PRICE'].round(decimals=12)*1e9
df_hist['L2_GAS_PRC_GWEI_MA'] = df_hist['L2_GAS_PRC_GWEI'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

df_hist['L1_GAS_USED_MA'] = df_hist['L1_GAS_USED'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')
df_hist['L2_GAS_USED_MA'] = df_hist['L2_GAS_USED'][::-1].rolling(ma_p).mean()[::-1].replace(np.nan, 'None')

## ------ VARIABLES ----------
curr_trx = df_hist.loc[:, ['NUM_TXS_MA']].iloc[:1, :].values[0][0]
last_trx = df_hist.loc[:, ['NUM_TXS_MA']].iloc[1:2, :].values[0][0]
curr_trx_delta = curr_trx - last_trx

curr_users = df_hist.loc[:, ['NUM_USERS_MA']].iloc[:1, :].values[0][0]
last_users = df_hist.loc[:, ['NUM_USERS_MA']].iloc[1:2, :].values[0][0]
curr_users_delta = curr_users - last_users

curr_fee_saved = df_hist.loc[:, ['EST_FEES_SAVED_MA']].iloc[:1, :].values[0][0]

curr_brgers = df_hist.loc[:, ['NUM_BGUSERS_MA']].iloc[:1, :].values[0][0]
last_brgers = df_hist.loc[:, ['NUM_BGUSERS_MA']].iloc[1:2, :].values[0][0]
curr_brgers_delta = curr_brgers - last_brgers


## ------ PLOTS ----------
# --> Total Active Contracts
fig_dev_act = px.line(df_Dev, x='DT', y='NUM_CONTRACTS_ACTIVE_MA', labels ={'DT':'Date', 'NUM_CONTRACTS_ACTIVE_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'DT':False,'NUM_CONTRACTS_ACTIVE_MA':True} )
fig_dev_act.add_bar(x=df_Dev['DT'],y=df_Dev['NUM_CONTRACTS_ACTIVE'], name="# Active Contracts / Day")
chart_update_layout(fig_dev_act, "", "Number of Active Contracts / Day")

fig_dev_act_brkdwn = px.bar(df_Dev_BrkDwn, x='DT', y='NUM_CONTRACTS_ACTIVE', color='LABEL_TYPE'
                             , hover_data={'DT':False,'NUM_CONTRACTS_ACTIVE':True, 'LABEL_TYPE':False} )
chart_update_layout(fig_dev_act_brkdwn, "", "Number of Active Contracts / Day")

# --> $OP Price
fig_hist_prc = px.line(df_hist, x='Date', y='OP_PRICE', labels ={'Date':'Date', 'OP_PRICE':'$OP Price'}
                ,color_discrete_sequence=['red']
                ,hover_data={'Date':False,'OP_PRICE':True})
chart_update_layout(fig_hist_prc, "", "OP Token Price (USD)")

# --> Total Transactions
fig_hist_txs = px.line(df_hist, x='Date', y='NUM_TXS_MA', labels ={'Date':'Date', 'NUM_TXS_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'NUM_TXS_MA':True} )
fig_hist_txs.add_bar(x=df_hist['Date'],y=df_hist['NUM_TXS'], name="# Transactions per Day")
chart_update_layout(fig_hist_txs, "", "Number of Daily Transactions")

# --> Total Users
fig_hist_user = px.line(df_hist, x='Date', y='NUM_USERS_MA', labels ={'Date':'Date', 'NUM_USERS_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'NUM_USERS_MA':True} )
fig_hist_user.add_bar(x=df_hist['Date'],y=df_hist['NUM_USERS'], name="# Users per Day")
chart_update_layout(fig_hist_user, "", "Number of Daily Unique Users")

# --> Total Fee (ETH / USD)
fig_hist_ttlfee = px.line(df_hist, x='Date', y='TX_FEE_MA', labels ={'Date':'Date', 'TX_FEE_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'TX_FEE_MA':True} )
fig_hist_ttlfee.add_bar(x=df_hist['Date'],y=df_hist['TX_FEE'], name="Total Fees (ETH)")
chart_update_layout(fig_hist_ttlfee, "", "Total Transaction Fees per Day (ETH)")

fig_hist_ttlfee_usd = px.line(df_hist, x='Date', y='TX_FEE_USD_MA', labels ={'Date':'Date', 'TX_FEE_USD_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'TX_FEE_USD_MA':True} )
fig_hist_ttlfee_usd.add_bar(x=df_hist['Date'],y=df_hist['TX_FEE_USD'], name="Total Fees (USD)")
            #,marker_color='rgba(86, 232, 198, 0.8)')
chart_update_layout(fig_hist_ttlfee_usd, "", "Total Transaction Fees per Day (USD)")

# --> Estimated Fees Saved
fig_hist_savedfee = px.line(df_hist, x='Date', y='EST_FEES_SAVED_MA', labels ={'Date':'Date', 'EST_FEES_SAVED_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'EST_FEES_SAVED_MA':True} )
fig_hist_savedfee.add_bar(x=df_hist['Date'],y=df_hist['EST_FEES_SAVED'], name="Estimated Fees Saved (ETH)")
chart_update_layout(fig_hist_savedfee, "", "Estimated Fees Saved (ETH)")

fig_hist_savedfee_usd = px.line(df_hist, x='Date', y='EST_FEES_SAVED_USD_MA', labels ={'Date':'Date', 'EST_FEES_SAVED_USD_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'EST_FEES_SAVED_USD_MA':True} )
fig_hist_savedfee_usd.add_bar(x=df_hist['Date'],y=df_hist['EST_FEES_SAVED_USD'], name="Estimated Fees Saved (USD)")
            #,marker_color='rgba(86, 232, 198, 0.8)')
chart_update_layout(fig_hist_savedfee_usd, "", "Estimated Fees Saved (USD)")

# --> Total L1 Fee (ETH / USD)
fig_hist_l1fee = px.line(df_hist, x='Date', y='L1_FEES_MA', labels ={'Date':'Date', 'L1_FEES_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L1_FEES_MA':True} )
fig_hist_l1fee.add_bar(x=df_hist['Date'],y=df_hist['L1_GAS_FEES'], name="L1 GAS Fees (ETH)")
            #,marker_color='rgba(86, 157, 232, 0.8)')
chart_update_layout(fig_hist_l1fee, "", "L1 Transaction Fees per Day (ETH)")


fig_hist_l1fee_usd = px.line(df_hist, x='Date', y='L1_FEES_USD_MA', labels ={'Date':'Date', 'L1_FEES_USD_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L1_FEES_USD_MA':True} )
fig_hist_l1fee_usd.add_bar(x=df_hist['Date'],y=df_hist['L1_GAS_FEES_USD'], name="L1 GAS Fees (USD)")
            #,marker_color='rgba(86, 157, 232, 0.8)')
chart_update_layout(fig_hist_l1fee_usd, "", "L1 Transaction Fees per Day (USD)")

# --> Total L2 Fee (ETH / USD)
fig_hist_l2fee = px.line(df_hist, x='Date', y='L2_FEES_MA', labels ={'Date':'Date', 'L2_FEES_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L2_FEES_MA':True} )
fig_hist_l2fee.add_bar(x=df_hist['Date'],y=df_hist['L2_GAS_FEES'], name="L2 GAS Fees (ETH)")
            #,marker_color='rgba(47, 229, 87, 0.8)')
chart_update_layout(fig_hist_l2fee, "", "L2 Transaction Fees per Day (ETH)")


fig_hist_l2fee_usd = px.line(df_hist, x='Date', y='L2_FEES_USD_MA', labels ={'Date':'Date', 'L2_FEES_USD_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L2_FEES_USD_MA':True} )
fig_hist_l2fee_usd.add_bar(x=df_hist['Date'],y=df_hist['L2_GAS_FEES_USD'], name="L2 GAS Fees (USD)")
            #,marker_color='rgba(47, 229, 87, 0.8)')
chart_update_layout(fig_hist_l2fee_usd, "", "L2 Transaction Fees per Day (USD)")

# --> Estimated Fee Saved
#https://streamlit-example-app-download-app-lk16x1.streamlit.app/
fig_hist_fee_saved = px.line(df_hist, x='Date', y='EST_FEES_SAVED_MA', labels ={'Date':'Date', 'EST_FEES_SAVED_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'EST_FEES_SAVED_MA':True} )
fig_hist_fee_saved.add_bar(x=df_hist['Date'],y=df_hist['EST_FEES_SAVED'], name="Est. Fees Saved")
chart_update_layout(fig_hist_fee_saved, "", "Estimated Gas Fees Saved (ETH)")

# --> Total Bridge Transactions
fig_hist_brg_txs = px.line(df_hist, x='Date', y='NUM_BGTX_MA', labels ={'Date':'Date', 'NUM_BGTX_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'NUM_TXS_MA':True} )
fig_hist_brg_txs.add_bar(x=df_hist['Date'],y=df_hist['NUM_BGTX'], name="# Bridge Transactions per Day")
chart_update_layout(fig_hist_brg_txs, "", "Number of Daily Bridge Transactions")

# --> Total Bridge Depositers

fig_hist_brg_deposit = px.line(df_hist, x='Date', y='NUM_BGUSERS_MA', labels ={'Date':'Date', 'NUM_BGUSERS_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'NUM_BGUSERS_MA':True} )
fig_hist_brg_deposit.add_bar(x=df_hist['Date'],y=df_hist['NUM_BGUSERS'], name="# Depositers per Day")
chart_update_layout(fig_hist_brg_deposit, "", "Number of Daily Unique Bridge Depositers")


# --> Avg Gas Price: l1 vs. l2 (in gwei)
fig_hist_l1gas_prc = px.line(df_hist, x='Date', y='L1_GAS_PRC_GWEI_MA', labels ={'Date':'Date', 'L1_GAS_PRC_GWEI_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L1_GAS_PRC_GWEI_MA':True} )
fig_hist_l1gas_prc.add_bar(x=df_hist['Date'],y=df_hist['L1_GAS_PRC_GWEI'], name="L1 Gas Price")
            #,marker_color='rgba(86, 157, 232, 0.8)')
chart_update_layout(fig_hist_l1gas_prc, "", "L1 Gas Price (gwei)")

fig_hist_l2gas_prc = px.line(df_hist, x='Date', y='L2_GAS_PRC_GWEI_MA', labels ={'Date':'Date', 'L2_GAS_PRC_GWEI_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L2_GAS_PRC_GWEI_MA':True} )
fig_hist_l2gas_prc.add_bar(x=df_hist['Date'],y=df_hist['L2_GAS_PRC_GWEI'], name="L2 Gas Price")
            #,marker_color='rgba(47, 229, 87, 0.8)')
chart_update_layout(fig_hist_l2gas_prc, "", "L2 Gas Price (gwei)")

# --># of Gas Used: l1 vs. l2
fig_hist_l1gas_used = px.line(df_hist, x='Date', y='L1_GAS_USED_MA', labels ={'Date':'Date', 'L1_GAS_USED_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L1_GAS_USED_MA':True} )
fig_hist_l1gas_used.add_bar(x=df_hist['Date'],y=df_hist['L1_GAS_USED'], name="L1 Gas Used")
            #,marker_color='rgba(86, 157, 232, 0.8)')
chart_update_layout(fig_hist_l1gas_used, "", "L1 Gas Used")

fig_hist_l2gas_used = px.line(df_hist, x='Date', y='L2_GAS_USED_MA', labels ={'Date':'Date', 'L2_GAS_USED_MA':'7-Day MA'}
                ,color_discrete_sequence=['gray']
                ,hover_data={'Date':False,'L2_GAS_USED_MA':True} )
fig_hist_l2gas_used.add_bar(x=df_hist['Date'],y=df_hist['L2_GAS_USED'], name="L2 Gas Used")
            #,marker_color='rgba(47, 229, 87, 0.8)')
chart_update_layout(fig_hist_l2gas_used, "", "L2 Gas Used")


# ============================ HISTORICAL WEEKLY TIME SERIES ===============================
## ------ DATA ----------
OpWeekly_HolderDistr = 'https://node-api.flipsidecrypto.com/api/v2/queries/496eccbb-bcdd-4f91-8337-27eb68088abe/data/latest'
df_hist_w = pd.read_json(OpWeekly_HolderDistr).iloc[1: , :]

## ----- PLOTS --------

fig_hist_hold_distr = px.bar(df_hist_w, x='WEEK', y='NO_HOLDERS', color='ACTIVITY'
                             , hover_data={'WEEK':False,'NO_HOLDERS':True} )
chart_update_layout(fig_hist_hold_distr, "", "Number of Holders")

# ============================ HISTORICAL MONTHLY TIME SERIES ===============================
OpMonthly_BrgOut = 'https://node-api.flipsidecrypto.com/api/v2/queries/ae10e2fc-ce56-40ab-b60f-9945c36c5491/data/latest'
df_hist_brgVolumeOut = pd.read_json(OpMonthly_BrgOut)

OpMonthly_BrgIn = 'https://node-api.flipsidecrypto.com/api/v2/queries/d7063e34-f6af-448e-98b4-62250b5bac09/data/latest'
df_hist_brgVolumeIn = pd.read_json(OpMonthly_BrgIn)


# --> Bridging In/Out Flow
fig_hist_brgVolumeIn = px.bar(df_hist_brgVolumeIn,x='DATE',y='ETH - USD Equivalent',color='SOURCE'
                           , hover_data={'DATE': False, 'SOURCE': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
fig_hist_brgInTokens = px.bar(df_hist_brgVolumeIn,x='DATE',y='ETH - USD Equivalent',color='SYMBOL'
                           , hover_data={'DATE': False, 'SYMBOL': True}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))

fig_hist_brgVolumeOut = px.bar(df_hist_brgVolumeOut,x='DATE',y='ETH - USD Equivalent',color='DESTINATION'
                           , hover_data={'DATE': False, 'DESTINATION': False}
                           ).update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))

# ============================ CURRENT STATS ===============================
## ------ DATA Frame Current 24hr----------
OptimismCurr24HR = 'https://node-api.flipsidecrypto.com/api/v2/queries/f845f416-fe82-4a62-af8e-f47145361930/data/latest'
df_24hr = pd.read_json(OptimismCurr24HR)
df_24hr['AVG_GAS_FEES_USD'].round(decimals=3)

## ------ DATA Frame Delegators----------
OptimismDelegatorTop = 'https://node-api.flipsidecrypto.com/api/v2/queries/00457e10-f65d-4cc5-95da-e7c1adf8206f/data/latest'
df_delegator = pd.read_json(OptimismDelegatorTop)

## ------ DATA Frame Popular Projects (30day rolling)----------
OpPopularProjects_DailyL30d = 'https://node-api.flipsidecrypto.com/api/v2/queries/9a88a69e-74fb-4cb1-9529-61662699dfd8/data/latest'
df_30d_proj_init = pd.read_json(OpPopularProjects_DailyL30d)
operator_num = len(df_30d_proj_init[df_30d_proj_init.LABEL_TYPE == 'operator'])

if operator_num > 0:
    df_30d_proj = df_30d_proj_init.drop(df_30d_proj_init[df_30d_proj_init.LABEL_TYPE == 'operator'].index)
else:
    df_30d_proj = df_30d_proj_init

df_30d_proj_table = df_30d_proj_init[:30]
df_30d_proj_table['PROJECT_NAME']=df_30d_proj_table['PROJECT_NAME'].str.upper()
df_30d_proj_table['LABEL_TYPE']=df_30d_proj_table['LABEL_TYPE'].str.upper()
df_30d_proj_table['NUM_TXS']=df_30d_proj_table['NUM_TXS'].astype(int)
df_30d_proj_table['NUM_USER']=df_30d_proj_table['NUM_USER'].astype(int)
cols=['PROJECT_NAME','NUM_TXS','NUM_USER','LABEL_TYPE']
df_30d_proj_table=df_30d_proj_table[cols]

## ------ DATA Frame Bridged in User Behavior ----------
OpBrgInPlatform = 'https://node-api.flipsidecrypto.com/api/v2/queries/38a8d8f0-59be-4417-a1d1-6129589cb6fc/data/latest'
df_brgIn_platform = pd.read_json(OpBrgInPlatform)
fig_brgIn_platform = px.pie(df_brgIn_platform,names='PROJECT',values='WALLETS'
                            , title = 'Platforms Used'
                           )
fig_brgIn_platform.update_traces(textposition='inside')
fig_brgIn_platform.update_layout(height=350, uniformtext_minsize=12,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))


OpBrgInUsage = 'https://node-api.flipsidecrypto.com/api/v2/queries/945ca0fc-dbcd-4a5d-99ad-67c1d66e3fce/data/latest'
df_brgIn_usage = pd.read_json(OpBrgInUsage)
fig_brgIn_usage = px.pie(df_brgIn_usage,names='EVENT_NAME',values='# Transactions'
                          , title = 'Transaction Events'
                           )
fig_brgIn_usage.update_traces(textposition='inside')
fig_brgIn_usage.update_layout(height=350, uniformtext_minsize=12,uniformtext_mode='hide',margin=dict(l=20, r=20, t=20, b=20))


## ------ DATA - Coingecko ----------
OpCoingecko = 'https://api.coingecko.com/api/v3/coins/optimism?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'
data_curr_coingecko = requests.request("GET", OpCoingecko).json()

## ------ DATA - DefiLlama ----------
OpDefiLTvl = 'https://api.llama.fi/charts/Optimism'
df_hist_tvl_init = requests.request("GET", OpDefiLTvl).json()
df_hist_tvl = pd.json_normalize(df_hist_tvl_init)

for i in range(len(df_hist_tvl['date'])):
    df_hist_tvl['date'][i]=time.strftime('%Y-%m-%d %H:%M:%S.000', time.localtime(int(df_hist_tvl['date'][i])))


## ------ VARIABLES ----------
curr_ttl_supply = data_curr_coingecko["market_data"]["total_supply"]
curr_circ_supply = data_curr_coingecko["market_data"]["circulating_supply"]

## ------- TABLES -----------

# --> Top Project Table
rowEvenColor = 'rgba(180, 180, 180, 0.8)'
rowOddColor = 'rgba(117, 117, 117, 0.8)'

fig_top_proj_table = go.Figure()
fig_top_proj_table.add_trace(
    go.Table(
        header = dict(
                    values=['<b>Project</b>','<b># Txs / Day</b>','<b># Addresses / Day</b>', '<b>Categery</b>'],
                    line_color='rgba(217, 217, 217, 0.8)',
                    fill_color='rgba(51, 45, 48, 0.8)',
                    align=['left','center'],
                    font=dict(color='white', size=12),
                    height=40

                ),
        cells = dict(
                    values=df_30d_proj_table.transpose().values.tolist(),
                    line_color='rgba(217, 217, 217, 1)',
                    fill_color = [[rowOddColor,rowEvenColor]*40],
                    align=['left', 'center'],
                    font=dict(color='white', size=12),
                    height=30
                )
    )
)


## ------ PLOTS ----------

# --> TVL
fig_tvl = px.bar(df_hist_tvl,x='date',y='totalLiquidityUSD'
                 , labels={'date': 'Date'
                            , 'totalLiquidityUSD': 'Ttl Liquidity ($)'}
                 , hover_data={'date': False}
                )
chart_update_layout(fig_tvl, "", "Total Liquidity (USD)")

# --> Popular Projects
fig_curr_proj_txs = px.bar(df_30d_proj,x='LABEL_TYPE',y='NUM_TXS',color='PROJECT_NAME'
                           , labels={'LABEL_TYPE': 'Transaction Type'
                                    , 'NUM_TXS': '# Transactions / Day'
                                    , 'PROJECT_NAME': 'Project Names'}
                           , hover_data={'LABEL_TYPE': False}
                           ).update_layout(height=400, autosize=True, title='by Projects')

fig_curr_type_txs = px.pie(df_30d_proj,names='LABEL_TYPE',values='NUM_TXS'
                           ).update_layout(height=400, autosize=True, title='by Transaction type')

fig_curr_proj_users = px.bar(df_30d_proj,x='LABEL_TYPE',y='NUM_USER',color='PROJECT_NAME'
                           , labels={'LABEL_TYPE': 'Transaction Type'
                                    , 'NUM_USER': '# Users / Day'
                                    , 'PROJECT_NAME': 'Project Names'}
                           , hover_data={'LABEL_TYPE': False}
                           ).update_layout(height=400, autosize=True, title='by Projects')

fig_curr_type_users = px.pie(df_30d_proj,names='LABEL_TYPE',values='NUM_USER'
                             ).update_layout(height=400, autosize=True, title='by Transaction type')

#--> Delegators

fig_delegator_amt = px.bar(df_delegator,x='Destination Name',y='Amount of Delegate (OP)').update_layout(height=400)
fig_delegator = px.bar(df_delegator,x='Destination Name',y='Number of Delegator').update_layout(height=400)

#--> Avg Fee for Popular Transaction types (perp/dex/nft/deposit) - Last 24 Hours
fig_24hr_avgfee = px.scatter(df_24hr, x='TYPE', y='AVG_GAS_FEES_USD', color='TYPE'
                             , labels={'TYPE': 'Transaction Type'
                                        , 'AVG_GAS_FEES_USD': 'Average Gas Fee / Transaction (USD)'}
                             , hover_data={'TYPE':False,'PROJECT':True,'AVG_GAS_FEES_USD':True} )
fig_24hr_avgfee.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))



# ============================ AVERAGE ACTIVE DAYS ===============================
## ------ DATA ----------
OpAvgActDays_all = 'https://node-api.flipsidecrypto.com/api/v2/queries/44f30ebd-f448-418c-91fb-71ba02384555/data/latest'
OpAvgActDays_cex = 'https://node-api.flipsidecrypto.com/api/v2/queries/c04e61f4-4470-4baa-9037-a5bb3da62f10/data/latest'
OpAvgActDays_defi = 'https://node-api.flipsidecrypto.com/api/v2/queries/0667dc68-00a1-42f0-a3f3-959bf8d3d2f7/data/latest'
OpAvgActDays_dapp = 'https://node-api.flipsidecrypto.com/api/v2/queries/0dd73c9c-7ab7-42d3-8003-2545c9400f66/data/latest'
OpAvgActDays_dex = 'https://node-api.flipsidecrypto.com/api/v2/queries/5b3ce87e-962d-46d3-8b4c-fbdd15768fab/data/latest'
OpAvgActDays_l2 = 'https://node-api.flipsidecrypto.com/api/v2/queries/90438ee2-5de7-47f1-bc2b-a1d63e0a2ee5/data/latest'
OpAvgActDays_nft = 'https://node-api.flipsidecrypto.com/api/v2/queries/d6d8169c-88a5-4b17-b7ef-bea14ecc59e1/data/latest'

df_act_d_all_init = pd.read_json(OpAvgActDays_all)
df_act_d_cex_init = pd.read_json(OpAvgActDays_cex)
df_act_d_defi_init = pd.read_json(OpAvgActDays_defi)
df_act_d_dapp_init = pd.read_json(OpAvgActDays_dapp)
df_act_d_dex_init = pd.read_json(OpAvgActDays_dex)
df_act_d_l2_init = pd.read_json(OpAvgActDays_l2)
df_act_d_nft_init = pd.read_json(OpAvgActDays_nft)

df_act_d_all = df_act_d_all_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_cex = df_act_d_cex_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_defi = df_act_d_defi_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_dapp = df_act_d_dapp_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_dex = df_act_d_dex_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_l2 = df_act_d_l2_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]
df_act_d_nft = df_act_d_nft_init[['DT','WEEKLY_DAYS_ACTIVE_PER_USER','MONTHLY_DAYS_ACTIVE_PER_USER']]

## ------ PLOTS ----------
# --> Avg Act Days (all)
fig_act_d_all = px.line(df_act_d_all, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_all, "", "Average Days Active")

# --> Avg Act Days (cex)
fig_act_d_cex = px.line(df_act_d_cex, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_cex, "", "Average Days Active")

# --> Avg Act Days (defi)
fig_act_d_defi = px.line(df_act_d_defi, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_defi, "", "Average Days Active")

# --> Avg Act Days (dapp)
fig_act_d_dapp = px.line(df_act_d_dapp, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_dapp, "", "Average Days Active")

# --> Avg Act Days (dex)
fig_act_d_dex = px.line(df_act_d_dex, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_dex, "", "Average Days Active")

# --> Avg Act Days (l2)
fig_act_d_l2 = px.line(df_act_d_l2, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_l2, "", "Average Days Active")

# --> Avg Act Days (nft)
fig_act_d_nft = px.line(df_act_d_nft, x='DT', y=['WEEKLY_DAYS_ACTIVE_PER_USER', 'MONTHLY_DAYS_ACTIVE_PER_USER']
                        , labels ={'DT':'Date', 'WEEKLY_DAYS_ACTIVE_PER_USER':'Weekly Days Active'
                                    , 'MONTHLY_DAYS_ACTIVE_PER_USER':'Monthly Days Active'}
                        , hover_data={'DT':False}
                        )
chart_update_layout(fig_act_d_nft, "", "Average Days Active")