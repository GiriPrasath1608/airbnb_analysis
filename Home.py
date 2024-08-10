import streamlit as st
import function
from streamlit_folium import st_folium

st.set_page_config(page_title = 'Airbnb',
                   page_icon = '🏠',
                   layout='wide',
                   initial_sidebar_state = 'collapsed'
)
st.title('Airbnb Listing Data')
st.divider()

total_df = function.alldata()
address_df = function.geospatial_data()
country_list = function.country(address_df)

st.subheader('Filter - Choose a Location')
selected_country = st.selectbox('Choose Country',country_list)
market_list = function.market(selected_country,address_df)
selected_market = st.selectbox('Choose market',market_list)
suburb_list = function.suburb(selected_country,selected_market,address_df)
selected_suburb = st.selectbox('Choose suburb', suburb_list)

st.subheader('Sort')
sort_selected = st.selectbox('Choose sort by',['_id','name','property_type','bedrooms','beds','accommodates','price','overall_rating'])
asc_selected = st.selectbox('True/False',[True,False])


geospatia_map,listing_df = function.map(selected_country,selected_market,selected_suburb,address_df)

st.subheader('Map With Property Location')
with st.container(border = True):
    st.write('Map')
    st_folium(geospatia_map,height = 500,use_container_width=True,
                pixelated= False, render =True)

st.subheader(f'Top 10 listed property by {sort_selected} and Ascending is {asc_selected}')
function.property_listing(total_df,listing_df,sort_selected,asc_selected)



