import requests
import sys
import re
from bs4 import BeautifulSoup

class Colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def printing_definitions(soup, tab_search, Colour):
    #grabbing searched Word Header
    word_header = soup.find(class_="headword")

    #there has to be a variable on the id to concatenate with dataset- so the search is correctly done for the wished tab
    language_block = soup.find(id="dataset-"+tab_search)

    #child block of definitions
    sense_block = language_block.find_all(class_="sense-block")

    #not printing yet, maybe use a flag whether to print it or not?
    #extra_examps = sense_block.find(class_="extraexamps")

    #looping through headers and definitions and printing
    print('======================================================================================================================================')
    for sb in sense_block:
        for txtblock in sb.find_all(class_="txt-block txt-block--alt2"):
            print (txtblock.get_text().capitalize())
            for defs in sb.find_all(class_="def-block pad-indent"):
                #checking if the definition is from a phrase-block
                if defs.findParent().findParent().attrs['class'][0] == 'phrase-block':
                    print (re.sub('[:.]','.\n',defs.findParent().findParent().get_text().capitalize()))
                else: 
                    print (re.sub('[:.]','.\n',defs.get_text())+'\n')
            print(Colour.RED + '======================================================================================================================================' + Colour.END)

    return '===========EOL============='

if __name__ ==  '__main__':
    #arg to specify which word is being searched
    word = sys.argv[1]
    
    #arg to select either Ingles or Americano or Business or Exemplos or Collocations
    tab = sys.argv[2]
    
    #setting headers and performing request, 
    headers = requests.utils.default_headers()

    #website doesn't accept python to make requests
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    r = requests.get('https://dictionary.cambridge.org/pt/dicionario/ingles/'+word, headers=headers)
    
    #setting page content as BeautifulSoup object
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #taking the wished options to look for definitions
    if sys.argv[2] == 'ingles':
        tab_search = 'cald4'
        printing_definitions(soup, tab_search, Colour)
    
    elif sys.argv[2] == 'americano':
        tab_search = 'cacd'
        printing_definitions(soup, tab_search)
    
    elif sys.argv[2] == 'business':
        tab_search = 'cbed'
        printing_definitions(soup, tab_search)
    
    elif sys.argv[2] == 'exemplos':
        tab_search = 'examples'
        printing_definitions(soup, tab_search)
    
    elif sys.argv[2] == 'collocations':
        tab_search = 'combinations'
        printing_definitions(soup, tab_search)
    
    
