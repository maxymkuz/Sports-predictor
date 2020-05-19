import json


class CoefficientsADT:
    """ ADT to hold all the information about a future match
    """

    def __init__(self, home_team, away_team, date, home_win=None, away_win=None, draw=None):
        self.home_team = home_team
        self.away_team = away_team
        self.date = date
        self.home_win = home_win
        self.away_win = away_win
        self.draw = draw
        self.profit = 0

    def _round_coefficients(self):
        """
        Rounds all current coefficients to 2 figures after comma
        :return: None
        """
        self.home_win = round(self.home_win, 2)
        self.away_win = round(self.away_win, 2)
        self.draw = round(self.draw, 2)

    def reset_profit(self):
        """
        Adjust the coefficient, so that the user won't
        make any profit, nor loss
        :return: None
        """
        # Calculating how much profit coefficients currently have
        profit = 1 / self.home_win + 1 / self.away_win + 1 / self.draw
        # Normalize coefficients
        self.home_win *= profit
        self.away_win *= profit
        self.draw *= profit
        profit = 1 / self.home_win + 1 / self.away_win + 1 / self.draw

    def make_profit(self, percentage):
        """
        Adjust all the coefficients, so that
        :param percentage:
        :return: None
        """
        # Resetting any profit that could be before
        self.reset_profit()

        # Make profit, or loss if percentage is negative
        profit = 1 + percentage / 100
        print(profit)
        self.home_win /= profit
        self.away_win /= profit
        self.draw /= profit

    def set_coeff(self, home_win, away_win, draw):
        """
        Sets, or resets all coefficients
        :param home_win: float
        :param away_win: float
        :param draw: float
        :return: None
        """
        self.home_win = home_win
        self.away_win = away_win
        self.draw = draw

    def get_json(self):
        """
        Converts class into json and returns it
        :return: json
        """
        # Round all coefficients to 2 figures after comma
        self._round_coefficients()
        return json.dumps({"HomeTeam": self.home_team, "AwayTeam":
                           self.away_team, "date": self.date,
                           "H": self.home_win, "A": self.away_win,
                           "D": self.draw})

    def __str__(self):
        # Round all coefficients to 2 figures after comma
        self._round_coefficients()
        return f"{self.home_team} VS {self.away_team} on {self.date}\n" \
               f"{self.home_team} win coefficient: {self.home_win}.\n" \
               f"{self.away_team} win coefficient: {self.away_win}.\n" \
               f"Draw coefficient: {self.draw}"


if __name__ == '__main__':
    x = CoefficientsADT("Liverpool", "Arsenal", '2020-04-22', 3.32, 3.88, 2.05)
    print(x)
    x.reset_profit()
    print(x)
    x.make_profit(10)
    print(x)

