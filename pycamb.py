#here the path for virtual environment python binary 
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

def default_printage(re, defs, Colour):
    if defs.findParent().findParent().attrs['class'][0] == 'phrase-block':
        print (Colour.DARKCYAN + re.sub('[:.]','.\n',defs.findParent().findParent().get_text().capitalize()) + Colour.END)
    else:
        p = re.compile('\[ .+?\]')
        m = p.findall(defs.find(class_='def-head semi-flush').get_text())
        #print header definition of a word
        try:
            print (re.sub('\[ .+?\]',Colour.RED+m[0]+Colour.END+Colour.DARKCYAN,defs.find(class_='def-head semi-flush').get_text()))
        except IndexError:
            print (re.sub('[:.]','.',Colour.DARKCYAN + defs.find(class_='def-head semi-flush').get_text())) 
            #print below examples of the word
        for examps in defs.find_all(class_='examp emphasized'):
            m = p.findall(examps.get_text())
            mod1 = Colour.GREEN + re.sub('[:.]','.',examps.get_text().capitalize())+ Colour.END
            try:
                mod2 = re.sub('\[ .+?\]',Colour.RED+m[0]+Colour.END+Colour.GREEN,mod1)
                print(mod2)
            except IndexError:
                print(mod1)


def yellow_line():
    print(Colour.YELLOW + '======================================================================================================================================' + Colour.END)

def printing_definitions(soup, tab_search, Colour, definition):
    #grabbing searched Word Header
    word_header = soup.find(class_="headword")

    #there has to be a variable on the id to concatenate with dataset- so the search is correctly done for the wished tab
    language_block = soup.find(id="dataset-"+tab_search)
    
    #parse only for examples category
    if tab_search == 'examples':
        yellow_line()
        print(Colour.BLUE + language_block.find(class_='cpexamps-head').get_text() + Colour.END)
        for egs in language_block.find_all(class_='eg'):
            #matching example source to highligh with another color
            p = re.compile('\n\n.*\n\n$')
            m = p.findall(egs.get_text())
            print (Colour.GREEN + re.sub('\n\n.*\n\n$',Colour.CYAN+Colour.BOLD+m[0],egs.get_text()) + Colour.END)
            yellow_line()
        sys.exit()

    #child block of definitions
    try:
        sense_block = language_block.find_all(class_="sense-block")
    except AttributeError:
        print (Colour.RED + "Ops, the selected category has no defitions for this word" + Colour.END)
        sys.exit()

    
    #not printing yet, maybe use a flag whether to print it or not?
    #extra_examps = sense_block.find(class_="extraexamps")
        

    #looping through headers and definitions and printing
    yellow_line()

    print(Colour.CYAN + Colour.BOLD + word_header.get_text().upper() + Colour.END)
    if definition == "full":
        for sb in sense_block:
            #some words have this class commented, don't know why
            if sb.find_all(class_="txt-block txt-block--alt2"):
                for txtblock in sb.find_all(class_="txt-block txt-block--alt2"):
                    print (Colour.CYAN + Colour.BOLD + txtblock.get_text().capitalize() + Colour.END)
                    for defs in sb.find_all(class_="def-block pad-indent"):
                        default_printage(re, defs, Colour)
                        yellow_line()

            #for those which have the above class commented, below is performed
            else:
                for defs in sb.find_all(class_="def-block pad-indent"):
                    #catch pos-header to print word kind (verb, noun, adjective...)
                    try:
                        print (Colour.PURPLE + Colour.BOLD + defs.findParent().findParent().findParent().findPreviousSibling().find(class_='pos').get_text())
                    except AttributeError:
                        pass
                    default_printage(re, defs, Colour)
                    yellow_line()

    #only first and main defitions for easy reading
    else:
        for txtblock in sense_block[0].find_all(class_="def-block pad-indent"):
            #VERY UGLY SECTION, RETHINK AND REFACTORY IT!
            try:
                #if pos header class exists, catch it and display
                print (Colour.PURPLE + Colour.BOLD + txtblock.findParent().findParent().findParent().findParent().findPreviousSibling().find(class_='pos').get_text() + Colour.END)
            except AttributeError:
                pass
            
            try:
                print(Colour.PURPLE + Colour.BOLD +re.sub('[\n]','',txtblock.findParent().findParent().findParent().findPreviousSibling().find(class_='pron-info').get_text()) + Colour.END)
            except AttributeError:
                pass
            
            try:
                print(Colour.PURPLE + Colour.BOLD +re.sub('[\n]','',txtblock.findParent().findParent().findParent().findPreviousSibling().find(class_='irreg-infls').get_text()) + Colour.END)
            except AttributeError:
                pass

            p = re.compile('\[.+?\]')
            m = p.findall(txtblock.find(class_='def-head semi-flush').get_text())
            #print header definition of a word
            try:
                print (re.sub('\[.+?\]',Colour.RED+m[0]+Colour.END+Colour.DARKCYAN,txtblock.find(class_='def-head semi-flush').get_text()))
            except IndexError:
                print (re.sub('[:.]','.',Colour.DARKCYAN + '\n' + txtblock.find(class_='def-head semi-flush').get_text())) 
            #print further below examples of the word
            for examps in txtblock.find_all(class_='examp emphasized'):
                m = p.findall(examps.get_text())
                mod1 = Colour.GREEN + re.sub('[:.]','.',examps.get_text()) + Colour.END
                #some definitions have no such curly braces blocks
                try:
                    mod2 = re.sub('\[ .+?\]',Colour.RED+m[0]+Colour.END+Colour.GREEN,mod1)
                    print(mod2)
                except IndexError:
                    print(mod1)
        yellow_line()

    return 0



#function to print help usage
def help():
    return Colour.GREEN + '''Usage ---> ''' + Colour.YELLOW + '''python pycamb.py word category ''' + Colour.PURPLE + Colour.BOLD + ''':full:''' + Colour.END + Colour.PURPLE  + '''
:full is an optional option if you want all the meanings of the word:
categories -> 'ingles' 'americano' 'business' 'collection' 'exemplos' '''+ Colour.END


if __name__ ==  '__main__':
    #specify which word is being searched
    word = sys.argv[1]

    #shows help usage
    if word == '--help':
        print(help())
        sys.exit()
    
    #select either Ingles or Americano or Business or Exemplos or Collocations
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

    #pratical case to use ingles as default
    elif tab == 'full':
        tab_search = 'cald4'
        printing_definitions(soup, tab_search, Colour, definition='full')   

    else:
        print(Colour.RED + "You've entered an invalid category\n" + help())
