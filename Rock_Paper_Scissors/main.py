import random
options = ("rock", "paper", "scissors")
wins=0
losses=0
ties=0
tries=0
running=True
while running:
    player=None
    computer=random.choice(options)
    while player not in options:
        player=input("Pick a choice: rock, paper, scissors? ").lower()
    print(f"computer: {computer}")
    print(f"player: {player}")
    if player==computer:
        print("It's a tie")
        ties+=1
    elif (player=="rock" and computer=="scissors") or (player=="paper" and computer=="rock") or (player=="scissors" and computer=="paper"):
        print("yayy! you win")
        wins+=1
    elif (player=="rock" and computer=="paper") or (player=="paper" and computer=="scissors") or (player=="scissors" and computer=="rock"):
        print("Oh no! you lose")
        losses+=1
    tries+=1
    print("Do you want to play again? (y/n)")
    answer=input().lower()
    if answer!="y":
        running=False
print("Thank you for playing!")
print(f"Final Score: Wins: {wins}, Losses: {losses}, Ties: {ties}, Tries: {tries}")