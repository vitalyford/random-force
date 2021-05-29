import random

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    server_number, client_number, flag = None, None, None
    context = {}
    if request.method == 'POST':
        server_number = str(random.randint(0, 100))
        client_number = request.form['guessed-number']
        if client_number == server_number:
            flag = 'Is ethical hacking only a skill<br>That may very well help pay you the bill?<br>I truly believe - it\'s the way to live life,<br>Like fixing it all with a ducktape and knife.<br>- VF'
        context = {'server_number': server_number, 'client_number': client_number, 'flag': flag}
    return render_template('index.html', context=context)
