from flask import Flask
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
    """Present some documentation"""

    # Open the README file
    return 'Hello!'


class Coefficients(Resource):
    def get(self):
        # Do something
        return {"message": "I did it"}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('identifier', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('device_type', required=True)
        parser.add_argument('controller_gateway', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        print(args)
        return {'message': 'Device registered', 'data': args}, 201


class TeamCoefficient(Resource):
    def get(self, hometeam, awayteam, profit):
        # if not in list of available teams
        if hometeam not in teams or awayteam not in teams:
            return {"Message": "Teams don't exist"}, 404
        match = pd.DataFrame(data={'Date': '2020-07-22',
                 'HomeTeam': hometeam,
                 'AwayTeam': awayteam}, columns=['Date', 'HomeTeam', 'AwayTeam'])

        match_features = get_features_for_match(match, matches, 10, 3)
        probabilities = clf_C.predict_proba(match_features)
        print(probabilities)
        return {"message": f"I did it. Return res of {hometeam} vs {awayteam}"}, 200


api.add_resource(TeamCoefficient,
                 '/coeffs/<string:hometeam>/<string:awayteam>/<float:profit>')

if __name__ == '__main__':
    app.run(debug=True)
