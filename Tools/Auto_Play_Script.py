#AI comparison script

import subprocess
import time
lstOfRatios = []
for i in range(10):
    print("GAME #: " + str(i))
    total_games = 0
    victories = 0
    start_time = time.time()
    while total_games < 100:

        # Replace 'your_cmd_line_command' with the actual command you use in the command prompt
        cmd_line_command = 'python3 AI_Runner.py 8 8 3 l ../src/checkers-python/main.py ./Sample_AIs/Random_AI/main.py'

        # Run the command and capture the output
        result = subprocess.run(cmd_line_command, shell=True, stdout=subprocess.PIPE, text=True)

        # Access the output of the command
        output = result.stdout

        # Process the output as needed
        # print("Output from the subprocess:")
        # print("1" if "player 1 wins" in output else "2")

        if "player 1 wins" in output or "Tie" in output:
            victories += 1
            total_games += 1
            # print("Current Victory Ratio: " + str(victories) + "/" + str(total_games))
        else:
            total_games += 1

    end_time = time.time()
    print("Ratio of wins/total games: " + str(victories) + "/" + str(total_games))
    lstOfRatios.append(str(victories) + "/" + str(total_games))
    print(lstOfRatios)
    # print("Time: " + str(end_time))