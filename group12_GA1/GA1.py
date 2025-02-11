# We Williams Beaumont, Hunter Forsythe, and McKinley Morris
# declare that We have completed this
# computer code in accordance with the UAB Academic Integrity
# Code and the UAB CS Honor Code. I/We have read the UAB
# Academic Integrity Code and understand that any breach of the
# Code may result in severe penalties.
# Student signature(s)/initials: MM
# Date: 2/23/2025

def c_ciphertext(text):
    for i in range(len(text)):
        print("user text")
        
        
    
def choice_switch(user_choice):
    match user_choice:
        case 1:
            user_input = input("Type your message to be encrypted\n")
        case 2:
            user_input = input("Choose your file to be encrypted\n")
        case default:
            print("Invalid input")


try:
    user_choice = int(input("Enter 1 for typed input\nEnter 2 to select txt file\n"))
    choice_switch(user_choice)
except ValueError:
    print("Please enter a valid option")