import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
from typing import List, Tuple, Dict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from copy import copy

SPACES = '&nbsp;' * 10
SPACES_NO_EMOJI = '&nbsp;' * 15


def load_page(df: pd.DataFrame,
              global_stats: Dict) -> None:
    """ The Teacher Statistics Page
    Parameters:
    -----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of a single Teacher
    teacher_list : list of str
        List of players that participated in the board games
    """
    # Prepare layout
    selected_teacher,selected_year = prepare_layout(global_stats['teacher list'])
    df_teacher = df[df['Teacher']==selected_teacher]
    if selected_year == '2021-2022':
        df_teacher = df_teacher[df_teacher['Academic-year']==selected_year]
    elif selected_year == '2022-2023':
        df_teacher = df_teacher[df_teacher['Academic-year']==selected_year]
        
    # Visualizations
    if not df_teacher.shape[0]:
        st.subheader("Teacher did not propose any subjects 😰")
    else:
        teacher_overview(df=df_teacher, global_stats=global_stats)
        teacher_speciality_priority(df=df_teacher,global_stats=global_stats)
        teacher_word_cloud(df=df_teacher, global_stats=None)
        teacher_list_of_topics(df=df_teacher, global_stats=None)



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

    st.sidebar.subheader("Choose a Teacher")
    
    
    teacher_list = copy(player_list)
    teacher_list.sort()
    selected_player = st.sidebar.selectbox("To show the profile for this player", teacher_list, index=0)
    selected_year = st.sidebar.radio('Select Academic year',('Both Academic years','2022-2023','2021-2022'))
    st.title("👨‍🏫 Teacher Statistics for {}".format(selected_player))
    st.markdown("There are several things you see on this page:".format(SPACES))
    st.markdown("{}🔹 An overview of the teacher".format(SPACES))
    st.markdown("{}🔹 Teacher speciality prioritizing".format(SPACES))
    st.markdown("{}🔹 Teacher subjects word cloud.".format(SPACES))
    st.markdown("{}🔹 List of Proposed topics.".format(SPACES))
    st.write(" ")
    return selected_player,selected_year


def teacher_overview(df: pd.DataFrame, global_stats: Dict) -> None:
    number_of_topics = len(df.index)
    grade = df['Grade'].iloc[0]
    number_of_topics_taken = df['Taken'].value_counts()[0]
    number_of_topics_not_taken = number_of_topics - number_of_topics_taken
    percentage_of_taken = round(number_of_topics_taken / number_of_topics * 100)
    percentage_of_not_taken = round(number_of_topics_not_taken / number_of_topics * 100)
    # Drawing
    st.subheader('Overview:')
    st.metric("Grade", grade,)
    col1, col2= st.columns(2)
    col1.metric("Number of topics", number_of_topics,number_of_topics-global_stats['average publish'])
    col2.metric("Percentage of taken", f'{percentage_of_taken}%', f"{percentage_of_taken-global_stats['percentage of taken']}%")


def teacher_speciality_priority(df: pd.DataFrame, global_stats: Dict) -> None:

    st.subheader('Speciality prioritizing:')
    st.write("You can see how many times each speciality was given a certain priority")
    st.markdown("Or you can visualize the average priority for each speciality (**the lower the better**).")

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
    else: # User did not select average option
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


def teacher_word_cloud(df: pd.DataFrame, global_stats: Dict) -> None:
    st.subheader('Teacher subjects word cloud:')
    st.markdown('The world cloud contains the most common words in the subjects titles proposed by this teacher:')
    text = df['Title'].to_string()

    # Remove French and English stopwords 
    stop_words = set(stopwords.words("french") + stopwords.words("english"))
    
    text = ' '.join([word for word in text.split() if word.lower() not in stop_words])

    # Create a wordcloud object
    wordcloud = WordCloud().generate(text)

    # Show the wordcloud in the app
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    st.pyplot()


def teacher_list_of_topics(df: pd.DataFrame, global_stats: Dict) -> None:
    st.subheader('List of Proposed topics:')
    st.markdown('Full list of proposed topics including other information.')

    df_no_teacher_grade = df.drop(labels=['Teacher', 'Grade'], axis='columns')
    st.table(df_no_teacher_grade)






