
import numpy as np

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'NOC', 'Medal'])

    temp = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        temp = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if temp == 1:
        a = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index()
    else:
        a = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values(
                by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    a['Total'] = a['Gold'] + a['Silver'] + a['Bronze']

    a['Gold'] = a['Gold'].astype('int')
    a['Silver'] = a['Silver'].astype('int')
    a['Bronze'] = a['Bronze'].astype('int')
    a['Total'] = a['Total'].astype('int')

    return a

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'NOC', 'Medal'])

    medal_tally = medal_tally.groupby('region')[['Gold', 'Silver', 'Bronze']].sum().sort_values(
        by=['Gold', 'Silver', 'Bronze'], ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')


    return medal_tally


def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year, country

def data_over_time(df, col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().sort_index(ascending=True)
    nations_over_time = nations_over_time.rename_axis('Edition').reset_index(name=col)

    return nations_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().rename_axis('Name_x').reset_index(name='Medal_x').merge(df, how='left',
                                                                                               left_on='Name_x',
                                                                                               right_on='Name')[
        ['Name_x', 'Medal_x', 'region', 'Sport']].drop_duplicates('Name_x').head(15)
    x.rename(columns={'Name_x': 'Name', 'Medal_x': 'Medal'}, inplace=True)
    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().rename_axis('Name_x').reset_index(name='Medal_x').merge(df, how='left',
                                                                                               left_on='Name_x',
                                                                                               right_on='Name')[
        ['Name_x', 'Medal_x', 'Sport']].drop_duplicates('Name_x').head(10)
    x.rename(columns={'Name_x': 'Name', 'Medal_x': 'Medal'}, inplace=True)
    return x

def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Sex'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Sex'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Sex_x': 'Male', 'Sex_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final
