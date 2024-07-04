import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters

df=pd.read_csv('cleaned_data.csv')

st.title(':gray-background[:rainbow[*Choose your dream car!*] :sunglasses:]')
st.write('Use this app to select a car based on your preferences.')
st.divider()
st.header(':orange[Choose a car by price and model year]')

# a filter based on the price
price_range = st.slider("What is your price range?", min_value=1, value=(1, 375000))
selected_price_range = list(range(price_range[0], price_range[1]+1))
selected_price=df[df.price.isin(selected_price_range)]

# a filter based on the model year
year_range = st.slider("What is the time frame?", min_value=1908, max_value=2019, value=(1908, 2019))
selected_year_range = list(range(year_range[0], year_range[1]+1))
selected_year=selected_price[selected_price.model_year.isin(selected_year_range)]

# a scatterplot of vehicles from the selected price & time range
st.write('These are the options with a split by price and model year:')
fig1 = px.scatter(selected_year, x='model_year', y='price', hover_data=[selected_year['model_year'], selected_year['price'], selected_year['model']])
st.plotly_chart(fig1)

# a table with vehicles from the selection
st.write('Here is the list of selected cars:')
st.dataframe(selected_year)

# a download button for the table
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df(selected_year)

st.download_button(
    label="Download the selection as CSV",
    data=csv,
    file_name="selected cars.csv",
    mime="text/csv",
)

st.subheader(':green[The distribution of the selected cars by type and condition:]')     
fig2 = px.histogram(selected_year, x='type', color='condition', hover_data=df.columns).update_xaxes(categoryorder='total descending')
st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.header(':orange[Choose a car by its technical specifications]')

# creating an instance of the DynamicFilters class, passing the dataframe and the list of columns that will serve as filters
dynamic_filters = DynamicFilters(df, filters=['transmission', 'fuel', 'is_4wd', 'cylinders'])
# displaying the filters in the app
dynamic_filters.display_filters()
# displaying the filtered dataframe
dynamic_filters.display_df()

#tech = ['price','type','Condition']
#options = st.multiselect('Compare the condition by these specifications', options = tech)
