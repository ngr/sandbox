#! /usr/bin/env python
def censor( text, word ):
    result = ""

    nw = True
    suspect = 0
    for i, c  in enumerate(text):
        if nw == True:
            if c == word[0]:
#                print "First letter match! Index: " + str(i) + " Letter: " + str(c)
                suspect = True
                if text[i:i+len(word)] == word:
                    suspect = len(word)
	    nw = False
        if c == " ":
#            print "Next is new word"
            nw = True

        if suspect > 0:
            result += "*"
            suspect -= 1
        else:
            result += c
    return result

print censor("this hack is wack hack", "hack")             
