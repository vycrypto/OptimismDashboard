import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import plotly.express as px
import plotly.graph_objects as go
import figures as f

st.set_page_config(page_title='OPTIMISM Dashboard',  layout='wide')

proj_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;"><i><b>OPTIMISM</b></i></p>'

with st.sidebar:

    st.markdown(proj_title, unsafe_allow_html=True)
    selected = option_menu(
        menu_title = None,
        options = ['Overview', 'Transactions', 'Users Activity', 'Staking and Bridging', 'Ecosystem and Development', 'About'],
        #icons = ['house', 'book', 'envelope'],
    )


if selected == 'About':

    st.markdown(
        """
        # About
        
        This dashboard is designed by Phi Deltalytics for MetricsDao's 
        Optimism Mega Dashboard bounty. I hope it serves as a valuable tool for 
        both newcomers and experienced users to gain insights into the Optimism ecosystem. 
        Any comments and suggestions are welcomed. 
        
        ## Methodology
        Data is drawn from Flipside Crypto's Optimism tables and existing APIs 
        from Coingecko and DefiLlama. For Flioside's data, links to the underlying
        queries are provided in chart data descriptions (in "More"). 
        
        ## Other Information
        Page source: https://github.com/pd123459/OptimismDashboard
        
        Twitter: [@phi_deltalytics](https://twitter.com/phi_deltalytics) 

    """)

elif selected == 'Overview':

    st.markdown(
        """
        # Overview 
        
        This dashboard offers a holistic view of the Optimism ecosystem including 
        transactions, user activities, staking, and developments. Introduced in 
        June 2019, Optimism is a Layer 2 Optimistic Rollup network designed to utilize 
        the strong security guarantees of Ethereum while reducing 
        its cost and latency.
        
        :sunglasses: Learn more about Optimism: *https://www.optimism.io/about*
        
        :sunglasses: Bridge to Optimism: *https://app.optimism.io/bridge*
    
        :sunglasses: Explore the ecosystem: *https://www.optimism.io/apps/all*
        
    """)

    st.markdown(
        """
        #### **Optimism Token Price** 

        *The price of the $OP token. Currency in USD. [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*

    """)
    st.plotly_chart(f.fig_hist_prc, use_container_width=True)

    m1, m2, m3 = st. columns((1,1,1))

    m1.write('')
    m1.metric(label='Average Daily Transactions', value="{:,.0f}".format(f.curr_trx)
              , delta="{:,.0f}".format(f.curr_trx_delta)
              , delta_color='normal'
              , help='7-Day MA of the number of unique transactions sent on Optimism each day. For more, check out the Transactions section.')

    m1.metric(label='Average Daily Unique Users', value="{:,.0f}".format(f.curr_users)
              , delta="{:,.0f}".format(f.curr_users_delta)
              , delta_color='normal'
              , help='7-Day MA of the number of unique addresses that sent a transaction on Optimism each day. For more, check out the User Activity section.')

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
              , help='7-Day MA for estimated fees saved on Optimism each day. Calculated by using the difference between'
                     'L1 and L2 gas prices for each transaction. For more, check out the Transactions section.')

    m2.metric(label='Daily Bridge Depositers', value="{:,.0f}".format(f.curr_brgers)
              , delta="{:,.0f}".format(f.curr_brgers_delta)
              , delta_color='normal'
              , help='7-Day MA for the number of unique addresses that sent a transaction from Ethereum to Optimism L2 each day. '
                     'For more, check out the Staking and Bridging section.')

    m3.write('')
    m3.metric(label='Circulating Supply', value="{:,.0f}".format(f.curr_circ_supply)
              , delta=""
              , help='The amount of coins that are circulating in the market and are tradeable by the public. '
                     'It is comparable to looking at shares readily available in the market (not held & locked by insiders, governments). '
                     'Data sourced from CoinGecko API. For more, check out the About section.')

    m3.metric(label='Total Supply', value="{:,.0f}".format(f.curr_ttl_supply)
              #, delta="fee saved in ETH / day"
              #, delta_color='normal'
              , help='The amount of coins that have already been created, minus any coins that have been '
                     'burned (removed from circulation). It is comparable to outstanding shares in the stock market. '
                     'Total Supply = Onchain supply - burned tokens. Data sourced from CoinGecko API. For more, check out the About section.')

    n1, n2 = st.columns((1, 1))

    n1.write(""" #### **Daily Transactions**""")
    n1.write('The number of transactions sent on Optimism each day. [More.](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)')
    n1.plotly_chart(f.fig_hist_txs, use_container_width=True)
    n2.write(""" #### **Daily Users**""")
    n2.write("""The number of addresses that sent a transaction on Optimism each day. [More.](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)""")
    n2.plotly_chart(f.fig_hist_user, use_container_width=True)

    st.write(""" #### **Total Liquidity on Optimism**""")
    st.write(""" *The number of assets that are currently being staked on Optimism. Data sourced from DefiLlama API. For more, check out the About section.*""")
    st.plotly_chart(f.fig_tvl, use_container_width=True)

    st.write(""" #### **Monthly Bridge Inflow Volume (from Ethereum)**""")
    st.write("""*The monthly inflow volume of assets bridged from Ehereum to Optimism. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgVolumeIn, use_container_width=True)

    st.markdown("""---""")

    st.write('## Optimism Tokenomics')
    st.image('https://community.optimism.io/assets/img/pie2.1015b1b6.jpeg')
    st.write(
        """ 
        The Optimism token was initially launched on May 31th, 2022 with 
        an initial supply of 4,294,967,296 OP tokens. The total token supply will inflate at a rate of 2% per year.
        30% of the initial token supply were unlocked. The foundation expects the total 
        supply to be fully unlocked by May, 2026. Detailed token allocations shown in the pie chart above.
        
        Source: [Optimism Docs](https://community.optimism.io/docs/governance/allocations/)
        """)

elif selected == 'Transactions':
    st.write(f'# {selected}')

    st.write(""" ### **Transactions per Day**""")
    st.write("""*The number of transactions sent on Optimism each day.
    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    st.plotly_chart(f.fig_hist_txs, use_container_width=True)

    #o1, o2 = st.columns((1, 1))
    st.write(""" #### **Total Fees Earned by Optimism**""")
    st.write("""*Total Transaction fees earned by Optimism each day.
    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    st.plotly_chart(f.fig_hist_ttlfee, use_container_width=True)

    st.write(""" #### **Total Estimated Transaction Fees Saved**""")
    st.write("""*The estimated gas fees saved for transactions sent on L2 Optimism each day. Calculated by replacing L1 gas price with L2 gas price.
    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    st.plotly_chart(f.fig_hist_fee_saved, use_container_width=True)

    st.write(""" #### **Average Gas Fee Distribution**""")
    st.write("""*Project average Gas Fee for transactions in the last 24 hours. Categorized by project types.
    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    st.plotly_chart(f.fig_24hr_avgfee, use_container_width=True)

    st.markdown("""---""")
    #------------------------- L1 VS. L2
    st.write(""" ## **Layer1 vs Layer2 Transactions**""")

    st.write(""" A deeper dive into the L1 vs. L2 gas breakdowns. L1 transactions fees are
     fees the Optimism protocol pays to submit L2 transactions to L1 (also referred to as L1 Security Fees or Security Costs).
    L2 transactions fees are fees that users pay on L2 Optimism to submit transactions. """)

    fee_unit = st.selectbox('Display Fee Value in:', ['ETH', 'USD'], help='Choose the unit used in transaction fee charts below.')


    if fee_unit == 'ETH':

        #st.write(""" #### **Estimated Transaction Fees Saved**""")
        #st.write("""*Description*""")
        #st.plotly_chart(f.fig_hist_savedfee, use_container_width=True)

        m1, m2 = st.columns((1, 1))
        m1.write(""" #### **L1 Gas Fees per Day**""")
        m1.write("""*Total L1 transaction fees on Optimism each day. Sum in ETH.
        [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
        m1.plotly_chart(f.fig_hist_l1fee, use_container_width=True)


        m2.write(""" #### **L2 Gas Fees per Day**""")
        m2.write("""*Total L2 transaction fees on Optimism each day. Sum in ETH.
        [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
        m2.plotly_chart(f.fig_hist_l2fee, use_container_width=True)


    else:
        #st.write(""" #### **Estimated Transaction Fees Saved**""")
        #st.plotly_chart(f.fig_hist_savedfee_usd, use_container_width=True)
        m1, m2 = st.columns((1, 1))
        m1.write(""" #### **L1 Gas Fees per Day**""")
        m1.write("""*Total L1 transaction fees on Optimism each day. Sum in USD.
        [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
        m1.plotly_chart(f.fig_hist_l1fee_usd, use_container_width=True)


        m2.write(""" #### **L2 Gas Fees per Day**""")
        m2.write("""*Total L2 transaction fees on Optimism each day. Sum in USD.
        [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
        m2.plotly_chart(f.fig_hist_l2fee_usd, use_container_width=True)

    # ------------> Gas Price
    m1, m2 = st.columns((1, 1))
    m1.write(""" #### **L1 Average Gas Price**""")
    m1.write("""*Average Gas price per transaction on Optimism L1 each day. Weighted by gas used.
            [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    m1.plotly_chart(f.fig_hist_l1gas_prc, use_container_width=True)

    m2.write(""" #### **L2 Average Gas Price**""")
    m2.write("""*Average Gas price per transaction on Optimism L2 each day. Weighted by gas used.
                [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    m2.plotly_chart(f.fig_hist_l2gas_prc, use_container_width=True)

    # ------------> Gas Used
    n1, n2 = st.columns((1, 1))
    n1.write(""" #### **L1 Gas Used per Day**""")
    n1.write("""*Aggregated Gas used for transaction on Optimism L1 each day.
                [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    n1.plotly_chart(f.fig_hist_l1gas_used, use_container_width=True)

    n2.write(""" #### **L2 Gas Used per Day**""")
    n2.write("""*Aggregated Gas used for transaction on Optimism L2 each day.
                    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    n2.plotly_chart(f.fig_hist_l2gas_used, use_container_width=True)


elif selected == 'Users Activity':
    st.write(f'# {selected}')

    st.write(""" #### **Unique Users per Day**""")
    st.write("""*The number of unique addresses that sent a transaction on Optimism each day.
    [More](https://app.flipsidecrypto.com/velocity/queries/51c77615-ff28-44e0-953a-db05b8e8f0e5)*""")
    st.plotly_chart(f.fig_hist_user, use_container_width=True)

    st.write(""" #### **$OP Holder Activities**""")
    st.write("""*The distribution of transaction event types of active Optimism token holders each week.
    [More](https://app.flipsidecrypto.com/velocity/queries/496eccbb-bcdd-4f91-8337-27eb68088abe)*""")
    st.plotly_chart(f.fig_hist_hold_distr, use_container_width=True)

    st.markdown("""---""")

    st.write(""" ## **Active User Days Active**""")
    st.write(""" *Average amount of days an address transacted per time period.*""")

    st.write(""" #### **Average Days Active - ALL**""")
    st.write(""" *Average Days active for all transaction types. 
    [More](https://app.flipsidecrypto.com/velocity/queries/44f30ebd-f448-418c-91fb-71ba02384555)*""")
    st.plotly_chart(f.fig_act_d_all, use_container_width=True)

    n1, n2 = st.columns((1, 1))
    n1.write(""" #### **Average Days Active - CEX**""")
    n1.write(""" *Average Days active for transactions associated with centralize exchanges. 
        [More](https://app.flipsidecrypto.com/velocity/queries/44f30ebd-f448-418c-91fb-71ba02384555)*""")
    n1.plotly_chart(f.fig_act_d_cex, use_container_width=True)

    n2.write(""" #### **Average Days Active - DEX**""")
    n2.write(""" *Average Days active for transactions associated with decentralized exchanges. 
            [More](https://app.flipsidecrypto.com/velocity/queries/5b3ce87e-962d-46d3-8b4c-fbdd15768fab)*""")
    n2.plotly_chart(f.fig_act_d_dex, use_container_width=True)

    n1.write(""" #### **Average Days Active - DEFI**""")
    n1.write(""" *Average Days active for transactions associated with Defi. 
            [More](https://app.flipsidecrypto.com/velocity/queries/0667dc68-00a1-42f0-a3f3-959bf8d3d2f7)*""")
    n1.plotly_chart(f.fig_act_d_defi, use_container_width=True)

    n2.write(""" #### **Average Days Active - DAPP**""")
    n2.write(""" *Average Days active for transactions associated with DAPP. 
            [More](https://app.flipsidecrypto.com/velocity/queries/0dd73c9c-7ab7-42d3-8003-2545c9400f66)*""")
    n2.plotly_chart(f.fig_act_d_dapp, use_container_width=True)

    n1.write(""" #### **Average Days Active - Layer2**""")
    n1.write(""" *Average Days active for transactions associated with L2. 
            [More](https://app.flipsidecrypto.com/velocity/queries/90438ee2-5de7-47f1-bc2b-a1d63e0a2ee5)*""")
    n1.plotly_chart(f.fig_act_d_l2, use_container_width=True)

    n2.write(""" #### **Average Days Active - NFT**""")
    n2.write(""" *Average Days active for transactions associated with NFT. 
            [More](https://app.flipsidecrypto.com/velocity/queries/d6d8169c-88a5-4b17-b7ef-bea14ecc59e1)*""")
    n2.plotly_chart(f.fig_act_d_nft, use_container_width=True)



elif selected == 'Staking and Bridging':
    st.write(f'# {selected}')

    st.write(""" #### **Total Liquidity on Optimism**""")
    st.write(""" *The number of assets that are currently being staked on Optimism. Data sourced from DefiLlama API. For more, check out the About section.*""")
    st.plotly_chart(f.fig_tvl, use_container_width=True)

    st.write(""" #### **Bridge Transactions and Depositers per Day**""")
    st.write(""" *Bridge transactions is the number of inflow and outflow transactions 
    associated with Optimism bridges each day. Bridge depositers is the number of unique addresses that 
    bridged from ETH to Optimism each day. [More](https://app.flipsidecrypto.com/velocity/queries/a6767ad0-2bd3-48b1-a132-6e7bc732ac27)*""")
    n1, n2 = st.columns((1, 1))
    n1.plotly_chart(f.fig_hist_brg_txs, use_container_width=True)
    n2.plotly_chart(f.fig_hist_brg_deposit, use_container_width=True)

    st.write(""" #### **Monthly Bridge Inflow Volume (from Ethereum)**""")
    st.write("""*The monthly inflow volume of assets bridged from Ehereum to Optimism. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgVolumeIn, use_container_width=True)

    st.write(""" #### **Monthly Bridged Token Distribution (from Ethereum)**""")
    st.write("""*The monthly distribution for bridge inflow volume by tokens bridged. [More](https://app.flipsidecrypto.com/velocity/queries/d7063e34-f6af-448e-98b4-62250b5bac09)*""")
    st.plotly_chart(f.fig_hist_brgInTokens, use_container_width=True)

    st.write(""" #### **Bridged User Behaviors**""")
    st.write("""*Destinations and type of actions of bridged Optimism users. Distribution for historical aggregates. [More for protocols used.](https://app.flipsidecrypto.com/velocity/queries/38a8d8f0-59be-4417-a1d1-6129589cb6fc)
            [ More for usage.](https://app.flipsidecrypto.com/velocity/queries/945ca0fc-dbcd-4a5d-99ad-67c1d66e3fce)*""")

    m1, m2 = st.columns((1, 1))
    m1.plotly_chart(f.fig_brgIn_platform, use_container_width=True)
    m2.plotly_chart(f.fig_brgIn_usage, use_container_width=True)

    st.write(""" #### **Monthly Bridge Ouflow Volume**""")
    st.write("""*The monthly outflow volume of assets bridged from Optimism to other chains. [More](https://app.flipsidecrypto.com/velocity/queries/ae10e2fc-ce56-40ab-b60f-9945c36c5491)*""")
    st.plotly_chart(f.fig_hist_brgVolumeOut, use_container_width=True)

elif selected == 'Ecosystem and Development':
    st.write(f'# {selected}')

    st.write(""" #### **Daily Active Contracts**""")
    st.write("""*Total number of active contracts on Optimism each day. [More](https://app.flipsidecrypto.com/velocity/queries/5e0853a7-17d0-4a43-92fc-f4fac754e073)*""")
    st.plotly_chart(f.fig_dev_act, use_container_width=True)

    st.write(""" #### **Daily Active Contracts Breakdown**""")
    st.write("""*Total number of active contracts on Optimism each day for popular transaction types. [More](https://app.flipsidecrypto.com/velocity/queries/72be8fec-cca7-44a0-8e3d-34767bd71b86)*""")
    st.plotly_chart(f.fig_dev_act_brkdwn, use_container_width=True)

    st.write(""" #### **Top 10 Delegate**""")
    st.markdown("""*Top 10 delegate by amount delegated(OP) 
    [More](https://app.flipsidecrypto.com/velocity/queries/00457e10-f65d-4cc5-95da-e7c1adf8206f)*""")

    p1, p2 = st.columns((1, 1))
    p1.plotly_chart(f.fig_delegator_amt, use_container_width=True)
    p2.plotly_chart(f.fig_delegator, use_container_width=True)

    st.markdown("""---""")
    st.write(""" ## **Popular Projects (Last 30 Days)**""")
    st.markdown("""*A deeper dive into the Optimism ecosystem breakdown by projects. 
    Most popular projects in the past 30 days are listed below. 
    [More](https://app.flipsidecrypto.com/velocity/queries/9a88a69e-74fb-4cb1-9529-61662699dfd8)*""")

    st.write(""" #### **Total Transactions per Day**""")
    st.write(""" *The number of transactions on Optimism each day by popular transaction types and projects.* """)

    n1, n2 = st.columns((1, 2))
    n1.plotly_chart(f.fig_curr_type_txs, use_container_width=True)
    n2.plotly_chart(f.fig_curr_proj_txs, use_container_width=True)

    st.write(""" #### **Total Users per Day**""")
    st.write(""" *The number of users on Optimism each day by popular transaction types and projects.* """)

    m1, m2 = st.columns((1, 2))
    m1.plotly_chart(f.fig_curr_type_users, use_container_width=True)
    m2.plotly_chart(f.fig_curr_proj_users, use_container_width=True)

    #st.write(""" #### Popular Projects Stats""")
    st.plotly_chart(f.fig_top_proj_table, use_container_width=True)

else:
    st.write(f'# {selected}')







