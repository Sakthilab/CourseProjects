import random

computer = random.randint(1, 100)
print("Enter number between 1 and 100:")
for i in range(1,8):
    user = int(input(f"Enter the number: "))
    if user == computer:
        print(f"✨Congratulations🎉,You have guessed number in {i} attempt")
        break
    elif user < computer:
        print("your guess is lesser than the number")
    else:
        print("Your guess is greater than the number")

else:
    print(f"😢Sorry you have exhausted all your chances, number to be guessed was {computer}")


