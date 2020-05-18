# Sport's Predictor
### Description
I am making an API, which will predict an outcome of any
 sports event using profound classification Machine Learning algorithms, and
  figure out coefficients of all possible outcomes(win, draw, lose). As
  sport betting
  market turnover steadily grows at about +7-8% per year, and is already worth
   more than 7$ billion, the demand for betting platforms is rising. This
    API is meant to be used as the core in setting coefficients at any sports
     betting platform.

It also has a website, a graphic interface to provide the same functionality
 for ordinary users in a more visual and convenient way. 

## Table of contents
* **[Installation and setup](#setup)**
    * [Hosting web application on local machine](#local)
* **[Usage](#usage)**
* [Credits](#credits)
* [License](#license)

<a name="setup"></a>
# Installation and setup 

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
pip install pandas numpy matplotlib flask Scikit-learn

```
> Note that on linux you should use pip3 instead

<a name="usage"></a>
# Usage
All responses will have a form
```json
{
  "HomeTeam": "the name of the home team",
  "AwayTeam": "the name of the away team",
  "H": "the probability of the home team winning",
  "A": "the probability of the away team winning",
  "D": "the probability of the draw"
}
```
#### Sample request
**Definition**

`GET /HomeTeam/AwayTeam`

**Response**

- `404 Not Found` if such teams doesn't exist in EPL

- `200 OK` Success
```json
{
  "HomeTeam": "Liverpool",
  "AwayTeam": "Arsenal",
  "H": "0.53",
  "A": "0.2",
  "D": "0.27"
}
```




<a name="credits"></a>
### Credits
Maxym Kuzyshyn. More to come
<a name="license"></a>
### License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/maxymkuz/Sports-predictor/blob/master/LICENSE)
file for details.