from datetime import datetime
from tempfile import NamedTemporaryFile
import csv
import re
import shutil


MESSAGES_DIR = 'data/whatsapp/'

# message format:
# [%m/%d/%y, %I:%M:%S %p] <Sender>: <message>
# e.g.
# [5/31/19, 1:59:51 AM] Annie Wu: Messages to this chat and calls are now secured with end-to-end encryption.
class WhatsAppReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def addToWindows(self, windowFile):
        tempfile = NamedTemporaryFile(delete=False)
        lineCount = 0
        with open(MESSAGES_DIR + self.user + '_whatsapp.txt') as messages, open(windowFile) as windows, tempfile:
            for line in messages:
                lineCount += 1
            messages.seek(0)

            messageCount = 0

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
                windowDT = self.timeOfWindow(row[0])
                curMessageDT = self.timeOfMessage(curMessage)
                while curMessageDT <= windowDT:
                    curMessage = messages.readline()
                    if curMessage[0:3] == '\xe2\x80\x8e': # some (valid) messages have this in front idk why
                        curMessage = curMessage[3:]
                    if curMessage == '': # readline() returns empty string when it's reached EOF
                        break
                    while not (curMessage[0] == '[' and ('AM]' in curMessage or 'PM]' in curMessage) and ('] Annie Wu:' in curMessage or '] Anirudh Kaushik:' in curMessage)):
                        curMessage = messages.readline()
                        if curMessage[0:3] == '\xe2\x80\x8e': # some (valid) messages have this in front idk why
                            curMessage = curMessage[3:]
                        if curMessage == '': # readline() returns empty string when it's reached EOF
                            break
                    curMessageDT = self.timeOfMessage(curMessage)
                    messageCount += 1

                row[idx] = messageCount - 1
                writer.writerow(row)
        shutil.copy(tempfile.name, windowFile)

    def timeOfMessage(self, message):
        dtString = re.search('\[(.*)M\]', message).group(1) + 'M'
        dt = datetime.strptime(dtString, '%m/%d/%y, %I:%M:%S %p')
        return dt

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
