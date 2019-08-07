from whatsapp_reader import WhatsAppReader

whatsAppReader = WhatsAppReader('data/whatsapp/annie_whatsapp.txt')
print(whatsAppReader.oldestMessage())
print(whatsAppReader.newestMessage())
print(whatsAppReader.addToWindows('blah'))
