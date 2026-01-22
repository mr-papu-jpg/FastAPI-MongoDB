# FastAPI-MongoDB

Fastapi project where everything learned from database management with Mongomock from the MongoDB standard interface is put into practice.

## Technologies:

* fastapi

* uvicorn

## Updates:

* *20/01/2026*: Basic creation of a project, the basis of the project.

## Connectivity Report 

**Issue**: MongoDB Atlas Connectivity from Mobile Environment (Termux)

While developing the backend on a Termux environment (Android/Linux emulated), we encountered a series of networking layers that prevented a stable handshake with the MongoDB Atlas Cloud.

**Technical Obstacles Encountered:**

1. DNS Resolution Failure (ISP Level):

* Symptom: Failed to resolve cluster0-shard-00-00.4rsloai.mongodb.net.

* Cause: Local ISP DNS servers were blocking or failing to resolve MongoDB SRV and Shard records.

* Workaround Attempted: Implemented a custom DNS resolver in Python and manually mapped hostnames to known AWS IPs.

2. Port 27017 Filtering (Firewall/CGNAT):

* Symptom: nmap reported port 27017 as filtered.

* Cause: Mobile network providers often block non-standard ports (like 27017) to prevent unauthorized traffic or due to CGNAT restrictions.

3. TLS/SSL Handshake Timeout via VPN:

* Symptom: No servers found yet (Timeout: 10.0s).

* Cause: Even after establishing a VPN tunnel (which changed port status from filtered to open), the Pymongo driver failed to complete the TLS handshake. This is likely due to MTU (Maximum Transmission Unit) fragmentation or protocol interference within the VPN/Android network stack.


**Current Status & Strategy:**

* Cloud Readiness: The codebase is 100% "Cloud Ready." The connection logic includes fallback mechanisms for mongomock to ensure development continuity.

* Fallback Implementation:

```python
try:
    # Cloud Connection Attempt
    client = MongoClient(URL_CLOUD, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
except Exception:
    # Local Memory Mock for Development
    client = mongomock.MongoClient()
```

* **Future Action**: Connectivity will be re-tested from a different network gateway or via a dedicated proxy to bypass mobile ISP restrictions.

Why we are using mongomock instead of MongoDB Atlas (Current Status)

This project currently uses mongomock for the database layer. This decision was made due to infrastructure limitations specific to the Termux/Android environment in certain network regions:

Network Restrictions: Local ISPs and mobile network gateways often block port 27017 and intercept custom DNS resolutions required for MongoDB Atlas SRV records.


Protocol Overhead: Even with VPN tunneling, the Android network stack in an emulated terminal environment (Termux) introduces latency and handshake failures during TLS/SSL negotiation with AWS-hosted MongoDB clusters.

Development Velocity: To prioritize the development of core API features (Authentication, JWT, Financial Logic) over network troubleshooting, we implemented a Mocking Strategy that allows the app to be fully functional in a local-memory environment.

How to Switch to a Production Environment (Standard PC/Server)

The codebase is built with a "Cloud-Ready" architecture. If you are running this project on a standard Linux, macOS, or Windows environment, you can switch to a real MongoDB Atlas instance in two steps:

1. Configure Environment Variables:
Update your .env file with your Atlas Connection String:

```env
DATA_BASE_URL_CLOUD=mongodb+srv://<user>:<password>@cluster0.mongodb.net/my_db
```

The Connection Logic:
The system is designed to automatically attempt a cloud connection. If the environment allows it, the app will prioritize the MongoClient over mongomock automatically:

```python
try:
    client = MongoClient(URL_CLOUD, serverSelectionTimeoutMS=5000)
    client.admin.command('ping') # Official handshake
except Exception:
    client = mongomock.MongoClient() # Automatic fallback

```

## Comands:

**Turn on the server:**

```bash
uvicorn main:app --reload
```

**API Testing Guide (Using HTTPie)**

Once the server is running with uvicorn main:app --reload, you can use the following commands to test the endpoints

1. **User Management**

* Register a new user:

```bash
http POST :8000/usuarios/ nombre="Angstart" dinero:=1000 password="tu_password_segura"
```

* Login (Obtain JWT Token):

Note: This will return an access_token. You need it for the protected routes.

```bash
http -f POST :8000/auth/login username="Angstart" password="tu_password_segura"
```

2. **Protected Routes (Require Token)**

* Get current user profile:

*(Replace TU_TOKEN_AQUI with the token received from login)*

```bash
http GET :8000/usuarios/me "Authorization: Bearer TU_TOKEN_AQUI"
```

3. **Financial Transactions (Coming Soon)**

* Transfer money to another user:

```bash
http POST :8000/transacciones/enviar destino_nombre="UsuarioB" monto:=250.50 "Authorization: Bearer TU_TOKEN_AQUI"
```

Go to your favorite browser and copy the default URL uvicorn and add to the end /docs and authenticate button "ang" as username, and "11092003" as key

### All made in Termux

### @User: mr-papu-jpg
