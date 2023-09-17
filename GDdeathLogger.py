import os
import sys
import gd 
import time
import math

version = 'v3.0.0'
mainDir = os.getcwd()

def deathLogger():
    # Screen is cleared by this point
    try:
        memory = gd.memory.get_memory()
        gdOpen = True
    except RuntimeError:
        gdOpen = False
        
    if not gdOpen:
        print('''Open Geometry Dash before using this!
Returning in 3 seconds...''')
        time.sleep(3)
        
    else: # If GD is open
        
        # Asks for respawnTime, if it's not a number OR less than 0.1 it asks again
        while True:
            print('''Input your respawn time. (default = 1)
                ''')
            
            try:
                respawnTime = float(input('Input: ')) - 0.1 # So there's 0 chance it skips over a death
            except ValueError:
                print()
                print('Invalid input. (Number greater than 0.1)')
                time.sleep(1.5)
                os.system('cls')
            else:
                if respawnTime < 0.1:
                    print()
                    print('Invalid input. (Number greater than 0.1)')
                    time.sleep(1.5)
                    os.system('cls')
                else:
                    break
        
        # At this point respawnTime is fully defined as a float >= 0.1
        while True:
            os.system('cls')
            print('''Input a file name to log deaths to.
Make sure this MATCHES the level name if it's a local level.''')
            print()
            filename = input('Input: ')
            
            if not filename or filename.startswith('.txt'): # if it's a blank string or starts with '.txt'
                print()
                print('Enter a name.')
                time.sleep(1)
            elif filename.endswith('.txt'):
                break
            else:
                filename = f'{filename}.txt'
                break
        
        # 'filename' is now a string ending in '.txt'
        if not os.path.exists(fr'{mainDir}\levels'):
            os.mkdir('levels') # create 'levels' folder if it doesn't exist
        
        if not os.path.exists(fr'{mainDir}\levels\{filename}'):
            fileExists = False
        else:
            fileExists = True
            
        if not fileExists:
            # Ask for level ID
            while True:
                os.system('cls')
                print('''Input the level ID of the level you want to record deaths for (0 for local level).
                      ''')
                
                try:
                    levelID = int(input('Level ID: '))
                except ValueError:
                    print()
                    print('Invalid input. (input a positive integer)')
                    time.sleep(1.5)
                else:
                    if levelID < 0:
                        print()
                        print('Invalid input. (input a positive integer)')
                        time.sleep(1.5)
                    else:
                        break
                    
            # Level ID is a positive integer
            while True:
                os.system('cls')
                print('''Input the percentage you want to start recording deaths.
                      ''')
                try:
                    perSpecified = int(input('Percentage: '))
                except ValueError:
                    print()
                    print('Invalid input. (input an integer between 0-99)')
                    time.sleep(1.5)
                else:
                    if perSpecified < 0 or perSpecified > 99:
                        print()
                        print('Invalid input. (input an integer between 0-99)')
                        time.sleep(1.5)
                    else:
                        break
                
            os.chdir(f'{mainDir}\levels')
            with open(filename, 'a') as file:
                file.write(f'{levelID}\n{perSpecified}\n\n') # Write the levelID -> newline -> perSpecified -> 2 newlines
        
        # fileExists, gets levelID and perSpecified from the file
        else:
            os.chdir(f'{mainDir}\levels')
            with open(filename, 'r') as file:
                lines = file.readlines()
                levelID = int(lines[0].rstrip('\n'))
                perSpecified = int(lines[1].rstrip('\n'))
                
        # RECORDING DEATHS
        deathLogged = False
        fileBasename = filename.removesuffix('.txt')
        os.system('cls')
        print('Logging deaths... (do not close this window until you\'re done)')
        while True:
            if memory.is_dead() and memory.get_percent() >= perSpecified and not memory.is_practice_mode() and deathLogged == False:
                    if memory.level_id == levelID and levelID != 0:
                        with open(filename, 'a') as file:
                            file.write(f'{math.floor(memory.get_percent())}\n')
                            deathLogged = True
                    
                    if memory.level_id == levelID and levelID == 0 and memory.level_name == fileBasename:
                        with open(filename, 'a') as file:
                            file.write(f'{math.floor(memory.get_percent())}\n')
                            deathLogged = True
                        
            if deathLogged == True and memory.get_percent() < perSpecified:
                deathLogged = False



def descConverter():
    os.system('cls')
    levelDirectory = fr'{mainDir}\levels'
    os.chdir(levelDirectory)
    
    while True:
        print('''This program takes a properly formatted .txt file from GDdeathLogger
and converts it to a reader-friendly format.

Input the filename of the log you want to convert...
    ''')
        
        filename = input('File: ')
        
        if filename and not filename.endswith('.txt'):
            filename = f'{filename}.txt'
            
            
            
        if os.path.exists(fr'{levelDirectory}\{filename}'):
            break
        else:
            print('File not found. Retype it or move the file to the \levels\ directory.')
            time.sleep(1.5)
            os.system('cls')
            
    with open(filename, 'r') as file:
        perList = {}
        lines = file.readlines()
        perSpecified = int(lines[1].rstrip('\n'))
        for line in lines[3:]:
            line = int(line.rstrip('\n'))
            if line in perList.keys():
                perList[line] += 1
            else:
                perList[line] = 1
                    
    fileBasename = filename.removesuffix('.txt')
    with open(f'{fileBasename}_DESC.txt', 'w') as file:
        myKeys = list(perList.keys())
        myKeys.sort()
        sorted_dict = {i: perList[i] for i in myKeys}
        totalDeaths = 0
        for i in list(sorted_dict.values()):
            totalDeaths += i
        
        file.write(f'DEATHS PAST {perSpecified}%:\n')
        for percent in sorted_dict.keys():
            file.write(f'{percent}% x{perList[percent]}\n')
        file.write(f'\nTOTAL: {totalDeaths}')
     
    os.system('cls')        
    print('Done!')
    print('Do NOT import this back into GDdeathLogger! Use the base file again!')
    print()
    print('Returning to menu in 3 seconds...')
    time.sleep(3)

def convertLog():
    levelDirectory = fr'{mainDir}\levels'
    os.chdir(levelDirectory)
    while True:
        print('''This tool converts a log file made with versions <3.0.0 into
a log file usable with the latest versions.
''')
        
        filename = input('File: ')
            
        if filename and not filename.endswith('.txt'):
            filename = f'{filename}.txt'
            
            
            
        if os.path.exists(fr'{levelDirectory}\{filename}'):
            break
        else:
            print('File not found. Retype it or move the file to the \levels\ directory.')
            time.sleep(1.5)
            os.system('cls')
            
    with open(filename, 'r') as file:
        perList = []
        lines = file.readlines()
        levelID = lines[0].lstrip('Level ID: ').rstrip('\n')
        perSpecified = lines[1].lstrip('DEATHS PAST ').rstrip('%:\n')
        for line in lines[2::]:
            perList.append(int(line.rstrip('\n')))
            
    with open(filename, 'w') as file:
        file.write(f'{levelID}\n{perSpecified}\n\n')
        for percent in perList:
            file.write(f'{percent}\n')
            
    os.system('cls')        
    print('''Done!
Now you can import this into GDdeathLogger! :D
Returning to menu in 3 seconds...
''')
    time.sleep(3)

def menuScreen(version):
    print(f'''GDdeathLogger {version}
by falaflewaffel

1 - GDdeathLogger
2 - Description Converter
3 - Convert log from older version
4 - Exit program
''')













def main():
    while True:
        os.system('cls')
        menuScreen(version)
        
        while True:
            try:
                userInput = int(input("Input: "))
            except ValueError:
                print()
                print('Invalid input. (input 1, 2, 3, or 4)')
                time.sleep(1)
                os.system('cls')
                menuScreen()
            else:
                if userInput in [1, 2, 3, 4]:
                    break
                else:
                    print()
                    print('Invalid input. (input 1, 2, 3, or 4)')
                    time.sleep(1)
                    os.system('cls')
                    menuScreen()
                    
        if userInput == 1:
            os.system('cls')
            deathLogger()
            
        elif userInput == 2:
            os.system('cls')
            descConverter()
            
        elif userInput == 3:
            os.system('cls')
            convertLog()
        else:
            sys.exit()
                
            

if __name__ == '__main__':
    main()
