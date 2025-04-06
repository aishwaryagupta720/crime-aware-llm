import streamlit as st
import pandas as pd
import geopandas as gpd
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objs as go
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from matplotlib.colors import LinearSegmentedColormap, to_hex
from io import BytesIO
import json
from streamlit_chat import message
import requests

# Load Dataset
@st.cache_data
def load_data():
    file_path = r'crime_dataset.csv'
    data = pd.read_csv(file_path)
    return data

data = load_data()

# Title
st.title("Violent Crime Rate in California")

# Create tabs
tab1, tab2, tab3, tab4, tab5= st.tabs(["Heatmap", "Crime Rate Over Time", "Crime Types Distribution", "Geospatial Clustering","CalCrime Bot"])

# Common functions
@st.cache_data
def load_geojson():
    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/california-counties.geojson"
    geojson_data = gpd.read_file("california-counties.geojson")
    return geojson_data

geojson_data = load_geojson()

with tab1:
    # Heatmap Visualization
    years = sorted(data['reportyear'].unique())
    selected_year = st.selectbox("Select Year", years, key='heatmap_year')

    data_selected = data[(data['reportyear'] == selected_year) & (data['strata_level_name'] == 'Violent crime total')]
    columns_to_keep = ['reportyear', 'geoname', 'rate', 'numerator']
    data_selected = data_selected[columns_to_keep].dropna(subset=['rate'])
    data_selected['rate'] = pd.to_numeric(data_selected['rate'], errors='coerce').dropna()

    merged_data = geojson_data.merge(data_selected, left_on='name', right_on='geoname')
    merged_data['geometry'] = merged_data['geometry'].simplify(tolerance=0.01)

    color_scale = LinearSegmentedColormap.from_list("custom_scale", ["white", "lightgrey", "grey", "darkred"])
    min_rate = merged_data['rate'].min()
    max_rate = merged_data['rate'].max()

    def get_color(value, min_val, max_val):
        norm_value = (value - min_val) / (max_val - min_val) if max_val > min_val else 0
        return to_hex(color_scale(norm_value))

    merged_data['color'] = merged_data['rate'].apply(lambda x: get_color(x, min_rate, max_rate))

    def get_crime_details(row):
        violent_crime_total = row['numerator']
        agg_assault = data[(data['reportyear'] == selected_year) & (data['geoname'] == row['geoname']) & (data['strata_level_name'] == 'Aggravated assault')]['numerator'].values[0]
        forcible_rape = data[(data['reportyear'] == selected_year) & (data['geoname'] == row['geoname']) & (data['strata_level_name'] == 'Forcible rape')]['numerator'].values[0]
        murder_manslaughter = data[(data['reportyear'] == selected_year) & (data['geoname'] == row['geoname']) & (data['strata_level_name'] == 'Murder and non-negligent manslaughter')]['numerator'].values[0]
        robbery = data[(data['reportyear'] == selected_year) & (data['geoname'] == row['geoname']) & (data['strata_level_name'] == 'Robbery')]['numerator'].values[0]
        return f"""
        County: {row['geoname']}<br>
        Total Violent Crime: {violent_crime_total}<br>
        Aggravated assault: {agg_assault}<br>
        Forcible Rape: {forcible_rape}<br>
        Murder and Manslaughter: {murder_manslaughter}<br>
        Robbery: {robbery}
        """

    merged_data['crime_details'] = merged_data.apply(get_crime_details, axis=1)

    fig1 = go.Figure(go.Choroplethmapbox(
        geojson=merged_data.geometry.__geo_interface__,
        locations=merged_data.index,
        z=merged_data['rate'],
        colorscale="Reds",
        marker_opacity=0.6,
        marker_line_width=0,
        text=merged_data['crime_details'],  # hover text
        hoverinfo='text'
    ))

    fig1.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4.5,
        mapbox_center={"lat": 37.0, "lon": -120.0},
        margin={"r":0,"t":30,"l":0,"b":0},
        coloraxis_colorbar=dict(
            title="Crime Rate"
        )
    )
    st.plotly_chart(fig1)

with tab2:
    st.header("Crime Rate Over Time")

    counties = sorted(data['geoname'].unique())
    selected_county = st.selectbox("Select County", counties, index=counties.index("Santa Clara"), key='time_series_county')

    data_total = data[data['strata_level_name'] == 'Violent crime total']
    
    def create_chart(county):
        data_county = data_total[data_total['geoname'] == county]
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=data_county['reportyear'], y=data_county['rate'], mode='lines', line=dict(color='red')))
        fig2.update_layout(
            title=f"Crime Rate in {county} County",
            xaxis=dict(tickmode='linear', tick0=2000, dtick=1, range=[2000, 2013]),
            yaxis=dict(title='Crime Rate'),
            transition={'duration': 300}
        )
        return fig2

    fig2 = create_chart(selected_county)
    chart = st.plotly_chart(fig2, use_container_width=True)

    def update_chart():
        county = st.session_state.time_series_county
        fig2 = create_chart(county)
        chart.plotly_chart(fig2, use_container_width=True)
    
    update_chart()

with tab3:
    st.header("Crime Types Distribution")

    
    # Filter for the year and county
    selected_year = st.selectbox("Select Year", years, key='piechart_year')
    selected_county = st.selectbox("Select County", counties, key='piechart_county')

    filtered_data = data[(data['reportyear'] == selected_year) & (data['geoname'] == selected_county)]
    filtered_data = filtered_data[filtered_data['strata_level_name'] != 'Violent crime total']

    # Calculate percentages
    total_crimes = filtered_data['numerator'].sum()
    filtered_data['percentage'] = (filtered_data['numerator'] / total_crimes) * 100

    # Create the pie chart
    fig3 = px.pie(filtered_data, values='percentage', names='strata_level_name', 
                  title=f'Crime Types in {selected_county} ({selected_year})', hole=0.4)

    fig3.update_traces(textinfo='percent+label', hoverinfo='none', pull=[0.1] + [0] * (len(filtered_data) - 1))

    # Add a central annotation
    fig3.update_layout(
        annotations=[dict(text=str(selected_year), x=0.5, y=0.5, font_size=20, showarrow=False)],
        showlegend=False
    )

    st.plotly_chart(fig3)


with tab4:
    st.header("Geospatial Analysis with Clustering")

    data_total = data[data['strata_level_name'] == 'Violent crime total']
    data_total['rate'] = pd.to_numeric(data_total['rate'], errors='coerce')
    data_total = data_total.dropna(subset=['rate'])

    merged_data = geojson_data.merge(data_total, left_on='name', right_on='geoname')
    merged_data['centroid'] = merged_data.geometry.centroid
    merged_data['longitude'] = merged_data.centroid.x
    merged_data['latitude'] = merged_data.centroid.y

    clustering_data = merged_data[['longitude', 'latitude', 'rate']]

    kmeans = KMeans(n_clusters=5, random_state=42)
    merged_data['cluster'] = kmeans.fit_predict(clustering_data)

    cluster_meanings = {
        0: "Low crime rate area",
        1: "Moderate crime rate area",
        2: "High crime rate area",
        3: "Very high crime rate area",
        4: "Extremely high crime rate area"
    }

    def map_cluster_to_color(cluster):
        colors = px.colors.qualitative.Plotly
        return colors[cluster % len(colors)]

    merged_data['color'] = merged_data['cluster'].apply(map_cluster_to_color)

    # Create a scatter mapbox with legends for clusters
    fig4 = go.Figure()

    for cluster in merged_data['cluster'].unique():
        cluster_data = merged_data[merged_data['cluster'] == cluster]
        fig4.add_trace(go.Scattermapbox(
            lat=cluster_data['latitude'],
            lon=cluster_data['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                color=map_cluster_to_color(cluster),
                opacity=0.7
            ),
            text=cluster_data['geoname'] + "<br>Cluster: " + cluster_data['cluster'].astype(str),
            hoverinfo='text',
            name=f"Cluster {cluster}: {cluster_meanings[cluster]}"
        ))

    fig4.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 37.0, "lon": -120.0},
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    st.plotly_chart(fig4)

with tab5:
    st.header("CalCrime Bot")

    API_URL = "http://127.0.0.1:5002/ask"
    headers = {'Content-Type': 'application/json'}


    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def query(payload):
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        return response.text

    def get_text():
        input_text = st.text_input("You: ","Ask Questions about Crime in California", key="input")
        return input_text 


    user_input = get_text()
    if user_input:
        output = query({
            "prompt": user_input
        }) 
        print(output)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:

        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')


