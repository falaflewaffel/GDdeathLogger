import flet as ft
from flet_core.control_event import ControlEvent
import os
import sys
import gd 
import time
import math



def main(page: ft.Page):
    # Define basic window functions
    page.title = 'GDdeathLogger'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = False
    page.window_maximizable = False
    page.update()
    
    # Initialize important variables
    global filepath
    filepath = 'None'
    global mainDir
    mainDir = os.getcwd()
    
    
    # Defines fonts
    page.fonts = {
        'Arial Rounded Bold': 'https://github.com/YeoLab/singlecell_pnm/raw/master/Arial%20Rounded%20Bold.ttf'
    }
    
    
    
    
    
    # Defines text boxes that the program grabs info from
    respawnTimeField = ft.TextField(label = 'Respawn time (sec)')
    filenameField = ft.TextField(label = 'File name')
    levelIDField = ft.TextField(label = 'Level ID')
    percentageField = ft.TextField(label = 'Percentage')
    
    
    # Add text, then disappear after one second
    def addTextOneSec(string):
        page.add(ft.Text(string))
        time.sleep(1)
        page.controls.pop()
        page.update()
    
    
    def checkForGD(e):
        try:
            global memory
            memory = gd.memory.get_memory()
        except RuntimeError:
            page.add(ft.Text('Open GD before running!'))
            time.sleep(1)
            page.controls.pop()
            page.update()
        else:
            respawnTimeScreen(ControlEvent)
    
    # Checks for the respawn time box input
    def verifyRespawnTime(e):
        try:
            global respawnTime
            respawnTime = float(respawnTimeField.value)
        except ValueError:
            addTextOneSec('Input a number greater than 0.1!')
        else:
            if respawnTime < 0.1:
                addTextOneSec('Input a number greater than 0.1!')
            else:
                page.clean()
                filenameScreen(ControlEvent)
    
    # Define respawnTimeScreen functionality
    def respawnTimeScreen(e):
        page.clean()
        page.vertical_alignment = ft.MainAxisAlignment.START
        
        page.add( # first row with main functionality
            ft.Row(controls=[
                ft.Text('Input your respawn time (default = 1)', width = 500),
                
                respawnTimeField,
                
                ft.Text('', width = 150), # Just shifts the 'Next' button to the right
                
                ft.FilledButton(
                    text = 'Next',
                    width = 250,
                    height = 40,
                    on_click = verifyRespawnTime
                )
            ])
        )
        
        page.add(
            ft.Row(controls=[
                ft.Text('', width = 970),
                
                ft.FilledTonalButton(
                    text = 'Back',
                    width = 250,
                    height = 40,
                    on_click = mainMenu
                )
            ])
        )
        
    def verifyFilename(e): # Check filename text box
        global filepath
        global filename
        global mainDir
        global loadedFile
        loadedFile = False
        if filepath == 'None':
            if filenameField.value.endswith('.txt') or not filenameField.value:
                page.add(ft.Text('Add a filename/get rid of .txt'))
                time.sleep(1)
                page.controls.pop()
                page.update()
                return
            else:
                filename = f'{filenameField.value}.txt'
                global fileBasename
                fileBasename = filenameField.value
                os.chdir(mainDir)
                if not os.path.exists(f'{mainDir}\\levels'):
                    os.mkdir('levels')
                filepath = f'{mainDir}\\levels'
                promptLevelID(ControlEvent)
        else:
            filename = filepath.split('\\')[-1]
            filepathAppend = ''
            for dir in filepath.split('\\')[0:-1]:
                filepathAppend = filepathAppend + f'{dir}\\'
            filepath = filepathAppend
            loadedFile = True
            os.chdir(filepath)
            with open(f'{filepath}{filename}', 'r') as file:
                lines = file.readlines()
                global levelID
                levelID = int(lines[0].rstrip('\n'))
                global perSpecified
                perSpecified = int(lines[1].rstrip('\n'))
                loggingScreen(ControlEvent)
            
    
    def loadExistingFile(e):
        global filepath
        if filepath != 'None':
            page.controls.pop()
        page.add(ft.Text(f'Current file loaded: {filePicker.result.files[0].name}', text_align=ft.TextAlign.RIGHT))
        filepath = filePicker.result.files[0].path
    
    def unloadFile(e):
        global filepath
        if filepath != 'None':
            filepath = 'None'
            page.controls.pop()
            page.update()
    
    
    def promptExistingFile(e):
        global filePicker
        filePicker = ft.FilePicker(on_result=loadExistingFile) 
        page.overlay.append(filePicker)
        page.update()
        filePicker.pick_files()
        
    
    def filenameScreen(e):
        page.clean()
        page.add( # Top row
            ft.Row(controls=[
                ft.Text('Input a filename. (this HAS to match the level name if it\'s a local level)', width = 500),
                
                filenameField,
                
                ft.Text('.txt', width = 150),
                
                ft.FilledButton(
                    text = 'Next',
                    width = 250,
                    height = 40,
                    on_click = verifyFilename
                )
            ])
        )
        
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970), # To offset the button to the right edge of the screen
                
                ft.FilledTonalButton(
                    text = 'Load existing file',
                    width = 250,
                    height = 40,
                    on_click = promptExistingFile
                )
            ])
        )
       
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970), # To offset the button to the right edge of the screen
                
                ft.TextButton(
                    text = 'Unload file',
                    width = 250,
                    height = 20,
                    on_click = unloadFile
                )
            ])
        )
        
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970, height=50) # To move the back button down
            ])
        )
       
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970), # To offset the button to the right edge of the screen
                
                ft.FilledTonalButton(
                    text = 'Back',
                    width = 250,
                    height = 40,
                    on_click = respawnTimeScreen
                )
            ])
        )
       
    def verifyLevelID(e):
        try:
            global levelID
            levelID = int(levelIDField.value)
        except ValueError:
            addTextOneSec('Error: please make sure input is a positive integer')
        else:
            if levelID < 0:
                addTextOneSec('Error: please make sure input is a positive integer')
            else:
                promptPercentage(ControlEvent)
            
            
            
            
    def promptLevelID(e):
        page.clean()
        
        page.add( # Top row
            ft.Row(controls=[
                ft.Text('Input level ID (Use 0 for a local level)', width = 500),
                
                levelIDField,
                
                ft.Text('', width = 150),
                
                ft.FilledButton(
                    text = 'Next',
                    width = 250,
                    height = 40,
                    on_click = verifyLevelID
                )
            ])
        )
        
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970), # To offset the button to the right edge of the screen
                
                ft.FilledTonalButton(
                    text = 'Back',
                    width = 250,
                    height = 40,
                    on_click = filenameScreen
                )
            ])
        )
       
    def verifyPercentage(e):
        try:
            global perSpecified
            perSpecified = int(percentageField.value)
        except ValueError:
            addTextOneSec('Input an integer in between 0 and 99.')
        else:
            if perSpecified < 0 or perSpecified > 99:
                addTextOneSec('Input an integer in between 0 and 99.')
            else:
                loggingScreen(ControlEvent)
    
    def promptPercentage(e):
        page.clean()
        
        page.add( # Top row
            ft.Row(controls=[
                ft.Text('Input percentage to start recording deaths at.', width = 500),
                
                percentageField,
                
                ft.Text('', width = 150),
                
                ft.FilledButton(
                    text = 'Next',
                    width = 250,
                    height = 40,
                    on_click = verifyPercentage
                )
            ])
        )
        
        page.add(
            ft.Row(controls=[
                ft.Text('', width=970), # To offset the button to the right edge of the screen
                
                ft.FilledTonalButton(
                    text = 'Back',
                    width = 250,
                    height = 40,
                    on_click = promptLevelID
                )
            ])
        )
       
    def loggingScreen(e):
        page.clean()
        
        page.add(
            ft.Row(controls=[
                ft.Text('Logging... (click the Main Menu button when done)', width=970), # To offset the button to the right edge of the screen
                
                ft.FilledTonalButton(
                    text = 'Main Menu',
                    width = 250,
                    height = 40,
                    on_click = mainMenu
                )
            ])
        )
        
        if loadedFile == False:
            os.chdir(f'{mainDir}\levels')
            with open(filename, 'w') as file:
                file.write(f'{levelID}\n{perSpecified}\n\n')
                
        else:
            os.chdir(filepath)
        global mainMenuStatus
        mainMenuStatus = False
        deathLogged = False
        while True:
            if mainMenuStatus == True:
                break
            
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
        
       
    def convertDesc(e):
        filename = filePicker.result.files[0].path.split('\\')[-1]
        filepathAppend = ''
        for dir in filePicker.result.files[0].path.split('\\')[0:-1]:
            filepathAppend = filepathAppend + f'{dir}\\'
        filepath = filepathAppend
        
        os.chdir(filepath)
        
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
            
            addTextOneSec('Done!')
        
        
       
        
    # Define Description Converter functionality
    def descConverter(e):
        global filePicker
        filePicker = ft.FilePicker(on_result=convertDesc) 
        page.overlay.append(filePicker)
        page.update()
        filePicker.pick_files()
        
    # Define exit functionality
    def exitProgram(e):
        page.window_destroy()
        
    
    
    
    
    
    
    
    
    
    
    
    def mainMenu(e):
        page.clean()
        global mainMenuStatus
        mainMenuStatus = True
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        # Add column with buttons
        page.add(
            ft.Column(controls=[
                ft.FilledButton(
                    text = 'GDdeathLogger',
                    width = 250,
                    height = 40,
                    on_click = checkForGD
                ),
                
                ft.FilledButton(
                    text = 'Description Converter',
                    width = 250,
                    height = 40,
                    on_click = descConverter
                ),

                ft.FilledTonalButton(
                    text = 'Exit',
                    width = 250,
                    height = 40,
                    on_click = exitProgram
                )
            ])
        )
    
    # Start screen
    page.add(
        ft.Text(
                'GDdeathLogger by falaflewaffel',
                size = 24,
                width = 400,
                font_family = 'Arial Rounded Bold',
                text_align = ft.TextAlign.CENTER
        )
    )
    
    page.add(
        ft.FilledButton(
                text = 'Start',
                width = 250,
                height = 40,
                on_click = mainMenu
            )
    )


if __name__ == '__main__':
    ft.app(target=main)
