from threading import Thread

class send_async_email(Thread):
    def __init__(self, app, msg, mail):
        Thread.__init__(self)
        self._app = app
        self._msg = msg
        self._mail = mail
        self.start()
    
    def run(self):
        with self._app.app_context():
            self._mail.send(self._msg)