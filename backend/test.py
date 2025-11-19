from engine.equity import best_hand_rank, str_to_card
print(best_hand_rank([str_to_card("Ah"), str_to_card("Kh"),str_to_card("Qh"), str_to_card("Jh"),str_to_card("Th")]))
print(best_hand_rank([str_to_card("Ah"), str_to_card("2d"),str_to_card("3c"), str_to_card("4h"),str_to_card("5s")]))
