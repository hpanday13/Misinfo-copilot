import streamlit as st
import pandas as pd
from hugchat import hugchat
from hugchat.login import Login

# Load data
df = pd.read_csv('extracted_articles_data_keyword_annotated_final.csv')
df['publication_date'] = pd.to_datetime(df['publication_date'], format='%d-%m-%Y')
email = st.secrets["email"]
passwd = st.secrets["password"]


sign = Login(email, passwd)
cookies = sign.login()
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
st.session_state['chatbot'] = chatbot  # Store chatbot in session state
# rest of your code

def display_images(filtered_df, offset, length):
    displayed_images = filtered_df['main_image'][offset:offset+length].tolist()
    col1, spacer, col2 = st.columns([1, 0.05, 1])
    col1.image(displayed_images[0], width=300)
    col1.markdown(f"[{filtered_df['headline'].iloc[offset]}]({filtered_df['Article Links'].iloc[offset]})")
    col2.image(displayed_images[1], width=300)
    col2.markdown(f"[{filtered_df['headline'].iloc[offset + 1]}]({filtered_df['Article Links'].iloc[offset + 1]})")
    
    selected_option = st.radio("Choose a misninformation to debunk:", ['Misinformation 1', 'Misinformation 2'], key='misinfo_radio')
    selected_index = 0 if selected_option == 'Misinformation 1' else 1
    st.subheader("You chosen misinformation to debunk is")
    st.image(displayed_images[selected_index], width=300)
    st.markdown(f"[{filtered_df['headline'].iloc[offset + selected_index]}]({filtered_df['Article Links'].iloc[offset + selected_index]})")
    selected_row = filtered_df.iloc[offset + selected_index]
    text_to_display = f"{selected_row.iloc[0]} | {selected_row.iloc[1]} | {selected_row.iloc[2]}"
    st.markdown(text_to_display)
    return(text_to_display)


def main():
    # Sub-Title: When
    st.header("Your Misinformation AI Co-pilot")
    st.write("Facing a challenging piece of misinformation? Our AI co-pilot is here to help! Select the misinformation you're keen on debunking and choose from personas like a Religious Leader, Doctor, or Librarian. Drawing upon their domain wisdom, the co-pilot curates a tailored response to counter the false narrative. It's our way of equipping you with knowledge, perspective, and the confidence to challenge misinformation effectively.")
    st.markdown(":orange[Caution]")
    st. write("Our AI co-pilot is an experimental release in understanding the role large language models can play in debunking misinformation. We are using this opportunity to look at safety risks, algorithmic biases, hallucinations, and model performances at this point. If you see a consistent pattern of failure, please send a screenshot to team@dignityindifference.org. The models are rate limited and self hosted. If you experience an error, please try again later.")
    st.subheader("Choose a misinformation")

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
    tag = st.selectbox('Select Tag:', ['health', 'Religious'])
    filtered_df = filtered_df[filtered_df[tag] == 1]
    if 'current_image_index' not in st.session_state:
        st.session_state['current_image_index'] = 0

    start_idx = st.session_state['current_image_index']
    end_idx = start_idx + 1

    prev_button, _, next_button = st.columns([2, 8, 2])

    with prev_button:
     st.write("", "", "")  # Empty space for alignment
     if st.button("Previous", key="prev_button"):
        st.session_state['current_image_index'] = max(0, start_idx - 2)

    with next_button:
     st.write("", "", "")  # Empty space for alignment
     if st.button("Next", key="next_button"):
        st.session_state['current_image_index'] = min(len(filtered_df) - 1, start_idx + 2)
    st.write ("Our classifiers are still a work in progress and there might be a few cases of miscategorised factchecks.")    
    text_to_display = display_images(filtered_df, start_idx, 2)


    st.subheader("I need help from")
    persona_choice = st.radio("Choose a persona:", ["Religious Leader", "Doctor", "Librarian"])

    if persona_choice == "Religious Leader":
       persona_text = "Take the role of a learned religious leader. You are helping a young person in fighting misinformation. Based on the misninformation text coming next, choose an appropiate religion and provide a relevant message containing religious teaching to fight the misinformation."
    elif persona_choice == "Doctor":
       persona_text = "Take the role of a senior doctor and medical researcher. You are helping a young person in fighting misinformation. Based on the misninformation text coming next, choose an appropiate source and provide a relevant message containing citations to fight the misinformation."
    else:  # Librarian
       persona_text = "Take the role of a senior librarian and historian. You are helping a young person in fighting misinformation. Based on the misninformation text coming next, choose an appropiate discipline and author and provide a relevant message containing citations to fight the misinformation."
    combined_text = persona_text + " " + text_to_display
    
    if 'chatbot' in st.session_state:
        if st.button("Help me with your wisdom"):
            st.write("This process could take some time. Please wait. The text would appear when the ruuninng animation on the top right stops.")
            response = st.session_state['chatbot'].query(text=combined_text, max_new_tokens=1500)
            st.subheader("What they say:")
            st.write(response['text'])




if __name__ == '__main__':
    main()
