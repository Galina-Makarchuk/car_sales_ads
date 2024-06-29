import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters

df=pd.read_csv('cleaned_data.csv')

st.header('Choose your car.')
st.subheader('Use this app to select a car based on your preferences')
st.title(':blue[Choose the price and model year]')

# creating a filter based on the price:
price_range = st.slider("What is your price range?", value=(1, 375000))
actual_range = list(range(price_range[0], price_range[1]+1))



# creating a filter based on the model year:
#options = st.multiselect(
#    "What is the time frame?", options=(df[df['model_year']>=2010], df[df['model_year']<1950]))          

st.write('Here are your options with a split by price and model year')
fig = px.scatter(df, x='model_year', y='price')
st.plotly_chart(fig)

st.title('Choose technical specifications of the car')
with st.sidebar:
    st.write("Apply filters in any order 👇")
dynamic_filters = DynamicFilters(df, filters=['transmission', 'is_4wd', 'fuel', 'cylinders'])
dynamic_filters.display_filters()
dynamic_filters.display_df()
