import time
from random import randint
from flask import Flask
from flask import url_for
from flask import redirect
from flask import render_template
import application
app = Flask(__name__, static_url_path='/static')

last_update = None
random_value = randint(0, 10000)

@app.route("/")
def index():
    global last_update
    global random_value
    print(random_value)
    return render_template('index.html', last_update=last_update, random=random_value)

@app.route("/update")
def update_graph():
    global last_update
    global random_value
    app.logger.debug('Before update: %s', last_update)
    last_update = application.generate_graph()
    app.logger.debug('After update: %s', last_update)
    random_value = randint(0, 10000)
    return redirect(url_for('index'))

if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
