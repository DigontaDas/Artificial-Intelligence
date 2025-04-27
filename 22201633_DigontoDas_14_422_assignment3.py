#########################################################    TASK-1    ##################################################################################################################
import math
import random

def game(starting_player, Magnus_base, caruana_base, game_num):
    if game_num is None: #if carlson starts next time caruana will go next and then carlson
        game_num = starting_player
    #assign max and min players based on current game number
    if game_num == 0:  # Carlsen starts
        maxV = Magnus_base
        minV = caruana_base
        next_game = 1  
        max_player = "Magnus Carlsen"
        min_player = "Fabiano Caruana"
    else:  # Caruana starts
        maxV = caruana_base
        minV = Magnus_base
        next_game = 0  
        max_player = "Fabiano Caruana"
        min_player = "Magnus Carlsen"

    tree_depth = 5
    alpha = float('-inf')
    beta = float("inf")
    alpha_beta = minimax(tree_depth, True, maxV, minV, alpha, beta)
 
    if alpha_beta > 0:
        winner = max_player 
        winner_type = "Max"
    elif alpha_beta < 0:
        winner = min_player  
        winner_type = "Min"
    else:
        winner = "Draw"
        winner_type = "Draw"
    
    return winner, winner_type, alpha_beta, next_game

def minimax(depth, current_max, maxV, minV, alpha, beta):
    if depth == 0:
        return utility_func(maxV, minV)
    else:
        if current_max == True:
            max_player = float('-inf')
            for i in range(2):
                turn = minimax(depth - 1, False, maxV, minV, alpha, beta)
                max_player = max(max_player, turn)
                alpha = max(alpha, turn)
                if beta <= alpha:
                    break
            return max_player
        else:
            min_player = float("inf")
            for j in range(2):
                turn = minimax(depth - 1, True, maxV, minV, alpha, beta)
                min_player = min(min_player, turn)
                beta = min(beta, turn)
                if beta <= alpha:
                    break
            return min_player
        
def strength_func(x):
    strength = math.log2(x + 1) + (x / 10)
    return strength

def utility_func(maxv, minv):
    i = random.choice([0, 1])

    utility = strength_func(maxv) - strength_func(minv) + ((-1) ** i * (random.randrange(0, 10) / 10))
    return utility

def count_game(game_results):
    magnus = 0
    caruana = 0
    draw = 0
    for result in game_results:
        winner = result[0]
        if winner == "Magnus Carlsen":
            magnus += 1
        elif winner == "Fabiano Caruana":
            caruana += 1
        else:
            draw += 1
    return magnus, caruana, draw


game_player = int(input("Enter starting player for game 1 (0 for Carlsen, 1 for Caruana): "))
Magnus_base = int(input("Enter base strength for Carlsen: "))
Caruana_base = int(input("Enter base strength for Caruana: "))

result = []
current_game = None
for num in range(4):
    winner, winner_type, utility_value, current_game = game(game_player, Magnus_base, Caruana_base, current_game)
    result.append((winner, utility_value))
    print(f"Game {num+1} Winner: {winner} ({winner_type}) (Utility value: {utility_value:.2f})")

magnus_wins, caruana_wins, draws = count_game(result)
print("\nOverall Results:")
print(f"Magnus Carlsen Wins: {magnus_wins}")
print(f"Fabiano Caruana Wins: {caruana_wins}")
print(f"Draws: {draws}")

if magnus_wins > caruana_wins:
    print("Overall Winner: Magnus Carlsen")
elif caruana_wins > magnus_wins:
    print("Overall Winner: Fabiano Caruana")
else:
    print("Overall Winner: Draw")

##########################################################    TASK-2    ##################################################################################################################

import math
import random

def strength(x):
    power = math.log2(x + 1) + x / 10
    return power

def utility_func(max_player_rating, min_player_rating):
    utility = strength(max_player_rating) - strength(min_player_rating) + (-1) ** random.choice([0, 1]) * (random.randrange(0, 10) / 10)
    return utility

def minimax(depth, maxV, minV, alpha, beta, current_max):
    if depth == 0:
        return utility_func(maxV, minV)
    else:
        if current_max == True:
            max_player = float('-inf')
            for i in range(2):
                turn = minimax(depth - 1, False, maxV, minV, alpha, beta)
                max_player = max(max_player, turn)
                alpha = max(alpha, turn)
                if beta <= alpha:
                    break
            return max_player
        else:
            min_player = float("inf")
            for j in range(2):
                turn = minimax(depth - 1, True, maxV, minV, alpha, beta)
                min_player = min(min_player, turn)
                beta = min(beta, turn)
                if beta <= alpha:
                    break
            return min_player

def minimax_with_mc(depth, max_rating, min_rating, alpha, beta, current_max):

    if depth == 0:
        return utility_func(max_rating, min_rating)

    if current_max==True:  #for true part
        max_val = float('-inf')
        for i in range(2):  
            turn = minimax_with_mc(depth - 1, max_rating, min_rating, alpha, beta, False)
            max_val = max(max_val, turn)
            alpha = max(alpha, turn)
            if alpha >= beta:
                break
        return max_val
    else:  #for false part
        max_val = float('-inf')  
        for i in range(2):  
            turn = minimax_with_mc(depth - 1, max_rating, min_rating, alpha, beta, True)
            max_val = max(max_val, turn)  
            alpha = max(alpha, turn)
            if alpha >= beta:
                break
        return max_val  

starting_player = int(input("Enter who goes first (0 for Light, 1 for L): "))
mc_cost = float(input("Enter the cost of using Mind Control: "))
light_str = float(input("Enter base strength for Light: "))
l_str= float(input("Enter base strength for L: "))
    

if starting_player == 0: 
    max_rating = light_str
    min_rating = l_str
    max_player_name = "Light"
    min_player_name = "L"
else: 
    max_rating = l_str
    min_rating = light_str
    max_player_name = "L"
    min_player_name = "Light"
    
alpha=float('-inf')
beta=float('inf')
depth = 5 

value_without_mc= minimax(depth, max_rating, min_rating,alpha ,beta , True)
value_with_mc = minimax_with_mc(depth, max_rating, min_rating, alpha,beta, True )
after_incurring = value_with_mc - mc_cost

print(f"Minimax value without Mind Control: {value_without_mc:.2f}")
print(f"Minimax value with Mind Control: {value_with_mc:.2f}")
print(f"Minimax value with Mind Control after incurring the cost: {after_incurring:.2f}")
if starting_player==0:
    if value_without_mc>0 and after_incurring>=0:
        print("Light should NOT use Mind Control as the position is already winning.")
    elif value_without_mc>0 and after_incurring<0:
        print("Light should NOT use Mind Control as it backfires.")
    elif value_without_mc<0 and after_incurring>=0:
        print("Light should use Mind Control.") 
    elif value_without_mc<0 and after_incurring<0:
        print("Light should NOT use Mind Control as the position is losing either way.")
else:
    if value_without_mc>0 and after_incurring>=0:
        print("L should NOT use Mind Control as the position is already winning.")
    elif value_without_mc>0 and after_incurring<0:
        print("L should NOT use Mind Control as it backfires.")
    elif value_without_mc<0 and after_incurring>=0:
        print("L should use Mind Control.") 
    elif value_without_mc<0 and after_incurring<0:
        print("L should NOT use Mind Control as the position is losing either way.")





