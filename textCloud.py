""" Name: Hang Ha
    Course: CSCI 203
    Assignment: Final Project
    Date: 1/13/2015 """

from hmc_urllib import getHTML
from visual import *
import math
import random

DEPTH = 2
MAX_WORDS = 1000

def makeInput(url):
    """Take the url as input and gets the contents of the website and convert it into list"""
    return list(getHTML(url))

def union(a, b):
    """merge two list"""
    for entry in b:
        if entry not in a:
            a.append(entry)

# "Clean" the list of words 
def removePunc(content):
    """Remove punctuations and numbers. Split content into list of words"""
    listWord = []
    atSplit = True
    for char in content:
        if not char.isalpha():
            atSplit = True
        else:
            if atSplit:
                listWord.append(char)
                atSplit = False
            else:
                listWord[-1] = listWord[-1] + char
    return listWord

def removeStopList(content):
    #Source: http://99webtools.com/blog/list-of-english-stop-words/
    """Remove unimportant words from the list"""
    stopList = ['i','a','an','the','is','are','of','not','or','to','as','and',
                'it','able','about','across','after','all','almost','also',
                'am','among','any','at','be','because','been','but','by','can',
                'cannot','could','dear','did','do','does','either','else',
                'ever','every','for','from','get','got','had','has','have','he',
                'her','hers','him','his','how','however','if','in','into',
                'its','just','least','let','may','me','might','most','must',
                'my','neither','no','nor','off','often','on','only','other',
                'our','own','rather','she','should','since','so','some','than',
                'that','their','them','then','there','these','they','this','tis',
                'too','us','was','we','were','what','when','where','which',
                'while','who','whom','why','will','with','would','yet','you',
                'your','another','that','s','t','ll']
    listWord = removePunc(content)
    for i in range(0,len(listWord)):
        if listWord[i] in stopList:
            listWord[i] = ''
    return listWord

# "Stemming" words
def isVowel(char):
    """Determine if the character is vowel"""
    return char in ['a','e','i','o','u']

### Conditions
def isDoubleC(word):
    """Determine if that word have double consonant at the end"""
    specialCase=['ll','ss','zz']
    if len(word) > 2:
        if word[-1] == word[-2] and not isVowel(word[-1]):
            if word.endswith('ll') or word.endswith('ss') or word.endswith('zz'):
                return False
            else:
                return True                  
    return False
    
### Strip and correct    
def stripSuffix(word):
    """If the word ends in 's', 'ed', 'ing', etc remove those letters, but if
    the resulting stemmed word is only 1 or 2 letters long, use the
    original word. """
    
    suffixs = ['s','es','ed','er','ly','ing']
    if word == '':
        return word
    if word.endswith('eed'):
        if len(word[:-2]) > 2:
            return word[:-1]
    if word.endswith('sses'):
        return word[:-2]
    for suffix in suffixs:
        if word.endswith(suffix):
            if word.endswith('ss') or word.endswith('ter') or word.endswith('ber'):
                break
            if len(word[:-len(suffix)]) > 2:
                word = word[:-len(suffix)]
    return word

def correctWord(word):
    """If the word end in at,bl... add 'e' at the end( ex: tabl -> table).
    If the word have double consonant at the en remove one consonant"""
    
    newWord = stripSuffix(word)
    endsE = ['bl','iz','ot','tur','lac','tl','zl']
    if newWord.endswith('at'):
        if len(newWord)>4:
            return newWord + 'e'
    for end in endsE:
        if newWord.endswith(end):
            return newWord + 'e'
    if isDoubleC(newWord):
        return newWord[:-1]
    return newWord
  
    
# Make the official list of words after "clean" and "stem"
def finalList(content):
    """Takes the content of the website and output the list of words after clean and stem"""
    listWord = removeStopList(content)
    for i in range(0,len(listWord)):
        listWord[i] = correctWord(listWord[i])
    return listWord
         
# Create data structure. Add words and count into index
def addWordToIndex(index, content):
    """Add words from list of words to index"""
    listWord = finalList(content)
    for word in listWord:
        addToIndex(index, word)
        
def addToIndex(index, keyword):
    """Add count to index"""
    if keyword in index:
        index[keyword] = index[keyword] + 1
    else:
        index[keyword] = 1

# Crawl web and return a dictionary of words and number of appearances
def crawlWeb(seed,maxDepth):
    """Takes url and maxDepth return a dictionary with word and its number of apperances"""
    toCrawl = [seed]
    crawled = []
    nextDepth = []
    depth = 0
    index = {}
    while toCrawl and depth <= maxDepth: 
        page = toCrawl.pop()
        if page not in crawled:
            content = makeInput(page)
            addWordToIndex(index, content[0])         
            union(nextDepth,content[1])
            crawled.append(page)
        if not toCrawl:
            toCrawl,nextDepth = nextDepth,[]
            depth = depth + 1
    return index

# Sort and return maximum MAX_WORDS of most popular words
def constrainList(index,maxWords):
    """Sort the list and return list of tuples with maxWords entry"""
    if '' in index:
        del index['']   #remove all the empty '' result from removeStopList
    index = sorted(index.items(), key=lambda x: (-x[1], x[0]))
    return index[:maxWords]

def windowSetup():   
    """" Sets up the VPython window "scene"
         See http://www.vpython.org/webdoc/visual/display.html"""
    
    scene.autoscale = false        # Don't auto rescale
    scene.background = color.yellow
    scene.foreground = color.black
    scene.height = 1000            # height of graphic window in pixels
    scene.width = 1000             # width of graphic window in pixels
    scene.x = 100                  # x offset of upper left corner in pixels
    scene.y = 100                  # y offset of upper left corner in pixels
    scene.title = 'Text Cloud'

def spiral(nloop=1,tightness=1.0, dir=1.0):
    """Initialize spiral shape"""
    spr = []
    for t in range(1, 1024*nloop, 16):
        t *= 0.001
        x = tightness/10.0* t * math.cos(t)*dir
        y = tightness/10.0* t * math.sin(t)
        z= t/7
        spr.append((x,y,z))
    return spr

def displayCloud(sortedList):
    """ Displays on a VPython graphics window the text cloud
        Input: sortedList - a list of tuples with first item a common word
               and second item the count for that word.  Sorted from high
               to low on counts. """
    
    position = (0,0,0) 
    maxHeight = 100 # max height of letter in pixels
    count = 0
    
    maxCount = sortedList[0][1]
    if MAX_WORDS < 100:
        path = spiral(nloop=50,tightness=4)
    else:
        path = spiral(nloop=MAX_WORDS*2,tightness=2)
    
    myLabels = []
    for w in range(len(sortedList)):
        
        # wordHeight is proportional to word's count
        wordHeight = sortedList[w][1]/maxCount * maxHeight
        
        myLabels += [ label(text = sortedList[w][0], pos = position,
                    color = (wordHeight/maxHeight, 0, wordHeight/maxHeight),
                    height = wordHeight, box = 0, border = 0, font = "times") ]
        if wordHeight > 90:
            count = count+ int(wordHeight * 4)
        else:
            count = count + int(wordHeight)
        position = path[count]
        

def main():
    """Main program"""
    seed = input('Enter a URL: ')
    print('Use right mouse button to move around the word spiral')
    index = crawlWeb(seed,DEPTH)
    output = constrainList(index,MAX_WORDS)
    windowSetup()
    cloud = displayCloud(output)
    
    
