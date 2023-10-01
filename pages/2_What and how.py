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
    # Sub-Title: What and how
    st.subheader("What and how")
    st.write("Venture into the thematic intricacies of misinformation with our categorized area charts. Trace political, religious, and health-related themes and their nuanced sub-categories like political entities, religious affiliations, and Covid-19 related misinformation. Further delve into specifics with hyperlinked articles, enabling an informed understanding of the underlying facts.")
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
  
    yearly_area_data = filtered_df.resample('M', on='publication_date').agg({
        'health': 'sum',
        'Religious': 'sum',
        'Political': 'sum'
    }).reset_index()
    st.area_chart(yearly_area_data.set_index('publication_date')[['health', 'Religious', 'Political']])
    # Prepare data for radar chart for health-related columns from filtered_df
    st.subheader("Health")
    st.write("The health theme includes misinformation around topics pertaining to health like vaccines, COVID etc. The radar chart shows the spread among these topics for the selected date range.")
    health_cols = ['vaccine', 'lockdown', 'quarantine', 'social distancing', 'COVID_Related']
    health_data = filtered_df[health_cols].sum()  # Make sure filtered_df is defined in your code
            
    # Create radar chart
    labels = health_data.index
    stats = health_data.values
            
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
      r=stats,
      theta=labels,
      fill='toself',
      name='Health Topics'
    ))

    fig.update_layout(
        polar=dict(
        radialaxis=dict(
        visible=True,
    )),
        showlegend=False
    )
            
    st.plotly_chart(fig)
    
    st.subheader("Religion")
    st.write("The religion theme includes misinformation around religious entities. The radar chart shows the spread among different religious identifiers for the selected date range.")
    religion_cols = ['hindu', 'muslim', 'islam', 'christian', 'sikh', 'jain', 'buddhist', 'temple', 'mosque', 'church']
    religion_data = filtered_df[religion_cols].sum()
    labels = religion_data.index
    stats = religion_data.values
    fig_religion = go.Figure()
    fig_religion.add_trace(go.Scatterpolar(r=stats, theta=labels, fill='toself', name='Religion Topics'))
    fig_religion.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig_religion)
    st.subheader("Political")
    st.write("The political theme includes misinformation involving political entities. The trendline shows a cumulative trend for the selected date range.")
    politics_trend = filtered_df.resample('M', on='publication_date').sum()['Political']  # Summing the mentions of politics per month
    fig = px.line(politics_trend, x=politics_trend.index, y='Political', title='Monthly Mentions of Political entities')
    st.plotly_chart(fig)
    tag = st.selectbox('Select Tag:', ['health', 'Political', 'Religious'])
    filtered_df = filtered_df[filtered_df[tag] == 1]
    
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
    st.markdown(":orange[Our classifiers are still a work in progress and there might be a few cases of miscategorized factchecks.]")
if __name__ == '__main__':
    main()
