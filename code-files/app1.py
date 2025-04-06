import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd

# Title
st.title("California Violent Crime Rate (2000-2013)")

# Load Dataset
@st.cache_data
def load_data():
    file_path = r'C:\Users\ankit\Downloads\trimmed_crime_data_2000.xlsx'
    data = pd.read_excel(file_path)
    return data

data = load_data()

# Display column names to verify
st.write("Columns in the dataset:", data.columns)

# Filter by Year
st.subheader("Filter Data by Year")
if 'reportyear' in data.columns:
    years = st.slider("Select Year Range", min_value=2000, max_value=2013, value=(2000, 2013))
    filtered_data = data[(data['reportyear'] >= years[0]) & (data['reportyear'] <= years[1])]
    st.write(filtered_data)
    
    # Ensure the correct column name is used for plotting
    crime_rate_column = 'rate'  # Replace with the actual column name for violent crime rate
    county_column = 'county_name'  # Column representing county names in your dataset

    # Interactive Line Chart with Plotly
    st.subheader("Violent Crime Rate Over Time")
    fig = px.line(filtered_data, x='reportyear', y=crime_rate_column, title='Violent Crime Rate Over Time')
    st.plotly_chart(fig)

    # Interactive Bar Chart with Plotly
    st.subheader("Violent Crime Rate by Year")
    fig = px.bar(filtered_data, x='reportyear', y=crime_rate_column, title='Violent Crime Rate by Year')
    st.plotly_chart(fig)

    # Load California GeoJSON data for the heatmap
    @st.cache_data
    def load_geojson():
        geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
        geojson_data = gpd.read_file(geojson_url)
        return geojson_data

    geojson_data = load_geojson()

    # Merge crime data with GeoJSON
    merged_data = geojson_data.merge(filtered_data, left_on='name', right_on=county_column)

    # Heatmap
    st.subheader("Crime Rate Heatmap")
    fig = px.choropleth_mapbox(
        merged_data, geojson=merged_data.geometry, locations=merged_data.index,
        color=crime_rate_column, color_continuous_scale="OrRd",
        mapbox_style="carto-positron", zoom=5, center={"lat": 37.7749, "lon": -122.4194},
        opacity=0.5, labels={crime_rate_column: 'Crime Rate'}
    )
    fig.update_geos(fitbounds="locations")
    st.plotly_chart(fig)
else:
    st.error("The 'reportyear' column is not in the dataset.")
