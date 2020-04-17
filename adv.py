from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
# world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# e.g. traversal_path = ['n', 'n']

directions = ['n', 'e', 's', 'w']
def change_direction(direction, num): 
    # clockwise
    return directions[(directions.index(direction) + num) % len(directions)]

# initial values
traversal_path = []
visited_rooms = {}
exit = player.current_room.get_exits()[0] # a random possible exit

while len(visited_rooms) < 500: # early stop
    # find new direction
    exits = player.current_room.get_exits() # get all possible exits
    exit, entry, next_room = change_direction(exit, 2), None, None
    while exit not in exits or next_room is None \
    or (next_room.id in visited_rooms and visited_rooms[next_room.id] != entry):
        exit = change_direction(exit, 1)
        entry = change_direction(exit, 2)
        next_room = player.current_room.get_room_in_direction(exit)

    # log and move
    traversal_path.append(exit)
    visited_rooms[player.current_room.id] = exit
    player.travel(exit)


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
