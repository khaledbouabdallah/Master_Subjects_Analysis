import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import regex as re

SPACES = '&nbsp;' * 10


def load_page(df: pd.DataFrame) -> None:
    """ The Data Exploration Page
    Parameters:
    -----------

    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of proposed thesis subjects
    """

    prepare_layout()
    # general_information(df)
    did_every_proposed_topic_get_chosen_by_a_student(df)
    did_all_teachers_propose_the_same_number_of_topics(df)
    do_teachers_grades_have_any_impact_on_the_number_of_topics_proposed(df)
    did_teachers_from_other_departments_propose_a_topic(df)
    what_is_the_most_prioritized_specialty(df)


def prepare_layout() -> None:
    """ Prepare the text of the page at the top """
    st.title("💘 General Statistics")
    st.write("This page contains basic exploratory data analyses for the purpose of getting a general "
             "feeling of what the data contains. ".format(SPACES))
    st.markdown("There are several questions that this page tries to answer:".format(SPACES))
    st.markdown("{}🔹 Did every proposed topic get chosen by a student? ".format(SPACES))
    st.markdown("{}🔹 Did all teachers propose the same number of topics? ".format(SPACES))
    st.markdown("{}🔹 Do teachers' grades have any impact on the number of topics proposed? ".format(SPACES))
    st.markdown("{}🔹 Did teachers from other departments propose a topic? ".format(SPACES))
    st.markdown("{}🔹 What is the most prioritized specialty? ".format(SPACES))
    st.write(" ")


def general_information(df: pd.DataFrame) -> None:
    """
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The data to be used for the analyses of proposed thesis subjects
    """
    number_of_topics = len(df.index)
    number_of_teachers = len(df['Teacher'].unique())

    st.header("General Information")
    st.markdown(f"In total ___{number_of_topics}___ topic got proposed by ___{number_of_teachers}___ teacher.")


def did_every_proposed_topic_get_chosen_by_a_student(df: pd.DataFrame) -> None:
    """
        Parameters
        ----------
        df : pandas.core.frame.DataFrame
            The data to be used for the analyses of proposed thesis subjects
    """
    number_of_topics = len(df.index)
    number_of_topics_taken = df['Taken'].value_counts()[1]
    number_of_topics_not_taken = number_of_topics - number_of_topics_taken
    percentage_of_taken = round(number_of_topics_taken / number_of_topics * 100)
    percentage_of_not_taken = round(number_of_topics_not_taken / number_of_topics * 100)
    st.subheader("Did every proposed topic get chosen by a student?")
    st.markdown(f"From ___{number_of_topics}___ proposed topic, only ___{number_of_topics_taken}___ got chosen"
                f" and ___{number_of_topics_not_taken}___ were left.")
    source = pd.DataFrame(
        {"category": [f"taken {percentage_of_taken}%", f"not taken {percentage_of_not_taken}%"],
         "value": [number_of_topics_taken, number_of_topics_not_taken]}
    )
    base = alt.Chart(source, width=400, height=400).encode(
        theta=alt.Theta("value:Q", stack=True), color=alt.Color("category:N", legend=None)
    )
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=140, size=20).encode(text="category:N")
    st.write(pie + text)


def did_all_teachers_propose_the_same_number_of_topics(df: pd.DataFrame) -> None:
    """
            Parameters
            ----------
            df : pandas.core.frame.DataFrame
                The data to be used for the analyses of proposed thesis subjects
    """
    number_of_teachers = len(df['Teacher'].unique())
    st.subheader("Did all teachers propose the same number of topics?")
    grade_number_of_proposed = df['Teacher'].value_counts().to_frame().reset_index()
    number_of_teachers_proposed_more_3_or_more = len(
        grade_number_of_proposed[grade_number_of_proposed['Teacher'] >= 3])
    percentage_of_teachers_proposed_more_3_or_more = round(
        number_of_teachers_proposed_more_3_or_more / number_of_teachers * 100)

    st.write("Below you can see the total number of proposed topics by some of the teachers,")

    bars = alt.Chart(grade_number_of_proposed[:30],
                     height=100 + (20 * len(grade_number_of_proposed[:30])), width=700).mark_bar(
        color='#4db6ac').encode(
        x=alt.X('Teacher:Q', axis=alt.Axis(title='Total topics proposed')),
        y=alt.Y('index:O', axis=alt.Axis(title='Teacher'),
                sort=alt.EncodingSortField(
                    field="Teacher",  # The field to use for the sort
                    order="descending"  # The order to sort in
                )
                )
    )
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Teacher:Q'
    )
    st.write(bars + text)

    st.markdown(
        f"🔹 from ___{number_of_teachers}___ teacher in total, only ___{number_of_teachers_proposed_more_3_or_more}({percentage_of_teachers_proposed_more_3_or_more}%)___ "
        f" proposed 3 topics or more")

    st.markdown(
        f"🔹 On average ___{round(df['Teacher'].value_counts().to_frame().reset_index().Teacher.mean())}___ topic per "
        f"teacher were proposed.")


def do_teachers_grades_have_any_impact_on_the_number_of_topics_proposed(df: pd.DataFrame) -> None:
    """
            Parameters
            ----------
            df : pandas.core.frame.DataFrame
                The data to be used for the analyses of proposed thesis subjects
    """

    def remove_department(string: str) -> str:
        split = re.split('\)', string)
        return split[0].strip()

    df2 = df.copy()
    df2['Grade'] = df['Grade'].apply(remove_department)
    st.subheader("Do teachers' grades have any impact on the number of topics proposed?")
    grade_number_of_proposed = df2['Grade'].value_counts().to_frame().reset_index()
    st.write("Below you can see the total number of proposed topics for every grade")
    bars = alt.Chart(grade_number_of_proposed,
                     height=100 + (20 * len(grade_number_of_proposed)), width=740).mark_bar(
        color='#4db6ac').encode(
        x=alt.X('Grade:Q', axis=alt.Axis(title='Total topics proposed')),
        y=alt.Y('index:O', axis=alt.Axis(title='Grade'),
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
        text='Grade:Q'
    )
    st.write(bars + text)


def did_teachers_from_other_departments_propose_a_topic(df: pd.DataFrame) -> None:
    """
            Parameters
            ----------
            df : pandas.core.frame.DataFrame
                The data to be used for the analyses of proposed thesis subjects
    """
    st.subheader("Did teachers from other departments propose a topic?")

    def get_department_from_string(
            string: str) -> str:  # 'Maitre de conferences -> Hors department: faculty de science'
        # --> 'faculty de science'
        result = re.search(':(.)*', string).group(0)
        return re.sub(':', '', result).strip()  # Remove ':'

    grade_number_of_proposed = df['Grade'].value_counts().to_frame().reset_index()
    outside_our_department = grade_number_of_proposed[grade_number_of_proposed['index'].str.contains('Hors')]
    outside_our_department['index'] = outside_our_department['index'].apply(get_department_from_string)

    bars = alt.Chart(outside_our_department,
                     height=100 + (20 * len(outside_our_department)), width=700).mark_bar(
        color='#4db6ac').encode(
        x=alt.X('Grade:Q', axis=alt.Axis(title='Total topics proposed')),
        y=alt.Y('index:O', axis=alt.Axis(title='Department'),
                sort=alt.EncodingSortField(
                    field="Teacher",  # The field to use for the sort
                    order="descending"  # The order to sort in
                )
                )
    )
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Grade:Q'
    )
    st.write(bars + text)


def what_is_the_most_prioritized_specialty(df: pd.DataFrame) -> None:
    """
            Parameters
            ----------
            df : pandas.core.frame.DataFrame
                The data to be used for the analyses of proposed thesis subjects
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
        for speciality in df['Priority 1'].unique():
            averages[speciality] = 0

        for priority in ['1', '2', '3', '4', '5']:
            counts = df['Priority ' + priority].value_counts()
            for speciality in df['Priority 1'].unique():
                averages[speciality] += counts[speciality] * int(priority)

        for speciality in df['Priority 1'].unique():
            averages[speciality] = round(averages[speciality] / (1 * 2 * 3 * 4 * 5), 2)
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
