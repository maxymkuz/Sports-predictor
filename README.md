![](https://img.shields.io/github/license/maxymkuz/Sports-predictor)
![](https://img.shields.io/github/last-commit/maxymkuz/Sports-predictor)
![](https://img.shields.io/github/languages/code-size/maxymkuz/Sports-predictor)

# Sport's Predictor
### Description
I am making an API, which will predict an outcome of any
 sports event using profound regression Machine Learning algorithms, and
  figure out coefficients of all possible outcomes(win, draw, lose) with
   an option to make a fixed amount of profit from each bet. As
  sport betting
  market turnover steadily grows at about +7-8% per year, and is already worth
   more than 7$ billion, the demand for betting platforms is rising. This
    API is meant to be used as the core in setting coefficients at any sports
     betting platform, especially web-based ones.


## Table of contents
* **[Installation and setup](#setup)**
    * [For hosting an API on local machine](#local)
* **[Usage](#usage)**
    * [Locally, via GET requests](#local)
    * [Using GET requests on my server](#server)
    * [Example code snippet for developing websites](#example)
* [Modules and data explained](#data)
* [Contribution](#contribute)
* [Credits](#credits)
* [License](#license)

### Wiki pages:

[№0. Goal of the project, Q&A](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%960.-%D0%9F%D1%80%D0%B5%D0%B4%D1%81%D1%82%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F.-%D0%9F%D0%B8%D1%82%D0%B0%D0%BD%D0%BD%D1%8F-%D1%82%D0%B0-%D0%B2%D1%96%D0%B4%D0%BF%D0%BE%D0%B2%D1%96%D0%B4%D1%96.)

[№1. Main theme](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%961.-%D0%A2%D0%B5%D0%BC%D0%B0-%D0%B4%D0%BE%D1%81%D0%BB%D1%96%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.-API.)

[№2. Functional/non-functional requirements. Libraries](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%962.-%D0%A4%D1%83%D0%BD%D0%BA%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%96-%D0%BD%D0%B5%D1%84%D1%83%D0%BD%D0%BA%D1%86%D1%96%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C%D0%BD%D1%96-%D0%B2%D0%B8%D0%BC%D0%BE%D0%B3%D0%B8.-%D0%94%D0%B0%D0%BD%D1%96-%D1%82%D0%B0-%D0%B1%D1%96%D0%B1%D0%BB%D1%96%D0%BE%D1%82%D0%B5%D0%BA%D0%B8.)

[№3. ADT](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%963.-ADT)

[№4.Gathering data and the research itself](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%964.-%D0%9D%D0%B0%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%B0%D0%BD%D0%B8%D1%85-%D1%82%D0%B0-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%BE%D1%81%D0%BB%D1%96%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.)

[№5.Conclusions](https://github.com/maxymkuz/Sports-predictor/wiki/%D0%94%D0%97-%E2%84%964.-%D0%9D%D0%B0%D0%BA%D0%BE%D0%BF%D0%B8%D1%87%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%B0%D0%BD%D0%B8%D1%85-%D1%82%D0%B0-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D0%B4%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%BE%D1%81%D0%BB%D1%96%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F.)

<a name="setup"></a>
# Installation and setup for local usage
> You can skip this section if you would use it on a web server 

<a name="local"></a>
If you need reliability and independence from internet services, you
 can deploy an API on your local machine:
## Hosting web application on your local machine

#### 1. Installing pip
You need to have pip installed. If you don't, follow [these instructions
](https://www.makeuseof.com/tag/install-pip-for-python/) for
 your operating system.

#### 2. Getting lates version of project from git
`git clone https://github.com/maxymkuz/Sports-predictor`
#### 3. Installing prerequisites
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
>
<a name="local"></a>
##### To run, enter the following command
```bash
python3 run.py
```

<a name="usage"></a>
# Usage
<a name="server"></a>
### [kuzyshyn.pythonanywhere.com - API domain](kuzyshyn.pythonanywhere.com )

### Profit setting
Key feature of this API is that the user is able to adjust profit, (s)he
 wants to make from a bets on
 average. Profit has to be of **float** type, in percent, and is placed in the
  last
  position in request url. For instance, if you want to set 5% profit, then the
   request
   should have a form of _path_/HomeTeam/AwayTeam/**5.0**

**Definition**

`GET path/<string:hometeam>/<string:awayteam>/<float:profit>`

All responses will have a form
```json
{
  "Status": "200 if Success, 404 otherwise",
  "HomeTeam": "the name of the home team",
  "AwayTeam": "the name of the away team",
  "home_win": "the probability of the home team winning",
  "away_win": "the probability of the away team winning",
  "draw": "the probability of the draw"
}
```
#### Sample request
###### For server requests, path=`maxkuz.pythonanywhere.com/`
###### for local usage, path=`http://0.0.0.0:1300/`

**Response**

`GET path/HomeTeam/AwayTeam/<float>`

- `200 OK` Success

`GET path/None/None/None`

- `404 Not Found` if such teams doesn't exist in EPL

**Example requests**

`maxkuz.pythonanywhere.com/Arsenal/Liverpool/0.0`
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
##### Now lets set profit to 10.5% _(that means that all coefficients will increase by 10.5%)_
`maxkuz.pythonanywhere.com/Arsenal/Liverpool/10.5`
```json
{
  "AwayTeam": "Liverpool",
  "HomeTeam": "Arsenal",
  "home_win": 2.97,
  "away_win": 2.79,
  "draw": 2.44,
  "status": 200
}
```
> Notice that 

<a name="example"></a>
#### Example code snippet for developing websites
The following code is placed in [example.py](https://github.com/maxymkuz/Sports-predictor/blob/master/API/examole.py)
```python3
import requests

url = "http://maxkuz.pythonanywhere.com/"

away_team = "Chelsea"
home_team = "Man City"
profit = 5.0

response = requests.get(url + f"{home_team}/{away_team}/{profit}")

data = response.json()
```
Response:
```json
{
    "AwayTeam": "Chelsea",
    "HomeTeam": "Man City",
    "away_win": 10.17,
    "draw": 2.77,
    "home_win": 1.69,
    "status": 200
}
```
<a name="data"></a>
## Modules and Data explained
If you want to play around with the code, which I used for the feature
 creating and Machine Learning modules training, I encourage you to check
  [train_model.ipynb](https://github.com/maxymkuz/Sports-predictor/blob/master/train_model.ipynb)
   module.

> [/adt/coefficientsADT.py](https://github.com/maxymkuz/Sports-predictor/blob/master/adt/coefficients_ADT.py) - main module to work with coefficients
>
> [/api/predictor.py](https://github.com/maxymkuz/Sports-predictor/blob/master/API/predictor.py) is used to create features for future prediction
> 
>[/api/__init\__.py](https://github.com/maxymkuz/Sports-predictor/blob/master/API/__init__.py) is main module, where all functions for API are processed 

All .csv files can be downloaded [here.](https://datahub.io/sports-data/english
-premier-league)

Each match in database has total of 62 statistical criteria, like 
> **Date** = Match Date (dd/mm/yy);
**FTHG** = Full Time Home Team Goals;
**FTR** = Full Time Result (H=Home Win, D=Draw, A=Away Win);
**HS** = Home Team Shots;
**HF** = Home Team Fouls Committed...`

Full list of abbreviations you can find [here.](https://github.com/woobe/footballytics/blob/master/data/notes.txt)

<a name="contribute"></a>
### Contributing
For now, I'm the only contributor to this project. If you have an idea on
 how to improve it, I highly encourage you to set up the project using
  abovementioned instructions, and open the pull request.

<a name="credits"></a>
### Credits
Maxym Kuzyshyn. 2020))
<a name="license"></a>
### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/maxymkuz/Sports-predictor/blob/master/LICENSE)
file for details.