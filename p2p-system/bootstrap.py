from flask import Flask, request, jsonify

app = Flask(__name__)
peers = set()

@app.route('/register', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_url = data.get("address")
    if peer_url:
        peers.add(peer_url)
    return jsonify({"status": "registered", "peers": list(peers)})

@app.route('/peers', methods=['GET'])
def get_peers():
    return jsonify({"peers": list(peers)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
