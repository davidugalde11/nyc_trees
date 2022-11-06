import random


major_arcana = {
    0: ["The Fool", 1],
    1: ["The Magician", 1],
    2: ["The High Priestess", 1],
    3: ["The Empress", 1],
    4: ["The Emperor", 0],
    5: ["The Hierophant", 0],
    6: ["The Lovers", 1],
    7: ["The Chariot", 0],
    8: ["Strength", 1],
    9: ["The Hermit", 0],
    10: ["The Wheel of Fortune", 0],
    11: ["Justice", 0],
    12: ["The Hanged Man", -1],
    13: ["Death", -2],
    14: ["Temperance", 1],
    15: ["The Devil", -2],
    16: ["The Tower", -2],
    17: ["The Star", 1],
    18: ["The Moon", -1],
    19: ["The Sun", 2],
    20: ["Judgement", 0],
    21: ["The World", 1]


                }

#Minor Arcana



def get_card():
    return random.randint(0,21)

def calculate_fortune(past, present, future):
    sum = past[1] + present[1] + future[1]
    if sum > 1:
        return "Great Fortune!"
    elif sum < -1:
        return "Bad Fortune"
    else:
        return "Neutral Fortune"




def get_fortune():
    name = input("What is your name? ")
    past = major_arcana[get_card()]
    present = major_arcana[get_card()]
    future = major_arcana[get_card()]
    print(f"{name} these are your cards.\nPast: {past[0]}\nPresent: {present[0]}\nFuture: {future[0]}\n")
    print(calculate_fortune(past, present, future))



get_fortune()