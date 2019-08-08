from reader import Reader

r = Reader()
print(r.oldestMessage())
print(r.newestMessage())
r.initWindows()
r.addToWindows()

# create
# whatsAppReader = WhatsAppReader('data/whatsapp/annie_whatsapp.txt')
# print(whatsAppReader.oldestMessage())
# print(whatsAppReader.newestMessage())
# print(whatsAppReader.addToWindows('blah'))
