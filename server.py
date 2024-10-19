from flask import Flask, request, send_from_directory

app = Flask(__name__, static_folder='UI', template_folder='UI')


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.template_folder, 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api', methods=['GET'])
def ping():
    return 'pong'

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    print(data)
    return {'data': 'okay'}, 200, {'Content-Type': 'application/json'}
