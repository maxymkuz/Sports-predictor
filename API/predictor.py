import pandas as pd

# Tools for machine learning
from sklearn.model_selection import train_test_split
import xgboost as xgb


matches = pd.read_csv('../data/seasons_merged.csv')
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


def create_features(matches):
    '''
    Iterate throu all matches, create features for every single of them
    if possible and aggregate them together
    '''
    print('Generating features... Please wait for one or two minutes')
    # Creates dataframe with features for all matches
    matches_features = matches.apply(lambda x: get_features_for_match(x, matches, n1=12, n2=3), axis=1)
    return matches_features


from time import time


def train_classifier(clf, X_train, y_train):
    ''' Fits a classifier to the training data. '''

    # Start the clock, train the classifier, then stop the clock
    start = time()
    clf.fit(X_train, y_train)
    end = time()

    # Print the results
    print("Trained model in {:.4f} seconds".format(end - start))


def predict_labels(clf, features, target):
    ''' Makes predictions using a fit classifier based on F1 score. '''

    # Start the clock, make predictions, then stop the clock
    start = time()
    y_pred = clf.predict_proba(features)

    end = time()
    # Print and return results
    print("Made predictions in {:.4f} seconds.".format(end - start))
    # f1_score(target, y_pred, pos_label='H'),
    return sum(target == y_pred) / float(len(y_pred))


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Train and predict using a classifer based on F1 score. '''

    # Indicate the classifier and the training set size
    print("Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train)))

    # Train the classifier
    train_classifier(clf, X_train, y_train)

    # Print the results of prediction for both training and testing
    # f1,
    f1 = 'hz'
    acc = predict_labels(clf, X_train, y_train)
    print(f1, acc)
    print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))

    # f1,
    acc = predict_labels(clf, X_test, y_test)
    print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))


import time
time_start = time.time()
features = pd.read_csv('../data/features.csv')
labels = matches.loc[:, 'HTR']
labels.name = 'label'

print('Generated features in', time.time() - time_start, 'sec.')

# Splitting the data into training and test sets:
X_train, X_test, y_train, y_test = train_test_split(features, labels,
                                                    test_size=50,
                                                    random_state=2,
                                                    stratify=labels)

# Classifiers
y_train = y_train.apply(lambda x: letter_to_result[x])

clf_C = xgb.XGBClassifier(seed=82)


clf_C.fit(X_train, y_train)

if __name__ == '__main__':
    # make a prediction
    ynew = clf_C.predict_proba(X_test.iloc[-1:])

    print(ynew[0][0], type(ynew))

