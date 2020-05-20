from flask import Flask, jsonify
from flask_restful import Resource, reqparse, Api
from adt.coefficients_ADT import CoefficientsADT
from API.predictor import clf_C, get_features_for_match, matches
import pandas as pd

# Creating an instance of Flask
app = Flask(__name__)
# Create the API
api = Api(app)

# List of EPL teams
teams = ['Arsenal',
         'Aston Villa',
         'Bournemouth',
         'Brighton',
         'Burnley',
         'Chelsea',
         'Crystal Palace',
         'Everton',
         'Leicester City',
         'Liverpool',
         'Manchester City',
         'Manchester United',
         'Newcastle United',
         'Southamptony',
         'Tottenham Hotspur',
         'Watford',
         'West Ham United',
         'Wolverhampton']


@app.route("/")
def index():
    """Send basic responce"""
    return f'Hello!, here is the list of available teams\n{teams}\n' \
           f'Here is an example call '


class Coefficients(Resource):
    def get(self):
        # Do something
        return {"message": "I did it"}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('hometeam', required=True)
        parser.add_argument('awayteam', required=True)
        parser.add_argument('date', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        print(args)
        return {'message': 'This feature will come soon', 'data': args}, 201


class TeamCoefficient(Resource):
    def get(self, hometeam, awayteam, profit):
        # if not in list of available teams
        if hometeam not in teams or awayteam not in teams:
            return {"Message": "Teams don't exist"}, 404
        try:
            match = pd.DataFrame(data={'Date': ['2020-07-22'],
                                       'HomeTeam': [hometeam],
                                       'AwayTeam': [awayteam], },
                                 columns=['Date', 'HomeTeam',
                                          'AwayTeam'])
            match_features = get_features_for_match(match.iloc[0], matches, 10,
                                                    3)
            df = pd.DataFrame(data={'Unnamed: 0': [3333]},
                              columns=['Unnamed: 0'])
            for i in match_features.to_frame().reset_index()['index']:
                df[i] = match_features[i]
            result = clf_C.predict_proba(df)[0]

            # Creating ADT for convenience
            coefficients = CoefficientsADT(hometeam, awayteam, '2020-07-22',
                                           1 / result[2], 1 / result[0],
                                           1 / result[1])

            # Resetting all the profit, and setting it back(just in case)
            coefficients.reset_profit()
            coefficients.make_profit(profit)
            print(coefficients.get_json())
            return jsonify(coefficients.get_json())
        except:  # Ignore all kinds of errors and go on
            return {"Message": "An unexpected error occured, please resend "
                               "your request"}, 404


api.add_resource(TeamCoefficient,
                 '/<string:hometeam>/<string:awayteam>/<float:profit>')

if __name__ == '__main__':
    app.run(debug=True)
