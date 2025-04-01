# Import required libraries
from flask import Flask, jsonify, request  # Flask for HTTP server, jsonify for sending JSON responses
import uuid  # UUID for generating a unique node identifier

# Create a Flask application instance
app = Flask(__name__)

# Generate a unique ID for this node
node_id = str(uuid.uuid4())

# Store registered peer addresses
peers = []

# Define the root endpoint to return the node's status
@app.route('/')
def home():
    # Return a message with the node's UUID
    return jsonify({"message": f"Node {node_id} is running!"})

# Define a ping endpoint to test connectivity
@app.route('/ping')
def ping():
    # Return a simple JSON response including the node's UUID
    return jsonify({"response": "pong", "node_id": node_id})

# Peer Registration
@app.route('/register', methods=['POST'])
def register_peer():
    data = request.get_json()
    peer_address = data.get('address')

    if not peer_address:
        return jsonify({"error": "Missing peer address"}), 400
    
    if peer_address not in peers:
        peers.append(peer_address)
        print(f"Registered new peer: {peer_address}")
        return jsonify({"message": "Peer registered", "peers": peers}), 201
    else:
        return jsonify({"message": "Peer already registered", "peers": peers}), 200
    
@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    sender = data.get("sender")
    msg = data.get("msg")

    if not sender or not msg:
        return jsonify({"error": "Missing sender or msg"}), 400

    print(f"📨 Received message from {sender}: {msg}")
    return jsonify({"status": "received"}), 200

# Run the app on host 0.0.0.0 (accessible externally) and port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
