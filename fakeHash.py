"""
This is a toy demo of hashing. It's intended to communicate the concept to bright students who are new to programming.

Features of hashing:

- it converts a string of characters into a number
- it's unique. The hash for a word or sentence is unique. There is no other word or sentence that will have the same hash. It's a fingerprint number for the string.
- it's one way. You can't go from the hash back to the original word or sentence.
- it's fast. It's a simple calculation that can be done in a few lines of code.
- it's consistent. If you hash a word or sentence twice, you will get the same hash both times.

I recommend starting with an even simpler algorithm and demonstrating why it will not work.
- count the number of letters in a word
- give each letter a number, and add them up

After showing the below, briefly mention proper hashing algorithms which practice bit-shifting, XOR, and other techniques to make the hash more secure.
"""

# import the alphabet, upper and lower case
from string import ascii_lowercase, ascii_uppercase

def split_word(word):
    return [char for char in word]

def split_sentence(sentence):
    return sentence.split(" ")

# does not handle punctuation
def alphabet_to_numbers(word):
    # create a dictionary with the alphabet and numbers
    alphabet = ascii_lowercase + ascii_uppercase
    numbers = range(1, 53)
    alphabet_dict = dict(zip(alphabet, numbers))
    return alphabet_dict


def fake_hash_word(word):
    word_hash = 0
    # split the word into a list of characters
    word = split_word(word)
    # convert the alphabet into numbers
    alphabet_scores = alphabet_to_numbers(word)

    for index, letter in enumerate(word):
        # each letter gets a score based on its position in the word
        letter_position = index + 1
        # multiply position score by letter score to get a unique score for each letter
        letter_score = alphabet_scores[letter] * letter_position

        word_hash += letter_score

    return word_hash

def fake_hash_sentence(sentence):
    sentence_hash = 0
    # split the sentence into a list of words
    sentence = split_sentence(sentence)
    # and put them back together
    no_spaces_sentence = "".join(sentence)
    sentence_hash = fake_hash_word(no_spaces_sentence)
    return sentence_hash

print(fake_hash_word("hello") != fake_hash_word("olleh"))
print(fake_hash_sentence("hello world") != fake_hash_sentence("world hello"))

print(fake_hash_word("hello"))
print(fake_hash_word("olleh"))
print(fake_hash_sentence("hello world"))
print(fake_hash_sentence("world hello"))

# TODO come up with list of words that will have the same hash
