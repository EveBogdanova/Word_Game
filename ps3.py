# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Eve Bogdanova
# Collaborators : only me
# Time spent    :

import math
import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
#

WORDLIST_FILENAME = "words.txt"

def load_words():
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# 
# -----------------------------------
#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    word = word.lower()
    first_component = 0
    word_length = 0
    for letter in word:
        points = SCRABBLE_LETTER_VALUES.get(letter,0)
        first_component+=points
        word_length+=1
    multiply = 7*word_length - 3*(n-word_length)
    if multiply < 1:
        return first_component
    elif multiply > 1:
        return first_component*multiply
    
    
def display_hand(hand):
    hand_letters = []
    for letter in hand.keys():
        for i in range(hand.get(letter)):
            hand_letters.append(letter)
    return ' '.join(hand_letters)


def deal_hand(n):
    hand={}
    num_vowels = int(math.ceil(n / 3))
    hand["*"]=1
    for i in range(num_vowels-1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    new_hand = hand.copy()
    word = word.lower()
    for letter in word:
        if letter in new_hand.keys():
            if new_hand.get(letter)<=1:
                del new_hand[letter]
            else:
                new_hand[letter] = new_hand.get(letter)-1        
    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    word = word.lower()
    word.replace(' ','')
    matches = []
    for possible_word in word_list:
        if len(possible_word)==len(word) and (possible_word[0]==word[0] or word[0]=='*'):
                res=0
                for i in range(len(word)):
                    if word[i] == possible_word[i]:
                        res+=1
                    else:
                        if possible_word[i] in VOWELS and word[i] == '*':
                            res+=1                 
                if res == len(word):
                    matches.append(possible_word)
    if len(matches)>=1:                
        for match in matches:
            result=0
            for letter in word:
                if letter in hand.keys() and hand.get(letter) >= word.count(letter):
                    result +=1 
            if result == len(word):
                return True
            else:
                return False    
    else:
        return False       
                
#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    handlen = list(hand.keys())
    return len(handlen)

def play_hand(hand, word_list):
    total_score = 0
    while calculate_handlen(hand)>0:
        print('\nYour Hand: ',display_hand(hand))
        user_word = input('\nTry your luck with a new word or enter a "!!" if you want to finish: ')
        if user_word == '!!':
            break
        else:
            if is_valid_word(user_word, hand, word_list) == True:
                n = calculate_handlen(hand)
                score = get_word_score(user_word, n)
                total_score+=score
                print(f'The word "{user_word}" earned {score} points.\nYour total score: {total_score}')   
            else:
                print(f'Sorry, "{user_word}" is not a valid word')
            hand = update_hand(hand, user_word)
    if calculate_handlen(hand) == 0:
        print(f"\nYou ran out of letters. You've finished this hand with {total_score} points")
    else:
        print(f"\nYou've finished this hand with {total_score} points")
    return total_score
#
# Problem #6: Playing a game
#

def substitute_hand(hand, letter):
    rand_vow = VOWELS
    rand_con = CONSONANTS
    new_hand = hand.copy()
    new_value = hand.get(letter)
    for lett in rand_vow:
        if lett in new_hand.items():
            rand_vow.replace(lett,'')
    for lett in rand_con:
        if lett in new_hand.items():
            rand_con.replace(lett,'')            
    del new_hand[letter]
    approp_lett = list(rand_con)+list(rand_vow)
    new_letter = random.choice(approp_lett)
    new_hand[new_letter] = new_value 
    return new_hand
    
def play_game(word_list):
    hands = []
    total_game_score = 0
    replay_count=0
    substitution_count=0
    start = 1
    while start == 1:
        try:
            hands_number = int(input('\nEnter a number of hands: '))
            if hands_number <= 0:
                print('You should pick a integer positive number')
                start = 1
            else:
                start = 0    
        except ValueError:
            print('You should pick a integer positive number')
            start = 1
    for i in range(hands_number):
        hands.append(deal_hand(HAND_SIZE)) 
    for hand in hands:
        print(f'\nThe hand number {hands.index(hand)+1} is: {display_hand(hand)}')
        if substitution_count==0:
            ask = 0
            while ask==0:
                substitution = input('Do you want to substitute a letter? ----> Answer: ')
                if substitution == 'yes':
                    substitution = True
                    while substitution == True:
                        chose_letter = input('Which letter you want to change? ----> Answer: ')
                        if chose_letter in hand:
                            hand = substitute_hand(hand, chose_letter) 
                            substitution_count+=1
                            substitution = False
                            ask=1
                        else:
                            print('This letter is not in your hand, pick another one')
                            substitution = True                            
                elif substitution == 'no':
                    ask = 1
                else:
                    print('Just enter yes or no')
                    ask = 0 
        score1 = play_hand(hand, word_list)
        print(score1,'\n-----------------------------------')
        if replay_count==0:
            ask2 = 0
            while ask2==0:
                replay = input('Do you want to replay this hand? ----> Answer: ')
                if replay == 'yes':
                    hand2 = hand.copy()
                    score2 = play_hand(hand2, word_list)
                    print(score2,'\n-----------------------------------')
                    total_game_score+=max(score1,score2)
                    replay_count+=1
                    ask2=1                        
                elif replay == 'no':
                    total_game_score+=score1
                    ask2 = 1
                else:
                    print('Just enter yes or no')
                    ask2 = 0    
        else:
            total_game_score+=score1
    print(f'\nYour total score over all hands is: {total_game_score}')
    return''                             
    
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
   
    
