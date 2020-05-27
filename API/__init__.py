from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from adt.coefficients_ADT import CoefficientsADT
from API.predictor import get_features_for_match, matches, get_cached
import pandas as pd
import pickle

# Creating an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)

# Loading my already pre-trained model:
clf_boosted = pickle.load(open('models/finalized_home.sav', 'rb'))

# List of EPL teams
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


@app.route("/")
def index():
    """Send basic responce"""
    return """<div><h3>Hey! Here is the list of crrently available 
    teams:</h3> <ul><li>Arsenal</li><li>Aston Villa</li><li>Bournemouth</li>
 <li>Brighton</li><li>Burnley</li><li>Chelsea</li><li>Crystal Palace</li>
 <li>Everton</li><li>Leicester</li><li>Liverpool</li><li>Man City</li>
 <li>Man United</li><li>Newcastle</li><li>Southampton</li><li>Tottenham</li>
 <li>Watford</li><li>West Ham</li><li>Wolves</li></ul> 
<p>Get-request example: <b>http://maxkuz.pythonanywhere.com/Liverpool
/Tottenham/5.0</b></p></div>"""


class TeamCoefficient(Resource):
    def get(self, hometeam, awayteam, profit):
        """
        (str, str, int) -> json
        Analyzes an input, and returns json if input is correct,
        error 404 Not Found else
        """
        # if not in list of available teams
        print(hometeam, awayteam, profit)
        if hometeam not in teams or awayteam not in teams:
            return {"Message": "Teams don't exist"}, 404
        try:
            # If a team exists in a cache
            if get_cached(hometeam, awayteam):
                print('got it')
                home_win, draw, away_win = get_cached(hometeam, awayteam)
                coefficients = CoefficientsADT(hometeam, awayteam,
                                               '2020-07-22',
                                               away_win, home_win, draw)

                # Resetting all the profit, and setting it back(just in case)
                coefficients.reset_profit()
                coefficients.make_profit(profit)
                print(coefficients.get_json())
                return jsonify(coefficients.get_json())
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

            coefficients = CoefficientsADT(hometeam, awayteam, '2020-07-22',
                                           home_win, away_win, draw)

            # Resetting all the profit, and setting it back(just in case)
            coefficients.reset_profit()
            coefficients.make_profit(profit)
            print(coefficients.get_json())
            return jsonify(coefficients.get_json())
        except:  # Ignore all kinds of errors and go on
            return {"Message": "An unexpected error occured, please resend "
                               "your request"}, 404


class Coefficients(Resource):
    def get(self, hometeam, awayteam, profit):
        # Do something
        return {"message": "Note that the last figure after slash has to be "
                           "float, e.g. 5.6. " + f"Try using {float(profit)}"
                                                 f" insted of {profit}"}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('hometeam', required=True)
        parser.add_argument('awayteam', required=True)
        parser.add_argument('date', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        print(args)
        return {'message': 'This feature will come soon', 'data': args}, 201


api.add_resource(TeamCoefficient,
                 '/<string:hometeam>/<string:awayteam>/<float:profit>')
api.add_resource(Coefficients,
                 '/<string:hometeam>/<string:awayteam>/<int:profit>')

if __name__ == '__main__':
    app.run(debug=True)
