import random
from ast import literal_eval

from player import Player
from room import Room
from world import World

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
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# e.g. traversal_path = ['n', 'n']
traversal_path = []

##########################################################################
# Solution
##########################################################################
# helper function
directions = ['n', 'e', 's', 'w']
def change_direction(direction, num): 
    # clockwise
    return directions[(directions.index(direction) + num) % len(directions)]

# initial values
rooms_visited = dict() # e.g.{0:'w', 7:'w', ...}
exits_not_visited = dict()
current_loop = []
loops = []             # e.g. [current_loop, ...]

exit = player.current_room.get_exits()[0] # get a random possible exit
moves = [(None, exit)]

count = 0
while len(rooms_visited) < 500 and count < 2000: # early stop
    # current values
    exits = player.current_room.get_exits() # get all possible exits
    entry, next_entry, next_room = change_direction(exit, 2), None, None 
    exit = entry

    # if exit is not valid, find a new direction
    while exit not in exits or next_room is None:
        exit = change_direction(exit, 1)
        next_entry = change_direction(exit, 2) # e.g. if exit current room at 'e', you will enter next room at 'w'.
        next_room = player.current_room.get_room_in_direction(exit)

    # get exits not visited yet
    if player.current_room.id not in exits_not_visited:
        exits_not_visited[player.current_room.id] = exits
    l = exits_not_visited[player.current_room.id]
    if entry in l: l.remove(entry)
    if exit in l: l.remove(exit)
    exits_not_visited[player.current_room.id] = l

    # handle a loop: if exit and enter the room at different exits, it is a loop.
    if next_room is not None and next_room.id in rooms_visited \
    and rooms_visited[next_room.id] != next_entry:
        print(f'There is a loop starting at {next_room.id} ending at {player.current_room.id}!')
        # get all exits in the loop that are visited
        # check whether all exits in the loop are visited
        current_loop, move = [(player.current_room.id, exit)], (None, None)
        flag_all_visited = True
        for i in range(-1, -1-len(moves), -1):
            r, e = moves[i]
            current_loop.insert(0, moves[i])
            if r != next_room.id:
                if exits_not_visited[r]:
                    flag_all_visited = False
            else:
                break
        
        # print(f'current loop: {current_loop}')
        # print(f'visited rooms: {rooms_visited}')
        # print(f'exits not visited: {exits_not_visited}')

        # if not all exits in the loop are visited, go back to the beginning of the loop
        if flag_all_visited == False:
            loops.append(current_loop) # store the current loop information
            while move[0] != next_room.id:
                move = moves.pop() # remove move history
                rooms_visited.pop(move[0], None) # remove room visit history accordingly
            player.travel(exit)
            exit = moves[-1][1]
            continue

    # if the move is part of current loop, visit the non-loop exit first
    if (player.current_room.id, exit) in current_loop:
        if player.current_room.id == current_loop[0]: # at the beginning of the loop
            continue
        else: # at some other vertex of the loop
            if player.current_room.id in exits_not_visited:
                l = exits_not_visited[player.current_room.id]
                if l: exit = l.pop()

    # log and move
    rooms_visited[player.current_room.id] = exit
    moves.append((player.current_room.id, exit))
    player.travel(exit)

    count += 1
traversal_path = [m[1] for m in moves[1:]]

##########################################################################
# TRAVERSAL TEST
##########################################################################
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room.id)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room.id)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms:")
    print([r for r in range(500) if r not in visited_rooms])

##########################################################################
# UNCOMMENT TO WALK AROUND
##########################################################################
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
