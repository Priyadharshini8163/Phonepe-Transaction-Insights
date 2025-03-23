import pandas as pd
import numpy as np
import json
import os
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import plotly.express as px
import plotly.io as pio
import nbformat
import streamlit as st

st.set_page_config(
    page_title="PhonePe Transaction Insights",  # Title of the page (appears in the browser tab)
    page_icon=":guardsman:",  # Icon displayed in the browser tab (emoji, URL to an image, etc.)
    layout="wide",  # Layout style: 'centered' or 'wide'
    initial_sidebar_state="auto"  # Sidebar state: 'auto', 'expanded', or 'collapsed'
)
#st.title("PhonePe Transaction Insights")

st.markdown("""
<style>
body {
    background-color: "#FFFFFF";
}
</style>
""", unsafe_allow_html=True)





#MYSQL Connection Establishment to create required DataFrames
def get_data(query, params=None):
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='mysql@123',database="Phonepe")
    if params:
        df = pd.read_sql_query(query, conn, params=params)
    else:
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

map_state = {
'andaman-&-nicobar-islands': 'Andaman & Nicobar',
'andhra-pradesh': 'Andhra Pradesh',
'arunachal-pradesh': 'Arunachal Pradesh',
'assam': 'Assam',
'bihar': 'Bihar',
'chandigarh': 'Chandigarh',
'chhattisgarh': 'Chhattisgarh',
'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
'delhi': 'Delhi',
'goa': 'Goa',
'gujarat': 'Gujarat',
'haryana': 'Haryana',
'himachal-pradesh': 'Himachal Pradesh',
'jammu-&-kashmir': 'Jammu & Kashmir',
'jharkhand': 'Jharkhand',
'karnataka': 'Karnataka',
'kerala': 'Kerala',
'ladakh': 'Ladakh',
'madhya-pradesh': 'Madhya Pradesh',
'maharashtra': 'Maharashtra',
'manipur': 'Manipur',
'meghalaya': 'Meghalaya',
'mizoram': 'Mizoram',
'nagaland': 'Nagaland',
'odisha': 'Odisha',
'puducherry': 'Puducherry',
'punjab': 'Punjab',
'rajasthan': 'Rajasthan',
'sikkim': 'Sikkim',
'tamil-nadu': 'Tamil Nadu',
'telangana': 'Telangana',
'tripura': 'Tripura',
'uttar-pradesh': 'Uttarakhand',
'uttarakhand': 'Uttar Pradesh',
'west-bengal': 'West Bengal'}

col1,col2 = st.columns([1,8])
with col1:
    st.image("C:/Users/conta/OneDrive/Desktop/Phonepe/logo.png")
with col2:
    st.title("Phonepe Transaction Insights")



r = st.sidebar.radio('Navigation',["Home Page","Business Case Study"],index=0)
if r == "Home Page":
    st.subheader("**A Streamlit App for Exploring Phonepe Transaction & User Trends**")
    st.write(""" With the increasing reliance on digital payment systems like PhonePe, understanding the dynamics of transactions and user engagement
             is crucial for improving services and targeting users effectively. 
             This project aims to analyze and visualize aggregated values of payment categories, 
             create maps for total values at state and district levels, and identify top-performing states, districts, and pin codes.

    **Database Used:** `Phone_pay`
    """)

    col1,col2 = st.sidebar.columns(2,gap="small")
    with col1:
        category = ["Transaction","User"]
        cat_select = st.sidebar.selectbox("",category)
    with col2:
        q = f"select DISTINCT concat(Year,'_Q', Quater) as Year_Qtr from agg_transaction;"
        df = get_data(q)
        yq_select = st.sidebar.selectbox("",df)



    if cat_select == "Transaction":
        tabname = "trans"
        cntname = "Transaction_District_count"
        cnt2name = "Transaction_Pincode_count"

        q = f'''select sum(Transaction_count) as 'Total Transactions',sum(Transaction_amount) as 'Total Revenue',
            avg(Transaction_count) as 'Avg Transactions',avg(Transaction_amount) as 'Average Revenue'
            from agg_transaction where concat(Year,'_Q', Quater) = \"{yq_select}\"
            order by 2 DESC limit 10;'''
        df = get_data(q)
        total_transactions = df['Total Transactions'].iloc[0]
        total_revenue = df['Total Revenue'].iloc[0]
        avg_transactions = df['Avg Transactions'].iloc[0]
        avg_revenue = df['Average Revenue'].iloc[0]

        col1, col2 = st.columns(2,gap = "small")
        with col1:
            st.metric('Total Transactions',value=total_transactions)
        with col2:
            st.metric('Total Revenue (₹)',value=total_revenue)    
        col1, col2 = st.columns(2,gap = "small")
        with col1:
            st.metric('Average Transactions',value=avg_transactions)    
        with col2:
            st.metric('Average Revenue (₹)',value=avg_revenue)    

        #INDIA MAP
        df = pd.read_csv("C:/Users/conta/OneDrive/Desktop/Phonepe/csv/Agg_Transaction.csv")
        df['State'] = df['State'].map(map_state)
        df['Year_Qtr'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        df1 = df[(df['Year_Qtr'] == yq_select)]
        state_list = df1['State'].unique()
        df2 = df1.groupby(['State']).agg(transcount=('Transaction_count', 'sum')).reset_index()
        fig = px.choropleth(
            df2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",  # This should match the property key in the GeoJSON file
            locations="State",  # Column in df1 that holds the state names
            color="transcount",  # Using transaction count as the color scale
            color_continuous_scale="Reds",
            labels={'transcount': 'Total Transactions'}
        )

        fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
        )

        fig.update_layout(
            width=1200,
            height=800,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=True ,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    else:
        tabname = "user"
        cntname = "User_DistrictRegisteredusers"
        cnt2name = "User_PincodeRegisteredusers"

        q = f'''SELECT sum(Users_count) as 'Total Users', avg(Users_count) as 'Average Users' FROM agg_users
         where concat(Year,'_Q', Quater) = \"{yq_select}\";'''
        df = get_data(q)
        total_users = df['Total Users'].iloc[0]
        avg_users = df['Average Users'].iloc[0]
        col1,col2 = st.columns(2,gap="small")
        with col1:
            st.metric('Total Users',value=total_users)
        with col2:
            st.metric('Average Users',value=avg_users)

        #INDIA MAP
        df = pd.read_csv("C:/Users/conta/OneDrive/Desktop/Phonepe/csv/Agg_Users.csv")
        df['State'] = df['State'].map(map_state)
        df['Year_Qtr'] = df['Year'].astype(str) + '_Q' + df['Quater'].astype(str)
        df1 = df[(df['Year_Qtr'] == yq_select)]
        state_list = df1['State'].unique()
        df2 = df1.groupby(['State']).agg(usrcount=('Users_count', 'sum')).reset_index()
        fig = px.choropleth(
            df2,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey="properties.ST_NM",  # This should match the property key in the GeoJSON file
            locations="State",  # Column in df1 that holds the state names
            color="usrcount",  # Using transaction count as the color scale
            color_continuous_scale="Blues",
            labels={'usrcount': 'Total Users'}
        )

        fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lat": 22, "lon": 80},
        lonaxis_range=[68, 98],
        lataxis_range=[6, 38],
        )

        fig.update_layout(
            width=1200,
            height=800,
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            coloraxis_showscale=True ,
            legend=dict(orientation="v", x=1, y=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)


    st.sidebar.write(f"**Top 10 {cat_select}s**")
    col1,col2,col3 = st.sidebar.columns([1,1,2])
    with col1:
        if st.button("State"):
            q = f''' Select concat(substr(upper(State),1,1),substr(lower(State),2)) as State, 
            sum({cntname}) as 'Total {cat_select}'
            from top_{tabname}_district
            where concat(Year,'_Q', Quater) = \"{yq_select}\" 
            group by State order by 2 DESC limit 10;
                '''
            df = get_data(q)
            st.sidebar.write(df[['State',f'Total {cat_select}']].set_index('State'))
        
    with col2:
        if st.button('District'):
            q = f''' Select concat(substr(upper({cat_select}_District),1,1),substr(lower({cat_select}_District),2)) as District, 
            sum({cntname}) as 'Total {cat_select}'
            from top_{tabname}_district
            where concat(Year,'_Q', Quater) = \"{yq_select}\" 
            group by District order by 2 DESC limit 10;
            '''
            df = get_data(q)
            st.sidebar.write(df[['District',f'Total {cat_select}']].set_index('District'))
    
    with col3:
        if st.button("Postal Codes"):
            q = f''' Select concat(substr(upper({cat_select}_Pincode),1,1),substr(lower({cat_select}_Pincode),2)) as 'Postal Codes', 
            sum({cnt2name}) as 'Total {cat_select}'
            from top_{tabname}_pincode
            where concat(Year,'_Q', Quater) = \"{yq_select}\"
            group by 1 order by 2 DESC limit 10;
        '''
            df = get_data(q)
            st.sidebar.write(df[['Postal Codes',f'Total {cat_select}']].set_index('Postal Codes'))


else:
    case_studies = ["Decoding Transaction Dynamics on PhonePe",
                    "Device Dominance and User Engagement Analysis",                    
                    "Transaction Analysis for Market Expansion",
                    "User Engagement and Growth Strategy",
                    "Transaction Analysis Across States and Districts",
                    "User Registration Analysis"]

    case_select = st.sidebar.selectbox("Select Business Case Study: ",case_studies)

    if case_select == case_studies[0]:

        st.subheader("Decoding Transaction Dynamics on PhonePe")
        st.write(''' PhonePe, a leading digital payments platform, has recently identified significant variations in transaction behavior 
                 across states, quarters, and payment categories. While some regions and transaction types demonstrate consistent growth, 
                 others show stagnation or decline. The leadership team seeks a deeper understanding of these patterns to drive targeted 
                 business strategies.
        ''')

        #Insight 1
        st.subheader("Top 10 States by Total Transaction Value")
        q = "select State, sum(Transaction_amount) as 'Total Transaction Value' from agg_transaction group by State order by 2 DESC limit 10;"
        df = get_data(q)
        st.bar_chart(df,x='State',y='Total Transaction Value')



        #Insight 2
        st.subheader("Most Popular Payment Category")
        col1,col2 = st.columns(2,gap="small")
        q = "select Transaction_type, sum(Transaction_count) as 'Total Number of Transactions', sum(Transaction_amount) as 'Total Transaction Value' from agg_transaction group by Transaction_type"
        df = get_data(q)
        
        with col1:
            fig1 = px.pie(df,
                     names='Transaction_type',
                     values='Total Number of Transactions',
                     title="Distribution of Transaction value",
                     hole=0.4,
                     labels=['Transaction_type','Total Number of Transactions'])
            st.plotly_chart(fig1)  
        with col2:
            fig2 = px.pie(df,
                     names='Transaction_type',
                     values='Total Transaction Value',
                     title="Distribution of Transaction Volume",
                     hole=0.4,
                     labels=['Transaction_type','Total Transaction Value'])
            st.plotly_chart(fig2)  

        
        #Insight 3
        st.subheader(f"Total Transaction Value by Payment Category")
        q = "select State from agg_transaction group by State;"
        ste = get_data(q)      
        ste_select = st.selectbox("Select State: ", ste)
        q = f"select Transaction_type,sum(Transaction_amount) as 'Total Transaction Value' from agg_transaction where State = \"{ste_select}\" group by Transaction_type;"
        df = get_data(q)
        st.line_chart(df,x='Transaction_type', y='Total Transaction Value')



        #Insight 4
        st.subheader("Total Transaction Value Over Trend")
        q = f"select concat(Year,'_Q', Quater) as Year_Qtr,sum(Transaction_amount) as 'Total Transaction Value' from agg_transaction where State = \"{ste_select}\" group by 1;"
        df = get_data(q)
        
        lne = px.line(df,x='Year_Qtr', y='Total Transaction Value',
            labels={'Year_Qtr': 'Year & Quarter','total_trans_amt': 'Total Transaction Value'},
            title='Total Transaction Value Trend')
        st.plotly_chart(lne)




    #2. Device Dominance and User Engagement Analysis
    elif case_select == case_studies[1]:   
        st.subheader("Device Dominance and User Engagement Analysis")
        st.write('''PhonePe aims to enhance user engagement and improve app performance by understanding user preferences across 
                 different device brands. The data reveals the number of registered users and app opens, segmented by device brands, 
                 regions, and time periods. However, trends in device usage vary significantly across regions, 
                 and some devices are disproportionately underutilized despite high registration numbers
        ''')

        #Insight 1
        st.subheader("Total Registered Users by State")
        q = '''SELECT State, Year, Quater, SUM(RegisteredUsers) as 'Total Registered Users'
        FROM (
            SELECT State, Year, Quater, RegisteredUsers,
                row_number() OVER (PARTITION BY State, Year, Quater ORDER BY RegisteredUsers) AS rownum
            FROM agg_users
        ) AS ranked_users
        WHERE rownum = 1
        GROUP BY State, Year, Quater;'''
        df = get_data(q)
        st.bar_chart(df,x='State', y='Total Registered Users')



        #Insight 2
        st.subheader("Distribution of Users count and Usage ratio by State")
        q = "select State from agg_users group by State;"
        ste = get_data(q)      
        ste_select = st.selectbox("Select State: ", ste)

        q = f"""
        select Users_brand, sum(Users_count) as 'Users Count' from agg_users
        where State = \"{ste_select}\" group by Users_brand order by 2 DESC;
        """
        df = get_data(q)
        fig = px.pie(df,
                     names='Users_brand',
                     values='Users Count',
                     title="Distribution of Users by Device Brand",
                     hole=0.4,
                     labels=['Users_brand','Users Count'])
        st.plotly_chart(fig)  



        #Insight 3:
        q = f""" Select concat(Year,"_Q", Quater) as Year_Qtr, Users_percentage * 100 as Users_percentage, Users_brand
        FROM agg_users where State = \"{ste_select}\";
        """
        df = get_data(q)
        lne = px.line(df,x='Year_Qtr', y='Users_percentage',
                title='Device Usage Ratio Over Time',
                labels={'Year_Qtr': 'Year & Quarter','Users_percentage': 'Usage Ratio'},
                color=df['Users_brand'], markers=True)
        st.plotly_chart(lne)



        #Insight 4:
        st.subheader("Underutilized Devices by State")
        q = f""" Select State, Users_brand, Users_percentage
        FROM agg_users where Users_percentage < 0.10;
        """
        df = get_data(q)
        sctr = px.scatter(df,x='State', y='Users_brand',size='Users_percentage',
                    title='Underutilized Devices by State',
                    size_max=15,
                    labels={'State': 'State','Users_brand': 'Device Brand'},
                    color='Users_brand')        
        # Increase chart size (width and height)
        sctr.update_layout(
            width=1000,  # Width of the chart
            height=700,  # Height of the chart
        )
        st.plotly_chart(sctr)
        



    elif case_select == case_studies[2]: 
        st.subheader("Transaction Analysis for Market Expansion")
        st.write('''PhonePe operates in a highly competitive market, and understanding transaction dynamics at the state level is crucial 
                 for strategic decision-making. With a growing number of transactions across different regions, 
                 the company seeks to analyze its transaction data to identify trends, opportunities, and potential areas for expansion.
        ''')

        #Insight 1 & 2:
        col1,col2,col3 = st.columns(3,gap="small")
        with col1:
            q = "select State from agg_users group by State;"
            ste = get_data(q)    
            ste_select = st.selectbox("Select State: ", ste)
        with col2:
            q = "select Year from agg_transaction group by Year;"
            yr = get_data(q)
            yr_sel = st.selectbox("Select Year: ", yr)
        with col3:    
            q = "select Quater from agg_transaction group by Quater;"
            qr = get_data(q)
            q_sel = st.selectbox("Select Quarter: ", qr)


        q = f'''
        SELECT * from map_transaction_hover
        WHERE State = \"{ste_select}\" AND Year = \"{yr_sel}\" AND Quater = {q_sel}
        ORDER BY Transaction_Hover_count DESC;
        '''
        df = get_data(q)        
        brr = px.bar(df,x='Transaction_Hover_name', y='Transaction_Hover_amount',
                title='Total Transaction Amount by District',
                labels={'Transaction_Hover_name': 'Districts','Transaction_Hover_amount': 'Total Transaction Amount'})
        st.plotly_chart(brr)
        
     
        brr = px.bar(df,x='Transaction_Hover_name', y='Transaction_Hover_count',
                title='Total Transactions by District',
                labels={'Transaction_Hover_name': 'Districts','Transaction_Hover_count': 'Total Number of Transactions'})
        st.plotly_chart(brr)


        #Insight 3:
        q = f'''Select *, concat(Year,"_Q", Quater) as Year_Qtr FROM map_transaction_hover
        WHERE State = \"{ste_select}\";
        '''
        df = get_data(q)

        lne = px.line(df,x='Year_Qtr', y='Transaction_Hover_count',
                title='Transaction ratio over time by Districts',
                labels={'Year_Qtr': 'Year & Quarter','Transaction_Hover_count': 'District Level Number of Transaction'},
                color=df['Transaction_Hover_name'], markers=True)
        lne.update_layout(width = 2000, height=500,)
        st.plotly_chart(lne)






    elif case_select == case_studies[3]:         
        st.subheader("User Engagement and Growth Strategy")
        st.write('''PhonePe seeks to enhance its market position by analyzing user engagement across different states and districts. 
                 With a significant number of registered users and app opens, 
                 understanding user behavior can provide valuable insights for strategic decision-making and growth opportunities.
        ''')

        #Insight 1:
        st.subheader("User engagement with the Phonepe App")
        col1,col2 = st.columns(2,gap="small")
        with col1:
            q = "select Upper(State) from agg_users group by State;"
            ste = get_data(q)    
            ste_select = st.selectbox("Select State: ", ste)
        with col2:
            q = "select Year from agg_transaction group by Year;"
            yr = get_data(q)
            yr_sel = st.selectbox("Select Year: ", yr)

        q = f''' Select District, sum(((App_Opens/ Registered_Users) * 100)) as App_Opens_Rate from map_user_hover
        where State = \"{ste_select}\" AND Year = \"{yr_sel}\"
        Group by District order by 2 DESC;
        '''

        df = get_data(q)        
        brr = px.bar(df,x='District', y='App_Opens_Rate',
                title='App Open Rate by District',
                labels={'District': 'Districts','App_Opens_Rate': 'App Opens Rate'})
        st.plotly_chart(brr)



        #Insight 2:
        q = f''' Select substr(District,1,instr(District,'District')-1) as Districts, 
        concat(Year,"_Q",Quater) as Year_Qtr, 
        sum(((App_Opens/ Registered_Users) * 100)) as App_Opens_Rate
        FROM map_user_hover
        WHERE State =  \"{ste_select}\" AND Year = \"{yr_sel}\"
        GROUP BY Districts, Year_Qtr;
        '''
        df = get_data(q)

        lne = px.line(df, x='Year_Qtr', y='App_Opens_Rate',
                title='Trends in App Open Rate Over Time',
                labels={'Year_Qtr': 'Year & Quarter','App_Opens_Rate': 'App Opens Rate'},
                color=df['Districts'], markers=True)
        #lne.update_layout(width = 1000, height=500,)
        #lne.update_layout(
        #       yaxis=dict(
        #        tickmode='linear',  # Use linear tick mode
        #        dtick=10,  # Set the tick interval to 10 (adjust as needed)
        #       ))
        st.plotly_chart(lne)


        #Insight 3:
        q = f"Select * FROM map_user_hover where Year = \"{yr_sel}\";"
        df = get_data(q)
        df['first_quarter'] = df.groupby('State')['Quater'].transform('min')

        retention = df[df['Quater'] > df['first_quarter']].groupby(['State', 'Year', 'Quater']).agg(
             returning_users=('Registered_Users', 'sum')
            ).reset_index()
        
        retention = pd.merge(retention, df, on=['State', 'Year', 'Quater'])
        
        fig = px.line(retention, x='Quater', y='returning_users',
                      title='Retention of Users by State Over Quarters',
                      labels={'Quater': 'Quarter','returning_users': 'Retained Users'},
                      color=retention['State'],markers= 'o')
        
        st.plotly_chart(fig)






    elif case_select == case_studies[4]: 
        st.subheader("Transaction Analysis Across States and Districts")
        st.write('''PhonePe is conducting an analysis of transaction data to identify the top-performing states, districts, and pin codes
                  in terms of transaction volume and value. 
                 This analysis will help understand user engagement patterns and identify key areas for targeted marketing efforts..        
        ''')

        #Insight 1:
        q = ''' Select concat(substr(upper(State),1,1),substr(lower(State),2)) as State, 
            sum(Transaction_District_count) as Transaction_Value
            from top_trans_district 
            group by State order by Transaction_Value DESC limit 10;
                '''
        df = get_data(q)
        fig = px.bar(df,x='State', y='Transaction_Value',
                     title='Top 10 Total Number of Transactions by State',
                     labels={'State': 'State', 'Transaction_Value': 'Total Transaction Value'})

        st.plotly_chart(fig)

        #Insight 1b:
        q = "select *, concat(Year,'_Q', Quater) as Year_Qtr from top_trans_district"
        df = get_data(q)
        
        df1 = df.groupby(['State','Year_Qtr']).agg(tot_trans_usr=('Transaction_District_count','sum')).reset_index()

        lne = px.line(df1, x='Year_Qtr', y='tot_trans_usr',
            labels={'Year_Qtr': 'Year & Quarter','tot_trans_usr': 'Total Transactions'},
            title='Total Transactions Trend by State',
            color=df1['State'])
        st.plotly_chart(lne)



        #Insight 2:
        q = ''' Select concat(substr(upper(Transaction_District),1,1),substr(lower(Transaction_District),2)) as Transaction_District, 
                sum(Transaction_District_count) as Transaction_Value
                from top_trans_district 
                group by Transaction_District order by Transaction_Value DESC limit 10;
            '''
        df = get_data(q)
        fig = px.bar(df,x='Transaction_District', y='Transaction_Value',
                     title='Top 10 Total Number of Transactions by Districts',
                     labels={'Transaction_District': 'Districts', 'Transaction_Value': 'Total Transaction Value'})

        st.plotly_chart(fig)

        #Insight 2b:
        q = "select State from agg_users group by State;"
        ste = get_data(q)      
        ste_select = st.selectbox("Select State: ", ste)

        q = "select *, concat(Year,'_Q', Quater) as Year_Qtr from top_trans_district"
        df = get_data(q)
        
        df1 = df.groupby(['State','Transaction_District','Year_Qtr']).agg(tot_trans_usr=('Transaction_District_count','sum')).reset_index()
        df1 = df1[df1['State'] == ste_select]

        lne = px.line(df1, x='Year_Qtr', y='tot_trans_usr',
            labels={'Year_Qtr': 'Year & Quarter','tot_trans_usr': 'Total Transactions'},
            title='Total Transactions Trend at District Level',
            color=df1['Transaction_District'])
        lne.update_layout(
            xaxis=dict(
            tickmode='linear',  # Make ticks linear
            dtick=1  # Display a tick for every data point, set dtick=1 to show each x-axis label
            ))
        st.plotly_chart(lne, use_container_width=True)


        #Insight 3:
        col1,col2 = st.columns(2,gap="small")
        with col1:
            q = ''' Select concat(substr(upper(Transaction_Pincode),1,1),substr(lower(Transaction_Pincode),2)) as 'Postal Codes', 
                    sum(Transaction_Pincode_count) as 'Transaction Value'
                    from top_trans_pincode
                    group by 1 order by 2 DESC limit 10;
                '''
            df = get_data(q)
            st.markdown("**Top 10 Transactions by Postal Codes**")
            st.table(df.set_index('Postal Codes'))

        with col2:
            q = ''' Select concat(substr(upper(Transaction_Pincode),1,1),substr(lower(Transaction_Pincode),2)) as 'Postal Codes', 
                    sum(Transaction_Pincode_amount) as Transaction_Volume
                    from top_trans_pincode
                    group by Transaction_Pincode order by Transaction_Volume DESC limit 10;
                '''
            df = get_data(q)
            st.markdown("**Top 10 Transaction Volume by Postal Codes**")
            st.table(df.set_index('Postal Codes'))






    elif case_select == case_studies[5]:         
        st.subheader("User Registration Analysis")
        st.write('''PhonePe aims to conduct an analysis of user registration data to identify the top states, districts, and pin codes 
                 from which the most users registered during a specific year-quarter combination. 
                 This analysis will provide insights into user engagement patterns and highlight potential growth areas.
        ''')

        #Insight 1a:
        q = ''' Select concat(substr(upper(State),1,1),substr(lower(State),2)) as State, 
            sum(User_DistrictRegisteredUsers) as Total_Registered_Users
            from top_user_district 
            group by State order by Total_Registered_Users DESC limit 10;
        '''
        df = get_data(q)
        fig = px.bar(df,x='State', y='Total_Registered_Users',
                     title='Top 10 Total Number of Registered Users at State Level',
                     labels={'State': 'State','Total_Registered_Users': 'Total Registered Users'})
        st.plotly_chart(fig)

        #Insight 1b:
        q = "select *, concat(Year,'_Q', Quater) as Year_Qtr from top_user_district"
        df = get_data(q)
        
        df1 = df.groupby(['State','Year_Qtr']).agg(tot_reg_usr=('User_DistrictRegisteredUsers','sum')).reset_index()

        lne = px.line(df1, x='Year_Qtr', y='tot_reg_usr',
            labels={'Year_Qtr': 'Year & Quarter','tot_reg_usr': 'Total Registered Users'},
            title='Total Number of Registered Users Trend by State',
            color=df1['State'])
        st.plotly_chart(lne)


        #Insight 2a:
        q = ''' Select concat(substr(upper(User_District),1,1),substr(lower(User_District),2)) as District, sum(User_DistrictRegisteredUsers) as Total_Registered_Users
            from top_user_district
            group by District order by 2 DESC limit 10;
            '''
        df = get_data(q)
        fig = px.bar(df,x='District', y='Total_Registered_Users',
                     title='Top 10 Total Number of Registered Users at District Level',
                     labels={'District': 'Districts','Total_Registered_Users': 'Total Registered Users'})
        st.plotly_chart(fig)

        #Insight 2b:
        q = "select State from agg_users group by State;"
        ste = get_data(q)      
        ste_select = st.selectbox("Select State: ", ste)

        q = "select *, concat(Year,'_Q', Quater) as Year_Qtr from top_user_district"
        df = get_data(q)
        
        df1 = df.groupby(['State','User_District','Year_Qtr']).agg(tot_reg_usr=('User_DistrictRegisteredUsers','sum')).reset_index()
        df1 = df1[df1['State'] == ste_select]

        lne = px.line(df1, x='Year_Qtr', y='tot_reg_usr',
            labels={'Year_Qtr': 'Year & Quarter','tot_reg_usr': 'Total Registered Users'},
            title='Total Number of Registered Users Trend at District Level',
            color=df1['User_District'])
        st.plotly_chart(lne)


        #Insight 3:
        q = ''' Select User_Pincode as 'Postal Codes', sum(User_PincodeRegisteredUsers) as 'Total Registered Users'
            from top_user_pincode
            group by User_Pincode order by 2 DESC limit 10;
                '''
        df = get_data(q)
        st.markdown("**Top 10 Number of Registered Users by Postal Codes**")
        col1,col2 = st.columns([1,2])
        with col1:
            st.table(df.set_index('Postal Codes'))


    else:
        pass


st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            text-align: center;
            background-color: white;
            padding: 1px;
            font-size: 12px;
            color: #333;
            z-index: 1;  /* Ensure the footer stays above content */
            display: flex;
            justify-content: center;  /* Center horizontally */
            align-items: flex-end;  /* Align text to the bottom */
        }
    </style>
    <div class="footer">
        <p>Created by Priyadharshini S</p>
    </div>
""", unsafe_allow_html=True)
