import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# Load data
df = pd.read_csv('extracted_articles_data_keyword_annotated_final.csv')
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d-%m-%Y')

def display_images(filtered_df, offset, length):
    displayed_images = filtered_df['main_image'][offset:offset+length].tolist()
    for i in range(0, len(displayed_images), 2):
       col1, spacer, col2 = st.columns([1, 0.05, 1])
       col1.image(displayed_images[i], width=300)
       col1.markdown(f"[{filtered_df['headline'].iloc[offset + i]}]({filtered_df['Article Links'].iloc[offset + i]})")
       if i + 1 < len(displayed_images):
          col2.image(displayed_images[i + 1], width=300)
          col2.markdown(f"[{filtered_df['headline'].iloc[offset + i + 1]}]({filtered_df['Article Links'].iloc[offset + i + 1]})")
       st.write('---')  # Adding a line for spacing


def main():
    # Sub-Title: Where
    st.subheader("What and how")
    st.write("Uncover the geographical hotspots of misinformation with our intuitive map, indicating areas based on the frequency of related fake news. Complement this with a glance at the platforms and their mentions around misinformation. Navigate the charts, choose dates, and use the selection tools to obtain hyperlinked fact-checking articles related to your theme of interest.")
    st.markdown(":orange[Our current dataset is from July 2017 to August 2023. We are in the process of building a real-time data-stream. Selecting a date range beyond the data availability would throw an error.]")
    # Month and Year Picker
    st.write("Select Date Range")
    col1, col2, col3, col4 = st.columns(4)
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    with col1:
        start_month = st.selectbox('From - Month:', month_list, index=0)
    with col2:
        start_year = st.selectbox('From - Year:', list(range(2017, 2024)), index=0)
    with col3:
        end_month = st.selectbox('To - Month:', month_list, index=7)
    with col4:
        end_year = st.selectbox('To - Year:', list(range(2017, 2024)), index=6)
        
    start_month_num = month_list.index(start_month) + 1
    end_month_num = month_list.index(end_month) + 1
    
    start_date = pd.Timestamp(year=start_year, month=start_month_num, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month_num, day=1)
    
    filtered_df = df[(df['publication_date'] >= start_date) & (df['publication_date'] <= end_date)]
    st.subheader("Geo-location")
    st.write("An enhanced location recogniser is being trained and will soon be available for hyperlocal visualisation.")
    state_coords = {
    "andhra pradesh": (15.9129, 79.7400),
    "arunachal pradesh": (28.2180, 94.7278),
    "assam": (26.2006, 92.9376),
    "bihar": (25.0961, 85.3131),
    "chhattisgarh": (21.2787, 81.8661),
    "goa": (15.2993, 74.1240),
    "gujarat": (22.2587, 71.1924),
    "haryana": (29.0588, 76.0856),
    "himachal pradesh": (31.1048, 77.1734),
    "jharkhand": (23.6102, 85.2799),
    "karnataka": (15.3173, 75.7139),
    "kerala": (10.8505, 76.2711),
    "madhya pradesh": (22.9734, 78.6569),
    "maharashtra": (19.7515, 75.7139),
    "manipur": (24.6637, 93.9063),
    "meghalaya": (25.4670, 91.3662),
    "mizoram": (23.1645, 92.9376),
    "nagaland": (26.1584, 94.5624),
    "odisha": (20.9517, 85.0985),
    "punjab": (31.1471, 75.3412),
    "rajasthan": (27.0238, 74.2179),
    "sikkim": (27.5330, 88.5122),
    "tamil nadu": (11.1271, 78.6569),
    "telangana": (18.1124, 79.0193),
    "tripura": (23.9408, 91.9882),
    "uttar pradesh": (26.8467, 80.9462),
    "uttarakhand": (30.0668, 79.0193),
    "west bengal": (22.9868, 87.8550),
    "andaman and nicobar islands": (11.7401, 92.6586),
    "chandigarh": (30.7333, 76.7794),
    "dadra and nagar haveli": (20.1809, 73.0169),
    "daman and diu": (20.4283, 72.8397),
    "lakshadweep": (10.5667, 72.6417),
    "delhi": (28.6139, 77.2090),
    "puducherry": (11.9416, 79.8083)
     }
    state_columns = filtered_df.columns[45:74]  
    state_event_counts = filtered_df[state_columns].sum(axis=0)

    # Prepare map data
    map_data = pd.DataFrame({
      'lat': [state_coords[state][0] for state in state_event_counts.index],
      'lon': [state_coords[state][1] for state in state_event_counts.index],

      'events': state_event_counts.values
     })

    fig = px.scatter_mapbox(map_data, lat='lat', lon='lon', size='events', 
                        color_discrete_sequence=["fuchsia"], size_max=15, zoom=3)
    fig.update_layout(mapbox_style="open-street-map", height=600)
    st.plotly_chart(fig)
    st.subheader("Platfroms")
    social_media_cols = ['facebook', 'twitter', 'instagram', 'whatsapp', 'linkedin', 'snapchat', 'youtube', 'tiktok', 'pinterest']
    social_media_counts = filtered_df[social_media_cols].sum()
    # Assuming social_media_counts is a pandas Series
    fig = px.bar(y=social_media_counts.index, x=social_media_counts.values, text=social_media_counts.values, orientation='h')
    fig.update_traces(texttemplate='%{text}', textposition='outside', marker_color='rgb(55, 83, 109)')
    fig.update_layout(title='Distribution of Events on Social Media Platforms',
         yaxis_title='Platform',
          xaxis_title='Number of Events',
          uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_traces(marker_color=['#E53935', '#D32F2F', '#C62828', '#B71C1C', '#F44336', '#EF5350', '#E57373', '#EF9A9A', '#FFCDD2'])
    st.plotly_chart(fig)
    category_selection = st.selectbox("Choose Category:", ["Geo Location", "Platforms"])

    if category_selection == "Geo Location":
       sub_category = st.selectbox("Choose State:", list(state_coords.keys()))
       filtered_df = df[df[sub_category.lower()] == 1]
    else:
       sub_category = st.selectbox("Choose Platform:", ["facebook", "twitter", "instagram", "whatsapp", "linkedin", "snapchat", "youtube", "tiktok", "pinterest"])
       filtered_df = df[df[sub_category] == 1]

    if 'current_image_index' not in st.session_state:
       st.session_state['current_image_index'] = 0

    start_idx = st.session_state['current_image_index']
    end_idx = start_idx + 6

    display_images(filtered_df, start_idx, 6)

    prev_button, _, next_button = st.columns([2, 8, 2])
    with prev_button:
     st.write("", "", "")  # Empty space for alignment
     if st.button("Previous", key="prev_button"):
        st.session_state['current_image_index'] = max(0, start_idx - 6)

    with next_button:
     st.write("", "", "")  # Empty space for alignment
     if st.button("Next", key="next_button"):
        st.session_state['current_image_index'] = min(len(filtered_df) - 1, start_idx + 6)
    st.write ("Our classifiers are still a work in progress and there might be a few cases of miscategorised factchecks.")

if __name__ == '__main__':
    main()
