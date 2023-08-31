# GD Death Logger
A program that logs deaths in a Geometry Dash level past a specified percentage.

## Download
Go to the "Releases" tab and download the latest "GDdeathLogger.zip" file. Unzip the file and you'll get a folder with 2 .exe files.

## Usage
Have Geometry Dash currently open and then launch the GDdeathLogger.exe file.

### Respawn time 
This is used to determine the interval that the program checks for deaths. If you input the wrong respawn time, the program may end up recording duplicate deaths or miss a death entirely.

### Time to wait after logging death
Often times, players pause immediately after they die far into a level. The problem is that this program will still record deaths, even when the game is paused. This would result in duplicate death recording. The implementation of the waiting feature, however, prevents this. For most use cases, it is recommended to set this to 10-15 seconds, though it could vary depending on if it's a challenge or a full level.

## file_to_desc
file_to_desc.exe takes a properly formatted .txt file from GDdeathLogger and re-formats it into a separate .txt file, formatted in a more reader-friendly version that you would see in a YouTube video description.


## Contributing
If you have a bug to report or a feature you would like to be added, feel free to either open an issue or DM me on Discord (@falaflewaffel)
