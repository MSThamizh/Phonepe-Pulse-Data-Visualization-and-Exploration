import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import plotly.graph_objects as go
import streamlit as st
from streamlit_option_menu import option_menu

# SQL Connection
connection= mysql.connector.connect(host="localhost",user="root",password="SQL@2023",database="phonepe_data")
mycursor=connection.cursor()

# Alter State Name
def AlterState(df):
    df['State'] = df['State'].str.title()
    df['State'] = df['State'].replace({'Andaman-&-Nicobar-Islands':'Andaman & Nicobar', 
                                    'Andhra-Pradesh':'Andhra Pradesh', 
                                    'Arunachal-Pradesh':'Arunachal Pradesh', 
                                    'Dadra-&-Nagar-Haveli-&-Daman-&-Diu':'Dadra and Nagar Haveli and Daman and Diu', 
                                    'Himachal-Pradesh':'Himachal Pradesh', 
                                    'Jammu-&-Kashmir':'Jammu & Kashmir', 
                                    'Madhya-Pradesh':'Madhya Pradesh', 
                                    'Tamil-Nadu':'Tamil Nadu', 
                                    'Uttar-Pradesh':'Uttar Pradesh', 
                                    'West-Bengal':'West Bengal'})

# SQL to Dataframe
# Aggregate Insurance Dataframe
mycursor.execute("select * from agg_ins")
result1 = mycursor.fetchall()
Agg_Ins_DF=pd.DataFrame(result1, columns=['State','Year','Quarter','Type','Count','Amount'])
AlterState(Agg_Ins_DF)

# Aggregate Transaction Dataframe
mycursor.execute("select * from agg_trans")
result2 = mycursor.fetchall()
Agg_Trans_DF=pd.DataFrame(result2, columns=['State','Year','Quarter','Type','Count','Amount'])
AlterState(Agg_Trans_DF)

# Aggregate User Dataframe
mycursor.execute("select * from agg_user")
result3 = mycursor.fetchall()
Agg_User_DF=pd.DataFrame(result3, columns=['State','Year','Quarter','Brand','Count','Percentage'])
AlterState(Agg_User_DF)

# Map Insurance Dataframe
mycursor.execute("select * from map_ins")
result4 = mycursor.fetchall()
Map_Ins_DF=pd.DataFrame(result4,columns=['State','Year','Quarter','District','Count','Amount'])
AlterState(Map_Ins_DF)

# Map Transaction Dataframe
mycursor.execute("select * from map_trans")
result5=mycursor.fetchall()
Map_Trans_DF=pd.DataFrame(result5,columns=['State','Year','Quarter','District','Count','Amount'])
AlterState(Map_Trans_DF)

# Map User Dataframe
mycursor.execute("select * from map_user")
result6=mycursor.fetchall()
Map_User_DF=pd.DataFrame(result6,columns=['State','Year','Quarter','District','RegisteredUsers','AppOpens'])
AlterState(Map_User_DF)

# Top Insurance Dataframe
mycursor.execute("select * from top_ins")
result7 = mycursor.fetchall()
Top_Ins_DF=pd.DataFrame(result7,columns=['State','Year','Quarter','Pincode','Count','Amount'])
AlterState(Top_Ins_DF)

# Top Transaction Dataframe
mycursor.execute("select * from top_trans")
result8=mycursor.fetchall()
Top_Trans_DF=pd.DataFrame(result8,columns=['State','Year','Quarter','Pincode','Count','Amount'])
AlterState(Top_Trans_DF)

# Top User Dataframe
mycursor.execute("select * from top_user")
result9=mycursor.fetchall()
Top_User_DF=pd.DataFrame(result9,columns=['State','Year','Quarter','Pincode','RegisteredUsers'])
AlterState(Top_User_DF)

# Top User Dataframe
mycursor.execute("select * from top_user")
result9=mycursor.fetchall()
Top_User_DF=pd.DataFrame(result9,columns=['State','Year','Quarter','Pincode','RegisteredUsers'])
AlterState(Top_User_DF)

# Aggregated Dataframe
df1_agg = Agg_Trans_DF.groupby(['State','Year','Quarter','Type'])[['Amount','Count']].sum()
df1_agg.reset_index(inplace=True)

df2_agg = Agg_Ins_DF.groupby(['State','Year','Quarter','Type'])[['Amount','Count']].sum()
df2_agg.reset_index(inplace=True)

df_agg = pd.concat([df1_agg,df2_agg],ignore_index=True)
df_agg = df_agg.groupby(['State','Year','Quarter','Type'])[['Amount','Count']].sum()
df_agg.reset_index(inplace=True)

YearSelectionOption=[]
for i in df_agg['Year'].unique():
    YearSelectionOption.append(i)

QuarterSelectionOption=[]
for i in df_agg['Quarter'].unique():
    QuarterSelectionOption.append(i)

# Map Dataframe
df1_map = Map_Trans_DF.groupby(['State','Year','Quarter','District'])[['Amount','Count']].sum()
df1_map.reset_index(inplace=True)

df2_map = Map_Ins_DF.groupby(['State','Year','Quarter','District'])[['Amount','Count']].sum()
df2_map.reset_index(inplace=True)

df_map = pd.concat([df1_map,df2_map],ignore_index=True)
df_map = df_map.groupby(['State','Year','Quarter','District'])[['Amount','Count']].sum()
df_map.reset_index(inplace=True)

for i in df_map['Year'].unique():
    YearSelectionOption.append(i)

for i in df_map['Quarter'].unique():
    QuarterSelectionOption.append(i)

# Top Dataframe
df1_top = Top_Trans_DF.groupby(['State','Year','Quarter','Pincode'])[['Amount','Count']].sum()
df1_top.reset_index(inplace=True)

df2_top = Top_Ins_DF.groupby(['State','Year','Quarter','Pincode'])[['Amount','Count']].sum()
df2_top.reset_index(inplace=True)

df_top = pd.concat([df1_top,df2_top],ignore_index=True)
df_top = df_top.groupby(['State','Year','Quarter','Pincode'])[['Amount','Count']].sum()
df_top.reset_index(inplace=True)

for i in df_top['Year'].unique():
    YearSelectionOption.append(i)

for i in df_top['Quarter'].unique():
    QuarterSelectionOption.append(i)

unique_years = list(set(YearSelectionOption))
unique_quarters = list(set(QuarterSelectionOption))

# Year Filter
def YearOptions(df):
    YearSelectionOption=[]
    for i in df['Year'].unique():
        YearSelectionOption.append(i)
    return YearSelectionOption

# Quarter Filter
def QuarterOptions(df):
    QuarterSelectionOption=[]
    for i in df['Quarter'].unique():
        QuarterSelectionOption.append(i)
    return QuarterSelectionOption

# Type Filter
def TypeOptions(df):
    TypeSelctionOption=[]
    for i in df['Type'].unique():
        TypeSelctionOption.append(i)
    return TypeSelctionOption

# State Filter
def StateOptions(df):
    StateSelctionOption=[]
    for i in df['State'].unique():
        StateSelctionOption.append(i)
    return StateSelctionOption

# Transaction Amount Across States - Bar Plot
def plot1(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_bar_amt = px.bar(df,x='State',y='Amount',title=f'Transaction Amount Across States - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,height=450, width=450)   
    st.plotly_chart(fig_bar_amt)

# Transaction Count Across States - Bar Plot
def plot2(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig__bar_count = px.bar(df,x='State',y='Count',title=f'Transaction Count Across States - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,height=450, width=450)
    st.plotly_chart(fig__bar_count)

# Transaction Amount Distribution Across Transaction Types - Donut Chart
def plot7(df,Year,Quarter):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df.groupby('Type')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut1=px.pie(df,
                    names='Type',
                    values='Amount',
                    title=f'Transaction Amount Distribution Across Transaction Types - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut1)

# Transaction Count Distribution Across Transaction Types - Donut Chart
def plot8(df,Year,Quarter):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df.groupby('Type')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut2=px.pie(df,
                    names='Type',
                    values='Count',
                    title=f'Transaction Count Distribution Across Transaction Types - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut2)

# Transaction Amount, Transaction Count Distribution Across States by Transaction Type - Bubble Chart
def plot9(df,Year,Quarter,Type):   
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['Type']==Type]
    df.reset_index(inplace=True)

    fig_line = px.line(df,x='State',y=['Amount','Count'],
                        title=f'Peer-to-peer payments: Transaction Amount, Transaction Count Distribution Across States- {2021} Q{1}',
                        color_discrete_sequence=["#AA0DFE","rgb(136,204,238)"], 
                        height=550,
                        width=900, markers=True  
    )
    st.plotly_chart(fig_line)

# Transaction Amount Across States  - Geo Plot
def plot3(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_amt = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State',
        featureidkey='properties.ST_NM',
        color='Amount',
        color_continuous_scale='Bupu', 
        range_color=(df['Amount'].min(),df['Amount'].max()),
        title=f"Transaction Amount Across States - {Year} Q{Quarter}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_amt.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_amt)

# Transaction Count Across States  - Geo Plot
def plot4(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_count = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State', 
        featureidkey='properties.ST_NM', 
        color='Count', 
        color_continuous_scale='Bupu',  
        range_color=(df['Count'].min(),df['Count'].max()),
        title=f"Transaction Count Across States  - {Year} Q{Quarter}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_count.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_count)


# Transction Amount Across Districts  - Bar Chart
def plot10(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_bar1 = px.bar(
    df,
    x='District',
    y='Amount',
    title=f"{State}: Transction Amount Across Districts - {Year} Q{Quarter}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_bar1)

# Transction Count Across Districts  - Bar Chart
def plot11(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_area1 = px.bar(
    df,
    x='District',
    y='Count',
    title=f"{State}: Transction Count Across Districts  - {Year} Q{Quarter}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_area1)

# Transaction Amount Across States - Bar Plot (Horizontal)
def plot5(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    df = df.sort_values('State',ascending=False)

    fig_bar_amt = px.bar(df,x='Amount',y='State',title=f'Transaction Amount Across States - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,height=500, width=900)   
    st.plotly_chart(fig_bar_amt)

# Transaction Count Across States - Bar Plot (Horizontal)
def plot6(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    df = df.sort_values('State',ascending=False)

    fig__bar_count = px.bar(df,x='Count',y='State',title=f'Transaction Count Across States - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,height=500, width=900)
    st.plotly_chart(fig__bar_count)

# Transaction Amount Distribution Across Pincode - Pie Chart
def plot12(df,Year,Quarter,State):    
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_pie1=px.pie(df,
                    names='Pincode',
                    values='Amount',
                    title=f'{State}: Transaction Amount Distribution Across Pincode - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_pie1)

# Transaction Count Distribution Across Pincode
def plot13(df,Year,Quarter,State):    
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_pie2=px.pie(df,
                    names='Pincode',
                    values='Count',
                    title=f'{State}: Transaction Count Distribution Across Pincode - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_pie2)

# Charts without Quarter Selection
# Transaction Amount Across States - Bar Plot
def plot1_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_bar_amt = px.bar(df,x='State',y='Amount',color='Quarter',title=f'Transaction Amount Across States - {Year}',
                    color_discrete_sequence=px.colors.qualitative.Antique,height=450, width=450)
    
    st.plotly_chart(fig_bar_amt)

# Transaction Count Across States - Bar Plot
def plot2_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig__bar_count = px.bar(df,x='State',y='Count',color='Quarter',title=f'Transaction Count Across States - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450, 
                    width=450)
    st.plotly_chart(fig__bar_count)

# Transaction Amount Across States - Geo Plot
def plot3_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_amt = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State',
        featureidkey='properties.ST_NM',
        color='Amount', 
        color_continuous_scale='Bupu',
        range_color=(df['Amount'].min(),df['Amount'].max()),
        title=f"Transaction Amount Across States- {Year}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_amt.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_amt)

# Transaction Amount Across States - Geo Plot
def plot4_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_count = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State', 
        featureidkey='properties.ST_NM', 
        color='Count', 
        color_continuous_scale='Bupu',  
        range_color=(df['Count'].min(),df['Count'].max()),
        title=f"Transaction Count Across States - {Year}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_count.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_count)

# Transaction Amount Across States - Bar Plot (Horizontal)
def plot5_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    df = df.sort_values('State',ascending=False)

    fig_bar_amt = px.bar(df,x='Amount',y='State',color='Quarter',
                         title=f'Transaction Amount Across States (Horizontal) - {Year}',
                         color_discrete_sequence=px.colors.sequential.Viridis,
                         height=500, width=900)   
    st.plotly_chart(fig_bar_amt)

# Transaction Amount Count States - Bar Plot (Horizontal)
def plot6_yr(df,Year):
    df=df[df['Year']==Year]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    df = df.sort_values('State',ascending=False)

    fig__bar_count = px.bar(df,x='Count',y='State',color='Quarter',
                            title=f'Transaction Count Across States (Horizontal) - {Year}',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            height=500, width=900)
    st.plotly_chart(fig__bar_count)

# Quarter-wise Distribution of Transaction Amount by State - Donut Chart
def plot7_yr(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut1=px.pie(df,
                    names='Quarter',
                    values='Amount',
                    title=f'{'State'}: Quarter-wise Distribution of Transaction Amount - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,  # Optional: creates a donut chart
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut1)

# Quarter-wise Distribution of Transaction Count by State - Donut Chart
def plot8_yr(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df = df.groupby(['State','Quarter'])[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut2=px.pie(df,
                    names='Quarter',
                    values='Count',
                    title=f'{'State'}: Quarter-wise Distribution of Transaction Count - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,  # Optional: creates a donut chart
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut2)

# Transaction Amount, Transaction Count Distribution Across States - Bubble Chart
def plot9_yr(df,Year):   
    df = df[df['Year']==Year]
    df.reset_index(inplace=True)

    fig_line = px.line(df,x='State',y=['Amount','Count'],hover_data=['Quarter'],
                        title=f'Transaction Amount, Transaction Count Distribution Across States - {Year}',
                        color_discrete_sequence=["#AA0DFE","rgb(136,204,238)"], 
                        height=550,
                        width=900, markers=True  
    )
    st.plotly_chart(fig_line)

    fig_bubble = px.scatter(df,
                             x='State',
                             y='Amount',
                             size='Amount',
                             color='Count',
                             hover_data=['Quarter'],
                             color_continuous_scale='Bupu',
                             title=f'Statewise Transaction Amount, Transaction Count Distribution - {Year}',
                             height=650,
                             width=900       
    )
    st.plotly_chart(fig_bubble)

# Transction Amount Across Districts - Grouped Bar Chart
def plot10_yr(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_area1 = px.bar(
    df,
    x='Quarter',
    y='Amount',
    hover_data='District',
    title=f"{State}: Transction Amount Across Districts - {Year}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_area1)

# Transction Count Across Districts - Grouped Bar Chart
def plot11_yr(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_area1 = px.bar(
    df,
    x='Quarter',
    y='Count',
    hover_data='District',
    title=f"{State}: Transction Count Across Districts - {Year}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_area1)

# Transction Amount Distribution Across Pincode - Pie Chart
def plot12_yr(df,Year,State):    
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_pie1=px.pie(df,
                    names='Pincode',
                    values='Amount',
                    title=f'{State}: Transction Amount Distribution Across Pincode  - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_pie1)

# Transction Count Distribution Across Pincode - Pie Chart
def plot13_yr(df,Year,State):    
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_pie2=px.pie(df,
                    names='Pincode',
                    values='Count',
                    title=f'{State}: Transction Count Distribution Across Pincode  - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_pie2)

# User Plots
# Transaction Count Contribution Across Brands - Line Plot
def plot_user1(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_line = px.line(df,x='Brand',y='Count',
                title=f'Transaction Count Contribution Across Brands- {Year} Q{Quarter}',
                color_discrete_sequence=px.colors.sequential.Viridis,height=450,width=450)
    st.plotly_chart(fig_line)

# Transaction Percentage Contribution Across Brands - Line Plot
def plot_user2(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_line = px.line(df,x='Brand',y='Percentage',
                title=f'Transaction Percentage Contribution Across Brands - {Year} Q{Quarter}',
                color_discrete_sequence=px.colors.sequential.Viridis,height=450,width=450)
    st.plotly_chart(fig_line)

# Registered Users, App Opens Across Districts - Bubble Chart
def plot_user3(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_bubble = px.scatter(df,
                                x='District',
                                y='RegisteredUsers',
                                size='RegisteredUsers',
                                color='AppOpens',
                                color_continuous_scale='Bupu',
                                title=f'{"State"}: Registered Users, App Opens Across Districts - {Year} Q{Quarter}',
                                height=550,
                                width=900       
    )
    st.plotly_chart(fig_bubble)

# Registered Users Across Pincode
def plot_user4(df,Year,Quarter,State):
    df = df[df['Year']==Year]
    df = df[df['Quarter']==Quarter]
    df = df[df['State']==State]
    df.reset_index(inplace=True)

    fig_donut=px.pie(df,
                    names='Pincode',
                    values='RegisteredUsers',
                    title=f'{"State"}: Registered Users Across Pincode - {Year} Q{Quarter}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,  # Optional: creates a donut chart
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut)

# Overall Charts
# Total Transaction Amount Distribution Across Transaction Types - Donut Chart
def plot_overall1(df,Year):
    df = df[df['Year']==Year]
    df = df.groupby('Type')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut1=px.pie(df,
                    names='Type',
                    values='Count',
                    title=f'Total Transaction Amount Distribution Across Transaction Types - {Year}',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,  # Optional: creates a donut chart
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut1)

# Total Transaction Count Distribution Across Transaction Types - Donut Chart
def plot_overall2(df,Year):
    df = df[df['Year']==Year]
    df = df.groupby('Type')[['Amount','Count']].sum()
    df.reset_index(inplace=True)

    fig_donut2=px.pie(df,
                    names='Type',
                    values='Count',
                    title=f'Total Transaction Count Distribution Across Transaction Types - {Year} ',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                    hole=0.5,
                    height=450, 
                    width=450)
    st.plotly_chart(fig_donut2)

# Total Transction Amount Across Districts - Bar Chart
def plot_overall3(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_bar1 = px.bar(
    df,
    x='District',
    y='Amount',
    title=f"{State}: Total Transction Amount Across Districts - {Year}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_bar1)

# Total Transction Count Across Districts - Bar Chart
def plot_overall4(df,Year,State):
    df = df[df['Year']==Year]
    df = df[df['State']==State]
    df['District'] = df['District'].str.title()
    df = df.sort_values('District')
    df.reset_index(inplace=True)

    fig_bar1 = px.bar(
    df,
    x='District',
    y='Count',
    title=f"{State}: Total Transction Count Across Districts - {Year}", 
    color_discrete_sequence=px.colors.sequential.Viridis,
    height=450, 
    width=450  
    )
    st.plotly_chart(fig_bar1)

# Total Transaction Amount Across States - Geo Plot
def plot_overall5(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_amt = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State',
        featureidkey='properties.ST_NM', 
        color='Amount',
        color_continuous_scale='Bupu',
        range_color=(df['Amount'].min(),df['Amount'].max()),
        #hover_name='State',
        title=f"Total Transaction Amount Across States- {Year} Q{Quarter}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_amt.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_amt)

# Total Transaction Count Across States - Geo Plot
def plot_overall6(df,Year,Quarter):
    df=df[df['Year']==Year]
    df=df[df['Quarter']==Quarter]
    df = df.groupby('State')[['Amount','Count']].sum()
    df.reset_index(inplace=True)
    
    url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    states_geojson = requests.get(url).json()
    fig_map_count = px.choropleth(
        df,
        geojson=states_geojson,
        locations='State', 
        featureidkey='properties.ST_NM', 
        color='Count', 
        color_continuous_scale='Bupu',  
        range_color=(df['Count'].min(),df['Count'].max()),
        #hover_name='State',
        title=f"Total Transaction Count Across States - {Year} Q{Quarter}",
        fitbounds="locations",
        height=450,
        width=450
    )
    fig_map_count.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_map_count)

# Query Charts
def query_chart1(df,Column_Name1,Column_Name2,Year,Quarter): # Bar Plot (Horizontal)
    fig__amt_count = px.bar(df,x=Column_Name2,y=Column_Name1,
                            title=f'Total Transaction Amount Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,height=350, width=450)
    st.plotly_chart(fig__amt_count)

def query_chart2(df,Column_Name1,Column_Name2,Year,Quarter): # Bar Plot (Horizontal)
    fig__bar_count = px.bar(df,x=Column_Name2,y=Column_Name1,
                            title=f'Total Transaction Count Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,height=350, width=450,
                            orientation='h')
    st.plotly_chart(fig__bar_count)

def query_chart3(df,Column_Name1,Column_Name2,Year,Quarter): # Donut Chart
    fig_pie_amt_count = px.pie(df,names=Column_Name1,values=Column_Name2,
                            title=f'Total Transaction Amount Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,hole=0.5,
                            height=400, width=450)
    st.plotly_chart(fig_pie_amt_count)

def query_chart4(df,Column_Name1,Column_Name2,Year,Quarter): # Donut Chart
    fig_pie_amt_count = px.pie(df,names=Column_Name1,values=Column_Name2,
                            title=f'Total Transaction Count Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,hole=0.5,
                            height=400, width=450)
    st.plotly_chart(fig_pie_amt_count)

def query_chart5(df,Column_Name1,Column_Name2,Year,Quarter,Title): # Line Chart
    fig_line = px.line(df,x=Column_Name1,y=Column_Name2,
                            title=f'{Title} Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            height=400, width=450,markers=True)
    st.plotly_chart(fig_line)

def query_chart6(df,Column_Name1,Column_Name2,Year,Quarter,title): # Bar Plot (Horizontal)
    fig__amt_count = px.bar(df,x=Column_Name1,y=Column_Name2,
                            title=f'{title} Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,height=350, width=450)
    st.plotly_chart(fig__amt_count)

def query_chart7(df,Column_Name1,Column_Name2,Year,Quarter,title): # Pie Chart
    fig_pie = px.pie(df,names=Column_Name1,values=Column_Name2,
                            title=f'{title} Across {Column_Name1}s - {Year} Q{Quarter}',
                            color_discrete_sequence=px.colors.sequential.Viridis,
                            height=400, width=450)
    st.plotly_chart(fig_pie)

# Query Outputs
def query_output(df1,df2,Column_Name1,Column_Name2,Column_Name3,Year,Quarter):
    if Column_Name1 == 'State':
        AlterState(df1)
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df1,column_config={Column_Name2:'Total Transaction Amount'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df1 = df1.sort_values(by=Column_Name2, ascending=True)
            query_chart1(df1,Column_Name1,Column_Name2,Year,Quarter)
        
        AlterState(df2)
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df2,column_config={Column_Name3:'Total Transaction Count'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df2 = df2.sort_values(by=Column_Name3, ascending=True)
            query_chart2(df2,Column_Name1,Column_Name3,Year,Quarter)

    elif Column_Name1 == 'District':
        df1[Column_Name1] = df1[Column_Name1].str.title()
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df1,column_config={Column_Name2:'Total Transaction Amount'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df1 = df1.sort_values(by=Column_Name2, ascending=True)
            query_chart1(df1,Column_Name1,Column_Name2,Year,Quarter)

        df2[Column_Name1] = df2[Column_Name1].str.title()
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df2,column_config={Column_Name3:'Total Transaction Count'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df2 = df2.sort_values(by=Column_Name3, ascending=True)
            query_chart2(df2,Column_Name1,Column_Name3,Year,Quarter)

    elif Column_Name1 == 'Pincode':
        df1[Column_Name1] = df1[Column_Name1].astype(str)
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df1,column_config={Column_Name2:'Total Transaction Amount'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df1 = df1.sort_values(by=Column_Name2, ascending=True)
            query_chart3(df1,Column_Name1,Column_Name2,Year,Quarter)
        
        df2[Column_Name1] = df2[Column_Name1].astype(str)
        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(df2,column_config={Column_Name3:'Total Transaction Count'},
                        hide_index=True,height=350,width=450)
        with col2: 
            df2 = df2.sort_values(by=Column_Name3, ascending=True)
            query_chart4(df2,Column_Name1,Column_Name3,Year,Quarter)

    elif Column_Name1 == 'Type': 
        df1[Column_Name1] = df1[Column_Name1].str.title()
        col1, col2 = st.columns(2)    
        with col1:
            df1 = df1.sort_values(by=Column_Name2, ascending=True)
            query_chart1(df1,Column_Name1,Column_Name2,Year,Quarter) 
            
        with col2:  
            df2 = df2.sort_values(by=Column_Name3, ascending=True)
            query_chart2(df2,Column_Name1,Column_Name3,Year,Quarter) 
        
        df2[Column_Name1] = df2[Column_Name1].str.title()
        col1, col2 = st.columns(2)    
        with col1:
            df1 = df1.sort_values(by=Column_Name2, ascending=False)
            st.dataframe(df1,column_config={Column_Name2:'Total Transaction Amount'},
                        hide_index=True,width=450)
        with col2:
            df2 = df2.sort_values(by=Column_Name3, ascending=False)
            st.dataframe(df2,column_config={Column_Name3:'Total Transaction Count'},
                        hide_index=True,width=450)


def query_function1(Column_Name,table_name1,table_name2,Year,Quarter):
    query1 = f'''SELECT {Column_Name}, SUM(Transaction_Amount) AS Total_Transaction_Amount
                FROM (
                SELECT {Column_Name}, SUM(Amount) AS Transaction_Amount FROM {table_name1} 
                where Year='{Year}' and Quarter='{Quarter}' GROUP BY {Column_Name}
                UNION ALL
                SELECT {Column_Name}, SUM(Amount) AS Transaction_Amount FROM {table_name2} 
                where Year='{Year}' and Quarter='{Quarter}' GROUP BY {Column_Name}
                ) AS Comined_Transactions
                GROUP BY {Column_Name} ORDER BY Total_Transaction_Amount desc limit 10;'''
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    query_df1 = pd.DataFrame(result1,columns=[Column_Name,'Total_Transaction_Amount'])

    query2 = f'''SELECT {Column_Name}, SUM(Transaction_Count) AS Total_Transaction_Count
                FROM (
                SELECT {Column_Name}, SUM(Count) AS Transaction_Count FROM {table_name1} 
                where Year='{Year}' and Quarter='{Quarter}' GROUP BY {Column_Name}
                UNION ALL
                SELECT {Column_Name}, SUM(Count) AS Transaction_Count FROM {table_name2} 
                where Year='{Year}' and Quarter='{Quarter}' GROUP BY {Column_Name}
                ) AS Comined_Transactions
                GROUP BY {Column_Name} ORDER BY Total_Transaction_Count desc limit 10;'''
    mycursor.execute(query2)
    result2=mycursor.fetchall()
    query_df2 = pd.DataFrame(result2,columns=[Column_Name,'Total_Transaction_Count'])
    query_output(query_df1,query_df2,Column_Name,'Total_Transaction_Amount','Total_Transaction_Count',Year,Quarter)

def query_function2(Column_Name,Table_Name,Year,Quarter):
    query1 = f'''select {Column_Name}, SUM(Amount) as Transaction_Amount from {Table_Name}
                where Year={Year} and Quarter={Quarter} group by {Column_Name} 
                order by Transaction_Amount desc limit 10;'''
    mycursor.execute(query1)
    result1=mycursor.fetchall()
    query_df1 = pd.DataFrame(result1,columns=[Column_Name,'Transaction_Amount'])
    
    query2 = f'''select {Column_Name}, SUM(Count) as Transaction_Count from {Table_Name} 
                where Year={Year} and Quarter={Quarter} group by {Column_Name} 
                order by Transaction_Count desc limit 10;'''
    mycursor.execute(query2)
    result2=mycursor.fetchall()
    query_df2 = pd.DataFrame(result2,columns=[Column_Name,'Transaction_Count'])
    query_output(query_df1,query_df2,Column_Name,'Transaction_Amount','Transaction_Count',Year,Quarter)

def query_function3(Column_Name1,Column_Name2,Column_Name3,Table_Name,Year,Quarter):
    query1 = f'''select {Column_Name1}, SUM({Column_Name2}) as Transaction_{Column_Name2} from {Table_Name} 
                where Year={Year} and Quarter={Quarter} group by {Column_Name1} 
                order by Transaction_{Column_Name2} desc limit 10'''
    mycursor.execute(query1)
    result1=mycursor.fetchall()


    query2 = f'''select {Column_Name1}, SUM({Column_Name3}) as Transaction_{Column_Name3} from {Table_Name} 
                where Year={Year} and Quarter={Quarter} group by {Column_Name1} 
                order by Transaction_{Column_Name3} desc limit 10'''
    mycursor.execute(query2)
    result2=mycursor.fetchall()

    if Column_Name1=='Brand':         
        query_df1 = pd.DataFrame(result1, columns=[Column_Name1, f'Transaction_{Column_Name2}'])
        query_df1[Column_Name1] = query_df1[Column_Name1].str.title() 

        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(query_df1,column_config={f'Transaction_{Column_Name2}':f'Total Transaction {Column_Name2}'},
                        hide_index=True,height=350,width=450)
        with col2: 
            query_df1 = query_df1.sort_values(by=f'Transaction_{Column_Name2}', ascending=True)
            query_chart5(query_df1,Column_Name1,f'Transaction_{Column_Name2}',Year,Quarter,
                        f'Total Transaction {Column_Name2}') 

        query_df2 = pd.DataFrame(result2, columns=[Column_Name1, f'Transaction_{Column_Name3}'])
        query_df2[Column_Name1] = query_df2[Column_Name1].str.title()

        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(query_df2,column_config={f'Transaction_{Column_Name3}':f'Total Transaction {Column_Name3}'},
                        hide_index=True,height=350,width=450)
        with col2: 
            query_df2 = query_df2.sort_values(by=f'Transaction_{Column_Name3}', ascending=True)
            query_chart5(query_df2,Column_Name1,f'Transaction_{Column_Name3}',Year,Quarter,
                        f'Total Transaction {Column_Name3}') 
    
    elif Column_Name1=='District':
        query_df2 = pd.DataFrame(result2, columns=[Column_Name1,Column_Name3])
        query_df2[Column_Name1] = query_df2[Column_Name1].str.title()

        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(query_df2,column_config={Column_Name3:'App Opens'},
                        hide_index=True,height=350,width=450)
        with col2: 
            query_df2 = query_df2.sort_values(by=Column_Name3, ascending=True)
            query_chart6(query_df2,Column_Name1,Column_Name3,Year,Quarter,
                        'App Opens') 
            
        query_df1 = pd.DataFrame(result1, columns=[Column_Name1, Column_Name2])
        query_df1[Column_Name1] = query_df1[Column_Name1].str.title() 

        col1, col2 = st.columns(2)    
        with col1:
            st.dataframe(query_df1,column_config={Column_Name2:'Registered Users'},
                        hide_index=True,height=350,width=450)
        with col2: 
            query_df1 = query_df1.sort_values(by=Column_Name2, ascending=True)
            query_chart6(query_df1,Column_Name1,Column_Name2,Year,Quarter,
                        'Registered Users') 

def query_function4(Column_Name1,Column_Name2,Table_Name,Year,Quarter):

    query4 = f'''select {Column_Name1}, SUM({Column_Name2}) as Transaction_{Column_Name2} from {Table_Name} 
                where Year={Year} and Quarter={Quarter} group by {Column_Name1} 
                order by Transaction_{Column_Name2} desc limit 10'''
    mycursor.execute(query4)
    result4=mycursor.fetchall()

    query_df4 = pd.DataFrame(result4, columns=[Column_Name1, Column_Name2])
    query_df4[Column_Name1] = query_df4[Column_Name1].astype(str)
    
    col1, col2 = st.columns(2)    
    with col1:
        st.dataframe(query_df4,column_config={Column_Name2:'Registered Users'},
                    hide_index=True,height=350,width=450)
    with col2: 
        query_df4 = query_df4.sort_values(by=Column_Name2, ascending=True)
        query_chart7(query_df4,Column_Name1,Column_Name2,Year,Quarter,
                    'Registered Users')   

# Streamlit Part
st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
with col1:
    st.image("D:\Guvi\Projects\Phonepe Pulse Data Visualization and Exploration\Images\Logo.jpeg", 
             width=450)
with col2:
    st.header("Data Visualization and Exploration")

# Sidebar
with st.sidebar:
    selected_tab = option_menu("Main Menu", ["Home", 'Data Exploration', 'Top Details'], 
        icons=['house', 'clipboard2-data', 'graph-up-arrow'], menu_icon="menu-button-wide-fill", default_index=0)

# Main Content based on Selected Tab
if selected_tab == "Home":  
    st.write("""
    ### Welcome to the :violet[PhonePe Pulse] Data Dashboard!
    This interactive platform allows you to explore transaction trends across India using data from PhonePe Pulse. 
    Visualize geographic insights, track transaction volumes, and analyze trends over time with dynamic plots and maps.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("D:\Guvi\Projects\Phonepe Pulse Data Visualization and Exploration\Images\Image_1.jpeg", 
             width=450)
    with col2:        
        st.markdown("### :violet[Key Features]")
        st.write("""
        - **Interactive Visualizations:** Explore transaction data at the state and district level using dynamic charts.
        - **Customizable Dashboards:** Apply filters to view transaction data by location, transaction type, payment modes, and more.
        - **Data Retrieval:** Data is fetched from the PhonePe Pulse database to ensure the insights.
        - **User-Friendly Interface:** Built with Streamlit, the tool offers an intuitive layout for seamless navigation and exploration.
        """)

    st.markdown("### :violet[Navigate and Usage]")
    st.write("""
    1. **Use the Sidebar Menu**: Select tabs to switch between different data views (Home, Data Exploration, Top Details).
    2. **Filter Options**: Customize your view by selecting specific states, transaction types, and time periods.
    3. **Visualize Data**: Explore trends with interactive graphs and charts""")       

elif selected_tab == "Data Exploration":  
    # Create sub tabs for Data Exploration
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["Transaction", "Insurance", "User", "Overall"])

    # Subtab 1: Transaction
    with subtab1:
        st.write("### Transaction Insights")   
        category_trans = st.radio(":violet[***Select the Category***]",
                                                   ["Aggregated Analysis", "Map Analysis", "Top Analysis"],
                                                   horizontal=True)
        
        if category_trans == "Aggregated Analysis":       
            df=Agg_Trans_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df)) 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df))       
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot1(df,int(YearSelection),int(QuarterSelection))
            with cols2:
                plot2(df,int(YearSelection),int(QuarterSelection))
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot7(df,int(YearSelection),int(QuarterSelection))
            with cols2:
                plot8(df,int(YearSelection),int(QuarterSelection))

            cols1, cols2 = st.columns(2)
            with cols1:
                Type_Selection = st.selectbox(":violet[***Select the Type***]",TypeOptions(df))
            plot9(df,int(YearSelection),int(QuarterSelection),Type_Selection)
        
        elif category_trans == "Map Analysis":       
            df=Map_Trans_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df)) 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df))       
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot3(df,int(YearSelection),int(QuarterSelection))
            with cols2:
                plot4(df,int(YearSelection),int(QuarterSelection))
            
            cols1, cols2 = st.columns(2)
            with cols1:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df))

            cols1, cols2 = st.columns(2)
            with cols1:
                plot10(df,int(YearSelection),int(QuarterSelection),State_Selection)
            with cols2:
                plot11(df,int(YearSelection),int(QuarterSelection),State_Selection)

        elif category_trans == "Top Analysis":       
            df=Top_Trans_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df)) 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df))       
                       
            plot5(df,int(YearSelection),int(QuarterSelection))
            plot6(df,int(YearSelection),int(QuarterSelection))

            cols1, cols2 = st.columns(2)
            with cols1:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df))
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot12(df,int(YearSelection),int(QuarterSelection),State_Selection)
            with cols2:
                plot13(df,int(YearSelection),int(QuarterSelection),State_Selection)
       
    # Subtab 2: Insurance
    with subtab2:
        st.write("### Insurance Insights")
        category_ins = st.radio(":violet[***Select the Category***]",
                            ["Aggregated Analysis", "Map Analysis", "Top Analysis"],
                            horizontal=True, key = "<uniquevalueofsomesort>")

        if category_ins == "Aggregated Analysis":       
            df=Agg_Ins_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort1>")      
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot1_yr(df,int(YearSelection))
            with cols2:
                plot2_yr(df,int(YearSelection))

            cols1, cols2 = st.columns(2)
            with cols1:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort2>")

            cols1, cols2 = st.columns(2)
            with cols1:
                plot7_yr(df,int(YearSelection),State_Selection)
            with cols2:
                plot8_yr(df,int(YearSelection),State_Selection)

            plot9_yr(df,int(YearSelection))

        elif category_ins == "Map Analysis":       
            df=Map_Ins_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort3>")     

            cols1, cols2 = st.columns(2)
            with cols1:
                plot3_yr(df,int(YearSelection))
            with cols2:
                plot4_yr(df,int(YearSelection))

            cols1, cols2 = st.columns(2)
            with cols1:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort4>")

            cols1, cols2 = st.columns(2)
            with cols1:
                plot10_yr(df,int(YearSelection),State_Selection)
            with cols2:
                plot11_yr(df,int(YearSelection),State_Selection)

        elif category_ins == "Top Analysis":       
            df=Top_Ins_DF 

            col1, col2 = st.columns(2)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort5>")       

            plot5_yr(df,int(YearSelection))
            plot6_yr(df,int(YearSelection))

            cols1, cols2 = st.columns(2)
            with cols1:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort6>")

            cols1, cols2 = st.columns(2)
            with cols1:
                plot12_yr(df,int(YearSelection),State_Selection)
            with cols2:
                plot13_yr(df,int(YearSelection),State_Selection)

    # Subtab 3: User
    with subtab3:
        st.write("### User Insights")  
        category_user = st.radio(":violet[***Select the Category***]",
                                                   ["Aggregated Analysis", "Map Analysis", "Top Analysis"],
                                                   horizontal=True,key = "<uniquevalueofsomesort7>")
        
        if category_user == "Aggregated Analysis":       
            df=Agg_User_DF 

            col1, col2, col3 = st.columns(3)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort8>") 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df), 
                                                key = "<uniquevalueofsomesort9>")                  
            with col3:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort17>")
            
            cols1, cols2 = st.columns(2)
            with cols1:
                plot_user1(df,int(YearSelection),int(QuarterSelection),State_Selection)
            with cols2:
                plot_user2(df,int(YearSelection),int(QuarterSelection),State_Selection)  
        
        elif category_user == "Map Analysis":       
            df=Map_User_DF 

            col1, col2, col3 = st.columns(3)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort11>") 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df), 
                                                key = "<uniquevalueofsomesort12>") 
            with col3:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort18>")
            
            plot_user3(df,int(YearSelection),int(QuarterSelection),State_Selection) 
       
        elif category_user == "Top Analysis":       
            df=Top_User_DF 

            col1, col2, col3 = st.columns(3)
            with col1:
                YearSelection = st.selectbox(":violet[***Select the Year***]",YearOptions(df), 
                                             key = "<uniquevalueofsomesort14>") 
            with col2:
                QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",QuarterOptions(df), 
                                                key = "<uniquevalueofsomesort15>")       
            with col3:
                State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df), 
                                               key = "<uniquevalueofsomesort16>")
            
            plot_user4(df,int(YearSelection),int(QuarterSelection),State_Selection) 
                
    # Subtab 4: Overall
    with subtab4:
        st.write("### Overall Insights - (Total Transactions)")

        col1, col2, col3 = st.columns(3)
        with col1:
            YearSelection = st.slider(":violet[***Select the Year***]",min(unique_years),
                                      max(unique_years),
                                      min(unique_years),
                                      step=1,
                                      key = "<uniquevalueofsomesort21>")
                                                           
        cols1, cols2 = st.columns(2)
        with cols1:
            plot3_yr(df_agg,int(YearSelection))
        with cols2:
            plot4_yr(df_agg,int(YearSelection))

        cols1, cols2 = st.columns(2)
        with cols1:
            plot_overall1(df_agg,int(YearSelection))
        with cols2:
            plot_overall2(df_agg,int(YearSelection))

        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df_agg), 
                                           key = "<uniquevalueofsomesort22>")
        
        cols1, cols2 = st.columns(2)
        with cols1:
            plot_overall3(df_map,int(YearSelection),State_Selection)
        with cols2:
            plot_overall4(df_map,int(YearSelection),State_Selection)

        cols1, cols2 = st.columns(2)
        with cols1:
            plot12_yr(df_top,int(YearSelection),State_Selection)
        with cols2:
            plot13_yr(df_top,int(YearSelection),State_Selection)

        cols1, cols2, cols3 = st.columns(3)

        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            QuarterSelection = st.slider(":violet[***Select the Quarter***]",min(unique_quarters),
                                      max(unique_quarters),
                                      min(unique_quarters),
                                      step=1,
                                      key = "<uniquevalueofsomesort23>")
            
        cols1, cols2 = st.columns(2)
        with cols1:
            plot_overall5(df_agg,int(YearSelection),int(QuarterSelection))
        with cols2:
            plot_overall6(df_agg,int(YearSelection),int(QuarterSelection))

        cols1, cols2 = st.columns(2)
        with cols1:
            plot7(df_agg,int(YearSelection),int(QuarterSelection))
        with cols2:
            plot8(df_agg,int(YearSelection),int(QuarterSelection))

        cols1, cols2, cols3 = st.columns(3)
        with cols1:
            State_Selection = st.selectbox(":violet[***Select the State***]",StateOptions(df_agg), 
                                           key = "<uniquevalueofsomesort24>")
        
        cols1, cols2 = st.columns(2)
        with cols1:
            plot10(df_map,int(YearSelection),int(QuarterSelection),State_Selection)
        with cols2:
            plot11(df_map,int(YearSelection),int(QuarterSelection),State_Selection)

        cols1, cols2 = st.columns(2)
        with cols1:
            plot12(df_top,int(YearSelection),int(QuarterSelection),State_Selection)
        with cols2:
            plot13(df_top,int(YearSelection),int(QuarterSelection),State_Selection)
             
elif selected_tab == "Top Details":
    st.write("### Top Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        YearSelection = st.selectbox(":violet[***Select the Year***]",unique_years,key = "<uniquevalueofsomesort31>")
    with col2:
        QuarterSelection = st.selectbox(":violet[***Select the Quarter***]",unique_quarters,key = "<uniquevalueofsomesort32>")

    Dropdown = st.selectbox(
    ':violet[***SQL Query Output***]',
    ('1. Top 10 States with the Highest Total Transaction Amount, Transaction Count', # agg_trans, agg_ins
     
     '2. Top 10 States with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions', # agg_trans
     '3. Top 10 States with the Highest Transaction Amount, Transaction Count from Insurance Transactions', # agg_ins

     '4. Top 10 Districts with the Highest Total Transaction Amount, Transaction Count', # map_trans, map_ins
     '5. Top 10 Pincodes with the Highest Total Transaction Amount, Transaction Count', # top_trans, top_ins
     '6. Top Transaction Types with the Highest Total Transaction Amount, Transaction Count', # agg_trans, agg_ins  
     
     '7. Top 10 Districts with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions', # map_trans
     '8. Top 10 Pincodes with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions', # top_trans
     '9. Top Types with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions', # agg_trans
     '10. Top 10 Districts with the Highest Transaction Amount, Transaction Count from Insurance Transactions', # map_ins
     '11. Top 10 Pincodes with the Highest Transaction Amount, Transaction Count from Insurance Transactions', # top_ins

     '12. Top 10 Brands with the Highest Transaction Count,Transaction Percentage', # agg_user
     '13. Top 10 Districts with the Highest Number of App Opens, Number of Registered Users', # map_user

     '14. Top 10 Pincodes with the Highest Number of Registered Users')) # top_user
    

    if Dropdown=='1. Top 10 States with the Highest Total Transaction Amount, Transaction Count':
        query_function1('State','agg_ins','agg_trans',int(YearSelection),int(QuarterSelection)) 

    elif Dropdown=='2. Top 10 States with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions':
        query_function2('State','agg_trans',int(YearSelection),int(QuarterSelection))    
    elif Dropdown=='3. Top 10 States with the Highest Transaction Amount, Transaction Count from Insurance Transactions':
        query_function2('State','agg_ins',int(YearSelection),int(QuarterSelection))


    elif Dropdown=='4. Top 10 Districts with the Highest Total Transaction Amount, Transaction Count':
        query_function1('District','map_ins','map_trans',int(YearSelection),int(QuarterSelection))   
    elif Dropdown=='5. Top 10 Pincodes with the Highest Total Transaction Amount, Transaction Count':
        query_function1('Pincode','top_ins','top_trans',int(YearSelection),int(QuarterSelection))
    elif Dropdown=='6. Top Transaction Types with the Highest Total Transaction Amount, Transaction Count':
        query_function1('Type','agg_ins','agg_trans',int(YearSelection),int(QuarterSelection))

    elif Dropdown=='7. Top 10 Districts with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions':
        query_function2('District','map_trans',int(YearSelection),int(QuarterSelection))   
    elif Dropdown=='8. Top 10 Pincodes with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions':
        query_function2('Pincode','top_trans',int(YearSelection),int(QuarterSelection))
    elif Dropdown=='9. Top Types with the Highest Transaction Amount, Transaction Count from Non-Insurance Transactions':
        query_function2('Type','agg_trans',int(YearSelection),int(QuarterSelection))

    elif Dropdown=='10. Top 10 Districts with the Highest Transaction Amount, Transaction Count from Insurance Transactions':
        query_function2('District','map_ins',int(YearSelection),int(QuarterSelection))   
    elif Dropdown=='11. Top 10 Pincodes with the Highest Transaction Amount, Transaction Count from Insurance Transactions':
        query_function2('Pincode','top_ins',int(YearSelection),int(QuarterSelection))

    elif Dropdown=='12. Top 10 Brands with the Highest Transaction Count,Transaction Percentage':
        query_function3('Brand','Count', 'Percentage', 'agg_user', int(YearSelection), int(QuarterSelection))
    elif Dropdown=='13. Top 10 Districts with the Highest Number of App Opens, Number of Registered Users':
        query_function3('District','RegisteredUsers', 'AppOpens', 'map_user', int(YearSelection), int(QuarterSelection))

    elif Dropdown=='14. Top 10 Pincodes with the Highest Number of Registered Users':
        query_function4('Pincode','RegisteredUsers', 'top_user', int(YearSelection), int(QuarterSelection))
      
# Footer Section
st.markdown("---")
st.write("© 2024 :violet[PhonePe Pulse] | All rights reserved.")