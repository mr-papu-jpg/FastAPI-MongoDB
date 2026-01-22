# FastAPI-MongoDB


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
