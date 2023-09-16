import os
import sys
import gd 
import time
import math
version = 'v2.0.1'

def deathLogger():
    os.system('cls')
    try:
        memory = gd.memory.get_memory() # this enables the program to read GD's memory values
        gdOpen = True
    except RuntimeError:
        print('Open Geometry Dash before selecting this option!')
        print('Returning to menu in 3 seconds...')
        time.sleep(3)
        gdOpen = False
    
    if gdOpen == True:
        os.system('cls')
        
        while True:
            try:
                print('Respawn time (sec)')
                respawnTime = float(input('[this is important to prevent missed deaths]: ')) - 0.1 # makes sure it notices EVERY time you die
                os.system('cls')
            except ValueError:
                os.system('cls')
                print('Invalid input.')
                time.sleep(1)
                os.system('cls')
            else:
                break
            
        
        print('Choose a name for the .txt file recording your deaths.')
        print('If you already have a file you want to continue with, input that instead.')
        print('If it is a locally created level, PLEASE make sure this exactly matches the level name ingame!')
        
        while True:
            print()
            filename = input('File name: ')
            if filename != '': # so the user doesn't just input something blank
                break
            
        # Connects to the levels directory, makes directory if fails
        try:
            os.mkdir('levels')
            parentDirectory = fr'{os.getcwd()}\levels'
            os.chdir(parentDirectory)
        except FileExistsError:
            parentDirectory = fr'{os.getcwd()}\levels'
            os.chdir(parentDirectory)
                
        os.system('cls')
        
        if not os.path.exists(fr'{parentDirectory}\{filename}.txt'): # if the text file doesn't already exist
            while True:
                try:
                    levelID = int(input('Input level ID (input "0" for a created level): '))
                    os.system('cls')
                except ValueError:
                    continue
                else:
                    break
            
            print('At what percentage do you want to record deaths?')
            print('Integer between 0-99.')
                
            while True:
                print()
                perSpecified = int(input('Percentage: '))
                if 0 <= perSpecified <= 99:
                    break
            
            with open(f'{filename}.txt', 'a') as file:
                file.write(f'Level ID: {levelID}\n')
                file.write(f'DEATHS PAST {perSpecified}%:\n')
            os.system('cls')
                
        if os.path.exists(fr'{parentDirectory}\{filename}.txt'):
            with open(f'{filename}.txt', 'r') as file:
                lines = file.readlines()
                levelID = int(lines[0].lstrip('Level ID: ').rstrip('\n'))
                perSpecified = int(lines[1].lstrip('DEATHS PAST ').rstrip('%:\n'))
            print('Logging deaths... (do not close this window until done playing)')
            
            recorded_death = False # Initializing the flag for if the program recorded something
            
            while True:
                time.sleep(respawnTime)
                
                if memory.is_dead() and memory.get_percent() >= perSpecified and not memory.is_practice_mode() and recorded_death == False:
                    if memory.level_id == levelID and levelID != 0:
                        with open(f'{filename}.txt', 'a') as file:
                            file.write(f'{math.floor(memory.get_percent())}\n')
                            recorded_death = True
                    
                    if memory.level_id == levelID and levelID == 0 and memory.level_name == filename:
                        with open(f'{filename}.txt', 'a') as file:
                            file.write(f'{math.floor(memory.get_percent())}\n')
                            recorded_death = True
                        
                if recorded_death == True and memory.get_percent() < perSpecified:
                    recorded_death = False
            
def file_to_desc():
    os.system('cls')
    parentDirectory = fr'{os.getcwd()}\levels'
    os.chdir(parentDirectory)
    
    
    print('This program takes a properly formatted .txt file from GDdeathLogger')
    print('and converts it to a reader-friendly format.')
    print()
    print('What file would you like to convert?')
    print()
    
    while True:
        filename = input()
        if os.path.exists(fr'{parentDirectory}\{filename}.txt'):
            break
        else:
            print('File not found. Retype it or move the file to the \levels\ directory.')
            print()
            
    with open(f'{filename}.txt', 'r') as file:
        perList = {}
        lines = file.readlines()[1::]
        for line in lines:
            if line.endswith('%:\n'):
                perSpecified = int(line.lstrip('DEATHS PAST ').rstrip('%:\n'))
            
            else:
                line = int(line.rstrip('\n'))
                if line in perList.keys():
                    perList[line] += 1
                else:
                    perList[line] = 1
                    
    with open(f'{filename}_DESC.txt', 'w') as file:
        myKeys = list(perList.keys())
        myKeys.sort()
        sorted_dict = {i: perList[i] for i in myKeys}
        
        file.write(f'DEATHS PAST {perSpecified}%:\n')
        for percent in sorted_dict.keys():
            file.write(f'{percent}% x{perList[percent]}\n')
     
    os.system('cls')        
    print('Done!')
    print('Do NOT import this back into GDdeathLogger! Use the base file again!')
    print()
    print('Returning to menu in 3 seconds...')
    time.sleep(3)
    
def main():
    while True:
        os.system('cls')
        print(f'GDdeathLogger {version}')
        print('by falaflewaffel')
        print()
        print('Input options:')
        print('1 - GDdeathLogger (open GD before selecting)')
        print('2 - Convert to Description')
        print('3 - Exit')
        print()
        
        while True:
            try:

                userInput = int(input("Input: "))
            except ValueError:
                print('Invalid input. (input 1, 2, or 3)')
                time.sleep(1)
                os.system('cls')
            else:
                if userInput in [1, 2, 3]:
                    break
                else:
                    print('Invalid input.')
                    time.sleep(1)
                    os.system('cls')
                    
        if userInput == 1:
            deathLogger()
            
        elif userInput == 2:
            file_to_desc()
            
        else:
            sys.exit()
                
            

if __name__ == '__main__':
    main()
