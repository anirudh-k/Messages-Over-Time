from datetime import datetime
from tempfile import NamedTemporaryFile
import csv
import json
import shutil


MESSAGES_DIR = 'data/messenger/'

# message format:
# {
#     "sender_name": "<sender>",
#     "timestamp_ms": <unix timestamp>,
#     "content": "<message>",
#     "type": "<type>"
# }
# e.g.
# {
#     "sender_name": "Adi Parmar",
#     "timestamp_ms": 1563230034198,
#     "content": "\u00f0\u009f\u0091\u00bd",
#     "type": "Generic"
# }
class MessengerReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def addToWindows(self, windowFile):
        tempfile = NamedTemporaryFile(delete=False)
        with open(self.fileName) as jsonFile, open(windowFile) as windows, tempfile:
            data = json.load(jsonFile)
            messages = data['messages']
            messages.reverse()
            reader = csv.reader(windows, delimiter=',', quotechar='\'')
            writer = csv.writer(tempfile, delimiter=',', quotechar='\'')

            firstRow = True
            totalMessages = len(messages)

            curMessageIdx = 0
            messageCount = 0
            for row in reader:
                # skip first window row because it's the header
                if firstRow == True:
                    idx = row.index(self.user)
                    writer.writerow(row)
                    firstRow = False
                    continue
                if curMessageIdx >= totalMessages:
                    row[idx] = int(row[idx]) + messageCount
                    writer.writerow(row)
                    continue
                windowDT = self.timeOfWindow(row[0])
                curMessageDT = self.timeOfMessage(messages[curMessageIdx])
                while curMessageDT <= windowDT:
                    curMessageIdx += 1
                    if curMessageIdx >= totalMessages: # surpassed last message
                        messageCount += 1 # do the count add here because it won't happen below (because of the break statement)
                        break
                    curMessageDT = self.timeOfMessage(messages[curMessageIdx])
                    messageCount += 1

                row[idx] = int(row[idx]) + messageCount
                writer.writerow(row)
        shutil.copy(tempfile.name, windowFile)

    def timeOfMessage(self, message):
        timestamp = message['timestamp_ms'] / 1000
        return datetime.fromtimestamp(timestamp)

    def timeOfWindow(self, window):
        return datetime.strptime(window, '%Y-%m-%d %H:%M:%S')

    def oldestMessage(self):
        with open(self.fileName) as jsonFile:
            data = json.load(jsonFile)
            messages = data['messages']
            oldestMessage = messages[len(messages) - 1]
            return self.timeOfMessage(oldestMessage)

    def newestMessage(self):
        with open(self.fileName) as jsonFile:
            data = json.load(jsonFile)
            messages = data['messages']
            newestMessage = messages[0]
            return self.timeOfMessage(newestMessage)
