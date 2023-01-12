from typing import List, Tuple, Dict
import streamlit as st
import pandas as pd

# Custom packages
from lib.preprocessing import prepare_data
import streamlit_page.generalstats as generalstats
import streamlit_page.teacherstats as teacherstats

FILE_PATH = 'dataset/subjects_master_2022.csv'


def main():
    path_to_data = ''
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
    number_of_topics = len(df.index)
    number_of_topics_taken = df['Taken'].value_counts()[1]
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
    After the release of the proposed thesis subjects, I was curious, and I had so many questions ... for example:
- Most proposed subject (trending subject)
- Most prioritized specialty in our department
- Percentage of affected/unaffected topics.
- What makes a topic undesirable (Why some topics didn't get chosen)
So to kill my curiosity, I created an Interactive Dashboard to explore the data.
Also, it felt like a nice opportunity to see how much information can be extracted from relatively simple data.
    """)
    st.markdown(
        "You can check the GITHUB repository for more information: [link](https://github.com/khaledbouabdallah/Master_Subjects_Analysis)")
    st.markdown("<div align='center'><br>"
                "<img src='https://img.shields.io/badge/MADE%20WITH-PYTHON%20-red?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/SERVED%20WITH-Heroku-blue?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-green?style=for-the-badge'"
                "alt='API stability' height='25'/></div>", unsafe_allow_html=True)
    for i in range(3):
        st.write(" ")
    st.header("📉 The Application 📉")
    st.write("This application is a Streamlit dashboard hosted on Heroku that can be used to explore "
             "the results from board game matches that I tracked over the last year.")
    st.write("There are currently four pages available in the application:")
    st.subheader("📄 General Statistics 📄")
    st.markdown("* This page contains basic exploratory data analyses for the purpose"
                " of getting a general feeling of what the data contains.")
    st.subheader("📄 Teacher Statistics 📄")
    st.markdown("* Coming Soon ")
    st.subheader("📄 Speciality Statistics 📄")
    st.markdown("* Coming Soon ")
    st.subheader("📄 Subject Statistics 📄")
    st.markdown("* Coming Soon ")


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
                                                             "Speciality Statistics",
                                                             "Subject Statistics"])
    if app_mode == 'Homepage':
        load_homepage()
    elif app_mode == "Instruction":
        body = " ".join(open("files/instructions.md", 'r').readlines())
        st.markdown(body, unsafe_allow_html=True)
    elif app_mode == "General Statistics":
        generalstats.load_page(df)
    elif app_mode == "Teacher Statistics":

        teacherstats.load_page(df, glb_stats)

    elif app_mode == "Speciality Statistics":
        st.markdown("* Coming Soon ")

    elif app_mode == "Subject Statistics":
        st.markdown("* Coming Soon ")


if __name__ == "__main__":
    main()
