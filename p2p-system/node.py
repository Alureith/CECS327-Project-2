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
    # Parse incomin JSON data from request
    data = request.get_json()
    # Get Address Field
    peer_address = data.get('address')

    # If no address is provided then return a bad request
    if not peer_address:
        return jsonify({"error": "Missing peer address"}), 400
    
    # Add peer to the list if not registered
    if peer_address not in peers:
        peers.append(peer_address)
        print(f"Registered new peer: {peer_address}")
        return jsonify({"message": "Peer registered", "peers": peers}), 201
    else:
    # If peer is registered then return confirmation 
        return jsonify({"message": "Peer already registered", "peers": peers}), 200

 # Message recieved endpoint    
@app.route('/message', methods=['POST'])
def receive_message():
    # Parse the incoming JSON data
    data = request.get_json()

    # Extract 'sender' and 'msg' fields
    sender = data.get("sender")
    msg = data.get("msg")

    # Validate that both fields are present
    if not sender or not msg:
        return jsonify({"error": "Missing sender or msg"}), 400

    # Log the received message to the console
    print(f"Received message from {sender}: {msg}")
    # Respond to the sender with confirmation
    return jsonify({"status": "received"}), 200

# Run the app on host 0.0.0.0 (accessible externally) and port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
