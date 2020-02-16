import json

import websocket
from PyQt5.QtCore import QThread, pyqtSignal

import Utils

user = Utils.getMacAddress()
mainUrl = 'ws://192.168.0.5:8080/chat/'
#endpoint = '1jY3mYV'
endpoint = Utils.getUrl()

class Stream(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def changeEndpoint(self, endpnt):
        global endpoint
        endpoint = endpnt
    def on_message(ws, message):
        message = json.loads(message)

        if message['sender'] != user:
            print(user)
            print(message['sender'])
            print('rcv>>' + message['message'])
            ws.log_signal.emit(message['message'])
        # stream.log_signal.emit(message)

    def on_error(ws, error):
        print(error)
        Stream.log_signal.emit(error)

    def on_close(ws):
        print('Close')
        Stream.log_signal.emit('Close')

    def on_open(ws):
        print('Open')
        print(endpoint)
        Stream.log_signal.emit('Open')

    def run(self):
        print(mainUrl+endpoint)
        self.ws = websocket.WebSocketApp(mainUrl+endpoint,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()