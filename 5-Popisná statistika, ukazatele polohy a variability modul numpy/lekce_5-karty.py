import itertools

#suits = ("Club", "Diamond", "Heart", "Spade")
suits = ("♣", "♦", "♥", "♠")
ranks = (1, 2, 3, 4, 5, 7, 8, 9, "J", "Q", "K", "A")

list_of_cards = list(itertools.product(suits, ranks))

for item in list_of_cards:
  print(f"{item[0]} {item[1]}")