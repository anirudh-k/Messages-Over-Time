from datetime import datetime
from tempfile import NamedTemporaryFile
import csv
import re
import shutil

# message format:
# [%m/%d/%y, %I:%M:%S %p] <Sender>: <message>
# e.g.
# [5/31/19, 1:59:51 AM] Annie Wu: Messages to this chat and calls are now secured with end-to-end encryption.
class WhatsAppReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def timeOfMessage(self, message):
        dtString = re.search('\[(.*)\]', message).group(1)
        dt = datetime.strptime(dtString, '%m/%d/%y, %I:%M:%S %p')
        return dt

    def oldestMessage(self):
        with open(self.fileName) as f:
            line = f.readline()
            return self.timeOfMessage(line)

    def newestMessage(self):
        with open(self.fileName) as f:
            lines = f.readlines()
            line = lines[len(lines) - 2] # the true last line is an empty line
            return self.timeOfMessage(line)

    def addToWindows(self, windowFile):
        tempfile = NamedTemporaryFile(delete=False)
        with open(windowFile) as f, tempfile:
            reader = csv.reader(f, delimiter=',', quotechar='\'')
            writer = csv.writer(tempfile, delimiter=',', quotechar='\'')

            messageCount = 8
            firstRow = True
            # idx = -1
            for row in reader:
                if firstRow == True:
                    idx = row.index(self.user)
                    writer.writerow(row)
                    firstRow = False
                    continue
                # print(row)
                row[idx] = messageCount
                writer.writerow(row)
                messageCount += 1
        shutil.copy(tempfile.name, windowFile)
