import re
import flet as ft
from flet import ImageFit
from classes import *
import os
import gd
import time
import math


def main(page: ft.Page):
    # Define basic window functions
    page.title = 'GDdeathLogger'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.NONE
    page.padding = 25
    page.theme_mode = ft.ThemeMode.DARK
    page.window_resizable = False
    page.window_maximizable = False
    page.update()

    # Define important variables
    mainDir = os.getcwd()

    # Logging deaths screen variables
    deathLogText = Text(
        'Logging deaths... (press "Main Menu" button when done)'
    ).value()

    # The actual logging function
    def logDeath(percent, filename):
        with open(filename, 'a') as file:
            file.write(f'{math.floor(percent)}\n')
            # memory.get_percent returns a float,
            # this floors it to just the integer value

    # Logging deaths screen
    def loggingScreen(e):
        global respawnTime
        global filename
        global levelid
        global perSpecified
        global memory
        global fileLoaded
        global inMainMenu
        os.chdir('levels')
        respawnTime -= 0.1
        page.clean()

        page.add(ft.Row(controls=[
            deathLogText,
            EmptySpace.shiftRight(575),
            MainMenuButton
        ]))

        # Initializing new file,
        # else grabbing levelid and perSpecified from file
        if not fileLoaded:
            with open(filename, 'a') as file:
                file.write(f'{levelid}\n{perSpecified}\n\n')
        else:
            with open(filename, 'r') as file:
                lines = file.readlines()
                levelid = int(lines[0].rstrip('\n'))
                perSpecified = int(lines[1].rstrip('\n'))

        # Death logging
        deathLogged = False
        while True:
            time.sleep(respawnTime)

            if (memory.is_dead() and
                    memory.get_percent() >= perSpecified and
                    not memory.is_practice_mode() and
                    levelid != 0 and
                    memory.get_level_id() == levelid and
                    not deathLogged):
                logDeath(memory.get_percent(), filename)
                deathLogged = True

            elif (memory.is_dead() and
                    memory.get_percent() >= perSpecified and
                    not memory.is_practice_mode() and
                    levelid == 0 and
                    memory.get_level_name() == filename[:-4] and
                    not deathLogged):
                logDeath(memory.get_percent(), filename)
                deathLogged = True

            elif (not memory.is_dead() and
                    deathLogged):
                deathLogged = False

            if inMainMenu:
                break

    # Input screen variables
    global fileLoadedName
    fileLoadedName = 'None (new file will be created)'

    logoVerySmall = Image(
                          f'{mainDir}/resources/GDdeathLogger_Logo.png',
                          206,
                          78,
                          ImageFit.CONTAIN).value()

    respawnText = Text(
        'Input your respawn time in seconds (default = 1)',
        True,
        'white',
        575).value()

    respawnTimeField = TextField(
        'Respawn time (sec)',
        300,
        50).value()

    respawnInvalid = Text(
        'Must be a number greater than 0.1',
        False,
        'red').value()

    filenameText = Text(
        'Input a file name (must be same as the level name if it\'s local)',
        True,
        'white',
        575).value()

    filenameField = TextField(
        'File name',
        300,
        50,
        'e.g. Acheron.txt').value()

    filenameInvalid = Text(
        'File name must follow the form [name].txt',
        False,
        'red').value()

    loadedFileText = Text(
        f'File loaded: {fileLoadedName}',
        True,
        'red').value()

    levelidText = Text(
        'Input level ID',
        True,
        'white',
        575).value()

    levelidField = TextField(
        'Level ID',
        300,
        50).value()

    levelidInvalid = Text(
        'Must be a positive integer',
        False,
        'red').value()

    percentageText = Text(
        'Input percentage to record deaths at',
        True,
        'white',
        575).value()

    percentageField = TextField(
        'Percentage',
        300,
        50,
        'e.g. 64').value()

    percentageInvalid = Text(
        'Must be an integer in between 0 and 99',
        False,
        'red').value()

    inputNextButton = FilledButton(
        'Next',
        250,
        40,
        loggingScreen,
        True).value()

    # Input screen
    def infoInputScreen(e):
        try:
            global memory
            memory = gd.memory.get_memory()
        except RuntimeError:
            global openGDText
            openGDText.visible = True
            page.update()
            time.sleep(1)
            openGDText.visible = False
            page.update()
        else:
            global inMainMenu
            inMainMenu = False
            page.clean()
            page.add(logoVerySmall)
            page.add(EmptySpace.shiftDown(50))

            page.add(ft.Row(controls=[
                respawnText,
                respawnTimeField,
                EmptySpace.shiftRight(40),
                respawnInvalid
            ]))

            page.add(ft.Row(controls=[
                filenameText,
                filenameField,
                EmptySpace.shiftRight(40),
                filenameInvalid
            ]))

            page.add(ft.Row(controls=[
                EmptySpace.shiftRight(575),
                loadedFileText
            ]))

            page.add(ft.Row(controls=[
                levelidText,
                levelidField,
                EmptySpace.shiftRight(40),
                levelidInvalid
            ]))

            page.add(ft.Row(controls=[
                percentageText,
                percentageField,
                EmptySpace.shiftRight(40),
                percentageInvalid
            ]))

            page.add(EmptySpace.shiftDown(175))

            page.add(ft.Row(controls=[
                EmptySpace.shiftRight(775),
                inputBackButton,
                EmptySpace.shiftRight(10),
                inputNextButton
            ]))

            global fileLoaded
            respawnValid = False
            filenameValid = False
            levelidValid = False
            percentageValid = False
            fileLoaded = False

            # Create levels folder if it does not exist
            if not os.path.exists(f'{mainDir}\\levels'):
                os.mkdir('levels')

            global respawnTime
            global filename
            global levelid
            global perSpecified
            global fileLoadedName

            while True:
                time.sleep(0.25)
                # Respawn time error checking/assignment
                if respawnTimeField.value:
                    try:
                        respawnTime = float(respawnTimeField.value)
                    except ValueError:
                        respawnInvalid.visible = True
                        respawnValid = False
                    else:
                        if respawnTime > 0.1:
                            respawnInvalid.visible = False
                            respawnValid = True
                        else:
                            respawnInvalid.visible = True
                            respawnValid = False
                else:
                    respawnInvalid.visible = False
                    respawnValid = False

                # Filename checking, will add loading files later
                if filenameField.value:
                    if re.search('^.+\.txt$', filenameField.value):
                        # only returns True if value follows [name].txt
                        filename = filenameField.value
                        filenameInvalid.visible = False
                        filenameValid = True
                        if os.path.exists(
                                f'{mainDir}\\levels\\{filenameField.value}'):
                            try:
                                with open(filenameField.value, 'r') as file:
                                    lines = file.readlines()
                                    int(lines[0].rstrip('\n'))
                                    int(lines[1].rstrip('\n'))
                                    assert lines[2] == '\n'
                            except (ValueError, IndexError, AssertionError):
                                fileLoadedName = 'None (new file will be created)'
                                loadedFileText.color = 'red'
                                loadedFileText.value = f'File loaded: {fileLoadedName}'
                                fileLoaded = False
                            else:
                                fileLoadedName = filenameField.value
                                filename = filenameField.value
                                loadedFileText.color = 'green'
                                loadedFileText.value = f'File loaded: {fileLoadedName}'
                                fileLoaded = True
                        else:
                            fileLoadedName = 'None (new file will be created)'
                            filename = filenameField.value
                            loadedFileText.color = 'red'
                            loadedFileText.value = f'File loaded: {fileLoadedName}'
                            fileLoaded = False
                    elif fileLoaded:
                        fileLoadedName = 'None (new file will be created)'
                        loadedFileText.color = 'red'
                        loadedFileText.value = f'File loaded: {fileLoadedName}'
                        fileLoaded = False
                    else:
                        filenameInvalid.visible = True
                        filenameValid = False
                elif fileLoaded:
                    # If fileLoaded == True but filenameField is empty
                    fileLoadedName = 'None (new file will be created)'
                    loadedFileText.color = 'red'
                    loadedFileText.value = f'File loaded: {fileLoadedName}'
                    fileLoaded = False
                else:
                    filenameInvalid.visible = False
                    filenameValid = False

                if fileLoaded:
                    levelidField.disabled = True
                    percentageField.disabled = True
                    if respawnValid:
                        inputNextButton.disabled = False
                else:
                    levelidField.disabled = False
                    percentageField.disabled = False
                    inputNextButton.disabled = True

                # Level ID checking
                if levelidField.value:
                    try:
                        levelid = int(levelidField.value)
                    except ValueError:
                        levelidInvalid.visible = True
                        levelidValid = False
                    else:
                        if levelid < 0:
                            levelidInvalid.visible = True
                            levelidValid = False
                        else:
                            levelidInvalid.visible = False
                            levelidValid = True
                else:
                    levelidInvalid.visible = False
                    levelidValid = False

                # Percentage checking
                if percentageField.value:
                    try:
                        perSpecified = int(percentageField.value)
                    except ValueError:
                        percentageInvalid.visible = True
                        percentageValid = False
                    else:
                        if perSpecified < 0 or perSpecified > 99:
                            percentageInvalid.visible = True
                            percentageValid = False
                        else:
                            percentageInvalid.visible = False
                            percentageValid = True
                else:
                    percentageInvalid.visible = False
                    percentageValid = False

                if not fileLoaded:
                    if (respawnValid and filenameValid
                            and levelidValid and percentageValid):
                        inputNextButton.disabled = False

                page.update()

    # Description converter
    def descConverter(e):
        global fileNotFoundText
        global filePicker
        try:
            filename = filePicker.result.files[0].path.split('\\')[-1]
        except TypeError:
            fileNotFoundText.visible = True
            fileNotFoundText.update()
            time.sleep(1)
            fileNotFoundText.visible = False
            fileNotFoundText.update()
            return
        filepathAppend = ''
        for dir in filePicker.result.files[0].path.split('\\')[0:-1]:
            filepathAppend = filepathAppend + f'{dir}\\'
        filepath = filepathAppend

        os.chdir(filepath)

        with open(filename, 'r') as file:
            perList = {}
            lines = file.readlines()
            try:
                perSpecified = int(lines[1].rstrip('\n'))
            except (ValueError, IndexError):
                fileNotFoundText.visible = True
                fileNotFoundText.update()
                time.sleep(1)
                fileNotFoundText.visible = False
                fileNotFoundText.update()
                return
            for line in lines[3:]:
                try:
                    line = int(line.rstrip('\n'))
                except ValueError:
                    fileNotFoundText.visible = True
                    fileNotFoundText.update()
                    time.sleep(1)
                    fileNotFoundText.visible = False
                    fileNotFoundText.update()
                    return
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
        os.chdir(mainDir)
        doneText.visible = True
        doneText.update()
        time.sleep(1)
        doneText.visible = False
        doneText.update()

    # Description file picker
    def descFilePicker(e):
        global filePicker
        filePicker = ft.FilePicker(on_result=descConverter)
        page.overlay.append(filePicker)
        page.update()
        filePicker.pick_files()

    # Main menu variables
    logoSmall = Image(
        f'{mainDir}/resources/GDdeathLogger_Logo.png',
        258,
        98,
        ImageFit.CONTAIN).value()

    deathLoggerButton = FilledButton(
        'GDdeathLogger',
        250,
        40,
        infoInputScreen).value()

    descConverterButton = FilledButton(
        'Description Converter',
        250,
        40,
        descFilePicker).value()

    exitButton = FilledTonalButton(
        'Exit',
        150,
        40,
        lambda _: page.window_destroy()).value()

    global openGDText
    openGDText = Text(
        'Open Geometry Dash before selecting this!',
        False,
        'red').value()

    global fileNotFoundText
    fileNotFoundText = Text(
        'File is not from GDdeathLogger or doesn\'t exist.',
        False,
        'red').value()

    global doneText
    doneText = Text(
        'Done!',
        False,
        'green'
    ).value()

    # Main menu
    def mainMenu(e):
        global inMainMenu
        global openGDText
        os.chdir(mainDir)
        inMainMenu = True

        page.clean()
        page.add(logoSmall)
        page.add(EmptySpace.shiftDown(75))
        page.add(deathLoggerButton)
        page.add(descConverterButton)
        page.add(exitButton)
        page.add(openGDText)
        page.add(fileNotFoundText)
        page.add(doneText)

    # Back button for the input screen, I had to put it here
    inputBackButton = FilledTonalButton('Back', 150, 40, mainMenu).value()

    # Logging screen main menu button
    MainMenuButton = FilledTonalButton('Main Menu', 250, 40, mainMenu).value()

    # Start screen variables
    startButton = FilledButton('Start', 250, 40, mainMenu, False).value()
    logoLarge = Image(
        f'{mainDir}/resources/GDdeathLogger_Logo.png',
        516,
        196,
        ImageFit.CONTAIN).value()

    creditsImg = Image(
        f'{mainDir}/resources/GDdeathLogger_Credit.png',
        367,
        27,
        ImageFit.CONTAIN).value()

    # Start screen
    page.add(logoLarge)
    page.add(creditsImg)
    page.add(EmptySpace.shiftDown(50))
    page.add(startButton)


if __name__ == '__main__':
    ft.app(target=main)
