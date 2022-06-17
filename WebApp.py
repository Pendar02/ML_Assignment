# ---- Import Libraries ----
import streamlit as st
import pickle
import numpy as np
import requests
from streamlit_lottie import st_lottie

# ---- Session States ----
if 'page' not in st.session_state:
    st.session_state.page = 0

if 'num' not in st.session_state:
    st.session_state.num = 0

if 'answers' not in st.session_state:
    st.session_state.answers = []

# ---- Page Configuration ----
st.set_page_config(page_title = "x", page_icon = ":sparkles:", layout = "wide")

# ---- Load Lottie Files ----
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottiFiles = [
    load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_czj9tlje.json'),
    load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_tijmpky4.json'),
    load_lottieurl('https://assets8.lottiefiles.com/packages/lf20_ibbakwps.json'),
    load_lottieurl('https://assets6.lottiefiles.com/private_files/lf30_of3skn6w.json'),
    load_lottieurl('https://assets1.lottiefiles.com/packages/lf20_1ef7g2lw.json'),
    load_lottieurl('https://assets10.lottiefiles.com/packages/lf20_fvybxiki.json'),
]

# ---- Load Model ----
model = pickle.load(open("model.sav", 'rb'))

# ---- Test assets ----
choices = [
    ['Not at all','Several days','More than half the days','Nearly every day'],
    ['Not difficult at all','Somewhat difficult','Very difficult','Extremly difficult'],
    ]

questions = [
    "Are you have a little interest or pleasure in doing things?",
    "Are you feeling down, depressed or hopeless?",
    "Are you have trouble falling or staying asleep, or sleeping too much?",
    "Are you feeling tired or having little energy?",
    "Are you poor appetite, weight loss or overeating?",
    "Are you feeling bad about yourself - or that you are a failure or have let yourself or your family down?",
    "Are you have trouble to concentrating in things? - such as reading the newspaper or watching television.",
    "Are you feeling slowed down when you are talking to others?",
    "Are you that you would be better off dead, or of hurting yourself?",
    "If you've had any days with issues above, how difficult have these problems made it for you at work, home, school, or with other people?",    
    ]

results = {
    0: [
        "Your Depression test result : No Depression",
        "you are not experiencing many of the symptoms seen in depression. However,it is recommended to ask for help if you have any concerns about your health or mood",
        "You can check out the links below to help you feel better!",
    ],
    1:[
        'Your Depression test result : Mild Depression',
        "Some common mild depression symptoms are: hopelessness, difficulties concentrating at work, a lack of motivation, appetite changes and weight changes",
        "Mild depression is noticeable but it’s the most difficult to diagnose, therefore, it’s easy to dismiss the symptoms and avoid discussing them with a doctor. However, mild depression is the easiest to treat! We suggest some certain lifestyle changes: exercising daily, adhering to a sleep schedule, eating a balanced diet rich in fruits and vegetables, practicing yoga or meditation, doing activities that reduce stress, such as journaling, reading, or listening to music",
    ],
    2:[
        'Your Depression test result : Moderate Depression',
        "Moderate and mild depression share similar symptoms: problems with self-esteem, reduced productivity, feelings of worthlessness, increased sensitivities, excessive worrying",
        "Moderate depression is easier to diagnose than mild cases because the symptoms significantly impact your daily life. The key to a diagnosis, though, is to make sure you talk to your doctor about the symptoms you’re experiencing. SSRIs, such as sertraline (Zoloft) or paroxetine (Paxil), may be prescribed. These medications can take up to six weeks to take full effect. Cognitive behavioral therapy (CBT) is also used in some cases of moderate depression.", 
    ],
    3:[
        'Your Depression test result : Moderately severe Depression',
        "Moderately severe depression is very common and very treatable. Some of the symptoms are: low mood and irritability most days as well as a loss of interest or enjoyment in activities that were previously enjoyed",
        "It is strongly recommended that you work with your doctor to develop a treatment plan that’s personalized to fit your needs. Talk to your doctor about whether medication for depression is right for you. They can help you develop a treatment plan based on your individual needs and preferences. ",
    ],
    4:[
        'Your Depression test result : Severe Depression',
        "Diagnosis is especially crucial in severe depression, and it may even be time-sensitive. Severe forms of depression may cause delusions, feelings of stupor, hallucinations, suicidal thoughts or behaviors",
        "Severe depression requires medical treatment as soon as possible. Your doctor will likely recommend an SSRI and some form of talk therapy. If you’re experiencing suicidal thoughts or behaviors, you should seek immediate medical attention. Call your local emergency services right away",
    ],
}

# ---- Placeholder of page ----
placeholder = st.empty()

# ---- Landing page ----
def landingPage():
    st.subheader("Hi, we are QWERT! :wave:")
    st.write("We are a group of students from Faculty of Computer Science, University Malaya. We are presenting Machine Learning Project for our course")
    st.write("---")
    st.title("Depression Test")

    # Defining columns
    col1, col2 = st.columns((2,1))
    
    with col1:
        st.text("")
        st.write("This depression quiz is based on the Depression Screening Test developed by Ivan K. Goldberg, MD, the founder of Psycom who was also a renowned psychiatrist.")    
        #Take test Button
        if st.button("Take the Test"):
            st.session_state.page = 1 #Session state to refresh page
            placeholder.empty()

    with col2:
        st_lottie(lottiFiles[5], height=250, key="landing")

# ---- Test page ----
def testPage():
    #Loop for all questions
    for q in questions:
        placeholder = st.empty()
        i = st.session_state.num
        with placeholder.form(key=str(i)):
            ans = st.radio(questions[i], key= i+1, options= choices[0] if i<9 else choices[1])       
                      
            if st.form_submit_button("Next" if i<9 else "Finish"):
                st.session_state.answers.append(choices[0].index(ans) if i<9 else choices[1].index(ans))
                #go to next question
                st.session_state.num += 1
                if st.session_state.num >= 10:
                    #end the test
                    placeholder.empty()
                    break
                placeholder.empty()
            else:
                st.stop()
    
    #ML
    #convert to 2d numpy array for model input
    arr = np.array([st.session_state.answers])
    #take the prediction from model
    result = model.predict(arr)
    #get the description for results
    outcome = results.get(result[0])[0]
    symptom = results.get(result[0])[1]
    note = results.get(result[0])[2]

    #Result layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Outcome")
        st.write("---")
        st.write("-" +outcome)
        st.text(" ")
        st_lottie(lottiFiles[int(result[0])], height=300, key="depression")

    with col2:
        st.header("Symptom")
        st.write("---")
        st.write("-" + symptom)

    with col3:
        st.header("Note")
        st.write("---")
        st.write("-" +note)
        if(int(result[0]==0)):
            st.write("- Check out this [link](https://www.nhs.uk/mental-health/self-help/tips-and-support/how-to-be-happier/)!")
            st.write("- Check out this [link](https://www.amazon.com/Happy-Mind-Life-Simple-Great-ebook/dp/B09KZNFNT1)!")

       

# ---- Running the Application ----
landingPage() if st.session_state.page == 0 else testPage()