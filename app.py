from typing import List, Tuple
import streamlit as st
import pandas as pd

# Custom packages
from lib.preprocessing import prepare_data
import streamlit_page.generalstats as generalstats

FILE_PATH = 'dataset/subjects_master_2022_modefied.csv'

def main():
    path_to_data = ''
    df, exception = load_external_data(FILE_PATH)
    create_layout(df)


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

    exception = False
    try:
        df = prepare_data(path)
        return df, False
    except Exception as exception:
        return False, exception


def load_homepage() -> None:
    """ Create Home page"""

    st.image("images/badge.png",
             use_column_width=True)
    st.markdown("> A Dashboard for the Board Game Geeks among us")
    st.markdown("""
    After the release of the proposed thesis subjects, I was curious, and I had so many questions ... for example:
- Most proposed subject (trending subject)
- Most prioritized specialty in our department
- Percentage of affected/unaffected topics.
- What makes a topic undesirable (Why some topics didn't get chosen)
So to kill my curiosity, I created an Interactive Dashboard to explore the data.
Also, it felt like a nice opportunity to see how much information can be extracted from relatively simple data.
    """)
    st.markdown("You can check the GITHUB repository for more information: [link](https://github.com/khaledbouabdallah/Master_Subjects_Analysis)")
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


def create_layout(df: pd.DataFrame) -> None:
    """ Create the layout after the data has successfully loaded
    Parameters:
    -----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of thesis subjects.
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
        st.markdown("* Coming Soon ")

    elif app_mode == "Speciality Statistics":
        st.markdown("* Coming Soon ")

    elif app_mode == "Subject Statistics":
        st.markdown("* Coming Soon ")



if __name__ == "__main__":
    main()
