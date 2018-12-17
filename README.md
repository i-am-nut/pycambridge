# pycambridge
A web-scrapper script to make consults to Advanced Cambridge Dictonary using shell command line.

### Example
```bash
$ pycamb.py hire
```

- The syntax of the command is  ```pycamb.py :word: :category: :full(meaning):```
- Pass the *word* you're looking for
- The categories may be: *ingles* , *americano*, *business*, *exemplos*
- If you want to see all the defitinitios and other diverse examples of the word, set **full** on the command line
- ```$ pycamb.py pace full``` or ```$ pycamb.py pace ingles full```
- To see the usage of the command, just type `pycamb.py --help`
- **To use it as on these examples** copy the script to somewhere into PATH and change the python binary used for execution (on the first line of the script) by the one used on your virtual environment for this project. *(not reccommended install pip depedencies with sudo)*. **Otherwise:** `$ python pycamb.py hire`

### TO-DO
- some definitions text needs a better regex to display it more readable.
