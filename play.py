import google.generativeai as genai
from game import Maze

GOOGLE_API_KEY='YOUR API KEY'

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

system_promt = """You will be coordinating a little game called 'Find the Treasure'. The user will be put in a maze at a random position. Some passages in the maze are blocked by walls. There is a hidden thresure in the maze. 
The game is over when the user finds the treasure. At the beginning of each tour, the user will be asked what they want to do next. Do your best to understand their intend and categorize it as one of the following options.
1) If they want to move in a direction, generate the following text 'maze.move(<direction>)' where <direction> is the string direction that they want to move in (up, down, left or right). Make sure <direction> is in quotations. 
2) If they want some help, generate the following text 'maze.hint()'.
3) If they want to see the maze, generate the following text 'maze.show(option='player')'.
4) If their response is irrelavent to any of the above, remind them where they are and why they are here and ask them what they want to do spesifically again. Tell them about their options.
Begin!
"""

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              system_instruction=[system_promt])

maze = Maze(5)
result = 0
while True:
    user_promt = input("Your input >> ")
    response = model.generate_content([user_promt])
    if response.text.split('.')[0] == 'maze':
        try:
            result = eval(response.text)
        except:
            print("Invalid operation")
    else:
        print("Response: >>", response.text)

    if result:
        break

