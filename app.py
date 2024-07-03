import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters

df=pd.read_csv('cleaned_data.csv')

st.title(':gray-background[:rainbow[*Choose your dream car!*] :sunglasses:]')
st.write('Use this app to select a car based on your preferences.')
st.subheader(':orange[Choose the price and the model year]')

# a filter based on the price:
price_range = st.slider("What is your price range?", min_value=1, value=(1, 375000))
selected_price_range = list(range(price_range[0], price_range[1]+1))

# a filter based on the model year:
year_range = st.slider("What is the time frame?", min_value=1908, max_value=2019, value=(1908, 2019))
selected_year_range = list(range(year_range[0], year_range[1]+1))

selected_price=df[df.price.isin(selected_price_range)]
selected_year=selected_price[selected_price.model_year.isin(selected_year_range)]

# a scatterplot of vehicles from the selected price & time range 
st.write('Here are your options with a split by price and model year:')
fig = px.scatter(selected_year, x='model_year', y='price')
st.plotly_chart(fig)

st.subheader(':orange[Choose technical specifications of the car]')
#with st.sidebar:
    #st.write("Choose your parameters here:")
# creating an instance of the DynamicFilters class, passing the dataframe and the list of columns that will serve as filters
dynamic_filters = DynamicFilters(selected_year, filters=['transmission', 'is_4wd', 'fuel', 'cylinders'])
# displaying the filters in the app
dynamic_filters.display_filters()
# displaying the filtered dataframe
dynamic_filters.display_df()


#options = st.multiselect(
#    "What is the time frame?", options=(df[df['model_year']>=2010], df[df['model_year']<1950]))          

