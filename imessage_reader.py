from datetime import datetime
from tempfile import NamedTemporaryFile
import csv
import shutil


MESSAGES_DIR = 'data/imessage/'

# message format:
# <sender>,%y-%m-%d %I:%M:%S %z,<message>
# e.g.
# Alice Wu,2018-08-25 20:09:45 +0000,Did you block me
class IMessageReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def addToWindows(self, windowFile):
        tempfile = NamedTemporaryFile(delete=False)
        with open(self.fileName) as messages, open(windowFile) as windows, tempfile:
            reader = csv.reader(windows, delimiter=',', quotechar='\'')
            writer = csv.writer(tempfile, delimiter=',', quotechar='\'')

            firstRow = True

            curMessage = messages.readline()
            messageCount = 1
            for row in reader:
                # skip first window row because it's the header
                if firstRow == True:
                    idx = row.index(self.user)
                    writer.writerow(row)
                    firstRow = False
                    continue
                if curMessage == '':
                    row[idx] = int(row[idx]) + messageCount - 1
                    writer.writerow(row)
                    continue
                windowDT = self.timeOfWindow(row[0])
                curMessageDT = self.timeOfMessage(curMessage)
                while curMessageDT <= windowDT:
                    curMessage = messages.readline()
                    if curMessage == '': # readline() returns empty string when it's reached EOF
                        messageCount += 1 # do the count add here because it won't happen below (because of the break statement)
                        break
                    while not (curMessage.count(',') >= 2 and curMessage.count(':') >= 2 and curMessage.count('-') >= 2 and '+0000' in curMessage):
                        curMessage = messages.readline()
                        if curMessage == '': # readline() returns empty string when it's reached EOF
                            curMessage = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '+0000' # do this so the timeOfMessage below doesn't fail
                            break
                    curMessageDT = self.timeOfMessage(curMessage)
                    messageCount += 1

                row[idx] = int(row[idx]) + messageCount - 1
                writer.writerow(row)
        shutil.copy(tempfile.name, windowFile)

    def timeOfMessage(self, message):
        dtString = ' '.join(message.split(',')[1].split(' ')[:2])
        return datetime.strptime(dtString, '%Y-%m-%d %H:%M:%S')

    def timeOfWindow(self, window):
        return datetime.strptime(window, '%Y-%m-%d %H:%M:%S')

    def oldestMessage(self):
        with open(self.fileName) as f:
            line = f.readline()
            return self.timeOfMessage(line)

    def newestMessage(self):
        with open(self.fileName) as f:
            lines = f.readlines()
            line = lines[len(lines) - 2] # the true last line is an empty line
            return self.timeOfMessage(line)
