from PyDictionary import PyDictionary
from google.cloud import language
import tkinter
import random
dictionary = PyDictionary()
client = language.LanguageServiceClient()
alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def sentiment(content):
    # Returns a list containing the sentiment of each sentence given.
    document = language.types.Document(content = content, language = 'en', type = 'PLAIN_TEXT')
    response = client.analyze_sentiment(document = document, encoding_type = 'UTF32')
    return [response.sentences[i].sentiment.score for i in range(len(response.sentences))]

def overall_sentiment(content):
    # Returns a single value containing the sentiment of the entire string of text.
    document = language.types.Document(content = content, language = 'en', type = 'PLAIN_TEXT')
    response = client.analyze_sentiment(document = document, encoding_type = 'UTF32')
    return response.document_sentiment.score

def good_word(word):
    if len(word) < 4:
        return False
    if not dictionary.meaning(word):
        return False
    if not ('Adjective' in dictionary.meaning(word) or 'Adverb' in dictionary.meaning(word)):
        return False
    return True

def synonyms(word):
    # Returns a list of synonyms of a given word, along with their sentiments.
    # Should make this more sophisticated to avoid grammar mistakes.
    allSynonyms = dictionary.synonym(word)
    if not allSynonyms or not good_word(word):
        return []
    allSynonyms.append(word)
    sentence = ""
    for i in allSynonyms:
        sentence += (i + ". ")
    sentiments = sentiment(sentence) + [0]
    return [[allSynonyms[i], sentiments[i]] for i in range(len(allSynonyms))]

def reduce_sentiment(content):
    words = content.split(" ")
    change_index = random.randint(0, len(words) - 1)
    to_change = words[change_index]
    possible_changes = synonyms(to_change)
    lowest = [to_change, 9999999]
    for i in range(len(possible_changes)):
        if possible_changes[i][1] < lowest[1]:
            lowest = possible_changes[i]
    words[change_index] = lowest[0]
    return " ".join(words)

def create_list(content):
    current = ""
    l = []
    for i in content:
        if not i in alphabet:
            if not current == "":
                l.append(current)
            current = ""
            if not i == " ":
                l.append(i)
        else:
            current += i
    if current != "":
        l.append(current)
    print(l)
    return l

def increase_sentiment(content):
    words = create_list(content)
    change_index = random.randint(0, len(words) - 1)
    to_change = words[change_index]
    possible_changes = synonyms(to_change)
    highest = [to_change, -9999999]
    for i in range(len(possible_changes)):
        if possible_changes[i][1] > highest[1]:
            highest = possible_changes[i]
    words[change_index] = highest[0]
    return " ".join(words)

def change_sentiment(content, newSentiment):
    currentSentiment = overall_sentiment(content)
    changed = content
    if currentSentiment > newSentiment:
        for i in range(15):
            changed = reduce_sentiment(changed)
            currentSentiment = overall_sentiment(changed)
            if currentSentiment < newSentiment:
                return changed
    else:
        for i in range(15):
            changed = increase_sentiment(changed)
            currentSentiment = overall_sentiment(changed)
            if currentSentiment > newSentiment:
                return change
    return changed

def remove_spaces(content):
    modified = ""
    for i in range(len(content) - 1):
        if not (content[i] == " " and not content[i + 1] in alphabet):
            modified += content[i]
    return modified + content[len(content) - 1]
#print(change_sentiment("I am having a good day. It is good.", 1))
#print(remove_spaces("I am having a good day ."))

class Modifier(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.b = tkinter.Button(self, text = "Change Text", command = self.on_button)
        self.box = tkinter.Entry(self, width = 50)
        self.box2 = tkinter.Text(self, height = 5, width = 50)
        self.box.pack()
        self.x = 0
        self.scale = tkinter.Scale(self, variable = self.x)
        self.scale.pack()
        self.b.pack()
        self.box2.pack()
    def on_button(self):
        happiness = self.scale.get() / 50 - 1
        original = self.box.get()
        print(original, happiness)
        modified = remove_spaces(change_sentiment(original, happiness))
        self.box2.delete('1.0', 'end')
        self.box2.insert('1.0', modified)
m = Modifier()
m.mainloop()
