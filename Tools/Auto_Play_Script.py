#AI comparison script

import subprocess
import time
lstOfRatios = []
output_file_path = 'output.txt'
cmdFromUser = input("Enter the command you wish to run for AI Project: ")
for i in range(5):
    print("GAME SET#: " + str(i))
    total_games = 0
    victories = 0
    start_time = time.time()
    while total_games < 100:
        interset_start_time = time.time()

        # Replace 'your_cmd_line_command' with the actual command you use in the command prompt
        cmd_line_command = cmdFromUser#'python3 AI_Runner.py 8 8 3 l ../src/checkers-python/main.py ./Sample_AIs/Random_AI/main.py'

        # Run the command and capture the output
        result = subprocess.run(cmd_line_command, shell=True, stdout=subprocess.PIPE, text=True)

        # Access the output of the command
        output = result.stdout
        if total_games == 0:
            with open('output.txt', 'w') as output_file:
                output_file.write(output)
        else:
            with open('output.txt', 'a') as output_file:
                output_file.write(output)

        # Process the output as needed
        # print("Output from the subprocess:")
        # print("1" if "player 1 wins" in output else "2")

        # if "player 1 wins" in output or "Tie" in output:
        #     victories += 1
        #     total_games += 1
        #     # print("Current Victory Ratio: " + str(victories) + "/" + str(total_games))
        # else:
            # total_games += 1
        total_games+=1
        interset_end_time = time.time()
        print("Game " + str(total_games) + " time: " + str((interset_end_time - interset_start_time)))

    with open('output.txt','r') as readingFile:
        for line in readingFile:
            if "player 1 wins" in line or "Tie" in line:
                victories += 1
            # total_games += 1
    end_time = time.time()
    print("Time Taken: " + str(end_time - start_time))
    print("Average Time per game: " + str((end_time - start_time)/100))
    print("Ratio of wins/total games: " + str(victories) + "/" + str(total_games))      
    lstOfRatios.append(str(victories) + "/" + str(total_games)) 
print(lstOfRatios)
    # print("Time: " + str(end_time))