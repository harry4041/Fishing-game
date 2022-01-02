import random
import time
import sys

def delay_print(s, delay):
    for x in s:
        sys.stdout.write(x)
        sys.stdout.flush()
        time.sleep(delay)


class Player():
    def __init__(self):
        self.inventory = []
        self.rod = Rod(5, 1, 50) # Starter rod needs changing, made OP for testing
        self.money = 75 # changed for testing
        self.xp = 0


class Rod():
    def __init__(self, speed, rare_chance, value):
        self.speed = speed
        self.rare_chance = rare_chance
        self.value = value


class Fish():
    def __init__(self, value):
        self.value = value
        self.names = ["Lenny", "Mr.Limpet", "Nemo", "Spongebob", "Dory", "Oscar", "Harry", "Mr.Bubbles"]
        self.name = random.choice(self.names) + " fish"


class NotFish():
    def __init__(self):
        self.choices = ["Cardboard box", "Boot", "Tyre", "Plastic bottle"]
        self.name = random.choice(self.choices)
        self.value = self.item_value()

    def item_value(self):
        if self.name in self.choices[:(len(self.choices) // 2)]:
            return random.randint(1, 5)
        else:
            return random.randint(6, 10)


class DefoNotFish():
    def __init__(self):
        self.name = "Hand"
        self.value = 0

    def not_fish_response(self):
        print("Blub...")
        print("You got a...")
        time.sleep(1)
        delay_print("uhh... \n", 0.5)
        time.sleep(1)
        print("You got a " + self.name + ".")
