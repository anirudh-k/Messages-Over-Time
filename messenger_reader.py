from datetime import datetime


MESSAGES_DIR = 'data/messenger/'

class MessengerReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def addToWindows(self, windowFile):
        return False

    def timeOfMessage(self, message):
        return False

    def timeOfWindow(self, window):
        return False

    def oldestMessage(self):
        return datetime.max

    def newestMessage(self):
        return datetime.min
