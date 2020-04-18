from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import defaultdict

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# e.g. traversal_path = ['n', 'n']
traversal_path = []

# Solution
directions = ['n', 'e', 's', 'w']
def change_direction(direction, num): 
    # clockwise
    return directions[(directions.index(direction) + num) % len(directions)]

# initial values
visited_rooms = {}
moves = []
loops = defaultdict(list)
exit = player.current_room.get_exits()[0] # a random possible exit

count = 0
while len(visited_rooms) < 500 and count < 20: # early stop
    # find new direction
    exits = player.current_room.get_exits() # get all possible exits
    exit, entry, next_room, isloop = change_direction(exit, 2), None, None, False
    while exit not in exits or next_room is None:
        exit = change_direction(exit, 1)
        entry = change_direction(exit, 2)
        next_room = player.current_room.get_room_in_direction(exit)

        # find a loop
        if next_room is not None \
        and (next_room.id in visited_rooms and visited_rooms[next_room.id] != entry):
            print('there is a loop!')
            isloop = True
            break
    
    # handle a loop
    if isloop == True:
        loops[next_room.id] = list()
        for move in moves[::-1]:
            loops[next_room.id].insert(0, move)
            if move[0] == next_room.id:
                break
        print(f'loops: {loops[next_room.id]}')
        # remove visited rooms
        for move in loops[next_room.id][1:]:
            del visited_rooms[move[0]]
        print(f'visited rooms: {visited_rooms}')

    # log and move
    visited_rooms[player.current_room.id] = exit
    moves.append([player.current_room.id, exit])
    player.travel(exit)

    count += 1


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
