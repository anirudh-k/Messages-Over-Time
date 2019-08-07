from datetime import datetime
import re

# message format:
# [%m/%d/%y, %I:%M:%S %p] <Sender>: <message>
# e.g.
# [5/31/19, 1:59:51 AM] Annie Wu: Messages to this chat and calls are now secured with end-to-end encryption.
class WhatsAppReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.user = fileName.split('/')[-1][:fileName.split('/')[-1].index('_')]

    def oldestMessage(self):
        with open(self.fileName) as f:
            line = f.readline()
            dtString = re.search('\[(.*)\]', line).group(1)
            dt = datetime.strptime(dtString, '%m/%d/%y, %I:%M:%S %p')
            return dt

    def newestMessage(self):
        with open(self.fileName) as f:
            lines = f.readlines()
            line = lines[len(lines) - 2] # the true last line is an empty line
            dtString = re.search('\[(.*)\]', line).group(1)
            dt = datetime.strptime(dtString, '%m/%d/%y, %I:%M:%S %p')
            return dt
