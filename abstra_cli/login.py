import webbrowser
from simple_websocket_server import WebSocketServer, WebSocket

from .utils import save_config


class LoginServer(WebSocket):
    def handle(self):
        save_config(self.data)
        print("Saved user config")
        exit(0)


def login():
    open_status = webbrowser.open(f'https://console.abstracloud.com/cli-login')
    if not open_status:
        print('Failed to open browser')
    server = WebSocketServer('', 6553, LoginServer)
    server.serve_forever()
