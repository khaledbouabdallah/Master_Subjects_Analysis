from typing import List, Tuple, Dict
import streamlit as st
import pandas as pd
import nltk

# Custom packages
from lib.preprocessing import prepare_data
import streamlit_page.generalstats as generalstats
import streamlit_page.teacherstats as teacherstats

FILE_PATH = 'dataset/subjects_master.csv'



def main():
    df, exception = load_external_data(FILE_PATH)
    glb_stats = global_stats(df)
    create_layout(df, glb_stats)


@st.cache
def load_external_data(path: str) -> Tuple[pd.DataFrame, Exception]:
    """ Load data from a link and preprocess it
    Parameters:
    -----------
    path : str
        Path to the data (should be hosted offline)
    Returns:
    --------
    df : pandas.core.frame.DataFrame | False
        The data loaded and preprocessed.
        If there is an issue loading/preprocessing then it
        returns False instead.
    exception : False | Exception
        If there is something wrong with preprocessing,
        return Exception, otherwise return False
    """

    try:
        df = prepare_data(path)
        return df, False
    except Exception as exception:
        print("failed to load data")
        return False, exception


@st.cache
def global_stats(df: pd.DataFrame) -> Dict:
    """ extract global stats to use it in the pages
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of thesis subjects.
    Returns
    -------
    dictionary in the form 'global_stat_name:value'


    """

    nltk.download('stopwords')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    number_of_topics = df.shape[0]
    number_of_topics_taken = df['Taken'].value_counts()[0]
    number_of_topics_not_taken = number_of_topics - number_of_topics_taken
    percentage_of_taken = round(number_of_topics_taken / number_of_topics * 100)
    # percentage_of_not_taken = round(number_of_topics_not_taken / number_of_topics * 100)
    number_of_teachers = len(df['Teacher'].unique())
    average_publish_number = round(df['Teacher'].value_counts().to_frame().reset_index().Teacher.mean())
    speciality_list = list(df['Priority 1'].unique())

    teacher_list = list(df['Teacher'].unique())
    return {
        'number of topics': number_of_topics,
        'number of topics taken': number_of_topics_taken,
        'percentage of taken': percentage_of_taken,
        'teacher list': teacher_list,
        'average publish': average_publish_number,
        'speciality list': speciality_list,

    }


def load_homepage() -> None:
    """ Create Home page"""

    st.image("images/badge.png",
             use_column_width=True)
    st.markdown("> A Dashboard for Exploratory Data Analysis of proposed Master thesis subjects")
    st.markdown("""
    The following dashboard gives some insights on the subjects proposed for master's thesis. The
Subjects were proposed by teachers so that master students can choose one as their subject.

- Year: 2021-2022 and 2022-2023 school years.
- University: Ferhat Abbas Setif 1.
- Faculty: Faculty of Science.  
- Department: Computer Science.

The dashboard can answer some following questions, among other things:
- What is the most proposed subject?
- What is the most prioritized specialty in our department?
- What is Percentage of affected/unaffected topics?
- Is there a big difference between 2022 and 2023 subjects?
- what kind of subjects that specific teacher likes to propose?
    """)
    st.markdown(
        "You can check the GITHUB repository for more information: [link](https://github.com/khaledbouabdallah/Master_Subjects_Analysis)")

    for i in range(3):
        st.write(" ")
    st.write("There are currently two pages available in the application:")
    st.subheader("📄 General Statistics 📄")
    st.markdown("* This page contains basic exploratory data analyses for the purpose"
                " of getting a general feeling of what the data contains.")
    st.subheader("📄 Teacher Statistics 📄") #TODO: 
    st.markdown("* This page contains additional information about each teacher. ") 


def create_layout(df: pd.DataFrame, glb_stats: Dict) -> None:
    """ Create the layout after the data has successfully loaded
    Parameters:
    -----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of thesis subjects.
    glb_stats: Dict
        dictionary in the form 'global_stat_name:value'
    """

    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Please select a page", ["Homepage",
                                                             "General Statistics",
                                                             "Teacher Statistics",
                                                             ])
    if app_mode == 'Homepage':
        load_homepage()
    elif app_mode == "Instruction":
        body = " ".join(open("files/instructions.md", 'r').readlines())
        st.markdown(body, unsafe_allow_html=True)
    elif app_mode == "General Statistics":
        generalstats.load_page(df)
    elif app_mode == "Teacher Statistics":

        teacherstats.load_page(df, glb_stats)



if __name__ == "__main__":
    main()
