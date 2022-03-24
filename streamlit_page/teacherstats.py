import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from scipy.stats import wilcoxon
from typing import List, Tuple, Dict

SPACES = '&nbsp;' * 10
SPACES_NO_EMOJI = '&nbsp;' * 15


def load_page(df: pd.DataFrame,
              global_stats: Dict) -> None:
    """ The Teacher Statistics Page

    After filtering for a Teacher, it includes the following sections:
        * Average Score per Game
            * Shows average score for all games played
        * Explore a Game
            * Gives general statistics for a specific game
        * Statistical Difference
            * Checks if there is a significant difference between scores of the user
            for a specific game and the average score
        * Performance
            * This section describes the performance of the player based on how
            frequently this person has won a game.

    Parameters:
    -----------

    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of played board game matches.

    teacher_list : list of str
        List of players that participated in the board games
    """

    # Prepare layout
    selected_teacher = prepare_layout(global_stats['teacher list'])
    df_teacher = df = df[df['Teacher']==selected_teacher]
    # Visualizations
    teacher_overview(df=df_teacher, global_stats=global_stats)
    teacher_speciality_priority(df=df_teacher,global_stats=global_stats)



def prepare_layout(player_list: List[str]) -> str:
    """Prepare selection box, title and empty previous readme


    Parameters:
    -----------

    player_list : list of str
        List of players

    Returns:
    --------

    selected_player : str
    """

    st.sidebar.subheader("Choose a player")
    selected_player = st.sidebar.selectbox("To show the scores for this player", player_list, index=0)
    st.title("🎲 Player Statistics for {}".format(selected_player))
    st.write("Below you can see statistics for a single player. "
             "This can relate to things like min, maximum and average scores "
             "but also how the performance of this person relates to all others he/she "
             "has played against.")

    st.markdown("There are several things you see on this page:".format(SPACES))
    st.markdown("{}🔹 An overview of the **average** scores per game.".format(SPACES))
    st.markdown("{}🔹 An **in-depth** overview of statistics per game.".format(SPACES))
    st.markdown("{}🔹 Whether there is a **significant** difference in scores for a game.".format(SPACES))
    st.markdown("{}🔹 The **performance** of a player across all games.".format(SPACES))
    st.write(" ")
    return selected_player


def teacher_overview(df: pd.DataFrame, global_stats: Dict) -> None:
    """

    Parameters
    ----------

    df
    global_stats

    Returns
    -------

    """
    number_of_topics = len(df.index)
    grade = df['Grade'].iloc[0]
    number_of_topics_taken = df['Taken'].value_counts()[1]
    number_of_topics_not_taken = number_of_topics - number_of_topics_taken
    percentage_of_taken = round(number_of_topics_taken / number_of_topics * 100)
    percentage_of_not_taken = round(number_of_topics_not_taken / number_of_topics * 100)
    st.metric("Grade", grade,)
    col1, col2= st.columns(2)
    col1.metric("Number of topics", number_of_topics,number_of_topics-global_stats['average publish'])
    col2.metric("Percentage of taken", f'{percentage_of_taken}%', f"{percentage_of_taken-global_stats['percentage of taken']}%")
    st.table(df)


def teacher_speciality_priority(df: pd.DataFrame, global_stats: Dict) -> None:
    """

    Parameters
    ----------
    df
    global_stats

    Returns
    -------

    """
    st.subheader('What is the most prioritized specialty?')
    st.write("Each proposed topic have 5 priorities, for example:")
    st.markdown("- A student who belongs to a speciality that have 'Priority 2' have more priority to take that topic "
                "more then students who belong to other speciality's that have priority 3,4 and 5")
    st.markdown("- Below you can chose a priority and see how many times a speciality appeared")
    st.markdown("- Or you can visualize the average priority for each speciality (the lower the better)")

    option = st.selectbox(
        'Priority?',
        ('1', '2', '3', '4', '5', 'average'))

    if option == 'average':
        averages = {}
        for speciality in global_stats['speciality list']:
            averages[speciality] = 0

        for priority in ['1', '2', '3', '4', '5']:
            counts = df['Priority ' + priority].value_counts()
            for speciality in global_stats['speciality list']:
                if speciality in counts:
                    averages[speciality] += counts[speciality] * int(priority)
        for speciality in global_stats['speciality list']:
            averages[speciality] = round(averages[speciality] / len(df.index), 2)
        df3 = pd.Series(averages)
        df3 = df3.to_frame().reset_index()
        df3 = df3.rename(columns={0: 'Average'})
        bars = alt.Chart(df3,
                         height=100 + (20 * len(df3)), width=740).mark_bar(
            color='#4db6ac').encode(
            x=alt.X('Average:Q', axis=alt.Axis(title='Average priority')),
            y=alt.Y('index:O', axis=alt.Axis(title='Speciality'),
                    sort=alt.EncodingSortField(
                        field="Average",  # The field to use for the sort
                        order="descending"  # The order to sort in
                    )
                    )
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=5  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='Average:Q'
        )
        st.write(bars + text)
    else:
        priority_count = df['Priority ' + option].value_counts().to_frame().reset_index()
        bars = alt.Chart(priority_count,
                         height=100 + (20 * len(priority_count)), width=740).mark_bar(
            color='#4db6ac').encode(
            x=alt.X('Priority ' + option + ':Q', axis=alt.Axis(title='Number of topics proposed')),
            y=alt.Y('index:O', axis=alt.Axis(title='Speciality'),
                    sort=alt.EncodingSortField(
                        field="Teacher",  # The field to use for the sort
                        order="descending"  # The order to sort in
                    )
                    )
        )
        text = bars.mark_text(
            align='left',
            baseline='middle',
            dx=5  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='Priority ' + option + ':Q'
        )
        st.write(bars + text)


