import random
import sched
import time
from FishingClasses import *

times_fished = 0

countdown = sched.scheduler(time.time, time.sleep)

"""
TODO:
An escape button to go back to what_next at any time
Add fish freshness to fish class to change value over time
Next story beat (currently in the shop)
Pacing/reduce walls of text
Currency balancing
"""

def shop_inv():
    print("Shop money: " + str(shop.money))
    print("Shop inventory: ")
    for x in range(len(shop.inventory)):
        if isinstance(shop.inventory[x], Rod):
            print(x, "Rod :-", "Speed:", shop.inventory[x].speed, "Rarity chance:", shop.inventory[x].rare_chance, "value:", shop.inventory[x].value)
        else:
            print(x, shop.inventory[x].name, shop.inventory[x].value)


def player_inv():
    print("Player money: " + str(player.money))
    print("Player inventory: ")
    for x in range(len(player.inventory)):
        print(x, player.inventory[x].name + ": " + str(player.inventory[x].value))


def item_or_fish():
    random_number = random.randint(1, 10)
    if random_number < 8:
        return Fish((player.rod.rare_chance * random.randint(2, 4)), )
    else:
        return NotFish()


def fishing_timer():
    if player.rod.speed > 0:
        print("Blub blub...")
        player.rod.speed = player.rod.speed - 1
        countdown.enter(1, 1, fishing_timer)
    elif player.rod.speed == 0:
        player.rod.speed = holding_player_rod_speed


def fish():
    global times_fished
    countdown.enter(1, 1, fishing_timer)
    countdown.run()
    print("Blub...") 
    a = item_or_fish()
    print("You got a..." + a.name + " worth " + str(a.value))
    keep = input("Would you like to keep it? Y/N \n")
    if keep.upper() == "Y":
        player.inventory.append(a)
        for x in range(len(player.inventory)):
            print(player.inventory[x].name + ": " + str(player.inventory[x].value))
    else:
        print("You threw it back in...")
    times_fished = times_fished + 1
    what_next()
    

def odd_fish():
    global times_fished
    odd_object = DefoNotFish()
    odd_object.not_fish_response()
    player.inventory.append(odd_object)
    times_fished = times_fished + 1
    what_next()


class Shop():
    def __init__(self):
        self.inventory = [Rod(player.rod.speed - 1, player.rod.rare_chance + 2, player.rod.value * 2)]
        self.money = 50

    def update_rod(self):
        if player.rod.speed > 0:
            self.inventory.insert(0, Rod(player.rod.speed - 1, player.rod.rare_chance + 2, player.rod.value * 2))


def shopping():
    buy_sell = input("HeLlO dEaRy. 's'ell/'b'uy/'r'eturn \n")
    if buy_sell.upper() == "S":
        selling()
    if buy_sell.upper() == "B":
        buying()
    if buy_sell.upper() == "R":
        what_next()


def selling():
    # Annoyingly cant use the player_inv function here
    # as need the x value from the for loop
    print("Player money: " + str(player.money))
    print("Shop money: " + str(shop.money))
    print("Player inventory: ")
    for x in range(len(player.inventory)):
        print(x, player.inventory[x].name + ": " + str(player.inventory[x].value))
    to_sell = input("WhAt Ya FlOgGiN'?! (Type the number or 'r' to return) \n")
    if str(to_sell).upper() == "R":
        what_next()
    elif int(to_sell) >= len(player.inventory):
        print("TrY aGaIn!")
        what_next()
    elif player.inventory[int(to_sell)].value == 0:
        print("NEXT STORY BEAT") # NEXT STORY BEAT
    elif player.inventory[int(to_sell)].value <= shop.money:
        to_sell = int(to_sell)
        print("You sold " + str(player.inventory[to_sell].name))
        shop.inventory.append(player.inventory[to_sell])
        shop.money = shop.money - player.inventory[to_sell].value
        player.money = player.money + player.inventory[to_sell].value
        player.inventory.pop(to_sell)
        shop_inv()
        player_inv()
        shopping()


def buying():
    # Annoyingly cant use the shop_inv function here
    # as need the x value from the for loop
    print("Player money: " + str(player.money))
    print("Shop money: " + str(shop.money))
    print("Shop inventory: ")
    for x in range(len(shop.inventory)):
        if isinstance(shop.inventory[x], Rod):
            print(x, "Rod :-", "Speed:", shop.inventory[x].speed, "Rarity chance:", shop.inventory[x].rare_chance, "value:", shop.inventory[x].value)
        else:
            print(x, shop.inventory[x].name, shop.inventory[x].value)
    to_buy = input("CoMe To SeE mE wArEs?! (Type the number or 'r' to return) \n")
    if str(to_buy).upper() == "R":
        what_next()
    elif int(to_buy) >= len(shop.inventory):
        print("cant do dat")
        what_next()
    elif shop.inventory[int(to_buy)].value <= player.money:
        to_buy = int(to_buy)
        if isinstance(shop.inventory[to_buy], Rod):
            player.rod = shop.inventory[int(to_buy)]
            print("You bought a rod with speed of ", str(shop.inventory[to_buy].speed), ", a rare chance of ", str(shop.inventory[to_buy].rare_chance), " and a value of ", str(shop.inventory[to_buy].value), ".")
            shop.money = shop.money + shop.inventory[to_buy].value
            player.money = player.money - shop.inventory[to_buy].value
            shop.inventory.pop(to_buy)
            shop.update_rod()
            what_next()
        else:
            print("You bought " + str(shop.inventory[to_buy].name))
            player.inventory.append(shop.inventory[to_buy])
            player.money = player.money - shop.inventory[to_buy].value
            shop.money = shop.money + shop.inventory[to_buy].value
            shop.inventory.pop(to_buy)
            shop_inv()
            player_inv()
            shopping()
    else:
        print("YoU dOn'T hAvE tHe CoIn Me DeAr!")
        what_next()
    
    
def what_next():
    global times_fished
    next = input("What would you like to do next? ('h' for all options) \n")
    if next.upper() == "H":
        print("'f' to fish")
        print("'i' to see inventory")
        print("'r' to see rod")
        print("'s' to shop")
        what_next()
    elif next.upper() == "F":
        if times_fished != 3: # Changed for debugging
            fish()
        else:
            odd_fish()
    elif next.upper() == "I":
        player_inv()
        what_next()
    elif next.upper() == "R":
        print("Your rods speed is: " + str(player.rod.speed))
        print("Your rods rare chance is : " + str(player.rod.rare_chance))
        print("Your rods value is : " + str(player.rod.value))
        what_next()
    elif next.upper() == "S":
        shopping()
    else:
        print("Woops! That wasn't one of the options!")
        what_next()


print("Hello, and welcome to my fishing game!")
print("""
 _   __/\__     o
| \_/    o \   o 
 > _  ((  -< oo  
|_/ \__  __/      
       |/
""")
print("The game is simple:")
print("Fish!")
print("Sell!")
print("Buy better rods to speed up fishing time and increase your chances of getting a higher value fish!")
print("Fish some more! \n")
print("How to play:")
print("TYPE THE APPROPRIATE LETTER FROM THE LIST OF LETTER PROMPTS \n")
input("Press enter key to play!")
player = Player()
shop = Shop()
holding_player_rod_speed = player.rod.speed
fish()





        

        
        
