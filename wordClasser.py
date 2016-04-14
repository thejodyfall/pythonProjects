import requests, json
from functools import reduce
from six import iteritems


############################################################
# find the word class of an inputted word
#
# how do you decide which definition to use?
# give user the choice:
# display word and definition as a choice, 1. 2. 3. etc
#
# once use has chosen, display word class
#
# future: sentences!
############################################################

# other key to use
# key kkXRJeyqIgmsh9nI64X6CgJJnHbxp1HPpbajsnm2gRcSXQfZrI

# example output
# {'frequency': 4.02, 'word': 'bump', 'syllables': {'count': 1, 'list': ['bump']}, 'pronunciation': {'all': 'bəmp'}, 'results': [{'partOfSpeech': 'verb', 'definition': 'come upon, as if by accident; meet with', 'synonyms': ['chance', 'encounter', 'find', 'happen']}, {'partOfSpeech': 'noun', 'definition': 'an impact (as from a collision)', 'hasTypes': ['jar', 'bash', 'belt', 'buffeting', 'concussion', 'bang', 'jolt', 'jounce', 'knock', 'pounding', 'rap', 'shock', 'sideswipe', 'slap', 'smack', 'smash', 'strike', 'tap'], 'typeOf': ['impact'], 'examples': ['the bump threw him off the bicycle'], 'synonyms': ['blow'], 'derivation': ['bumpy']}, {'partOfSpeech': 'verb', 'definition': 'knock against with force or violence', 'typeOf': ['impinge on', 'run into', 'strike', 'collide with', 'hit'], 'examples': ['My car bumped into the tree'], 'also': ['bump into'], 'synonyms': ['knock'], 'derivation': ['bumper']}, {'partOfSpeech': 'verb', 'definition': 'assign to a lower position; reduce in rank', 'hasTypes': ['reduce', 'sideline'], 'typeOf': ['delegate', 'assign', 'designate', 'depute'], 'also': ['bump off'], 'synonyms': ['break', 'demote', 'kick downstairs', 'relegate']}, {'partOfSpeech': 'verb', 'definition': 'remove or force from a position of dwelling previously occupied', 'hasTypes': ['throw'], 'synonyms': ['dislodge'], 'typeOf': ['displace']}, {'partOfSpeech': 'noun', 'definition': 'something that bulges out or is protuberant or projects from its surroundings', 'hasTypes': ['snag', 'mogul', 'nub', 'nubble', 'occipital protuberance', 'caput', 'frontal eminence', 'wart', 'belly'], 'synonyms': ['bulge', 'excrescence', 'extrusion', 'gibbosity', 'gibbousness', 'hump', 'jut', 'prominence', 'protrusion', 'protuberance', 'swelling'], 'typeOf': ['projection']}, {'partOfSpeech': 'noun', 'definition': 'a lump on the body caused by a blow', 'typeOf': ['injury', 'trauma', 'harm', 'hurt']}, {'partOfSpeech': 'verb', 'definition': 'dance erotically or dance with the pelvis thrust forward', 'typeOf': ['trip the light fantastic toe', 'trip the light fantastic', 'dance'], 'examples': ['bump and grind']}]}

apiKey = ''

def askForWord():
    wordToFind = raw_input('Type in the word you want to class (or Ctrl + c to Exit): ')
    resp = requests.get('https://wordsapiv1.p.mashape.com/words/' + wordToFind + '?mashape-key=' + apiKey)
    getWordClass(wordToFind, resp)
    

def getWordClass(wordToFind, resp):
    if resp.status_code != 200:
        # This means something went wrong.
        print('Something went wrong: ' + str(resp.status_code))
    else:
        # this means sth was returned
        data = json.loads(resp.text) # data is a dictionary now
        # set this here to check how many are returned
        partofSpeech = data.get('results') # now its a list
        
        if len(partofSpeech) > 1:
            # display to screen each of the defs for user to select        
            wordCount = 1
            print('\n') # leave a line in between
            for word in partofSpeech:
                print(str(wordCount) + '. ' + word['definition'])
                wordCount += 1
            # find out which is the correct word
            wordChoice = raw_input('\nMore than one definition has been returned.  Please choose which one you want: ')
            
            # check the number inputted is in the list
            if checkWord(wordChoice, partofSpeech):
                print('You chose: ', wordChoice + '\n\n')
                # get the correct word class
                wordChoice = int(wordChoice)-1
            else:
                wordChoice = raw_input('\n\nThat is not a valid option.\n\nMore than one definition has been returned.  Please choose which one you want: ')
                wordChoice = int(wordChoice)-1
                getWordClass()

            print('Word class: ' + str(partofSpeech[wordChoice]['partOfSpeech']) + '\n\n')
        else:
            # only one definition found

            print('Word class: ' + str(partofSpeech[0]['partOfSpeech']) + '\n\n')
    askForWord()



def checkWord(wordChoice, partofSpeech):
    if str(wordChoice).lower() == 'e':
        exit()
    return int(wordChoice) > 0 and int(wordChoice) <= len(partofSpeech)


def main():
    askForWord()



if __name__ == "__main__":
    main()









        

