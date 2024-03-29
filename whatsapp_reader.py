from datetime import datetime
from tempfile import NamedTemporaryFile
import csv
import re
import shutil


MESSAGES_DIR = 'data/whatsapp/'

# message format:
# [%m/%d/%y, %I:%M:%S %p] <sender>: <message>
# e.g.
# [5/31/19, 1:59:51 AM] Annie Wu: Messages to this chat and calls are now secured with end-to-end encryption.
class WhatsAppReader:
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
            messageCount = 0 # first message doesn't count
            for row in reader:
                # skip first window row because it's the header
                if firstRow == True:
                    idx = row.index(self.user)
                    writer.writerow(row)
                    firstRow = False
                    continue
                if curMessage == '':
                    row[idx] = int(row[idx]) + messageCount
                    writer.writerow(row)
                    continue
                windowDT = self.timeOfWindow(row[0])
                curMessageDT = self.timeOfMessage(curMessage)
                while curMessageDT <= windowDT:
                    curMessage = messages.readline()
                    if curMessage[0:3] == '\xe2\x80\x8e': # some (valid) messages have this in front idk why
                        curMessage = curMessage[3:]
                    if curMessage == '': # readline() returns empty string when it's reached EOF
                        messageCount += 1 # do the count add here because it won't happen below (because of the break statement)
                        break
                    while not (curMessage[0] == '[' and ('AM]' in curMessage or 'PM]' in curMessage) and ':' in curMessage):
                        curMessage = messages.readline()
                        if curMessage[0:3] == '\xe2\x80\x8e': # some (valid) messages have this in front idk why
                            curMessage = curMessage[3:]
                        if curMessage == '': # readline() returns empty string when it's reached EOF
                            curMessage = datetime.now().strftime('%m/%d/%y, %I:%M:%S %p') # do this so the timeOfMessage below doesn't fail
                            break
                    curMessageDT = self.timeOfMessage(curMessage)
                    messageCount += 1

                row[idx] = int(row[idx]) + messageCount
                writer.writerow(row)
        shutil.copy(tempfile.name, windowFile)

    def timeOfMessage(self, message):
        dtString = re.search('\[(.*)M\]', message).group(1) + 'M'
        return datetime.strptime(dtString, '%m/%d/%y, %I:%M:%S %p')

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
