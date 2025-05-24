# create a variable called total 
# set it to zero
total = 0

# Request the user to enter a number and
# Instruct the user the user to enter-1 to stop the request 
user_input = int(input("please enter a number (-1 to exit):"))

#  Create a program to add up the user input and keep
#  to repeat till the enters -1
while user_input != -1:
    total += user_input

    user_input = int(input("please enter a number(-1 to exist):"))

# Print the sum of all the user_input as a total
    if user_input == -1:
        print(total)
        break
    
# Create a program that will  calculate 
# the average sum of the user_input 
# exlude -1 and print the average
num = int(input("How many numbers did you enter, exluding -1 ?"))

for n in range (num) :
    avg = total /num 
    print("Average is :"  , avg)
    break