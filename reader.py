from datetime import datetime
from datetime import timedelta
from whatsapp_reader import WhatsAppReader
import csv
import os


WINDOWS_FILE = 'message_windows.csv'
DELTA = timedelta(hours=24)

class Reader:
    def __init__(self):
        self.friends = ['aditya', 'alice', 'amal', 'annie', 'christopher', 'edridge', 'grace', 'kavin', 'phillip', 'raghav', 'sangeetha', 'sarah', 'talitha', 'vishwa', 'yuliya']
        self.readers = [self.getReader(file) for file in self.listFiles('data/')]

    def initWindows(self):
        with open(WINDOWS_FILE, 'w+') as windows:
            writer = csv.writer(windows, delimiter=',', quotechar='\'')
            writer.writerow(['window'] + self.friends)

            oldDT = self.oldestMessage()
            newDT = self.newestMessage()

            windowCounts = [0 for x in self.friends]
            curDT = oldDT
            while (curDT < newDT):
                writer.writerow([curDT] + windowCounts)
                curDT += DELTA
        print('Success!')

    def addToWindows(self):
        for r in self.readers:
            r.addToWindows(WINDOWS_FILE)

    def oldestMessage(self):
        return min([r.oldestMessage() for r in self.readers])

    def newestMessage(self):
        return max([r.newestMessage() for r in self.readers])

    def getReader(self, filepath):
        if 'whatsapp' in filepath:
            return WhatsAppReader(filepath)

    def listFiles(self, path):
        for root, subdirs, files in os.walk(path):
            for f in files:
                if not f.startswith('.'):
                    yield os.path.join(root, f)
