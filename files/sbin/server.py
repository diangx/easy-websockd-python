from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import subprocess

class JSONRPCWebSocket(WebSocket):
    def handleMessage(self):
        print("Received:", self.data)
        try:
            req = json.loads(self.data)
        except json.JSONDecodeError:
            err = json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32700, "message": "Parse error"},
                "id": None
            })
            self.sendMessage(err)
            return

        if req.get("jsonrpc") != "2.0" or "method" not in req:
            err = json.dumps({
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": "Invalid Request"},
                "id": req.get("id", None)
            })
            self.sendMessage(err)
            return

        if req.get("method") == "echo":
            response = {
                "jsonrpc": "2.0",
                "result": req.get("params"),
                "id": req.get("id")
            }
        elif req.get("method") == "ubus":
            params = req.get("params", {})
            path = params.get("path")
            action = params.get("action")
            msg = params.get("msg", {})

            if not path or not action:
                response = {
                    "jsonrpc": "2.0",
                    "error": {"code": -32602, "message": "Missing required parameters: 'path' and 'action'"},
                    "id": req.get("id")
                }
            else:
                json_msg = json.dumps(msg)

                cmd = ["ubus", "call", path, action, json_msg]
                print("Executing command:", " ".join(cmd))
                try:
                    output = subprocess.check_output(
                        cmd,
                        stderr=subprocess.STDOUT,
                        text=True  # or universal_newlines=True (same as Python 3.7)
                    )
                    try:
                        result = json.loads(output)
                    except json.JSONDecodeError:
                        result = output
                    response = {
                        "jsonrpc": "2.0",
                        "result": result,
                        "id": req.get("id")
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "error": {"code": -32000, "message": str(e)},
                        "id": req.get("id")
                    }
        else:
            response = {
                "jsonrpc": "2.0",
                "error": {"code": -32601, "message": "Method not found"},
                "id": req.get("id")
            }

        self.sendMessage(json.dumps(response))

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")

server = SimpleWebSocketServer('', 8765, JSONRPCWebSocket)
print("JSON‑RPC WebSocket port 8765")
server.serveforever()
