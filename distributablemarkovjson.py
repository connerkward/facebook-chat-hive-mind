# -----------------------------------------------------------------------------
# Author: CONNER K WARD
# Date: 01 / 23 / 2019
# -----------------------------------------------------------------------------
"""
Takes your Facebook messages in JSON and generates synthetic user messages.
"""
import json
import random
import sys

def readJSONdata(filename):
    """
    Read JSON formatted txt file and return contents.
    param (string) filename

    """
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def outputfile(contents, username = ''):
    """Write contents to txt file."""
    stringof = '.\n'.join(contents)
    filename = username + 'outfile.txt'
    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(stringof)

def make_pairs(corpus):
    """
    Generator for generating next words.
    param (list) corpus = all messages as a non segmented linear list.
    """
    for i in range(len(corpus) - 1):
        yield (corpus[i],
               corpus[i + 1])  # .strip(string.punctuation + string.digits

def makewords(source, amount = 10):
    #  list of words from file
    corpus = open(source, encoding='utf8').read().split()

    #  assigning pairs as generator function
    pairs = make_pairs(corpus)

    #  creating dictionary of words as keys with next words as values
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

    #  generating first word
    first_word = random.choice(corpus)  # pick first word
    while first_word.islower():  # if first word is lower case get another word
        first_word = random.choice(corpus)
    chain = [first_word]

    #  generating message
    for i in range(amount):
        chain.append(random.choice(word_dict[chain[-1]]))
    stringof = ' '.join(chain)

    return stringof

def main():
    print('***Remember to change the json to txt and place "message.txt" in '
          'same '
          'folder as script***')

    # messages file
    filename = str(sys.argv[0])

    #  users in source
    users = readJSONdata(filename)['participants']
    users.append({"name":"All"})
    for user in users:
        print(users.index(user), user['name'])
    choice = int(input("Which StarGod would you like to replicate?"))

    #  JSON to message array
    #  change to check if file already exists and ask to rebuild
    data = readJSONdata(filename)['messages']
    contents = []
    lengthofmessage = []
    for message in data:
        if 'content' in message and 'photos' not in message:  # filter
                if users[choice]['name'] == "All":
                    #print(message)
                    contents.append(message['content'])
                    lengthofmessage.append(len(message['content']))

                elif message["sender_name"] == users[choice]['name']:
                    #print(message)
                    contents.append(message['content'])
                    lengthofmessage.append(len(message['content']))

    #  handles putting messages into a file
    outputfile(contents, users[choice]['name'])

    #  AVG MESSAGE LENGTH
    avgmessagelength = 0
    for messagelegnths in lengthofmessage:
        avgmessagelength = (avgmessagelength+messagelegnths)/2
    #  avg length of user's messages
    print(users[choice]['name'] + "'s average message length: " + str(
        avgmessagelength))

    #  FINAL PRINT
    if users[choice]['name'] == "All":
        print("The collective conciousness says:")
    else:
        print(users[choice]['name'] + " says:")
    source = users[choice]['name'] + "outfile.txt"
    amount = int(avgmessagelength)
    #  makes a message based on users average message length
    print(makewords(source, amount) + ".")

if __name__ == '__main__':
    sys.argv = ['message.txt']
    main()