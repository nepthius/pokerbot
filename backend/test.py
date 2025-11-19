from engine.equity import simulate_equity, str_to_card

hero = [str_to_card("Ah"), str_to_card("Kh")]
board = [str_to_card("Qh"), str_to_card("Jh"), str_to_card("3c")]
win, tie, lose = simulate_equity(hero, board, o=1, t=5000)
print("Win:", round(win*100,2), "Tie:", round(tie*100,2), "Lose:", round(lose*100,2))