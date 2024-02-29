import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize Streamlit app
st.set_page_config(page_title="eSIM Market Analysis", layout="wide")

st.markdown(
""" 
<style>
div.block-container{padding-top:2rem;}
img {
    max-width: 80%;
}
.main {
    background-color: #FFFFF7;
}
.sidebar .sidebar-content {
    background-color: #FFC000;
}
div.stButton > button {
        font-size: 15px;
        font-weight: bold;
        text-align: left;
        #padding: 5px 10px;
        width: 100%;
        border: none;
        background-color: #3c9de7;
        color: white;
    }
    div.stButton > button:hover {
        background-color: transparent;
    }
</style>
""",
unsafe_allow_html= True
)
# Function to load data
@st.cache_data
def load_data():
    file_path = 'eSimDB_Sep23.csv'
    data = pd.read_csv(file_path)
    return data
# Load the data
esim_data = load_data()
#print(esim_data.columns)
# Strip leading and trailing spaces from column names
esim_data.columns = esim_data.columns.str.strip()
# Calculate price per GB (using capacity_MB and usdPrice per plan)
esim_data['price_per_GB'] = esim_data['usdPrice'] / (esim_data['capacity_MB'] / 1000)
# Title and Introduction
st.title("eSIM Market Analysis Dashboard")
st.write("This dashboard provides a comprehensive analysis of eSIM plans from various providers in each country. Users can navigate through different analyses such as Country, Provider, Plan Type, Pricing etc. Filters at the top allow customization based on Region, Country, Provider, Plan Type, Capacity, and Period.")
st.write("Some sample analysis- \n\n a) check the global coverage of provider AstroCell \n\n b) compare the price of all providers for 1 GB plan at Singapore etc.")
st.markdown("## Explore eSIM plans across various countries and providers")

# Sidebar for page selection and color picker
st.sidebar.header("Select a Dashboard")

#page = st.sidebar.radio("Select a Dashboard", ["Country Analysis", "Provider Analysis", "Plan Type & Capacity", "Price Analysis", "Trend Analysis"])
#chart_color = st.sidebar.color_picker("Pick a chart color")
#page = None
# Initialize session state for page navigation if not already set
if 'page' not in st.session_state:
    st.session_state.page = 'Country Analysis'

# Sidebar for page selection using buttons
def set_page(page_name):
    st.session_state.page = page_name

pages = ["Country Analysis", "Provider Analysis", "Plan Type & Capacity", "Pricing Analysis", "All Plans"]


for p in pages:
    st.sidebar.button(p, key=p, on_click=set_page, args=(p,))

# Initialize filter states in session_state
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = 'All'
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = 'All'
if 'selected_provider' not in st.session_state:
    st.session_state.selected_provider = 'All'
if 'selected_plan_type' not in st.session_state:
    st.session_state.selected_plan_type = 'All'
if 'selected_capacity' not in st.session_state:
    st.session_state.selected_capacity = 'All'
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = 'All'

# Reset filters function
def reset_filters():
    st.session_state.selected_region = 'All'
    st.session_state.selected_country = 'All'
    st.session_state.selected_provider = 'All'
    st.session_state.selected_plan_type = 'All'
    st.session_state.selected_capacity = 'All'
    st.session_state.selected_period = 'All'


# Filters across the top of the dashboard
col11, col12, col13 = st.columns(3)

with col11:
    selected_region = st.selectbox('Select Region', ['All'] + sorted(esim_data['Region'].unique().tolist()))

with col12:
    selected_country = st.selectbox('Select Country', ['All'] + sorted(esim_data['Country'].unique().tolist()))

with col13:
    selected_provider = st.selectbox('Select Provider', ['All'] + sorted(esim_data['provider.name'].unique().tolist()))

col14, col15, col16 = st.columns(3)

with col14:
    selected_plan_type = st.selectbox('Select Plan type', ['All'] + sorted(esim_data['Plan_Type'].unique().tolist()))

with col15:
    selected_capacity = st.selectbox('Select Capacity', ['All'] + sorted(esim_data['Capacity_in_GB'].unique().tolist()))

with col16:
    selected_period = st.selectbox('Select Period', ['All'] + sorted(esim_data['period'].unique().tolist()))

#if st.button('Reset Filters'):
#    reset_filters()
# Applying filters to the data
def apply_filters(data):
    if selected_region != 'All':
        data = data[data['Region'] == selected_region]
    if selected_country != 'All':
        data = data[data['Country'] == selected_country]
    if selected_provider != 'All':
        data = data[data['provider.name'] == selected_provider]
    if selected_plan_type != 'All':
        data = data[data['Plan_Type'] == selected_plan_type]
    if selected_capacity != 'All':
        data = data[data['Capacity_in_GB'] == selected_capacity]
    if selected_period != 'All':
        data = data[data['period'] == selected_period]
    return data

filtered_data = apply_filters(esim_data)

# Page: Country Analysis
if st.session_state.page == "Country Analysis":
    st.header("Country Analysis")

    # First row of charts
    col1, col2 = st.columns(2)
    with col1:
        # Map visualization of eSIM plan presence
        st.subheader("Number of eSIM Plans by Country")
        country_count = filtered_data['Country'].value_counts().reset_index()
        country_count.columns = ['Country', 'Number of Plans']
        fig = px.choropleth(country_count, locations="Country", locationmode='country names', color="Number of Plans",
                            color_continuous_scale=px.colors.sequential.Blues)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Bar chart of number of plans per country
        st.subheader("Number of eSIM Plans by Country")
        fig = px.bar(country_count, x='Country', y='Number of Plans', text_auto=True, color='Number of Plans')
        st.plotly_chart(fig, use_container_width=True)

    # Second row of charts
    col3, col4 = st.columns(2)
    with col3:
        # Average price of plans per country
        st.subheader("Average Price of eSIM Plans per Country")
        avg_price_country = filtered_data.groupby('Country')['usdPrice'].mean().reset_index()
        fig = px.bar(avg_price_country, x='Country', y='usdPrice', text_auto=True, color='usdPrice')
        fig.update_layout(xaxis_title='Country', yaxis_title='Average Price per Plan')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Average Price per GB by Country")
        avg_price_per_gb = filtered_data.groupby('Country')['price_per_GB'].mean().reset_index()

        # Create a bar chart
        fig = px.bar(avg_price_per_gb, x='Country', y='price_per_GB', text_auto=True, color='price_per_GB')
        fig.update_layout(xaxis_title='Country', yaxis_title='Average Price per GB (USD)')
        st.plotly_chart(fig, use_container_width=True)

if st.session_state.page == "Provider Analysis":
    st.header("Provider Analysis")
    col1, col2 = st.columns(2)
    with col1:
        # Data preparation for provider-based analysis
        provider_data = filtered_data.groupby('provider.name').agg({'Capacity_in_GB': 'count', 'usdPrice': 'mean'}).reset_index()
        provider_data.columns = ['Provider', 'Number of Plans', 'Average Price']

        # Provider-wise number of plans
        fig = px.bar(provider_data, x='Provider', y='Number of Plans', text_auto=True, color='Number of Plans')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        # Provider-wise average price
        fig = px.bar(provider_data, x='Provider', y='Average Price', text_auto=True, color='Average Price')
        st.plotly_chart(fig, use_container_width=True)

    # Second row of charts
    col3, col4 = st.columns(2)
    with col3:
        fig = px.pie(filtered_data, names='Capacity_in_GB', hole=0.4, title='Distribution of Plan Types by Capacity')
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        fig = px.box(filtered_data, x='Capacity_in_GB', y='usdPrice',
                     title='Price Distributions for Different Capacity Ranges')
        st.plotly_chart(fig, use_container_width=True)

if st.session_state.page == "All Plans":
    st.header("Tabular View of All plans")
    st.dataframe(filtered_data)
# Implement similar logic for other pages: Provider Analysis, Plan Type & Capacity, Pricing Analysis, Trend Analysis
# Historical Data required for Trend Analysis
# For each of the provider, identify for which country they have thier best plan

# Show filtered data
#st.dataframe(filtered_data)
