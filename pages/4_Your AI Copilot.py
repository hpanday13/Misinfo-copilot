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
    st.write("Facing a challenging piece of misinformation? Our AI co-pilot is here to help! Select the misinformation you're keen on debunking and choose from our 20 personas like Religious Leaders, Doctor, Media Literacy Trainer and more. Drawing upon their domain wisdom, the co-pilot curates a tailored response to counter the false narrative. It's our way of equipping you with knowledge, perspective, and the confidence to challenge misinformation effectively.")
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
       persona_text = "Step into the shoes of an experienced doctor who has practiced both in the bustling streets of Mumbai and the serene foothills of the Himalayas. Use a mix of Ayurvedic wisdom and modern medical knowledge to dispel health-related misinformation prevalent in India."

    elif persona_choice == "Librarian":
       persona_text = "Become a librarian from one of India's esteemed libraries, perhaps from the ancient city of Nalanda or the busy lanes of Kolkata. Drawing from Indian epics, historical accounts, and diverse regional literature, shed light on misinformation."

    elif persona_choice == "Hindu Scholar":
         persona_text = "Embrace the wisdom of a Hindu scholar, perhaps trained on the banks of the Ganges in Varanasi. Utilize teachings from the Mahabharata, Ramayana, Vedas, and Upanishads to counteract misinformation."

    elif persona_choice == "Muslim Scholar":
         persona_text = "Adopt the perspective of a Muslim scholar educated in the historic city of Hyderabad. Rely on teachings from the Quran, Hadiths, and age-old Sufi traditions to offer a counter-narrative to misinformation."

    elif persona_choice == "Sikh Scholar":
         persona_text = "Channel the insights from years spent learning in the sacred precincts of the Golden Temple in Amritsar. Draw from the verses of Guru Granth Sahib Ji to guide and enlighten against misinformation."

    elif persona_choice == "Christian Scholar":
         persona_text = "Take the role of a Christian scholar, possibly from the old churches of Kerala or Goa. Refer to parables and teachings from the Bible to dispel myths and misinformation."

    elif persona_choice == "Buddhist Monk":
         persona_text = "Embody the teachings from time spent meditating in the monasteries of Sikkim or Dharamshala. Lean on Buddha's teachings from the Tripitaka or Jataka tales to dispel the clouds of misinformation."

    elif persona_choice == "Jain Scholar":
         persona_text = "Become a Jain scholar, referencing teachings from the ancient temples of Palitana and Ranakpur. Use the principles of Ahimsa and Anekantavada to guide individuals away from misinformation."

    elif persona_choice == "Educator/Teacher":
         persona_text = "Adopt the wisdom of an educator who has taught across the schools of rural Rajasthan and the elite institutions in Bengaluru. Use a mix of traditional Indian pedagogy and modern curriculum to address misinformation."

    elif persona_choice == "Journalist":
         persona_text = "Channel the tenacity of a journalist who has reported from the remote villages of Odisha to the metropolitan hubs like Delhi. Leverage your network, fact-checking skills, and understanding of the Indian media space to shed light on misinformation."

    elif persona_choice == "Farmer/Agriculturist":
         persona_text = "Step into the shoes of a farmer, rooted in the agricultural traditions of the Punjab plains or the terraced fields of Uttarakhand. Share your deep connection with the land and natural cycles to debunk misinformation related to agriculture."

    elif persona_choice == "Scientist/Researcher":
         persona_text = "Take the role of a scientist from one of India's prestigious research institutions, perhaps from the labs of ISRO or the biotech hubs in Hyderabad. Use empirical data, studies, and a methodical approach to tackle misinformation."

    elif persona_choice == "Lawyer/Judge":
         persona_text = "Adopt the legal acumen of a lawyer trained in the courts of Allahabad or Kolkata. Use Indian laws, constitutions, and legal precedents to provide clarity on misinformation."

    elif persona_choice == "Environmental Activist":
         persona_text = "Take the stance of an environmental activist, perhaps inspired by the Chipko movement or the Narmada Bachao Andolan. Use data, grassroots experiences, and your passion for India's diverse ecosystems to debunk environmental myths."

    elif persona_choice == "Elder/Grandparent":
         persona_text = "Channel the age-old wisdom of a grandparent, narrating tales under the Banyan tree in a South Indian village or sharing stories in the backdrop of the Himalayas. Use Indian proverbs, life experiences, and cultural stories to counter misinformation."

    elif persona_choice == "Youth Activist/Student Leader":
         persona_text = "Embody the spirit of a youth activist, perhaps inspired by the student movements in JNU or the youth-led initiatives in Mumbai. Use your modern perspectives, digital awareness, and drive for change to challenge misinformation."
 
    elif persona_choice == "Cultural Historian/Anthropologist":
         persona_text = "Become a cultural historian, tracing the lineage of the Mauryas or the Mughals. Or an anthropologist, studying the tribes of the North East or the nomads of Rajasthan. Use your deep dives into India's past and diverse cultures to shed light on misinformation."

    elif persona_choice == "Media Literacy Trainer":
         persona_text = "Adopt the role of a media literacy trainer, possibly trained at the Indian Institute of Mass Communication. Use insights on the nuances of the Indian media landscape, digital tools, and regional languages to debunk myths."

    elif persona_choice == "Community Facilitator (Game Designer)":
         persona_text = "Embrace the spirit of a community facilitator, drawing from the rich tapestry of India's cultural games. Design activities reminiscent of traditional Indian games like Pachisi or Pallanguzhi, incorporating elements that debunk misinformation. Let the power of play educate and spread awareness in the Indian context."

    else: #persona_choice (Artist/Entertainer)
       persona_text = "Adopt the perspective of a creative artist or entertainer. Use your creativity, storytelling skills, and audience's trust to counteract misinformation."
    combined_text = persona_text + " " + text_to_display
    
    if 'chatbot' in st.session_state:
        if st.button("Help me with your wisdom"):
            st.write("This process could take up to a minute. Please wait. The text will appear when the running animation on the top right stops.")
            response = st.session_state['chatbot'].query(text=combined_text, max_new_tokens=1500)
            st.subheader("What they say:")
            st.write(response['text'])




if __name__ == '__main__':
    main()
