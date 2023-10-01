import streamlit as st


st.set_page_config(
    page_title="Dignity at Scale",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded"
)

col = st.columns((1,1,1))
with col[1]:
    st.image('DID Logo.png', use_column_width=True)
col = st.columns((1,2,1))
with col[1]:
 st.header("       Dignity at Scale")

st.subheader("    Your AI and Data Co-pilot against Misinformation")
st.write("Fighting Misinformation doesn't have to be this hard :disappointed:") 
st.markdown(":orange[Please visit this app from a system's browser for best user experience.]")

st.markdown(":rainbow[Hey You!]")
st.write("[Brandolini's law](https://www.nature.com/articles/540171a)"" alternatively known as the Bullshit Asymmetry Principle says that:")
col = st.columns((1,3,1))
with col[1]:
 st.write("'The amount of energy needed to refute bullshit is an order of magnitude bigger than that needed to produce it.'")
st.write("You, my young friend, might have felt it upon seeing misinformation everywhere: in family WhatsApp groups, Instagram, news, and even gaming forums. Many times, you have stood up to fight for the truth and educate others through the ways that they trust. But it's so tiring, and coffee goes only so far.")
st.subheader("Don't you worry!")
st.write("After thousands of lines of code, many sleepless nights, and hundreds of cups of masala tea later, Dignity at Scale is here to assist you. It serves as your personal AI and Data Co-pilot, helping you navigate the vast sea of misinformation, focusing on what's most important and where, and delving deep into the tactics used in trending misinformation in your own community and on the platforms you cherish. It empowers you to harness the wisdom of our 20 AI personas to craft effective debunking and counter-speech campaigns. Whether you're an NGO combating misinformation or a youth influencer, Dignity at Scale ensures your voyage against falsehoods is as thrilling as it is impactful. ")

st.write(" Leveraging cutting-edge digital anthropological techniques and sophisticated data science methodologies, we aim to empower young influencers and NGOs with a dynamic and comprehensive view of the fake news ecosystem. Dive into curated dashboards that visualize temporal trends, thematic content, geographical locations, and their spread across platforms. Further, our unique AI co-pilot stands by to assist you in debunking and understanding misinformation. Get started and embark on this journey of truth.")

st.markdown(":blue[When Dashboard]")
st.write("Delve into the timeline of fake news events, navigating through headlines, lead paragraphs, and more, all anchored in reliable fact-checking sources.")
st.markdown(":blue[What and How Dashboard]")
st.write("Understand the thematic intricacies of misinformation, focusing on political, religious, and health themes, further distilled into insightful sub-categories.")
st.markdown(":blue[Where Dashboard]")
st.write("Locate the geographical epicenters of misinformation and familiarize yourself with how they are spread across platforms you love.")
st.markdown(":blue[AI Co-pilot]")
st.write("Further, our unique AI Co-pilot stands ready to assist in debunking and understanding misinformation with domain-specific wisdom from 20 personas. Begin your exploration, and gain a panoramic yet detailed view of the misinformation around you.")

st.subheader("Limitations and Word of Caution")
st.write("1. The public servers we use might sometimes get overwhelmed by the number of people accessing them. Please be patient.")
st.write("2. Our classifiers are a work in progress and sometimes might miscategorize the entities or general theme of the misinformation article. We are working on them.")
st.write("3. Please do not share this link beyond the evaluation panel or early testers. We do not currently have resources for servers and APIs to accommodate a large number of visitors.")
st.write("4. Our AI co-pilot is an experiment in understanding the role large language models can play in debunking misinformation. We are using this opportunity to look at safety risks, algorithmic biases, and model selection at this point. If you see a consistent pattern of failure, please send a screenshot to team@dignityindifference.org.")

st.subheader("In the background")
st.write("We have collected a corpus of a constantly updated data-lake through an IFCN member in India. Our algorithms then used cutting-edge natural language processing techniques to curate and expand the dataset. Our on-server algorithms allow an exploratory analysis of these datasets. In parallel, we are using capabilities of cutting edge large language models in helping build narratives against online misinformation.")

st.subheader("In near future")
st.write("1. Expanding the data-lake to multiple IFCN(International Fact-Checking Network) members across South Asia and including 10 most spoken languages in the region.")
st.write("2. Increase accuracy of our classifiers across languages and build a training dataset for Named Entity Recognition based on the current data-lake.")
st.write("3. Provide functionality for thick-big data gathering and analysis around misinformation on inputs provided by youth influencers.")

st.subheader("Team")
st.write("Dridhata, Hameeda, and Himanshu")
