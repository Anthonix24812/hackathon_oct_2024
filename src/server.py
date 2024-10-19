from flask import Flask, request, send_from_directory
from src.plotting.plot_service import plot

app = Flask(__name__, static_folder='UI', template_folder='UI')

analysis_id: int = 1


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
    global analysis_id
    query = request.json['query']
    # TODO: call data extractor
    data = {}
    
    analysis_id += 1
    plot(analysis_id, data, query)
    return {'analysis': f'analyses/{analysis_id-1}.png'}, 200, {'Content-Type': 'application/json'}
