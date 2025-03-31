# Import required libraries
from flask import Flask, jsonify  # Flask for HTTP server, jsonify for sending JSON responses
import uuid  # UUID for generating a unique node identifier

# Create a Flask application instance
app = Flask(__name__)

# Generate a unique ID for this node
node_id = str(uuid.uuid4())

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

# Run the app on host 0.0.0.0 (accessible externally) and port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
