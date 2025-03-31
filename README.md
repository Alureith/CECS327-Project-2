# CECS327-Project-2

# Project 2: A Try of Peer-to-Peer

# Overview 

This project introduces students to distributed systems by developing a peer-to-peer (P2P) network using
Docker containers. The system will consist of 50-100 nodes, each acting as both a client and a server,
enabling peer discovery, registration, and communication


## ** Project Files **

- "p2p-system" which contains: 
    - Dockerfile
    - node.py


## **Installation Instructions **

### **Step 1: Install Docker**

Ensure that Docker is installed on your system. You can download it from:

- [Docker for Windows/macOS](https://www.docker.com/products/docker-desktop)
- [Docker for Linux](https://docs.docker.com/engine/install/)

Verify the installation:

```bash
docker --version
docker run hello-world
```

---

## **Compiling and Running the Application**

### **Step 2: Verifying environment is setup**

Navigate to the p2p-system file. Run the following commands to verify that the environment is setup: 

```
    docker build -t p2p-node .
    docker run -d -p 5000:5000 --name node1 p2p-node
```

Then visit http://localhost:5000/ to verify that this worked. Expected output: 

```
    {"message": "Node <UUID> is running!"}
```

### **Step 3: Developing a basic P2P node**