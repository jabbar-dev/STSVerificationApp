from pickletools import markobject
from flask import Flask

app = Flask(__name__)


@app.route('/')
def welcome():
    return "Welcome"

@app.route('/members')
def mem():
    return 'hello members how are you'



if __name__ == '_main_':
    app.run(debug=True)