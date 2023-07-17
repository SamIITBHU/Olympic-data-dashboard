import streamlit as st
import pandas as pd

import helper
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)

st.sidebar.title('Olympic Analysis')
st.sidebar.image('https://l1nk.dev/2giaM')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)

    selected_years = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_years, selected_country)
    if selected_years == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_years == 'Overall' and selected_country != 'Overall':
        st.title('Overall Performance of ' + selected_country)
    if selected_years != 'Overall' and selected_country == 'Overall':
        st.title('Overall Performance in ' + str(selected_years))
    if selected_years != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_years))
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    nations = df['region'].unique().shape[0]
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]

    st.title('Statistics')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Nations Participated')
        st.title(nations)
    with col3:
        st.header('Cities Hosted')
        st.title(cities)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Sports')
        st.title(sports)
    with col2:
        st.header('Events')
        st.title(editions)
    with col3:
        st.header('Athletes Participated')
        st.title(editions)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title('Participating Nations over the Years')
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title('Events over the Years')
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title('Athletes over the Years')
    st.plotly_chart(fig)

    st.title('Events over the time for respective Sports')
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sports_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country-wise Analysis')
    region_list = df['region'].dropna().unique().tolist()
    region_list.sort()

    selected_country = st.sidebar.selectbox('Selected a Country', region_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal tally over the Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' Excels in the Following Sports ')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'Overall')

    st.title('Athlete Height vs Weight Distribution')
    selected_sport = st.selectbox('Select a Sport', sports_list)

    temp_df = helper.weight_v_height(df, selected_sport)
    fig, ax = plt.subplots()
    data = pd.concat([temp_df['Weight'], temp_df['Height']], axis=1)
    ax = sns.scatterplot(data=data, x='Weight', y='Height', hue=temp_df['Medal'], style=temp_df['Sex'], s=60, ax=ax)
    st.pyplot(fig)

    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.title('Men vs Women Participation Over the Years')
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)






