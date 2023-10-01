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
    
    selected_option = st.radio("Choose a misinformation to debunk:", ['Misinformation 1', 'Misinformation 2'], key='misinfo_radio')
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
    st.write("Facing a challenging piece of misinformation? Our AI co-pilot is here to help! Select the misinformation you're keen on debunking and choose from personas like Religious Leaders, Doctor, Media Literacy Trainer or more. Drawing upon their domain wisdom, the co-pilot curates a tailored response to counter the false narrative. It's our way of equipping you with knowledge, perspective, and the confidence to challenge misinformation effectively.")
    st.markdown(":orange[Caution]")
    st. write("Our AI co-pilot is an experimental release for understanding the role Large Language Models(LLMs) can play in debunking misinformation. We are using this opportunity to look at safety risks, algorithmic biases, hallucinations, and model performances at this point. If you see a consistent pattern of failure, please send a screenshot to team@dignityindifference.org. The models are rate limited and self hosted. If you experience an error, please try again later.")
    st.subheader("Choose a misinformation")

    # Month and Year Picker
    st.write("Select Date Range")
    st.markdown(":orange[Our current dataset is from July 2017 to August 2023. We are in the process of building a real-time data-stream. Selecting a date range beyond the data availability would throw an error.]")
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
    st.markdown(":orange[Our classifiers are still a work in progress and there might be a few cases of miscategorized factchecks.]")  
    text_to_display = display_images(filtered_df, start_idx, 2)


    st.subheader("I need help from")
    persona_choice = st.radio("Choose a persona:", ["Doctor", "Librarian", "Hindu Scholar", "Muslim Scholar", "Sikh Scholar", "Christian Scholar", "Buddhist Monk", "Jain Scholar", "Educator/Teacher", "Journalist", "Farmer/Agriculturist", "Scientist/Researcher", "Lawyer/Judge", "Environmental Activist", "Elder/Grandparent", "Youth Activist/Student Leader", "Cultural Historian/Anthropologist", "Artist/Entertainer", "Media Literacy Trainer", "Community Facilitator (Game Designer)"])

    
    if persona_choice == "Doctor":
       persona_text = "Take the role of a senior doctor and medical researcher. You are helping a young person in fighting misinformation. Based on the misinformation text coming next, choose an appropriate source and provide a relevant message containing citations to fight the misinformation."
    elif persona_choice == "Librarian":
       persona_text = "Take the role of a senior librarian and historian. You are helping a young person in fighting misinformation. Based on the misinformation text coming next, choose an appropriate discipline and author and provide a relevant message containing citations to fight the misinformation."
    elif persona_choice == "Hindu Scholar":
       persona_text = "Embody the wisdom of a Hindu scholar. Utilize teachings from sacred texts like the Bhagavad Gita, Vedas, or Upanishads to counteract the misinformation for the young seeker."
    elif persona_choice == "Muslim Scholar":
       persona_text = "Channel the insights of a Muslim scholar. Rely on teachings from the Quran or Hadiths to offer a counter-narrative to the misinformation."
    elif persona_choice == "Sikh Scholar":
       persona_text = "Adopt the perspective of a Sikh scholar. Use teachings from the Guru Granth Sahib Ji to provide a soothing and truthful message against the misinformation."
    elif persona_choice == "Christian Scholar":
       persona_text = "Stand as a Christian scholar. Use teachings from the Bible, both the Old and New Testaments, to dispel the misinformation."
    elif persona_choice == "Buddhist Monk":
       persona_text = "Embrace the serenity of a Buddhist monk. Use teachings from the Tripitaka or Dhammapada to enlighten the young individual against the misinformation."
    elif persona_choice == "Jain Scholar":
       persona_text = "Become a Jain scholar. Use teachings from the Agamas or Tattvartha Sutra to guide the young person away from misinformation."
    elif persona_choice == "Educator/Teacher":
       persona_text = "Take the role of a seasoned educator. Use logical reasoning, facts from textbooks, and your vast teaching experience to guide the young person through the misinformation maze."
    elif persona_choice == "Journalist":
       persona_text = "Channel the mindset of a seasoned journalist. Utilize your fact-checking skills, sources, and the code of journalistic ethics to shed light on the misinformation."
    elif persona_choice == "Farmer/Agriculturist":
       persona_text = "Embrace the wisdom of an experienced farmer. Use your practical knowledge of agriculture, nature, and rural life to address misinformation related to farming and the countryside."
    elif persona_choice == "Scientist/Researcher":
       persona_text = "Adopt the analytical approach of a scientist. Use empirical data, scientific literature, and critical thinking to dissect the misinformation."
    elif persona_choice == "Lawyer/Judge":
       persona_text = "Take on the role of a legal expert. Refer to the constitution, laws, and legal precedents to provide clarity on misinformation related to legal issues."
    elif persona_choice == "Environmental Activist":
       persona_text = "Stand as an environmental champion. Use data, reports, and your passion for the environment to debunk myths related to climate change, pollution, and conservation."
    elif persona_choice == "Elder/Grandparent":
       persona_text = "Channel the wisdom of an elder or grandparent. Use anecdotes, traditional wisdom, and life experiences to shed light on misinformation."
    elif persona_choice == "Youth Activist/Student Leader":
       persona_text = "Step into the shoes of a youth activist. Use your energy, modern viewpoints, and awareness of contemporary issues to challenge misinformation."
    elif persona_choice == "Cultural Historian/Anthropologist":
       persona_text = "Embrace the insight of a cultural historian or anthropologist. Use your knowledge of historical events, cultures, and societies to provide context and debunk misinformation."
    elif persona_choice == "Artist/Entertainer":
       persona_text = "Adopt the perspective of a creative artist or entertainer. Use your creativity, storytelling skills, and audience's trust to counteract misinformation."
    elif persona_choice == "Media Literacy Trainer":
       persona_text = "Step into the shoes of a media literacy expert. Use your deep understanding of media biases, digital tools, and fact-checking skills to guide the young person in discerning truth from misinformation in the media landscape."
    else:  # Community Facilitator (Game Designer)
       persona_text = "Embody the role of a community facilitator specializing in game design. Design engaging community games and activities that foster critical thinking and collaborative problem-solving to debunk misinformation. Use the power of play
    combined_text = persona_text + " " + text_to_display
    
    if 'chatbot' in st.session_state:
        if st.button("Help me with your wisdom"):
            st.write("This process could take up to a minute. Please wait. The text will appear when the running animation on the top right stops.")
            response = st.session_state['chatbot'].query(text=combined_text, max_new_tokens=1500)
            st.subheader("What they say:")
            st.write(response['text'])




if __name__ == '__main__':
    main()
