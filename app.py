import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_dynamic_filters import DynamicFilters

df=pd.read_csv('cleaned_data.csv')

st.title(':gray-background[:rainbow[*Choose your dream car!*] :sunglasses:]')
# put two whitespace characters in front of the newline character, so it is recognised as a new line in streamlit
st.write('Use this app to select a car based on your preferences.  \n You can choose by price and model year or by technical characteristics of the car.')

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
st.plotly_chart(fig1, use_container_width=True)

st.subheader(':green[The distribution of the selected cars by type and condition:]')
# a checkbox for new cars
# if the box is checked, the selected via the sliders cars (selected_year dataset) are filtered by condition
# if the box is not checked, the chart shows the selection made via the sliders
new_car = st.checkbox('Only new cars')
if new_car:
    filtered_data=selected_year[selected_year.condition=='new']
else:
    filtered_data=selected_year

# a histogram of type & condition distribution for the selected vehicles
fig2 = px.histogram(filtered_data, x='type', color='condition', hover_data=df.columns).update_xaxes(categoryorder='total descending')
st.plotly_chart(fig2, use_container_width=True)

# a table with vehicles from the selection
st.write('Here is the list of selected cars:')
st.dataframe(filtered_data)

# a download button for the table
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

csv = convert_df(filtered_data)

st.download_button(
    label="Download the selection as CSV",
    data=csv,
    file_name="selected cars.csv",
    mime="text/csv",
)

st.divider()
st.header(':orange[Choose a car by its technical specifications]')

# creating an instance of the DynamicFilters class, passing the dataframe and the list of columns that will serve as filters
dynamic_filters = DynamicFilters(df, filters=['transmission', 'fuel', 'is_4wd', 'cylinders'])
# displaying the filters in the app
dynamic_filters.display_filters()
# displaying the filtered dataframe
dynamic_filters.display_df()
# a new dataframe based on the selected filters
new_df = dynamic_filters.filter_df()

# a download button for the table
csv = convert_df(new_df)

st.download_button(
    label="Download the selection as CSV",
    data=csv,
    file_name="cars with selected specifications.csv",
    mime="text/csv",
)

st.subheader(':green[The distribution of the selected cars by mileage and condition:]')
# a multiselect option for condition
conditions = new_df['condition'].unique()
condition_select = st.multiselect('Choose the car condition', options = conditions)

if condition_select:
    df_selection = new_df[new_df['condition'].isin(condition_select)]
else:
    df_selection = new_df

# a scatterplot of vehicles based on the selected technical specifications
fig3 = px.scatter(df_selection, x='odometer', y='condition', hover_data=[df_selection['transmission'], df_selection['fuel'], df_selection['is_4wd'], df_selection['cylinders']])
st.plotly_chart(fig3, use_container_width=True)

# a table with vehicles with the selected specifications and condition
st.write('Here is the list of selected cars:')
st.dataframe(df_selection)

# a download button for the table
csv = convert_df(df_selection)

st.download_button(
    label="Download the selection as CSV",
    data=csv,
    file_name="cars with selected conditions.csv",
    mime="text/csv",
)