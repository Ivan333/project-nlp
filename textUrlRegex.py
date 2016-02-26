
from bs4 import BeautifulSoup

def readText(html):
    soup = BeautifulSoup(html, "lxml")
    
    for script in soup(['script','style']):
        script.extract()
    
    text = soup.get_text()
    
    text = text.split("\n")
    
    mk_text = ''
    
    #f = open("text.txt","w")
    for line in text:
        line = line.strip()
        if len(line) > 50:
            #f.write(line.encode("utf-8") + "\n")
            mk_text += line.encode('utf-8') + '\n'
    #f.close()
    
    return mk_text