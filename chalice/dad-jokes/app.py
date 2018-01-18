from chalice import Chalice
import random

app = Chalice(app_name='dad-jokes')

JOKES = [
    {
        "question": "How come you never see elephants hiding in trees?",
        "punchline": "Because they're so good at it"
    },
    {
        "question": "Why did the man smell bad on his birthday?",
        "punchline": "He was turning farty"
    },
    {
        "question": "Why couldn't the bicycle stand on it's own?",
        "punchline": "Because it was two tired"
    }
]

@app.route('/')
def index():

    return random.choice(JOKES)


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
