class Helper: 

    def __init__(self):
        pass

    def encodeString(self, string):
        return string.encode('utf8')
    
    def showUrlMod(self, item):
        showURL = "https://www4.gogoanime.io"
        showEndpoint = self.encodeString(item.find('a').attrs['href'])
        showURL += showEndpoint
        return showURL