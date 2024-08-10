import plotly.express as px
import pandas as pd
import streamlit as st 

def avail_list():
    avail_list = ['availability_30','availability_60','availability_90','availability_365']
    return avail_list

def property_overall(df):
    total_property = df['property_type'].value_counts().to_frame().reset_index()
    per_sum = total_property['count'].sum()
    for i in range(total_property.shape[0]):
        total_property.loc[i,'percentage'] = round((total_property.loc[i,'count']/per_sum)*100,2)
    
    color_sequence = px.colors.qualitative.Plotly
    fig = px.bar(data_frame = total_property,
                x = 'property_type',
                y = 'percentage',
                hover_data = 'count',
                text = 'percentage',
                color_discrete_sequence=color_sequence
                )
    return fig

def property_countrywise(df,add_df,country,market):

    result = add_df[(add_df['country']==country)&
                        (add_df['market']==market)]
    merged_df = pd.merge(df,result, on = '_id', how = 'inner')
    total_property_market = merged_df['property_type'].value_counts().to_frame().reset_index()
    per_sum = total_property_market['count'].sum()
    for i in range(total_property_market.shape[0]):
        total_property_market.loc[i,'percentage'] = round((total_property_market.loc[i,'count']/per_sum)*100,2)

    color_sequence = px.colors.qualitative.Plotly
    fig = px.bar(data_frame = total_property_market,
                x = 'property_type',
                y = 'percentage',
                hover_data = 'count',
                text = 'percentage',
                color_discrete_sequence=color_sequence
                )
    return fig

def propert_suburb(df,add_df,country,market,suburb):
    result = add_df[(add_df['country']==country)&
                        (add_df['market']==market)&
                        (add_df['suburb']==suburb)]
    merged_df = pd.merge(df,result, on = '_id', how = 'inner')
    property = merged_df['property_type'].value_counts().to_frame().reset_index()

    fig = px.pie(
        data_frame = property,
        names = 'property_type',
        values = 'count',
        color_discrete_sequence = ['orange', 'blue', 'green','yellow','purple'],
        title = f'Category Of Property in {suburb}',
        hover_name = 'property_type',
        hover_data = 'count'
        ) 
    return fig

def price_per_location(merged_df):

    bedrooms = list(merged_df['bedrooms'].unique())
    bedrooms = list(map(lambda x:int(x),bedrooms))
    bedrooms_selected = st.selectbox('select no.of bedrooms',bedrooms,key=6)

    beds = list(merged_df['beds'].unique())
    beds = list(map(lambda x:int(x),beds))
    beds_selected = st.selectbox('select no.of beds',beds, key=7)

    data = merged_df[
        (merged_df['bedrooms'] == bedrooms_selected)&
        (merged_df['beds'] == beds_selected)]
    fig = px.scatter(
        data_frame = data,
        x = 'price',
        y = 'country',
        color = 'market'
    )
    return fig

def price_property_location(merged_df):
    cmd = st.selectbox('Choose min/max/avg',['minimum','maximum','average'],key =8)
    property_selected = st.selectbox('choose property',list(merged_df[merged_df['country']=='United States']['property_type'].value_counts().keys()))
    if cmd == 'minimum':
        gh = merged_df[(merged_df['country'] == 'United States') & 
            (merged_df['bedrooms'] == 1)&
            (merged_df['beds'] == 1)].groupby(['market','property_type'])['price'].max().to_frame().reset_index()
    if cmd == 'maximum':
        gh = merged_df[(merged_df['country'] == 'United States') & 
            (merged_df['bedrooms'] == 1)&
            (merged_df['beds'] == 1)].groupby(['market','property_type'])['price'].min().to_frame().reset_index()
    if cmd == 'average':
        gh = merged_df[(merged_df['country'] == 'United States') & 
            (merged_df['bedrooms'] == 1)&
            (merged_df['beds'] == 1)].groupby(['market','property_type'])['price'].mean().to_frame().reset_index()
    
    fig = px.scatter(
        data_frame = gh[gh['property_type']==property_selected],
        x = 'market',
        y = 'price',
        color = 'property_type',
        title='property wise price in varies location')
    fig.update_layout(
        updatemenus = [
            dict(
                buttons = list([
                    dict(args = ['type', 'bar'],label = 'bar',method = 'restyle'),
                    dict(args = ['type', 'scatter'],label = 'scatter',method = 'restyle')]),
                    direction = 'down',
                    showactive = True
            )
        ]
    )
    return fig

#09/08/24
#heat map
def availability_heatmap(merged_df,country):
    heat_maps = merged_df[['availability_30','availability_60','availability_90','availability_365','country']]
    data = []
    for i in country:
        availability_30p =  (heat_maps[(heat_maps['country']==i) & (heat_maps['availability_30']==0)].shape[0])/(heat_maps[heat_maps['country']==i].shape[0])
        availability_60p =  (heat_maps[(heat_maps['country']==i) & (heat_maps['availability_60']==0)].shape[0])/(heat_maps[heat_maps['country']==i].shape[0])
        availability_90p =  (heat_maps[(heat_maps['country']==i) & (heat_maps['availability_90']==0)].shape[0])/(heat_maps[heat_maps['country']==i].shape[0])
        availability_365p = (heat_maps[(heat_maps['country']==i) & (heat_maps['availability_365']==0)].shape[0])/(heat_maps[heat_maps['country']==i].shape[0])
        data.append([availability_30p,availability_60p,availability_90p,availability_365p])
    heat_df = pd.DataFrame(data, columns=['No availability_30','No availability_60','No availability_90','No availability_365'])

    fig = px.imshow(
            heat_df.round(2),
            labels = dict(x='Occupancy rate',y='country',color='Occupancy rate'),
            x= ['day_30','day_60','day_90','day_365'],
            y = ['United States',
            'China',
            'Australia',
            'Portugal',
            'Brazil',
            'Canada',
            'Turkey',
            'Spain'],
            text_auto = True,
            width = 1000,
            height = 600,
            title = 'Heat map of occupancy rate')
    return fig

#propert wise occupancy
def property_occupancy(merged_df,country_name,avail): 
    property_in = list(merged_df[merged_df['country']==country_name]['property_type'].unique())
    initial_1 = []
    property = []
    total_val = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)].shape[0]
    for i in property_in:
        val = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)&(merged_df['property_type'] == i)].shape[0]  
        if val!=0:
            property.append(i)
            initial_1.append(round(val/total_val,3))
        else: 
            None
    df1 = pd.DataFrame({'property':property,'values':initial_1})
    df1 = df1.sort_values(by = 'values')
    fig = px.pie(data_frame = df1,
        names = 'property',
        values = 'values',
        color = 'property',
        title = f'Property wise occupancy rate in {country_name}',
        hole = 0.5)
    return fig

#bedroom wise occupancy 
def occupancy_relation_bedroom(merged_df,country_name,avail): 
    df_bed = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)]
    fig = px.histogram(data_frame=df_bed,
                    x = 'bedrooms',
                    title = 'occupancy rate bedroom wise')
    return fig

#occupanct bed wise
def occupancy_relation_bed(merged_df,country_name,avail):  
    df_bed = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)]
    fig = px.histogram(data_frame=df_bed,
                    x = 'beds',
                    title = 'occupancy rate bed wise')
    return fig

#accommodate wise occupancy
def occupancy_relation_accommodation(merged_df,country_name,avail):
    df_bed = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)]
    fig = px.histogram(data_frame=df_bed,
                    x = 'accommodates',
                    title = 'occupancy rate accommodates wise')
    return fig

#rating wise occupancy rate

def occupancy_relation_rating(merged_df,country_name,avail):
    df_bed = merged_df[(merged_df['country']==country_name)&(merged_df[avail] == 0)]
    fig = px.histogram(data_frame=df_bed,
                    x = 'overall_rating',
                    title = 'occupancy rate raitng wise')
    return fig