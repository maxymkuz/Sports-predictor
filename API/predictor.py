import pandas as pd
# Tools for machine learning
import pickle
import time
import xgboost as xgb
from sklearn.model_selection import train_test_split

matches = pd.read_csv('data/seasons_merged.csv')
letter_to_result = {'H': 1, 'D': 0, 'A': -1}


def get_n_last_matches(matches, date, team, n=10):
    '''
    Get the last n matches of a given team.
    '''

    # All matches with a given team
    team_matches = matches[(matches['HomeTeam'] == team) | (matches['AwayTeam'] == team)]

    # Filter n last matches from team matches
    n_last_matches = (team_matches[team_matches.Date < date]
                          .sort_values(by='Date', ascending=False)
                          .iloc[0:n, :])

    return n_last_matches


def get_n_last_matches_against_each_other(matches, date, home_team, away_team, n=5):
    '''
    Get the last n matches of two given teams. If possible, else
    get all matches available
    '''

    home_matches = matches[(matches['HomeTeam'] == home_team) & (matches['AwayTeam'] == away_team)]
    away_matches = matches[(matches['HomeTeam'] == away_team) & (matches['AwayTeam'] == home_team)]
    total_matches = pd.concat([home_matches, away_matches])

    # Get last n matches, if possible:
    try:
        last_matches = (total_matches[total_matches.Date < date]
                            .sort_values(by='Date', ascending=False)
                            .iloc[0:n, :])
    except:  # If there are less than n matches
        last_matches = (total_matches[total_matches.Date < date]
                            .sort_values(by='Date', ascending=False)
                            .iloc[0:total_matches.shape[0], :])

    return last_matches


def get_goals(matches, team):
    '''
    Get total number of goals,a specfic team has scored
    from a dataframe of specific matches
    '''
    home_goals = matches.FTHG[matches.HomeTeam == team].sum()
    away_goals = matches.FTAG[matches.AwayTeam == team].sum()

    return home_goals + away_goals


def get_concealed_goals(matches, team):
    '''
    Get all the goals, concealed of a specfic team from a dataframe of specific matches
    '''
    home_goals = matches.FTAG[matches.HomeTeam == team].sum()
    away_goals = matches.FTHG[matches.AwayTeam == team].sum()

    return home_goals + away_goals


def get_wins(matches, team):
    '''
    Get the number of wins of a specfic team from a dataframe of specific matches.
    '''
    home_wins = matches[(matches.FTR == 1) & (matches.HomeTeam == team)].shape[0]
    away_wins = matches[(matches.FTR == -1) & (matches.AwayTeam == team)].shape[0]

    return home_wins + away_wins


def coefficients_to_probability(matches):
    '''
    Converts betting platform coefficient(1 < x) with % of income
    into a probability coefficient(0 < x < 1)
    '''
    # How many profit betting companies make on bets
    matches['profit_B365'] = sum((1 / matches['B365H'], 1 / matches['B365D'], 1 / matches['B365A']))
    matches['profit_BbAv'] = sum((1 / matches['BbAvA'], 1 / matches['BbAvD'], 1 / matches['BbAvH']))

    # Converting all betting coefficients into probabilities of homw/draw/away:
    for betting_column in ['B365H', 'B365D', 'B365A', 'BbAvH', 'BbAvD', 'BbAvA']:
        matches[betting_column] = 1 / (matches[betting_column] * matches['profit_' + betting_column[:-1]])

    return matches


# Create features, based on which, the model would train and predict results

def get_features_for_match(match, matches, n1=10, n2=3):
    '''
    Creates a special set of features for each match, if possible(10 last matches
    and 3 last matches against each other)
    '''
    match_date = match.Date
    home_team = match.HomeTeam
    away_team = match.AwayTeam

    # Get n1 last matches of 2 teams
    home_last = get_n_last_matches(matches, match_date, home_team, n=n1)
    away_last = get_n_last_matches(matches, match_date, away_team, n=n1)
    # Get last n2 matches against each other
    home_last_against = get_n_last_matches_against_each_other(matches, match_date, home_team, away_team, n=n2)
    away_last_against = get_n_last_matches_against_each_other(matches, match_date, away_team, home_team, n=n2)
    # Goals stuff
    home_goals = get_goals(home_last, home_team)
    away_goals = get_goals(away_last, away_team)
    home_goals_conceided = get_concealed_goals(home_last, home_team)
    away_goals_conceided = get_concealed_goals(away_last, away_team)

    res = pd.DataFrame()
    res.loc[0, 'H_goal_diff'] = home_goals - home_goals_conceided
    res.loc[0, 'A_goal_diff'] = away_goals - away_goals_conceided
    res.loc[0, 'H_win'] = get_wins(home_last, home_team)
    res.loc[0, 'A_win'] = get_wins(away_last, away_team)
    res.loc[0, 'H_win_against'] = get_wins(home_last_against, home_team)
    res.loc[0, 'A_win_against'] = get_wins(away_last_against, away_team)
    # TODO ПОПРООБУВАТИ ЩЕ ЯКІСЬ КРИТЕРІЇ ПОТЕСТУВАТИ
    #     print(result.loc[0])
    return res.loc[0]


teams = ['Arsenal',
         'Aston Villa',
         'Bournemouth',
         'Brighton',
         'Burnley',
         'Chelsea',
         'Crystal Palace',
         'Everton',
         'Leicester',
         'Liverpool',
         'Man City',
         'Man United',
         'Newcastle',
         'Southampton',
         'Tottenham',
         'Watford',
         'West Ham',
         'Wolves']


def save_to_cache():
    """
    Saves the current standings into cache, so that you
    don't have to compute them every time
    """
    arr = []
    for hometeam in teams:
        for awayteam in teams:
            if hometeam == awayteam:
                continue
            # Creating a new match
            match = pd.DataFrame(data={'Date': ['2020-07-22'],
                                       'HomeTeam': [hometeam],
                                       'AwayTeam': [awayteam], },
                                 columns=['Date', 'HomeTeam',
                                          'AwayTeam'])

            # Creating features for a given match
            match_features = get_features_for_match(match.iloc[0],
                                                    matches, 20, 3)
            df = pd.DataFrame(data={'Unnamed: 0': [3333]},
                              columns=['Unnamed: 0'])
            # Filling a dataframe with features, needed for an analysis
            for i in match_features.to_frame().reset_index()['index']:
                df[i] = match_features[i]
            # Using a model to predict an outcome, returns an array
            df = df.drop(['Unnamed: 0'], axis=1)
            home_win, draw, away_win = clf_boosted.predict_proba(df)[0]
            arr.append(','.join((hometeam, awayteam, str(home_win), str(draw),
                                                         str(away_win))))


    with open('data/coefficients.txt', 'w') as f:
        f.write('\n'.join(arr))


def get_cached(hometeam, awayteam):
    """
    Uploads the result from the cache, if possible
    """
    with open('data/coefficients.txt', 'r') as f:
        for line in f:
            line = line.strip()
            home_team, away_team, away_win, draw, home_win = line.split(',')
            if hometeam != home_team or awayteam != away_team:
                continue
            home_win = float(home_win)
            away_win = float(away_win)
            draw = float(draw)
            return home_win, draw, away_win


features = pd.read_csv('data/features.csv')
features = features.drop('Unnamed: 0', axis=1)
labels = matches.loc[:, 'HTR']
labels.name = 'label'
labels = labels.iloc[100:]
X_train, X_test, y_train, y_test = train_test_split(features, labels,
                                                    test_size = 100,
                                                    random_state = 2,
                                                    stratify = labels)


clf_boosted = xgb.XGBClassifier(base_score=0.5, colsample_bylevel=1, colsample_bytree=0.8,
       gamma=0.4, learning_rate=0.1, max_delta_step=0, max_depth=3,
       min_child_weight=3, missing=None, n_estimators=40, nthread=-1,
       objective='binary:logistic', reg_alpha=1e-05, reg_lambda=1,
       scale_pos_weight=1, seed=2, silent=True, subsample=0.8)


# Main training of the model
start = time.time()
print('training home model')
clf_boosted.fit(X_train, y_train)