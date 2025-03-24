# Easy WebSockd Python

A lightweight JSON-RPC WebSocket server for OpenWrt using python3-light. It executes ubus commands based on JSON-RPC requests and returns the results.

## Installation & Usage

1. **Build & Install:**
   - Add this package to your OpenWrt build system.
   - The Makefile installs the Python server scripts to `/sbin` and the init script to `/etc/init.d`.

2. **Starting the Server:**
   - It auto-starts at boot via the init script.
   - To start manually, run:
     ```sh
     /etc/init.d/easy-websockd-python start
     ```

3. **Testing the Server:**
   - **Using websocat:**  
     Connect with:
     ```sh
     websocat ws://<OpenWrt_IP>:8765
     ```
     Then send a JSON-RPC request. For example:
     ```json
     {"jsonrpc": "2.0", "id": 801212, "method": "ubus", "params": {"path": "uci", "action": "get", "msg": {"config": "wireless", "type": "wifi-iface"}}}
     ```
   - **Using a Python Client:**  
     Create a simple client script to send the JSON-RPC request.