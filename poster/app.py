from flask import Flask, request
app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def query():
	user_query = request.form['query']
	print("user_query: ", user_query)
	return "received"


if __name__ == '__main__':
    app.run()
