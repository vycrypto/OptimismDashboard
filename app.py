import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import plotly.express as px
import plotly.graph_objects as go
import aboutPage as aboutPage
import figures as f

st.set_page_config(page_title='OPTIMISM Dashboard',  layout='wide', page_icon=':ambulance:')

proj_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;"><i><b>OPTIMISM</b></i></p>'

with st.sidebar:

    st.markdown(proj_title, unsafe_allow_html=True)
    selected = option_menu(
        menu_title = None,
        options = ['Overview', 'Transactions', 'Users Activity', 'Staking and Bridging', 'Ecosystem and Development', 'About'],
        #icons = ['house', 'book', 'envelope'],
    )


if selected == 'About':
    st.write(f'# {selected}')
    st.write(f'{aboutPage.about_text}')
    st.write(f'## Methodology')
    st.write(f'{aboutPage.method_text}')
    st.write(f'## Other Information')
    st.write(f'{aboutPage.other_text}')
    # expand a change-log

elif selected == 'Overview':

    st.markdown(
        """
        # Overview 
        
        Description for Optimism.......
    
        Bridge to Optimism: *https://app.optimism.io/bridge*
    
        Explore the ecosystem: *https://www.optimism.io/apps/all*
        
    """)

    st.markdown(
        """
        #### **Optimism Token Price** 

        *The price of the $OP token. Currency in USD. [More](https://app.optimism.io/bridge)*

    """)
    st.plotly_chart(f.fig_hist_prc, use_container_width=True)

    m1, m2, m3 = st. columns((1,1,1))

    m1.write('')
    m1.metric(label='Average Daily Transactions', value="{:,.0f}".format(f.curr_trx)
              , delta="{:,.0f}".format(f.curr_trx_delta)
              , delta_color='normal'
              , help='7-Day MA of the number of transactions sent on Optimism each day.')

    m1.metric(label='Average Daily Unique Users', value="{:,.0f}".format(f.curr_users)
              , delta="{:,.0f}".format(f.curr_users_delta)
              , delta_color='normal'
              , help='7-Day MA of the number of unique addresses that sent a transaction on Optimism each day.')

    m2.write(   #Remove arrow
        """
        <style>
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    m2.metric(label='Estimated Daily L2 Savings', value="{:,.0f}".format(f.curr_fee_saved)
              , delta="fee saved in ETH / day"
              , delta_color='normal'
              , help='7-Day MA for estimated fees saved on Optimism each day.')

    m2.metric(label='Average Savings Multiplier', value="{:,.0f}".format(f.curr_mul_saving)
              , help='7-Day MA for estimated fees saved on Optimism divided by the 7-Day MA of total L2 transaction fees each day.')

    m3.write('')
    m3.metric(label='Circulating Supply', value="{:,.0f}".format(f.curr_circ_supply)
              , delta=""
              , help='The amount of coins that are circulating in the market and are tradeable by the public. '
                     'It is comparable to looking at shares readily available in the market (not held & locked by insiders, governments). '
                     'Data sourced from CoinGecko API. More')

    m3.metric(label='Total Supply', value="{:,.0f}".format(f.curr_ttl_supply)
              #, delta="fee saved in ETH / day"
              #, delta_color='normal'
              , help='The amount of coins that have already been created, minus any coins that have been '
                     'burned (removed from circulation). It is comparable to outstanding shares in the stock market. '
                     'Total Supply = Onchain supply - burned tokens. Data sourced from CoinGecko API. More')

    n1, n2 = st.columns((1, 1))

    n1.write(""" #### **Transactions per Day**""")
    n1.write('The number of transactions sent on Optimism each day.')
    n1.plotly_chart(f.fig_hist_txs, use_container_width=True)
    n2.write(""" #### **Unique Users per Day**""")
    n2.write("""The number of unique addresses that sent a transaction on Optimism each day.""")
    n2.plotly_chart(f.fig_hist_user, use_container_width=True)

    st.write(""" #### **Total Liquidity on Optimism**""")
    st.plotly_chart(f.fig_tvl, use_container_width=True)

    st.write(""" #### **Monthly Bridge Inflow Volume (from Ethereum)**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgVolumeIn, use_container_width=True)

    st.markdown("""---""")

    st.write('## Optimism (OP) Tokenomics')
    st.image('https://community.optimism.io/assets/img/pie2.1015b1b6.jpeg') #Not sure if works yet


    #https: // community.optimism.io / docs / governance / allocations /  # token-distribution-details

elif selected == 'Transactions':
    st.write(f'# {selected}')
    st.write('Description for this page.... ')

    st.write(""" ### **Transactions per Day**""")
    st.write("""*The number of transactions sent on Optimism each day.*""")
    st.plotly_chart(f.fig_hist_txs, use_container_width=True)

    o1, o2 = st.columns((1, 1))
    o1.write(""" #### **Total Fees Earned by Optimism**""")
    o1.write("""*Fees that users pay on L2 Optimism each day.*""")
    o1.plotly_chart(f.fig_hist_l2fee, use_container_width=True)

    o2.write(""" #### **Total Estimated Transaction Fees Saved**""")
    o2.write("""*The estimated gas fees saved for transactions sent on L2 Optimism each day. Calculated by replacing L1 gas price with L2 gas price.*""")
    o2.plotly_chart(f.fig_hist_fee_saved, use_container_width=True)

    st.write(""" #### **Avg Gas Fee Distribution**""")
    st.write("""*Avg Gas Fee Distribution by transaction type and project in the last 24 hours.*""")
    st.plotly_chart(f.fig_24hr_avgfee, use_container_width=True)

    st.markdown("""---""")
    #------------------------- L1 VS. L2
    st.write(""" ## **Layer1 vs Layer2 Transactions**""")

    st.write(""" A deeper dive into the L1 vs. L2 gas breakdowns. L1 transactions fees are
     fees the Optimism protocol pays to submit L2 transactions to L1 (also referred to as L1 Security Fees or Security Costs).
    L2 transactions fees are fees that users pay on L2 Optimism to submit transactions. """)

    fee_unit = st.selectbox('Display Fee Value in:', ['ETH', 'USD'], help='Choose the unit used in transaction fee charts below.')

    if fee_unit == 'ETH':

        st.write(""" #### **Total Transaction Fees**""")
        st.write("""*Description*""")
        st.plotly_chart(f.fig_hist_ttlfee, use_container_width=True)
        m1, m2 = st.columns((1, 1))
        m1.write(""" #### **L1 Gas Fees per Day**""")
        m1.write("""*The number of transactions sent on Optimism each day.*""")
        m1.plotly_chart(f.fig_hist_l1fee, use_container_width=True)


        m2.write(""" #### **L2 Gas Fees per Day**""")
        m2.write("""*The number of unique addresses that sent a transaction on Optimism each day.*""")
        m2.plotly_chart(f.fig_hist_l2fee, use_container_width=True)


    else:
        st.write(""" #### **Total Transaction Fees**""")
        st.plotly_chart(f.fig_hist_ttlfee_usd, use_container_width=True)
        m1, m2 = st.columns((1, 1))
        m1.write(""" #### **L1 Gas Fees per Day**""")
        m1.write("""*The number of transactions sent on Optimism each day.*""")
        m1.plotly_chart(f.fig_hist_l1fee_usd, use_container_width=True)


        m2.write(""" #### **L2 Gas Fees per Day**""")
        m2.write("""*The number of unique addresses that sent a transaction on Optimism each day.*""")
        m2.plotly_chart(f.fig_hist_l2fee_usd, use_container_width=True)

    # ------------> Gas Price
    m1, m2 = st.columns((1, 1))
    m1.write(""" #### **L1 Average Gas Price**""")
    m1.write("""*TBD*""")
    m1.plotly_chart(f.fig_hist_l1gas_prc, use_container_width=True)

    m2.write(""" #### **L2 Average Gas Price**""")
    m2.write("""*TBD*""")
    m2.plotly_chart(f.fig_hist_l2gas_prc, use_container_width=True)

    # ------------> Gas Used
    n1, n2 = st.columns((1, 1))
    n1.write(""" #### **L1 Gas Used per Day**""")
    n1.write("""*TBD*""")
    n1.plotly_chart(f.fig_hist_l1gas_used, use_container_width=True)

    n2.write(""" #### **L2 Gas Used per Day**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_hist_l2gas_used, use_container_width=True)



elif selected == 'Users Activity':
    st.write(f'# {selected}')

    st.write('Description for this page.... ')

    st.write(""" #### **Unique Users per Day**""")
    st.write("""*The number of unique addresses that sent a transaction on Optimism each day.*""")
    st.plotly_chart(f.fig_hist_user, use_container_width=True)

    st.write(""" #### **$OP Holder Activities**""")
    st.write('The distribution of $OP holder activities per week.')
    st.plotly_chart(f.fig_hist_hold_distr, use_container_width=True)

    st.markdown("""---""")

    st.write(""" ## **Active User Days Active (Last 6 months)**""")
    st.write(""" *How many days per month or week are addresses transacting on Optimism?*""")

    st.write(""" #### **Average Days Active - ALL**""")
    st.write(""" *Average Days active for all transaction types. More*""")
    st.plotly_chart(f.fig_act_d_all, use_container_width=True)

    n1, n2 = st.columns((1, 1))
    n1.write(""" #### **Average Days Active - CEX**""")
    n1.write("""*TBD*""")
    n1.plotly_chart(f.fig_act_d_cex, use_container_width=True)

    n2.write(""" #### **Average Days Active - DEX**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_act_d_dex, use_container_width=True)

    n1.write(""" #### **Average Days Active - DEFI**""")
    n1.write("""*TBD*""")
    n1.plotly_chart(f.fig_act_d_defi, use_container_width=True)

    n2.write(""" #### **Average Days Active - DAPP**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_act_d_dapp, use_container_width=True)

    n1.write(""" #### **Average Days Active - Layer2**""")
    n1.write("""*TBD*""")
    n1.plotly_chart(f.fig_act_d_l2, use_container_width=True)

    n2.write(""" #### **Average Days Active - NFT**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_act_d_nft, use_container_width=True)



elif selected == 'Staking and Bridging':
    st.write(f'# {selected}')
    # see https://dune.com/eliasimos/Bridge-Away-(from-Ethereum)

    st.write(""" #### **Total Liquidity on Optimism**""")
    # (https://dune.com/blockworks_research/l2-comparison-dashboard bridge inflow/outflow breakdown)
    st.plotly_chart(f.fig_tvl, use_container_width=True)

    st.write(""" #### **Bridge Transactions and Depositers per Day**""")
    st.write(""" *Unique Bridge Depositers per Day. The number of unique addresses that bridged from ETH to Optimism each day.* """)
    n1, n2 = st.columns((1, 1))
    n1.plotly_chart(f.fig_hist_brg_txs, use_container_width=True)
    n2.plotly_chart(f.fig_hist_brg_deposit, use_container_width=True)

    st.write(""" #### **Monthly Bridge Inflow Volume (from Ethereum)**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgVolumeIn, use_container_width=True)

    st.write(""" #### **Monthly Bridged Token Distribution (from Ethereum)**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgInTokens, use_container_width=True)

    st.write(""" #### **Bridged User Behaviors**""")
    st.write("""*TBD. [More for protocols used.](https://app.flipsidecrypto.com/velocity/queries/38a8d8f0-59be-4417-a1d1-6129589cb6fc)
            [ More for usage.](https://app.flipsidecrypto.com/velocity/queries/945ca0fc-dbcd-4a5d-99ad-67c1d66e3fce)*""")

    m1, m2 = st.columns((1, 1))
    m1.plotly_chart(f.fig_brgIn_platform, use_container_width=True)
    m2.plotly_chart(f.fig_brgIn_usage, use_container_width=True)

    st.write(""" #### **Monthly Bridge-out Volume**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/ae10e2fc-ce56-40ab-b60f-9945c36c5491)*""")
    st.plotly_chart(f.fig_hist_brgVolumeOut, use_container_width=True)







elif selected == 'Ecosystem and Development':
    st.write(f'# {selected}')
    # https://opmega.vercel.app/
    #https://dune.com/queries/1622467/2689169

    # good flipside scored "development":
    #https://sociocrypto.gitlab.io/terra-dashboard/development.html --
    # https://terradashprime.vercel.app/development
    # weekly active / new contract

    # https://dune.com/Marcov/Optimism-Ethereum
    #  https: // dune.com / optimismfnd / Optimism - Overview
    # https://dune.com/optimismfnd/Optimism-Project-Usage-Trends
    # querie: https://app.flipsidecrypto.com/velocity/queries/9a88a69e-74fb-4cb1-9529-61662699dfd8
    # num of transactions and num of users, not addresses~ cuz this is "from"

    st.write('Description for this page.... ')


    st.write(""" #### **Daily Active Contracts**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/5e0853a7-17d0-4a43-92fc-f4fac754e073)*""")
    st.plotly_chart(f.fig_dev_act, use_container_width=True)

    st.write(""" #### **Daily Active Contracts Breakdown**""")
    st.write("""*TBD. [More](https://app.flipsidecrypto.com/velocity/queries/72be8fec-cca7-44a0-8e3d-34767bd71b86)*""")
    st.plotly_chart(f.fig_dev_act_brkdwn, use_container_width=True)

    st.write(""" #### **Top 10 Delegate**""")
    st.markdown("""*TBD.---Top 10 Delegate by Amount Delegated(OP)* 
    [More](https://app.flipsidecrypto.com/velocity/queries/00457e10-f65d-4cc5-95da-e7c1adf8206f)""")

    p1, p2 = st.columns((1, 1))
    p1.plotly_chart(f.fig_delegator_amt, use_container_width=True)
    p2.plotly_chart(f.fig_delegator, use_container_width=True)

    st.markdown("""---""")
    st.write(""" ## **Popular Projects (Last 30 Days)**""")
    st.write("""TBD""")

    n1, n2 = st.columns((1, 2))

    n1.write(""" #### **Transactions by Transaction Type**""")
    n1.write(""" *description* """)
    n1.plotly_chart(f.fig_curr_type_txs, use_container_width=True)

    n2.write(""" #### **Transactions by Project**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_curr_proj_txs, use_container_width=True)

    n1.write(""" #### **Users by Transaction Type**""")
    n1.write(""" *description* """)
    n1.plotly_chart(f.fig_curr_type_users, use_container_width=True)

    n2.write(""" #### **Users by Project**""")
    n2.write("""*TBD*""")
    n2.plotly_chart(f.fig_curr_proj_users, use_container_width=True)

    st.write(""" #### Popular Projects Stats Table**""")
    st.plotly_chart(f.fig_top_proj_table, use_container_width=True)



else:
    st.write(f'# {selected}')

    st.write("""
    # Heading1
    ## Heading2
    :sunglasses:

    Ask me a question!

    *italic* / **bold** / ***bold italic***

    """)

    query = st.text_input('Search!', '')

    st.write(f"Query == '{query}")






