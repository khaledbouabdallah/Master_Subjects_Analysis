from typing import List, Tuple
import streamlit as st
import pandas as pd

# Custom packages
import lib.preprocessing as preprocessing

FILE_PATH = '../dataset/subjects_master_2022_modefied.csv'

def main():
    path_to_data = ''
    df, exception = load_external_data(path_to_data)
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
        df = preprocessing.prepare_data(path)
        return df, False
    except Exception as exception:
        return False, exception


def load_homepage() -> None:
    """ The homepage is loaded using a combination of .write and .markdown.
    Due to some issues with emojis incorrectly loading in markdown st.write was
    used in some cases.
    When this issue is resolved, markdown will be used instead.
    """
    st.image("https://raw.githubusercontent.com/MaartenGr/boardgame/master/images/logo_small.jpg",
             use_column_width=True)
    st.markdown("> A Dashboard for the Board Game Geeks among us")
    st.write("As many Board Game Geeks like myself track the scores of board game matches "
             "I decided to create an application allowing for the exploration of this data. "
             "Moreover, it felt like a nice opportunity to see how much information can be "
             "extracted from relatively simple data.")
    st.write("As a Data Scientist and self-proclaimed Board Game Nerd I obviously made sure to "
             "write down the results of every board game I played. The data in the application "
             "is currently my own, but will be extended to include those of others.")
    st.markdown("<div align='center'><br>"
                "<img src='https://img.shields.io/badge/MADE%20WITH-PYTHON%20-red?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/SERVED%20WITH-Heroku-blue?style=for-the-badge'"
                "alt='API stability' height='25'/>"
                "<img src='https://img.shields.io/badge/DASHBOARDING%20WITH-Streamlit-green?style=for-the-badge'"
                "alt='API stability' height='25'/></div>", unsafe_allow_html=True)
    for i in range(3):
        st.write(" ")
    st.header("🎲 The Application")
    st.write("This application is a Streamlit dashboard hosted on Heroku that can be used to explore "
             "the results from board game matches that I tracked over the last year.")
    st.write("There are currently four pages available in the application:")
    st.subheader("♟ General Statistics ♟")
    st.markdown("* This gives a general overview of the data including frequency of games over time, "
                "most games played in a day, and longest break between games.")
    st.subheader("♟ Player Statistics ♟")
    st.markdown("* As you play with other people it would be interesting to see how they performed. "
                "This page allows you to see, per player, an overview of their performance across games.")
    st.markdown("* This also includes a one-sample Wilcoxon signed-rank test to test if a player performs "
                "significantly better/worse than the average for one board game.")
    st.subheader("♟ Head to Head ♟")
    st.markdown("* I typically play two-player games with my wife and thought it would be nice to include a "
                "head to head page. This page describes who is the better of two players between and within games.")
    st.subheader("♟ Explore Games ♟")
    st.markdown("* This page serves to show statistics per game, like its distribution of scores, frequency of "
                "matches and best/worst players.")


def create_layout(df: pd.DataFrame) -> None:
    """ Create the layout after the data has successfully loaded
    Parameters:
    -----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of thesis subjects.
    """

    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Please select a page", ["Homepage",
                                                             "Data Exploration",
                                                             "Author Statistics",
                                                             "Speciality Statistics",
                                                             "Subject Statistics"])
    if app_mode == 'Homepage':
        load_homepage()
    elif app_mode == "Instruction":
        body = " ".join(open("files/instructions.md", 'r').readlines())
        st.markdown(body, unsafe_allow_html=True)
    elif app_mode == "Data Exploration":
        pass
        # generalstats.load_page(df)
    elif app_mode == "Player Statistics":
        pass
        # playerstats.load_page(df, player_list)
    elif app_mode == "Game Statistics":
        pass
        # exploregames.load_page(df, player_list)
    elif app_mode == "Head to Head":
        pass
        # headtohead.load_page(df, player_list)


if __name__ == "__main__":
    main()
