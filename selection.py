import sys
import neural_net as nn

best_riddles = nn.eval_riddles(sys.argv[1])
with open(sys.argv[1], "r") as f, open(sys.argv[2], "w") as out:
    i=0
    for line in f:
        chosen_riddle = best_riddles[i]
        print(chosen_riddle)
        out.write(chosen_riddle+"\n")
        i = i+1
