import streamlit as st
import plotly.express as px
import univarinat_function
import function 
import pandas as pd

st.set_page_config(page_title = 'EDA_analysis',
                   layout = 'wide',
                   initial_sidebar_state='collapsed')
st.header('EDA Analysis')


df = function.alldata()
address_df = function.geospatial_data()
merged_df = pd.merge(df,address_df,on = '_id', how = 'inner')
country_list = function.country(address_df)
avail_list = univarinat_function.avail_list()


st.subheader('Overall listed Property type')
with st.container(border=True):
    fig0 = univarinat_function.property_overall(df)
    st.plotly_chart(fig0)

st.subheader('Overall listed Property type in market wise')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 0)
    market_list = function.market(selected_country,address_df)
    selected_market = st.selectbox('Choose market',market_list,key = 1)
    fig1 = univarinat_function.property_countrywise(df,address_df,selected_country,selected_market)
    st.plotly_chart(fig1)

st.subheader('Overall listed Property type in suburb wise')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 2)
    market_list = function.market(selected_country,address_df)
    selected_market = st.selectbox('Choose market',market_list,key = 3)
    suburb_list = function.suburb(selected_country,selected_market,address_df)
    selected_suburb = st.selectbox('Choose suburb', suburb_list,key = 4)
    fig2 = univarinat_function.propert_suburb(df,address_df,selected_country,selected_market,selected_suburb)
    st.plotly_chart(fig2)

st.subheader('Property type price variation in country wise')
with st.container(border=True):
    fig3 = univarinat_function.price_per_location(merged_df)
    st.plotly_chart(fig3)
    
st.subheader('Property type price variation in United States market wise')
with st.container(border=True):
    fig4 = univarinat_function.price_property_location(merged_df)
    st.plotly_chart(fig4)

st.subheader('Heat map of occupancy rate')
with st.container(border=True):
    fig5 = univarinat_function.availability_heatmap(merged_df)
    st.plotly_chart(fig5)

st.subheader('occupancy rate relation with property type')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 9)
    selected_avail = st.selectbox('Choose Country',avail_list,key = 10)
    fig6 = univarinat_function.property_occupancy(merged_df,selected_country,selected_avail)
    st.plotly_chart(fig6)


st.subheader('occupancy rate relation with number of bedrooms')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 11)
    selected_avail = st.selectbox('Choose Country',avail_list,key = 12)
    fig7 = univarinat_function.occupancy_relation_bedroom(merged_df,selected_country,selected_avail)
    st.plotly_chart(fig7)

st.subheader('occupancy rate relation with number of beds')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 13)
    selected_avail = st.selectbox('Choose Country',avail_list,key = 14)
    fig8 = univarinat_function.occupancy_relation_bed(merged_df,selected_country,selected_avail)
    st.plotly_chart(fig8)

st.subheader('occupancy rate relation with accommodation')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 15)
    selected_avail = st.selectbox('Choose Country',avail_list,key = 16)
    fig9 = univarinat_function.occupancy_relation_accommodation(merged_df,selected_country,selected_avail)
    st.plotly_chart(fig9)
    
st.subheader('occupancy rate relation with rating')
with st.container(border=True):
    selected_country = st.selectbox('Choose Country',country_list,key = 17)
    selected_avail = st.selectbox('Choose Country',avail_list,key = 18)
    fig10 = univarinat_function.occupancy_relation_rating(merged_df,selected_country,selected_avail)
    st.plotly_chart(fig10)
    