from flask import Flask, jsonify, request
import uuid
import requests
import socket
import threading
import time

# Create a Flask application instance
app = Flask(__name__)

# Generate a unique ID for this node
node_id = str(uuid.uuid4())

# Store registered peer addresses
peers = set()

def get_own_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

own_ip = get_own_ip()
own_url = f"http://{own_ip}:5000"


# Register with the bootstrap node
def register_with_bootstrap():
    try:
        print(f"Registering with bootstrap: {own_url}")
        res = requests.post("http://bootstrap:5000/register", json={"address": own_url})
        print(f"Bootstrap response: {res.text}")
        bootstrap_peers = requests.get("http://bootstrap:5000/peers").json().get("peers", [])
        for peer in bootstrap_peers:
            if peer != own_url:
                peers.add(peer)
    except Exception as e:
        print(f"Failed to register or fetch peers from bootstrap: {e}")

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
        peers.add(peer_address)
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

    # If new peer, add to set
    if msg == "New peer discovered":
        # Send reply
        try:
            res = requests.post(
                f"{sender}/message",
                json={"sender": own_url, "msg": "Welcome new peer"}
            )
            print(f"Replied to {sender}, response: {res.text}")
        except Exception as e:
            print(f"Failed to reply to {sender}: {e}")

    # Respond to the sender with confirmation
    return jsonify({"status": "received"}), 200

# Fetch peers from existing peers using /peers/{ip}
def fetch_peers_from_peers():
    global peers
    current_peers = list(peers)
    for peer in current_peers:
        try:
            res = requests.get(f"{peer}/peers")
            new_peers = res.json().get("peers", [])
            for p in new_peers:
                if p != own_url and p not in peers:
                    peers.add(p)
                    print(f"Discovered new peer from {peer}: {p}")
        except Exception as e:
            print(f"Failed to fetch peers from {peer}: {e}")

# Periodically update peers from other known peers
def periodic_peer_update():
    while True:
        time.sleep(10)
        fetch_peers_from_peers()

@app.route('/peers', methods=['GET'])
def get_peers():
    sender_ip = request.remote_addr
    sender_url = f"http://{sender_ip}:5000"

    # Register sender as a peer if it's not already in the list and not itself
    if sender_url != own_url and sender_url not in peers:
        peers.add(sender_url)
        print(f"Discovered peer from ping: {sender_url}")
        
        # Send message to newly discovered peer
        try:
            res = requests.post(
                f"{sender_url}/message",
                json={"sender": own_url, "msg": "New peer discovered"}
            )
            print(f"Message sent to {sender_url}, response: {res.text}")
        except Exception as e:
            print(f"Failed to message new peer {sender_url}: {e}")

    return jsonify({"peers": list(peers | {own_url})})


# Run the app on host 0.0.0.0 (accessible externally) and port 5000
if __name__ == '__main__':
    register_with_bootstrap()
    threading.Thread(target=periodic_peer_update, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
