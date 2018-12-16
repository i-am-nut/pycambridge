#!/home/emerson/Documentos/projects/pycambridge/app/bin/python
#aqui abaixo o caminho para o python de seu ambiente virtual
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


def printing_definitions(soup, tab_search, Colour, definition):
    #grabbing searched Word Header
    word_header = soup.find(class_="headword")


    word_classfication = soup.find(class_="pos")


    #there has to be a variable on the id to concatenate with dataset- so the search is correctly done for the wished tab
    language_block = soup.find(id="dataset-"+tab_search)

    #child block of definitions
    try:
        sense_block = language_block.find_all(class_="sense-block")
    except AttributeError:
        print (Colour.RED + "Ops, there's no definitions for the selected category" + Colour.END)
        sys.exit()

    #not printing yet, maybe use a flag whether to print it or not?
    #extra_examps = sense_block.find(class_="extraexamps")

    #looping through headers and definitions and printing
    print(Colour.YELLOW +'======================================================================================================================================' + Colour.END)

    print(Colour.CYAN + Colour.BOLD + word_header.get_text().upper() + Colour.END)
    if definition == "full":
        for sb in sense_block:
            #some words have this class commented, don't know why
            if sb.find_all(class_="txt-block txt-block--alt2"):
                for txtblock in sb.find_all(class_="txt-block txt-block--alt2"):
                    print (Colour.CYAN + Colour.BOLD + txtblock.get_text().capitalize() + Colour.END)
                    for defs in sb.find_all(class_="def-block pad-indent"):
                        #checking if the definition is from a phrase-block
                        if defs.findParent().findParent().attrs['class'][0] == 'phrase-block':
                            print (Colour.DARKCYAN + re.sub('[:.]','.\n',defs.findParent().findParent().get_text().capitalize()) + Colour.END)
                        else:
                            print (Colour.GREEN +re.sub('[:.]','.\n',defs.get_text())+'\n' + Colour.END)
                        print(Colour.YELLOW + '======================================================================================================================================' + Colour.END)
            else:
                for defs in sb.find_all(class_="def-block pad-indent"):
                    try:
                        print (Colour.PURPLE + Colour.BOLD + defs.findParent().findParent().findParent().findPreviousSibling().find(class_='pos').get_text())
                    except AttributeError:
                        pass
                    #checking if the definition is from a phrase-block
                    if defs.findParent().findParent().attrs['class'][0] == 'phrase-block':
                        print (Colour.DARKCYAN + re.sub('[:.]','.\n',defs.findParent().findParent().get_text().capitalize()) + Colour.END)
                    else: 
                        print (Colour.GREEN +re.sub('[:.]','.\n',defs.get_text())+'\n' + Colour.END)
                        print(Colour.YELLOW + '======================================================================================================================================' + Colour.END)

    
    else:
        #for txtblock in sense_block[0].find_all(class_="txt-block txt-block--alt2"):
        for txtblock in sense_block[0].find(class_="def-block pad-indent"):
            try:
                print (Colour.PURPLE + Colour.BOLD + txtblock.findParent().findParent().findParent().findParent().findPreviousSibling().find(class_='pos').get_text())
            except AttributeError:
                pass
            #print (Colour.CYAN + Colour.BOLD + txtblock.get_text().capitalize() + Colour.END)
            print (Colour.GREEN + re.sub('[:.]','.\n',txtblock.get_text().capitalize() + '\n') + Colour.END)
            #print (Colour.GREEN + re.sub('[:.]','.\n',sense_block[0].find(class_="def-block pad-indent").get_text()+'\n') + Colour.END)
        print(Colour.YELLOW + '======================================================================================================================================' + Colour.END)

    return '===========EOL============='



#function to print help usage
def help():
    return Colour.GREEN + '''Usage ---> ''' + Colour.YELLOW + '''python pycamb.py word category ''' + Colour.PURPLE + Colour.BOLD + ''':full:''' + Colour.END + Colour.PURPLE  + '''
:full is an optional option if you want all the meanings of the word:
categories -> 'ingles' 'americano' 'business' 'collection' '''+ Colour.END




if __name__ ==  '__main__':
    #arg to specify which word is being searched
    word = sys.argv[1]
    #if help, shows help usage
    if word == '--help':
        print(help())
        sys.exit()
    
    #arg to select either Ingles or Americano or Business or Exemplos or Collocations
    try:
        tab = sys.argv[2] 
    except IndexError:
        tab = 'ingles'

    #level of definitions searched, if full or only first definition
    try:
        level_def = sys.argv[3]
    except IndexError:
        level_def = 'whatever'
    
    #setting headers and performing request 
    headers = requests.utils.default_headers()

    #website doesn't accept python to make requests
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    r = requests.get('https://dictionary.cambridge.org/pt/dicionario/ingles/'+word, headers=headers)
    
    #setting page content as BeautifulSoup object
    soup = BeautifulSoup(r.content, 'html.parser')
    
    #taking the wished options to look for definitions
    if tab == 'ingles':
        tab_search = 'cald4'
        printing_definitions(soup, tab_search, Colour, level_def)
    
    elif tab == 'americano':
        tab_search = 'cacd'
        printing_definitions(soup, tab_search, Colour, level_def)
    
    elif tab == 'business':
        tab_search = 'cbed'
        printing_definitions(soup, tab_search, Colour, level_def)
    
    elif tab == 'exemplos':
        tab_search = 'examples'
        printing_definitions(soup, tab_search, Colour, level_def)
    
    elif tab == 'collocations':
        tab_search = 'combinations'
        printing_definitions(soup, tab_search, Colour, level_def)   

    #case of using default ingles
    elif tab == 'full':
        tab_search = 'cald4'
        printing_definitions(soup, tab_search, Colour, definition='full')   

    else:
        print(Colour.RED + "You've entered an invalid category\n" + help())
