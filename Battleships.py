from random import randint,choice


def is_sunk(ship):
    '''Returns Bool. True if ship is sunk, False otherwise'''
    if len(ship[4]) < ship[3]:
        return False
    else:
        return True

def ship_type(ship):
   '''Returns ship type as string to identify the ship.'''
   d = {4: "battleship", 3:"cruiser", 2:"destroyer", 1:"submarine"}
   if ship[3] in d:
       return d[ship[3]]

fleetcoords =[]

def is_open_sea(row, column, fleet):
    '''Checks if the square given by row,column neither contains or is adjacent to
    a ship in the fleet. Returns Bool, False is square occupied or adjacent to another ship,
    True otherwise.'''

    # first section creates a list of all the co-ordinates of the fleet
    rc = (row, column)
    for ship in fleet:
        if ship[2] == True:
            for i in range(ship[3]):
                colref = ship[1] + i
                rowcol = (ship[0], colref)
                fleetcoords.append(rowcol)
        if ship[2] == False:
            for i in range(ship[3]):
                rowref = ship[0] + i
                rowcol = (rowref, ship[1])
                fleetcoords.append(rowcol)

    #set result to True to return if square not in fleet or in adjacent sqaures
    result = True
    if rc in fleetcoords:
        #square already occupied by ship in fleet
        result =  False

    elif rc not in fleetcoords:
        #checking for adjacencies. If found returns false. if not continues until done, returns True
        for s in fleetcoords:
            if (row - 1 == s[0] and column - 1 == s[1]) or \
                    (row + 1 == s[0] and column + 1 == s[1]):
                result =  False
                break
            elif (row - 1 == s[0] and column + 1 == s[1]) or \
                    (row + 1 == s[0] and column - 1 == s[1]):
                result = False
                break
            elif (row == s[0] and column + 1 == s[1]) or \
                    (row == s[0] and column - 1 == s[1]):
                result =  False
                break
            elif (row + 1 == s[0] and column == s[1]) or \
                    (row - 1 == s[0] and column == s[1]):
                result = False
                break
    return result


fleet = []

def ok_to_place_ship_at(row, column, horizontal, length, fleet):
    '''checks of addition of referenced ship to the fleet results in legal placement.
    Returns True if placement is legal, False otherwise. Uses is_open-sea function'''

    result = True
    #checking if row,col is_open_sea is True, don't continue if not.
    if is_open_sea(row,column, fleet) == False:
        result = False
    #checking if length of ship exceeds playing grid
    elif horizontal is False and (row + length) > 9:
        result = False
    elif horizontal is True and (column + length) > 9:
        result = False
    else:
        #checking each subsequent co-ordinate of the ship
        for i in range(length-1):
            if horizontal is False:
                row = row+1
                if is_open_sea(row, column, fleet) == True:
                    result = True
                if is_open_sea(row, column,fleet) == False:
                    result = False
                    break
            if horizontal is True:
                column = column+1
                if is_open_sea(row, column,fleet) == True:
                    result = True
                if is_open_sea(row, column,fleet) == False:
                    result = False
                    break
    return result

def place_ship_at(row, column, horizontal, length, fleet):
    '''Returns a new fleet that is the result of adding referenced ship to
    the fleet. '''
    shipToPlace = (row, column,horizontal,length,set())
    fleet.append(shipToPlace)
    return fleet


d = {"battleship":4, "cruiser":3, "destroyer":2, "submarine": 1}
startfleet= ["battleship", 'cruiser', 'cruiser', 'destroyer','destroyer','destroyer','submarine','submarine','submarine','submarine']

def randomly_place_all_ships():
    '''Returns a fleet that is the result of a random legal arrangement
    of 10 ships in the ocean. Uses ok_to_place_ship_at (returns True or False)
    and uses place_ship_at (returns new fleet after adding ship).'''
    for ship in startfleet:
       findplace = True
       while findplace is True:
           row = randint(0, 9)
           column = randint(0, 9)
           horizontal = choice([True, False])
           length = d[ship]
           if ok_to_place_ship_at(row, column, horizontal, length, fleet) is False:
               findplace = True

           elif ok_to_place_ship_at(row, column, horizontal, length, fleet) is True:
               findplace = False
               place_ship_at(row, column, horizontal, length, fleet)
    return fleet

fleetcoords2 = []  # consider whether can re use fleetcoords from setting up the ships again here.

def check_if_hits(row, column, fleet):
    ''' returns Bool. True if row,column entered hits a ship in the fleet
    False otherwise.'''
    result = True
    # makes list of all co-ordinates occupied by ships in the fleet
    rc = (row, column)
    for ship in fleet:
        if ship[2] == True:
            for i in range(ship[3]):
                colref = ship[1] + i
                rowcol = (ship[0], colref)
                fleetcoords2.append(rowcol)
        if ship[2] == False:
            for i in range(ship[3]):
                rowref = ship[0] + i
                rowcol = (rowref, ship[1])
                fleetcoords2.append(rowcol)

    if rc not in fleetcoords2:  # a miss
        result = False

    elif rc in fleetcoords2:    # an already hit location = a miss
        for ship in fleet:
            if rc in ship[4]:
                result = False
                break

    return result

def hit(row, column, fleet):
    '''Returns a tuple of fleet and ship. Where the returned fleet is the result of a hit on the fleet
    and ship is resulting ship after the hit'''
    rc = (row, column)
    hitship = ()
    for ship in fleet:
        if ship[2] == True:
            for i in range(ship[3]):
                colref = ship[1] + i
                rowcol = (ship[0], colref)
                if rowcol == rc:
                    ship[4].add(rc)
                    hitship = ship
                    break
        if ship[2] == False:
            for i in range(ship[3]):
                rowref = ship[0] + i
                rowcol = (rowref, ship[1])
                if rowcol == rc:
                    ship[4].add(rc)
                    hitship = ship
                    break
    return fleet, hitship

def are_unsunk_ships_left(fleet):
    '''Returns Bool. True if there are ships still not sunk,
    False otherwise/all ships are sunk'''
    result = True
    for ship in fleet:
        if ship[3] > len(ship[4]):
            result = True
            break  # once one unsunk ship is found, no need to continue
        else:
            result = False

    return result

def main():
    print("Welcome to Battleships!")
    print("You can enter q to quit at any time.")
    player = str(input("Enter your Name: "))
    current_fleet = randomly_place_all_ships()
    game_over = False
    shots = 0

    while not game_over:
        loc_str = input("Enter row and column to shoot (separated by space): ").split()
        if loc_str[0].lower() == "q":
            print("OK, quitting game!")
            break

        try:
            current_row = int(loc_str[0])
            current_column = int(loc_str[1])
            shots += 1

            if loc_str == "q": game_over = True

            if (current_row or current_column) > 9 or (current_row or current_column) < 0:
                raise IndexError

            if check_if_hits(current_row, current_column, current_fleet):
                print("You have a hit!")
                (current_fleet, ship_hit) = hit(current_row, current_column, current_fleet)
                if is_sunk(ship_hit):
                    print("You sank a " + ship_type(ship_hit) + "!")
            else:
                print("You missed!")

        except IndexError:
            print("Please only enter numbers between 0 and 9. ")
        except ValueError:
            print("Please only enter numbers between 0 and 9. ")
        except KeyboardInterrupt:
            print("Please only enter numbers between 0 and 9. ")
        except Exception:
            print("Please only enter numbers between 0 and 9. ")

        if not are_unsunk_ships_left(current_fleet): game_over = True

    print("Well done", player,"! Game over! You required", shots, "shots.")

if __name__ == '__main__': #keep this in
   main()
