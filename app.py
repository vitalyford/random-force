from numpy import random
import redis
import pickle
from flask import Flask, render_template, request


app = Flask(__name__)

# port 6379 is only open for the app
# please no brute-forcing or scanning, it won't work
clients = redis.StrictRedis(host='redis', port=6379)


@app.route('/', methods=['GET', 'POST'])
def home():
    context = {'remote_addr': request.remote_addr}

    if request.method == 'POST':
        server_number, client_number, flag = None, None, None

        if not clients.exists(request.remote_addr):
            # sum up all individual numbers in the IP address
            client_seed = sum(list(map(int, request.remote_addr.split('.'))))
            # assign a specific seed for the server's randomizer
            # that is linked to that particular client
            random.seed(client_seed)
            clients.set(request.remote_addr, pickle.dumps(random.get_state()))

        random.set_state(pickle.loads(clients.get(request.remote_addr)))

        server_number = str(random.randint(0, 100))
        clients.set(request.remote_addr, pickle.dumps(random.get_state()))

        client_number = request.form['guessed-number']
        if client_number == server_number:
            flag = 'Is ethical hacking only a skill<br>That may very well help pay you the bill?<br>I truly believe - it\'s the way to live life,<br>Like fixing it all with a ducktape and knife.<br>- VF'
        context = {'server_number': server_number, 'client_number': client_number, 'flag': flag, 'remote_addr': request.remote_addr}
    return render_template('index.html', context=context)
