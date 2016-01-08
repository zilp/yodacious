import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


# runs yodaizer (used by server)
def yodaize(orig):
    orig = orig.strip()
    if len(orig) < 1 or not orig:
        return "If nothing to say have you, say nothing."
    words = word_tokenize(orig)
    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return words[1] + " " + words[0]
    else:
        words_pos = nltk.pos_tag(words)
        print words_pos
        return yoda(words_pos)

# determines type of sentence & corresponding function to call
def yoda(li):
    li2 = iter(li, 'CC')
    if li2[0] == 'true':
        if get_tag(li2[2], 0) == 'VP' or get_tag(li2[2], 0) == 'VBP' or get_tag(li2[2], 0) == 'VBZ':
            return question(li2[2]) + " " + li2[1] + verb(li2[3])
        else:
            return verb(li2[3]) + " " + li2[1] + verb(li2[2])
    elif get_tag(li2, 0) == 'VP' or get_tag(li2, 0) == 'VBP' or get_tag(li2, 0) == 'VBZ':
        return question(li2)
    else:
        return verb(li2)

# splits declarative sentence on verb & reformulates
def verb(li):
    for (word, tag) in li:
        word_list = [x[0] for x in li]
        tag_list = [x[1] for x in li]
        sentence = ""
        if tag == 'VBD' or tag == 'VBG' or tag == 'VBZ' or tag == 'VBP':
            index = [y[0] for y in li].index(word)
            verb = word
            first_words = word_list[(index + 1):(len(word_list))]
            last_words = word_list[0:index]
            for y in first_words:
                sentence = sentence + " " + y
            sentence = sentence + " " + verb
            for y in last_words:
                sentence = sentence + " " + y
            return sentence
        elif tag == 'VBN' or tag == 'VB':
            index = [y[0] for y in li].index(word)
            index = index + 1
            verb = word_list[index]
            first_words = word_list[(index + 1):(len(word_list))]
            last_words = word_list[0:index]
            for y in first_words:
                sentence = sentence + " " + y
            sentence = sentence + " " + verb
            for y in last_words:
                sentence = sentence + " " + y
            return sentence
    for w in word_list:
        sentence = sentence + " " + w
    return sentence

# splits questions & reformulates
def question(li):
    for (word, tag) in li:
        word_list = [x[0] for x in li]
        tag_list = [x[1] for x in li]
        sentence = ""
        if tag == 'PRP' or tag == 'IN':
            index = [y[0] for y in li].index(word)
            noun = word
            first_words = word_list[(index+1):(len(word_list))]
            last_words = word_list[0:index]
            for y in first_words:
                sentence = sentence + " " + y
            for y in last_words:
                sentence = sentence + " " + y
            return sentence + " " + noun

# returns POS tag attached to word at specified index
def get_tag(li, index):
    list = [x[1] for x in li]
    return list[index]

# iterates over list to find instance of specific POS tag
def iter(li, pos):
    for (word, tag) in li:
        if tag == pos:
            index = [y[0] for y in li].index(word)
            key = word
            list1 = li[(index + 1):(len(li))]
            list2 = li[0:index]
            return ('true', key, list1, list2)
    return li
