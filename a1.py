"""
Wordle
Assignment 1
Semester 1, 2022
CSSE1001/CSSE7030
"""

from string import ascii_lowercase
from typing import Optional

from a1_support import (
    load_words,
    choose_word,
    VOCAB_FILE,
    ANSWERS_FILE,
    CORRECT,
    MISPLACED,
    INCORRECT,
    UNSEEN,
)

# Replace these <strings> with your name, student number and email address.
__author__ = "<Adnaan Buksh>, <47435568>"
__email__ = "<adnaan.buksh@uqconnect.edu.au>"

# Add your functions here
def main():
    """Where all the defs are put together to make the game run

    
    """
    stats = (0,0,0,0,0,0,0)
    play_again = True
    
    while play_again != False:
        words = (load_words(VOCAB_FILE))
        answer = choose_word(load_words(ANSWERS_FILE))
        word = answer  # Done so everytime answer is used it doesn't change and will be fixed     
        guess_number = 0
        history = ()
        game_end = False
        while has_lost(guess_number) != True:
            guess_number = guess_number + 1
            guess = prompt_user(guess_number, words)
            
            if guess == 'k':
                guess_number = guess_number - 1  # Compensates for +1 in start of loop
                print_keyboard(history)
                
            elif guess == 'q':
                play_again = False
                break
            
            elif guess == 'h':
                guess_number = guess_number - 1
                print("Ah, you need help? Unfortunate.")
            
            elif has_won(guess, answer) == True:
                reveal_answer = ("Correct! You won in "+str(guess_number)+" guesses!")
                game_end = True
                break
                
            elif has_lost(guess_number) == True:
                reveal_answer = ("You lose! The answer was: " + word)
                game_end = True
                break
                
            else:
                process_guess(guess, answer)
                history = (update_history(history, guess, answer))
                print_history(history)
                
        if game_end == True:   
            process_guess(guess, answer)
            history = (update_history(history, guess, answer))
            print_history(history)
            print(reveal_answer)
            stats = update_stats(stats,guess_number,guess, answer)
            print_stats(stats)
            remove_word(words,word)
            
            again = input("Would you like to play again (y/n)? ").strip().lower()
            
            if again != 'y':
                play_again = False
                break
           
        
def has_won(guess: str, answer: str) -> bool:
    """Checks if answer is the same as the guess

    Parameters:
	    guess (str): user input
	    answer (str): word to match for the game

    Returns:
	    bool: True if guess and answer are equal. False otherwise.
    """
    if guess == answer:
        return True

    
def has_lost(guess_number: int) -> bool:
    """Checks to see if guess number has exceeded 6

    Parameters:
	    guess_number (int): number of guess

    Returns:
	    bool: True if number of guess more than or equal to 6. False otherwise.
    """
    if guess_number >= 6:
        return True

  
def remove_word(words: tuple[str, ...], word: str) -> tuple[str, ...]:
    """Removes word from the list of valid words

    Parameters:
	    words (tuple): list of valid words
	    word (str): a valid word contained in list

    Returns:
	    tuple: updated tuple of words without word in it
    """
    a1 = list(words)
    a1.remove(word)
    words = tuple(a1)
    return words


def prompt_user(guess_number: int, words: tuple[str, ...]) -> str:
    """Ask user to input a guess till a valid attempt is made or
       specific inputs are entered

    Parameters:
	    guess_number (int): used to display the guess attept number
	    words (tuple): list of valid words user can enter

    Returns:
	    string : a valid input either from the tuple words of k,h,q
    """
    tries = str(guess_number)
    
    while True:
        unknown = False
        guess =  input('Enter guess '+tries+': ').strip().lower()  # .strip() and .lower() makes input all lower case and removes spaces    
        
        if guess == "k" or guess == "h" or guess == "q":
            return guess
        
        elif len(guess) < 6:
            print("Invalid! Guess must be of length 6")
        
        else:
            # Checks if guessed word is a valid word
            for valid_words in words:
                if guess == valid_words:
                    unknown = True
                    return guess
                    
            if unknown == False:
                print("Invalid! Unknown word")
    
          
def process_guess(guess: str, answer: str) -> str:
    """Compares letters in guess and answer which returns the corosponding coloured box

    Parameters:
	    guess (str): used to compare the letter to answer
	    answer (str): used to compare the letter to guess

    Returns:
	    string: 6 corrosponding coloured squares
    """
    guess_stored = (
        INCORRECT, INCORRECT, INCORRECT,
        INCORRECT, INCORRECT, INCORRECT
        )
    guess_num = list(guess_stored)
    answer_word = list(answer)
    letter_pos = 0
    pos = 0

    # Compares to see if letters in answer is in same possition to letters in guess
    # If they match completely they are removed from a list
    for x in answer:
        if guess[letter_pos] == x:
            guess_num[letter_pos] = CORRECT
            answer_word[letter_pos]=''
            
        letter_pos = letter_pos + 1
        guess_stored = tuple(guess_num)
        
    # Remaining letters in the list are compared to the letters in guess
    # To see if they are in the word but in a different location or not in the word at all
    for y in guess:
        word_pos = 0
        
        while word_pos != 6:  
            if y == answer_word [word_pos]:
                if guess_num[pos] == INCORRECT:
                    guess_num[pos] = MISPLACED
                    guess_stored = tuple(guess_num)
                    answer_word[word_pos]=''
                    break
            word_pos = word_pos + 1
        pos = pos + 1
        
    return ''.join(guess_stored)


def update_history(history: tuple[tuple[str, str], ...], guess: str,
                   answer: str ) -> tuple[tuple[str, str], ...]:
    """Updates the history list by adding the guess and coloured boxes in a tuple

    Parameters:
	    history (tuple): hold the guess and coloured boxes
	    guess (str): used to add in history and get boxes from process_guess
	    answer (str): used to get boxes from process_guess

    Returns:
	    tuple: of all guesses made and the corresponding coloured boxes
    """
    history = history + ((guess, process_guess(guess, answer)),)
    return history


def print_history(history: tuple[tuple[str, str], ...]) -> None:
    """Displays the pervious guesses and the position of the letter below

    Parameters:
	    history (tuple): to use infomation to display

    Returns:
	    None: 
    """
    guess_num = 1
    
    print("---------------")

    # Loops in the history tuple to get guess and the boxes for the processed guess
    for guess in history:            
        space_guess = (' '.join(guess[0]))
        print("Guess "+str(guess_num)+":  "+space_guess)
        print("         "+guess[1])
        print("---------------")
        guess_num = guess_num + 1
        
    print()


def print_keyboard(history: tuple[tuple[str, str], ...]) -> None:
    """Update and displays the letters entered and the colour boxes for
       best position they have been on

    Parameters:
            history (tuple): Used to compare the letter and colour square to the
                            letter dictionary to display updated keyboard.

    Returns:
            None: 
    """
    letter = {'a':UNSEEN,'b':UNSEEN,'c':UNSEEN,'d':UNSEEN,'e':UNSEEN,
              'f':UNSEEN,'g':UNSEEN,'h':UNSEEN,'i':UNSEEN,'j':UNSEEN,
              'k':UNSEEN,'l':UNSEEN,'m':UNSEEN,'n':UNSEEN,'o':UNSEEN,
              'p':UNSEEN,'q':UNSEEN,'r':UNSEEN,'s':UNSEEN,'t':UNSEEN,
              'u':UNSEEN,'v':UNSEEN,'w':UNSEEN,'x':UNSEEN,'y':UNSEEN,
              'z':UNSEEN}

    for guess in history:
        square_index = 0

        for each_letter in guess[0]:
            
            # Checks the guess letter and compare to dictionary
            # Updates if the guess letter has a better postion than dictionary
            if letter[each_letter] == CORRECT:
                letter.update({each_letter:CORRECT})


            elif (letter[each_letter] == MISPLACED and
                  guess[1][square_index] == CORRECT):        
                letter.update({each_letter:guess[1][square_index]})
                  
            elif (letter[each_letter] == INCORRECT and
                  guess[1][square_index] == CORRECT or
                  guess[1][square_index] == MISPLACED):
                letter.update({each_letter:guess[1][square_index]})
                
            else:
                letter.update({each_letter:guess[1][square_index]})
                    
            square_index = square_index + 1  # Goes to the next coloured square    
            
    letter_keys = list(letter.keys())
    letter_values = list(letter.values())
    count = 0
    
    print()
    print("Keyboard information")
    print("------------")

    
    while count != 26:    
        print(letter_keys[count]+": "+letter_values[count]+
              "\t"+letter_keys[count+1]+": "+letter_values[count+1])
        count = count + 2
        
    print()

    
def update_stats(stats: tuple[int, ...], guess_number: str, guess: str, answer: str) -> tuple:
    """Updates number of time the player losses or in howmnay moves they win

    Parameters:
            stats (tuple): previous stat infomation
            guess_number (str): used to run has_lost and to update number of times user has
                                lost and in how many attempts they won in stats
            guess (str): used to run has_won
            answer (str): used to run has_won 

    Returns:
        tuple: a tuple of the updated stats
    """
    stat = list(stats)
            
    if has_won(guess,answer) == True:
        stat[guess_number - 1] = stat[guess_number - 1] + 1  # Guess_number - 1 is to compensates for +1 in start of loop in main    
        stats = tuple(stat)
        
    else:
        stat[6] = (int(stat[6]) + 1)
        stats = tuple(stat)
        
    return stats
    
def print_stats(stats: tuple[int, ...]) -> None:
    """Prints set of infomation after the game is ended

    Parameters:
        stats (tuple): Containts the number of times the game has been lost
                       and how many moves it took to win
	     
    Returns:
	    None: 
    """
    count = 0
    
    print()
    print("Games won in:")

    while count != 6:
        word_count = str(count+1)
        number_stat = str (stats[count])
        print(word_count + " moves: " + number_stat)
        count = count + 1
        
    print("Games lost: "+ str(stats[6]))

    
if __name__ == "__main__":
    """Runs the main program
 
    """
    main()

