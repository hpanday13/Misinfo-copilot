import streamlit as st
import pandas as pd

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
    # Sub-Title: When
    st.subheader("When")
    st.write("Explore the temporal spread of misinformation through our interactive bar chart detailing fake news events. Curate the headlines and paragraphs from reliable fact-checking sources, and view the visuals. Navigate through time, selecting dates of interest, to reveal how the misinformation landscape has evolved.")
    st.markdown(":orange[Our current dataset is from July 2017 to August 2023. We are in the process of building a real-time data-stream. Selecting a date range beyond the available data would throw an error.]")
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
    
    # Weekly count
    weekly_count = filtered_df.resample('W', on='publication_date').size().reset_index(name='Count')
    weekly_count['Date'] = weekly_count['publication_date']
    
    mean_count = weekly_count['Count'].mean()
    lower_threshold = 0.8 * mean_count
    upper_threshold = 1.2 * mean_count
    
    # Create separate columns based on condition
    weekly_count['Below_Threshold'] = weekly_count.apply(lambda row: row['Count'] if row['Count'] < lower_threshold else None, axis=1)
    weekly_count['Above_Threshold'] = weekly_count.apply(lambda row: row['Count'] if row['Count'] > upper_threshold else None, axis=1)
    weekly_count['Within_Threshold'] = weekly_count.apply(lambda row: row['Count'] if lower_threshold <= row['Count'] <= upper_threshold else None, axis=1)
    
    # Rename columns for funny chart keys
    weekly_count.rename(columns={
    'Below_Threshold': 'Just a Whiff of Gossip',
    'Above_Threshold': 'Liar Liar, Pants on Fire',
    'Within_Threshold': 'Talk of the town'
     }, inplace=True)
    # Create bar chart using Streamlit with specified Material Design colors
    st.bar_chart(weekly_count.set_index('Date')[['Just a Whiff of Gossip', 'Liar Liar, Pants on Fire', 'Talk of the town']], 
             color=["#03A9F4", "#FF5722", "#CDDC39"])
    
    # Write subtitle
    if 'current_data_index' not in st.session_state:
     st.session_state['current_data_index'] = 0  # Initialize session state

    start_data_idx = st.session_state['current_data_index']
    end_data_idx = start_data_idx + 100
    st.markdown(":blue[The bars are colored based on whether their height is below or above 20% of the mean count of articles. Bars below 80% of the mean are blue(Just a Whiff of Gossip), bars above 120% of the mean are orange(Liar Liar, Pants on Fire), and the rest are green(Talk of the town).]")

    st.write(filtered_df.iloc[start_data_idx:end_data_idx, :3])

    prev_data_button, _, next_data_button = st.columns([3, 8, 3])
    with prev_data_button:
     if st.button("Previous 100", key="prev_data_button"):
        st.session_state['current_data_index'] = max(0, start_data_idx - 100)

    with next_data_button:
     if st.button("Next 100", key="next_data_button"):
        st.session_state['current_data_index'] = min(len(filtered_df) - 1, start_data_idx + 100)

    
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

if __name__ == '__main__':
    main()
