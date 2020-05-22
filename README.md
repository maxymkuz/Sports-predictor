![](https://img.shields.io/github/license/maxymkuz/Sports-predictor)
![](https://img.shields.io/github/last-commit/maxymkuz/Sports-predictor)
![](https://img.shields.io/github/languages/code-size/maxymkuz/Sports-predictor)

# Sport's Predictor
### Description
I am making an API, which will predict an outcome of any
 sports event using profound regression Machine Learning algorithms, and
  figure out coefficients of all possible outcomes(win, draw, lose) with
   option to make a profit from a bet. As
  sport betting
  market turnover steadily grows at about +7-8% per year, and is already worth
   more than 7$ billion, the demand for betting platforms is rising. This
    API is meant to be used as the core in setting coefficients at any sports
     betting platform(preferably websites).


## Table of contents
* **[Installation and setup](#setup)**
    * [Hosting an API on local machine](#local)
* **[Usage](#usage)**
    * [Via GET requests](#local)
    * [Example code snippet for developing websites](#local)
* [Credits](#credits)
* [License](#license)

### Wiki pages:

[№0. Goal of the project, Q&A](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%960.-%D0%9F%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F.-%D0%9F%D0%B8%D1%82%D0%B0%D0%BD%D0%BD%D1%8F-%D1%82%D0%B0-%D0%B2%D1%96%D0%B4%D0%BF%D0%BE%D0%B2%D1%96%D0%B4%D1%96.)

[№1. Main theme](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%961.-%D0%A2%D0%B5%D0%BC%D0%B0-%D0%B4%D0%BE%D1%81%D0%BB%D1%96%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.-API.)

[№2. Functional/non-functional requirements. Libraries](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%962.-%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%96-%D0%BD%D0%B5%D1%84%D1%83%D0%BD%D0%BA%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%96-%D0%B2%D0%B8%D0%BC%D0%BE%D0%B3%D0%B8.-%D0%94%D0%B0%D0%BD%D1%96-%D1%82%D0%B0-%D0%B1%D1%96%D0%B1%D0%BB%D1%96%D0%BE%D1%82%D0%B5%D0%BA%D0%B8.)

[№3. ADT](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%963.-ADT)

[№4.](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%963.-ADT)


<a name="setup"></a>
# Installation and setup 
### [To use an app on server, click here](kuzyshyn.pythonanywhere.com )
<a name="local"></a>
## Hosting web application on your local machine

#### 1. Installing pip
You need to have pip installed. If you don't, follow [these instructions
](https://www.makeuseof.com/tag/install-pip-for-python/) for
 your operating system.

#### 2. Installing prerequisites
##### a) from requirements.txt
You need to execute the following command from the root directory of this
 project:
 ```bash
pip install -r requirements.txt
```
##### b) Manual installation
You need to do the following in your project directory:
```bash
pip install xgboost pandas numpy matplotlib flask flask-restful scikit-learn

```
> Note that on linux you should use pip3 instead

##### To run locally, enter the following command
```bash
python3 run.py
```

<a name="usage"></a>
# Usage

### Profit setting
User have the possibility to adjust profit, you want to make from a bets on
 average. Profit has to be of **float** type, and is placed in the last
  place in request url. If you want to set 5% profit, then the request
   should have a form of path/HomeTeam/AwayTeam/**5.0**


All responses will have a form
```json
{
  "Status": "200 if Success, 40X otherwise",
  "HomeTeam": "the name of the home team",
  "AwayTeam": "the name of the away team",
  "home_win": "the probability of the home team winning",
  "away_win": "the probability of the away team winning",
  "draw": "the probability of the draw"
}
```
#### Sample request
###### Online usage path: path=`maxkuz.pythonanywhere.com/`
###### for local usage path=`http://0.0.0.0:1300/`
**Definition**
`GET path/<string:hometeam>/<string:awayteam>/<float:profit>`

**Response**

- `404 Not Found` if such teams doesn't exist in EPL

`GET ___/<string:hometeam>/<string:awayteam>/<float:profit>`
- `200 OK` Success

`maxkuz.pythonanywhere.com/Arsenal/Crystal%20Palace/0.0`
```json
{
  "AwayTeam": "Liverpool",
  "HomeTeam": "Arsenal",
  "home_win": 3.08,
  "away_win": 3.28,
  "draw": 2.7,
  "status": 200
}
```
##### Now lets set profit to 10.5% _(All coefficients will increase by 10.5%)_
`maxkuz.pythonanywhere.com/Arsenal/Liverpool/10.5`
```json
{
  "AwayTeam": "Liverpool",
  "HomeTeam": "Arsenal",
  "home_win": 3.4,
  "away_win": 3.62,
  "draw": 2.98,
  "status": 200
}
```

<a name="credits"></a>
### Credits
Maxym Kuzyshyn. More to come
<a name="license"></a>
### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/maxymkuz/Sports-predictor/blob/master/LICENSE)
file for details.