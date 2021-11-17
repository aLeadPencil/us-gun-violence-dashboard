import pandas as pd
import numpy as np
from collections import Counter
import plotly.graph_objs as go
from dash import dcc
import sys
sys.path.insert(1, './data')
from data_cleaning_functions import gun_map, column_dtypes, string_to_list #type:ignore


def cleaned_data_reader():
    """
    Read the data into memory and apply a string_to_list() function to convert literal string values
    into lists.
    '[1, 2, 3]' -> [1, 2, 3]

    Parameters:
    -----------
    None

    Returns:
    data: dataframe
    """

    cleaned_data_1 = pd.read_csv('./data/cleaned_data/cleaned_data_1.csv', dtype = column_dtypes)
    cleaned_data_2 = pd.read_csv('./data/cleaned_data/cleaned_data_2.csv', dtype = column_dtypes)
    data = pd.concat([cleaned_data_1, cleaned_data_2], ignore_index = True)

    data['participant_age'] = data['participant_age'].apply(string_to_list)
    data['participant_status'] = data['participant_status'].apply(string_to_list)
    data['participant_type'] = data['participant_type'].apply(string_to_list)
    data['gun_type'] = data['gun_type'].apply(string_to_list)
    data['participant_gender'] = data['participant_gender'].apply(string_to_list)

    return data


# Heatmap for incidents across the US -----------------------------------#
def heatmap_generator(data):
    """
    Generate heatmap graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    incident_heatmap: dcc.Graph
    """

    states_incidents_sum = pd.DataFrame(data.groupby(['state_code'])['date'].count())
    states_incidents_sum = states_incidents_sum.sort_values(by = 'date', ascending = False)
    states_incidents_sum = states_incidents_sum.reset_index()
    states_incidents_sum.columns = ['state_code', 'counts']


    trace1 = go.Choropleth(
        locations = states_incidents_sum['state_code'],
        z = states_incidents_sum['counts'],
        locationmode = 'USA-states',
        colorbar_title = 'Counts',
        colorscale = 'Blues'
    )

    incident_heatmap = dcc.Graph(
        style = {'height': '55vh'},
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Heatmap of Incidents',
                geo_scope = 'usa',
            )
        }
    )

    return incident_heatmap


# Barchart for top dangerous states -----------------------------------#
def top_states_generator(data):
    """
    Generate top states graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    top_states: dcc.Graph
    """
    
    data['n_injured+killed'] = data['n_killed'] + data['n_injured']
    top_10_states = data['state'].value_counts()[:10].index.tolist()
    dangerous_states = data[data['state'].isin(top_10_states)]

    states_counts = dangerous_states.groupby('state')['n_injured+killed'].sum()
    states_counts = states_counts.sort_values(ascending = False)
    states_n_injured = dangerous_states.groupby('state')['n_injured'].sum().sort_values(ascending = False)
    states_n_killed = dangerous_states.groupby('state')['n_killed'].sum().sort_values(ascending = False)


    trace1 = go.Bar(
        x = states_counts.index.tolist(),
        y = states_counts.tolist(),
        name = 'Total'
    )

    trace2 = go.Bar(
        x = states_n_injured.index.tolist(),
        y = states_n_injured,
        name = 'Injured'
    )

    trace3 = go.Bar(
        x = states_n_killed.index.tolist(),
        y = states_n_killed,
        name = 'Killed'
    )

    top_states = dcc.Graph(
        style = {'height': '27.5vh'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Top 10 Dangerous States',
                xaxis = {'title': 'States'},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return top_states


# Barchart for top dangerous cities/counties --------------------------#
def top_cities_generator(data):
    """
    Generate top cities graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    top_cities: dcc.Graph
    """
    
    data['n_injured+killed'] = data['n_killed'] + data['n_injured']
    top_10_cities = data['city_or_county'].value_counts()[:10].index.tolist()
    dangerous_cities = data[data['city_or_county'].isin(top_10_cities)]

    cities_counts = dangerous_cities.groupby('city_or_county')['n_injured+killed'].sum()
    cities_counts = cities_counts.sort_values(ascending = False)
    cities_n_injured = dangerous_cities.groupby('city_or_county')['n_injured'].sum().sort_values(ascending = False)
    cities_n_killed = dangerous_cities.groupby('city_or_county')['n_killed'].sum().sort_values(ascending = False)


    trace1 = go.Bar(
        x = cities_counts.index.tolist(),
        y = cities_counts.tolist(),
        name = 'Counts'
    )

    trace2 = go.Bar(
        x = cities_n_injured.index.tolist(),
        y = cities_n_injured,
        name = 'Injured'
    )

    trace3 = go.Bar(
        x = cities_n_killed.index.tolist(),
        y = cities_n_killed,
        name = 'Killed'
    )

    top_cities = dcc.Graph(
        style = {'height': '27.5vh'},
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Top 10 Dangerous Cities/Counties',
                xaxis = {'title': 'Cities/Counties'},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return top_cities


# Barchart for average incidents per weekday --------------------------#
def incidents_per_day_generator(data):
    """
    Generate incidents per day graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    incidents_per_day: dcc.Graph
    """
    
    weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    day_counts = data['weekday'].value_counts()[weekdays].tolist()
    averages = [element/4 for element in day_counts]


    trace1 = go.Bar(
        orientation='h',
        x = averages,
        y = weekdays,
        name = 'Avg'
    )

    trace2 = go.Bar(
        orientation='h',
        x = day_counts,
        y = weekdays,
        name = 'Total',
        visible = 'legendonly'
    )

    incidents_per_day = dcc.Graph(
        figure = {
            'data': [trace1, trace2],
            'layout': go.Layout(
                title = 'Avg+Total Incidents Per Day',
                xaxis = {'title': 'Counts'},
                yaxis = {'title': 'Day'},
            )
        }
    )

    return incidents_per_day


# Barchart for incidents per month ------------------------------------#
def incidents_per_month_generator(data):
    """
    Generate incidents per month graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    incidents_per_month: dcc.Graph
    """

    month_counts_total = Counter(data['month'])
    month_counts_2014 = Counter(data[data['year'] == 2014]['month'])
    month_counts_2015 = Counter(data[data['year'] == 2014]['month'])
    month_counts_2016 = Counter(data[data['year'] == 2016]['month'])
    month_counts_2017 = Counter(data[data['year'] == 2017]['month'])

    months = list(month_counts_total)
    counts = list(month_counts_total.values())

    incident_counts_by_month = pd.DataFrame(
        {
            'months': months,
            'counts': counts
        }
    )


    trace1 = go.Bar(
        orientation='h',
        x = incident_counts_by_month['counts'],
        y = months,
        name = 'Total'
    )

    trace2 = go.Bar(
        orientation='h',
        x = list(month_counts_2014.values()),
        y = months,
        name = 2014,
        visible = 'legendonly'
    )

    trace3 = go.Bar(
        orientation='h',
        x = list(month_counts_2015.values()),
        y = months,
        name = 2015,
        visible = 'legendonly'
    )

    trace4 = go.Bar(
        orientation='h',
        x = list(month_counts_2016.values()),
        y = months,
        name = 2016,
        visible = 'legendonly'
    )

    trace5 = go.Bar(
        orientation='h',
        x = list(month_counts_2017.values()),
        y = months,
        name = 2017,
        visible = 'legendonly'
    )

    incidents_per_month = dcc.Graph(
        figure = {
            'data': [trace1, trace2, trace3, trace4, trace5],
            'layout': go.Layout(
                title = 'Incident Counts Per Month',
                xaxis = {'title': 'Counts'},
                yaxis = {'title': 'Month'},
            )
        }
    )

    return incidents_per_month


# Barchart for incidents per year -------------------------------------#
def incidents_per_year_generator(data):
    """
    Generate incidents per year graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    incidents_per_year: dcc.Graph
    """

    data['n_injured+killed'] = data['n_injured'] + data['n_killed']
    casualties_by_year = data[['year', 'n_killed', 'n_injured']].groupby('year').sum()
    data = data.groupby('year')['n_injured+killed'].sum().reset_index()

    trace1 = go.Bar(
        orientation='h',
        x = data['n_injured+killed'],
        y = data['year'],
        name = 'Total',
    )

    trace2 = go.Bar(
        orientation='h',
        x = casualties_by_year['n_injured'],
        y = casualties_by_year.index.tolist(),
        name = 'Injured',
    )

    trace3 = go.Bar(
        orientation='h',
        x = casualties_by_year['n_killed'],
        y = casualties_by_year.index.tolist(),
        name = 'Killed'
    )

    incidents_per_year = dcc.Graph(
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Incident Counts Per Year',
                xaxis = {'title': 'Counts'},
                yaxis = {'title': 'Year'},
            )
        }
    )

    return incidents_per_year


# Line plot for age distributions -------------------------------------#
def age_distribution_generator(data):
    """
    Generate age distribution graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    age_distribution: dcc.Graph
    """
    
    ages = data['participant_age'].tolist()
    types = data['participant_type'].tolist()
    age_list = []

    for idx, _ in enumerate(ages):
        if isinstance(ages[idx], list):
            for idx2, _ in enumerate(ages[idx]):
                age_list.append(ages[idx][idx2])

    age_list = list(map(int, age_list))
    unique_ages = list(sorted(set(age_list)))
    ages_count = [0] * len(unique_ages)

    for idx, _ in enumerate(age_list):
        for idx2, _ in enumerate(unique_ages):
            if unique_ages[idx2] == age_list[idx]:
                ages_count[idx2] += 1


    victim_age_list = []
    suspect_age_list = []

    for idx, _ in enumerate(ages):
        if ages[idx] is not np.nan:
            for idx2, _ in enumerate(ages[idx]):
                if 'Victim' in types[idx][idx2] and ages[idx][idx2] is not np.nan:
                    victim_age_list.append(ages[idx][idx2])

                elif 'Suspect' in types[idx][idx2] and ages[idx][idx2] is not np.nan:
                    suspect_age_list.append(ages[idx][idx2])

    victim_age_list = list(map(int, victim_age_list))
    victim_unique_ages = list(sorted(set(victim_age_list)))
    victim_ages_count = [0] * len(victim_unique_ages)

    suspect_age_list = list(map(int, suspect_age_list))
    suspect_unique_ages = list(sorted(set(suspect_age_list)))
    suspect_ages_count = [0] * len(suspect_unique_ages)


    for idx, _ in enumerate(victim_age_list):
        for idx2, _ in enumerate(victim_unique_ages):
            if victim_unique_ages[idx2] == victim_age_list[idx]:
                victim_ages_count[idx2] += 1

    for idx, _ in enumerate(suspect_age_list):
        for idx2, _ in enumerate(suspect_unique_ages):
            if suspect_unique_ages[idx2] == suspect_age_list[idx]:
                suspect_ages_count[idx2] += 1
                

    trace1 = go.Scatter(
        x = unique_ages,
        y = ages_count,
        mode = 'lines',
        name = 'All Participants'
    )

    trace2 = go.Scatter(
        x = victim_unique_ages,
        y = victim_ages_count,
        mode = 'lines',
        name = 'Victims'
    )

    trace3 = go.Scatter(
        x = suspect_unique_ages,
        y = suspect_ages_count,
        mode = 'lines',
        name = 'Suspects'
    )

    age_distribution = dcc.Graph(
        className = 'age-distribution',
        figure = {
            'data': [trace1, trace2, trace3],
            'layout': go.Layout(
                title = 'Age Distribution of People Involved',
                xaxis = {'title': 'Ages', 'range': [0, 100]},
                yaxis = {'title': 'Counts'}
            )
        }
    )

    return age_distribution


# Pie chart for gun type distribution ---------------------------------#
def gun_type_distribution_generator(data):
    """
    Generate gun type distribution graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    gun_type_distribution: dcc.Graph
    """
    
    gun_list = []
    gun_types = data['gun_type'].tolist()

    for idx, _ in enumerate(gun_types):
        if gun_types[idx] is not np.nan:
            for idx2, _ in enumerate(gun_types[idx]):
                if gun_types[idx][idx2] is not np.nan:
                    gun_list.append(gun_types[idx][idx2])
                    
    unique_guns = list(set(gun_list))
    gun_counts = [0] * len(unique_guns)

    for idx, _ in enumerate(gun_list):
        for idx2, _ in enumerate(unique_guns):
            if unique_guns[idx2] == gun_list[idx]:
                gun_counts[idx2] += 1

    temp_gun_type = pd.DataFrame(
        {
            'gun_list': gun_list
        }
    )

    temp_gun_type['gun_list'] = temp_gun_type['gun_list'].map(gun_map)
    gun_type_cleaned_labels = temp_gun_type['gun_list'].value_counts().index.tolist()
    gun_type_cleaned_counts = temp_gun_type['gun_list'].value_counts()


    trace1 = go.Pie(
        labels = gun_type_cleaned_labels,
        values = gun_type_cleaned_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value',
    )

    gun_type_distribution = dcc.Graph(
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Distribution of Gun Types'
            )
        }
    )

    return gun_type_distribution


# Pie chart for gun counts distribution -------------------------------#
def gun_count_distribution_generator(data):
    """
    Generate gun count distribution graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    gun_count_distribution: dcc.Graph
    """

    data_n_guns_drop = data[['n_guns_involved']].dropna().reset_index(drop = True)
    data_n_guns_drop = data_n_guns_drop['n_guns_involved'].tolist()
    data_n_guns_drop = list(map(float, data_n_guns_drop))

    for idx, _ in enumerate(data_n_guns_drop):
        if data_n_guns_drop[idx] >= 5:
            data_n_guns_drop[idx] = '5+'


    n_guns = pd.DataFrame(
        {
            'n_guns_involved': data_n_guns_drop
        }
    )

    n_guns_labels = [1.0, 2.0, 3.0, 4.0, '5+']
    n_guns_counts = n_guns.value_counts()[n_guns_labels].tolist()


    trace1 = go.Pie(
        labels = n_guns_labels,
        values = n_guns_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value',
        sort = False
    )


    gun_count_distribution = dcc.Graph(
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Gun Counts Per Incident'
            )
        }
    )

    return gun_count_distribution


# Pie chart of gender distribution for suspects -----------------------#
def suspect_gender_distribution_generator(data):
    """
    Generate suspect gender distribution graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    suspect_gender_distribution: dcc.Graph
    """

    genders = data['participant_gender'].tolist()
    types = data['participant_type'].tolist()
    suspect_gender_list = []

    for idx, _ in enumerate(genders):
        if isinstance(genders[idx], list):
            for idx2, _ in enumerate(genders[idx]):
                try:
                    if 'Suspect' in types[idx][idx2]:
                        suspect_gender_list.append(genders[idx][idx2])
                except:
                    pass
                    
    gender_labels = ['Male', 'Female']
    suspect_gender_counts = [suspect_gender_list.count('Male'), suspect_gender_list.count('Female')]


    trace1 = go.Pie(
        labels = gender_labels,
        values = suspect_gender_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value'
    )

    suspect_gender_distribution = dcc.Graph(
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Suspect Gender Distribution'
            )
        }
    )

    return suspect_gender_distribution


# Pie chart of gender distribution for victims ------------------------#
def victim_gender_distribution_generator(data):
    """
    Generate victim gender distribution graph

    Parameters:
    -----------
    data: dataframe

    Returns:
    victim_gender_distribution: dcc.Graph
    """

    genders = data['participant_gender'].tolist()
    types = data['participant_type'].tolist()
    victim_gender_list = []

    for idx, _ in enumerate(genders):
        if isinstance(genders[idx], list):
            for idx2, _ in enumerate(genders[idx]):
                try:
                    if 'Victim' in types[idx][idx2]:
                        victim_gender_list.append(genders[idx][idx2])
                except:
                    pass
                
    gender_labels = ['Male', 'Female']
    victim_gender_counts = [victim_gender_list.count('Male'), victim_gender_list.count('Female')]


    trace1 = go.Pie(
        labels = gender_labels,
        values = victim_gender_counts,
        hoverinfo = 'label+percent',
        textinfo = 'value'
    )

    victim_gender_distribution = dcc.Graph(
        figure = {
            'data': [trace1],
            'layout': go.Layout(
                title = 'Victim Gender Distribution'
            )
        }
    )

    return victim_gender_distribution


if __name__ == '__main__':
    print('This is the dashboard functions file')