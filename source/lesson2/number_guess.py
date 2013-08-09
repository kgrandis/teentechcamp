import random

"""
  Some challenges for you:

  1. Can you give yourself more guesses?
  2. Can you make the secret number between 1 and 199?
  3. Can you make it so the program lets the user know how many guesses they have left?
  4. Can you make it so that you can just change one variable (new or existing) 
     so that the program changes the guess and updates the message?
"""

secret = random.randint(1, 99)
allowed_tries = 6
num_tries = 0

print("I have picked a number between 1 and 99. You have 6 tries to guess the number.\n")

guess = 0
while guess != secret and num_tries < allowed_tries:
    guess = input("What is your guess? ")

    if guess < secret:
        print("too low\n")
    elif guess > secret:
        print("too high\n")
    num_tries = num_tries + 1

if guess == secret:
    print("Congratulations! You guessed the number!")
else:
    print("No more guesses! I win!")
    print("The secret number was %d" % secret)

