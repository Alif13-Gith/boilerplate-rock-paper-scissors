# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

import random
from collections import defaultdict

def player(prev_play, opponent_history=[]):
    ideal_response = {"R": "P", "P": "S", "S": "R"}

    if not hasattr(player, "my_history"):
        player.my_history = []
        player.ngram_freq = defaultdict(lambda: defaultdict(int))
        player.self_bigram_freq = defaultdict(int)
        player.strategy_score = defaultdict(int)
        player.last_guess = {}

    my_history = player.my_history
    ngram_freq = player.ngram_freq
    self_bigram_freq = player.self_bigram_freq
    strategy_score = player.strategy_score
    last_guess = player.last_guess

    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
        ngram_freq.clear()
        self_bigram_freq.clear()
        strategy_score.clear()
        last_guess.clear()

    if prev_play:
        opponent_history.append(prev_play)
        for name, guess in last_guess.items():
            if guess == ideal_response[prev_play]:
                strategy_score[name] += 1
            elif guess == prev_play:
                pass
            else:
                strategy_score[name] -= 1

        n = 4
        if len(opponent_history) > n:
            pattern = "".join(opponent_history[-(n + 1):-1])
            ngram_freq[pattern][opponent_history[-1]] += 1

    candidates = {}

    n = 4
    if len(opponent_history) >= n:
        pattern = "".join(opponent_history[-n:])
        if pattern in ngram_freq and ngram_freq[pattern]:
            predicted = max(ngram_freq[pattern], key=ngram_freq[pattern].get)
            candidates["ngram"] = ideal_response[predicted]

    if opponent_history:
        candidates["counter_last"] = ideal_response[opponent_history[-1]]

    if my_history:
        candidates["beat_kris"] = ideal_response[ideal_response[my_history[-1]]]

    if my_history:
        last10 = my_history[-10:]
        most_common_self = max(set(last10), key=last10.count)
        candidates["beat_mrugesh"] = ideal_response[ideal_response[most_common_self]]

    if my_history:
        last_move = my_history[-1]
        potential = [last_move + "R", last_move + "P", last_move + "S"]
        sub_scores = {k: self_bigram_freq[k] for k in potential if self_bigram_freq[k] > 0}
        if sub_scores:
            predicted_my_next = max(sub_scores, key=sub_scores.get)[-1]
        else:
            predicted_my_next = random.choice(["R", "P", "S"])
        abbey_predicted_move = ideal_response[predicted_my_next]
        candidates["beat_abbey"] = ideal_response[abbey_predicted_move]

    if not candidates:
        guess = random.choice(["R", "P", "S"])
    else:
        best_name = max(candidates, key=lambda k: strategy_score[k])
        guess = candidates[best_name]

    last_guess.clear()
    last_guess.update(candidates)

    if my_history:
        bigram = my_history[-1] + guess
        self_bigram_freq[bigram] += 1

    my_history.append(guess)
    return guess
