# Random Force

To run, use `docker-compose up --build -d` that will build a web and redis containers and run the web container on port 8000. Your goal is to get the flag by guessing the number based on the source code of the app:
```python
from numpy import random
import redis
import pickle
from flask import Flask, render_template, request


app = Flask(__name__)


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
            flag = ... # intentionally omited
        context = {'server_number': server_number, 'client_number': client_number, 'flag': flag, 'remote_addr': request.remote_addr}
    return render_template('index.html', context=context)
```
