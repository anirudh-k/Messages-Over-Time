from datetime import datetime
from datetime import timedelta
from whatsapp_reader import WhatsAppReader
import csv
import os


class Reader:
    def __init__(self):
        self.friends = ['aditya', 'alice', 'amal', 'annie', 'christopher', 'edridge', 'grace', 'kavin', 'phillip', 'raghav', 'sangeetha', 'sarah', 'talitha', 'vishwa', 'yuliya']

    def initWindows(self):
        with open('message_windows.csv', 'w+') as windows:
            writer = csv.writer(windows, delimiter=',')
            writer.writerow(['window'] + self.friends)
            oldDT = self.oldestMessage()
            newDT = self.newestMessage()
            delta = timedelta(hours=12)
            windowCounts = [0 for x in self.friends]
            curDT = oldDT
            while (curDT < newDT):
                writer.writerow([curDT] + windowCounts)
                curDT += delta

    def oldestMessage(self):
        oldestTime = datetime.max
        for filepath in self.listFiles('data/'):
            tempOldestTime = self.getReader(filepath).oldestMessage()
            oldestTime = tempOldestTime if tempOldestTime < oldestTime else oldestTime
        return oldestTime

    def newestMessage(self):
        newestTime = datetime.min
        for filepath in self.listFiles('data/'):
            tempNewestTime = self.getReader(filepath).newestMessage()
            newestTime = tempNewestTime if tempNewestTime > newestTime else newestTime
        return newestTime

    def getReader(self, filepath):
        if 'whatsapp' in filepath:
            return WhatsAppReader(filepath)

    def listFiles(self, path):
        for root, subdirs, files in os.walk(path):
            for f in files:
                if not f.startswith('.'):
                    yield os.path.join(root, f)
