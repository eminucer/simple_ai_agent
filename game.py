
import random

class Maze:
    def __init__(self, dim, num_steps=7, num_wals=7):

        def is_stuck(passage, x, y):
            result = ((([x+1, y] in passage) or (max(x+1,y) >= dim)) and  
                    (([x-1, y] in passage) or (min(x-1,y) < 0)) and 
                    (([x, y+1] in passage) or (max(x,y+1) >= dim)) and
                    (([x, y-1] in passage) or (min(x,y-1) <0 )))
            return result

        treas_x0 = random.randint(0, dim-1)
        treas_y0 = random.randint(0, dim-1)

        x=x0=treas_x0
        y=y0=treas_y0

        passages = list()
        step_count = 0

        while step_count <= num_steps:
            step = random.randint(0, 3)
            if step == 0: # move right
                x = min(dim-1, x0+1)
            elif step == 1: # move left
                x = max(0, x0-1)
            elif step == 2: # move up
                y = min(dim-1, y0+1)
            elif step == 3: # move down
                y = max(0, y0-1)
        
            if [x,y] not in passages and [x,y] != [treas_x0, treas_y0]:
                passages.append([x,y])
                step_count += 1

            x0 = x
            y0 = y
                
        walls = list()
        wall_count = 0
        
        while wall_count <= num_wals:
            x0 = random.randint(0, dim-1)
            y0 = random.randint(0, dim-1)
            if [x0,y0] not in passages and [x0,y0] not in walls and  [x0,y0] != [treas_x0, treas_y0]:
                walls.append([x0,y0])
                wall_count += 1

        self.maze = {'dim' : dim,
                'walls' : walls,
                'treasure_pos' : [treas_x0, treas_y0],
                'passages' : passages,
                'player_pos' : passages[-1],
                'init_player_pos' : passages[-1],
                'discovered' : [passages[-1]],
                }
        

    def show(self, option = 'original'):
        str_maze = ""
        for y in range(self.maze['dim']-1, -1, -1):
            row = ""
            for x in range(self.maze['dim']):
                if ([x,y] not in self.maze['discovered']) and (option == 'player') :
                    row = row + " " + "?"
                else:
                    if [x,y] in self.maze['walls']:
                        row = row + " " + "#"
                    else:
                        if [x,y] == self.maze['treasure_pos']:
                            row = row + " " + "X"
                        elif [x,y] == self.maze['player_pos']:
                            row = row + " " + "o"
                        else:
                            row = row + " " + "_"
            str_maze = str_maze + "|" + row[1:] + "|\n"
        print(str_maze)
        return 0

    def move(self, direction):
        new_pos = self.maze['player_pos'].copy()
        result = 0

        if direction == 'up':
            new_pos[1] = self.maze['player_pos'][1] + 1
        elif direction == 'down':
            new_pos[1] = self.maze['player_pos'][1] - 1
        elif direction == 'right':
            new_pos[0] = self.maze['player_pos'][0] + 1
        elif direction == 'left':
            new_pos[0] = self.maze['player_pos'][0] - 1
        elif direction == 'hint':
            give_hint(self.maze)
            return 0 
        else:
            print('Enter a valid direction!')
            return result

        if (new_pos[0] < 0 or new_pos[0] >= self.maze['dim']) or (new_pos[1] < 0 or new_pos[1] >= self.maze['dim']):
            print("You are on the edge, can't move!")
        else:
            if new_pos in self.maze['walls']:
                print("You hit a wall, can't move!")
            else:
                if new_pos == self.maze['treasure_pos']:
                    print("You have found the treasure!")
                    result = 1
                else:
                    print(f'You moved {direction}!')
                    self.maze['player_pos'] = new_pos.copy()
            self.maze['discovered'].append(new_pos)
            
        return result

    def hint(self):
        filtered_passage = [elem for elem in self.maze['passages'] if elem not in self.maze['discovered']]
        if filtered_passage:
            random_hint = random.choice(filtered_passage)
            self.maze['discovered'].append(random_hint)
            print('A passage cleared!')
        else:
            print("All passages discovered!")

        return 0
