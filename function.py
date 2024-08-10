import pandas as pd
import folium
import streamlit as st

def alldata():
    path = 'airbnb_data.csv'
    data = pd.read_csv(path)
    df = pd.DataFrame(data)
    return df

def geospatial_data():
    address_data = pd.read_csv('address.csv')
    address_df = pd.DataFrame(address_data)
    return address_df


def country(address_df):
    result = list(address_df['country'].value_counts().keys())
    return result

def market(country_name,address_df):
    result = list(address_df[address_df['country']==country_name]['market'].value_counts().keys())
    return result

def suburb(selected_country,selected_market,address_df):
    result = list(address_df[(address_df['country']==selected_country) & (address_df['market'] == selected_market)]['suburb'].value_counts().keys())
    return result    

def map(country,market,suburb,address_df):
    location_mean = address_df.groupby(['country','market','suburb'])[['latitude','longitude']].mean().sort_values(by=['country'],ascending=False).reset_index()
    m = folium.Map(
        location = location_mean[(location_mean['country']== country)&
                                (location_mean['market']==market)&
                                (location_mean['suburb']==suburb)][['latitude','longitude']].values[0],
        zoom_start = 14
    )
    for idx, row in address_df[(address_df['country']==country)&
                            (address_df['market']==market)&
                            (address_df['suburb']==suburb)].iterrows():
        folium.Marker(
            location = [row['latitude'],row['longitude']],
            popup = row[['_id','latitude','longitude']]
            ).add_to(m)
    listing = address_df[(address_df['country']==country)&
                        (address_df['market']==market)&
                        (address_df['suburb']==suburb)]   
    
    return m, listing 

    
def property_listing(total_df,listing_df,sort,asc):
    merged_df = pd.merge(total_df,listing_df, on = '_id', how = 'inner')[0:10]
    merged_df_c = merged_df.sort_values(by = [sort],ascending = asc)
    for index in range(merged_df_c.shape[0]):
        with st.container(border=True):
            st.write(f'Property ID:{merged_df_c['_id'][index]}')
            st.write(f'Property Name:{merged_df_c['name'][index]}')
            st.write(f'Property type:{merged_df_c['property_type'][index]}')
            st.write(f'No.of bedrooms:{merged_df_c['bedrooms'][index]}')
            st.write(f'No.of beds:{merged_df_c['beds'][index]}')
            st.write(f'Accommodates:{merged_df_c['accommodates'][index]}')
            st.write(f'Price:{merged_df_c['price'][index]}')
            st.write(f'Overall Rating:{merged_df_c['overall_rating'][index]}')
            with st.popover('Show more'):
                showm= ['_id',                    
                'listing_url',            
                'name',                   
                'summary',                
                'space',                  
                'description',            
                'neighborhood_overview',  
                'notes',                  
                'transit',                
                'access',                 
                'interaction',            
                'house_rules',            
                'property_type',          
                'room_type',
                'bed_type',
                'minimum_nights',
                'maximum_nights',
                'cancellation_policy',
                'accommodates',
                'bedrooms',
                'beds',
                'bathrooms',
                'amenities',
                'price',
                'security_deposit',
                'cleaning_fee',
                'extra_people',
                'guests_included',
                'overall_rating',
                'availability_30',
                'availability_60',
                'availability_90',
                'availability_365']
                for i in showm:
                    st.write(f'**{i}** : {merged_df_c[i][index]}')
