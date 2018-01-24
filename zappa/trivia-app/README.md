# Simple Trivia web app

Written in [Flask](http://flask.pocoo.org/), a Python micro framework

Using the [Qriusity API](https://qriusity.com/) allow a user to select a category, and answer trivia questions.

Deployable on AWS as serverless application using [Zappa](https://github.com/Miserlou/Zappa)

### To run locally
Navigate to the new directory
```
cd trivia-app
```
Install python requirements using [pip](https://pip.pypa.io/en/stable/)
```
pip install -r requirements.txt
```
Run the application locally
```
FLASK_APP=trivia.py flask run
```
Once running, open your browser and go to `localhost:5000` in your address bar

### Deploy serverless application

[Initialize Zappa](https://github.com/Miserlou/Zappa#running-the-initial-setup--settings). Defaults should work fine
```
zappa init
```
Deploy to AWS
```
zappa deploy dev
```
After packaging and deploying, Zappa will return an endpoint for your app
```
Deployment complete!: https://1qrl5107yb.execute-api.us-east-1.amazonaws.com/dev
```
Navigate to that url, but be sure to include a trailing slash (see [here](https://stackoverflow.com/q/5457885/1706504))
```
https://1qrl5107yb.execute-api.us-east-1.amazonaws.com/dev/
```

If you'd like to undeploy run:
```
zappa undeploy dev
```