## solar-system-maker
Repository for my A Level Computer Science coursework of which I plan to continue development after my A Levels. SolarSystemMaker is a minimalistic, educational 2D solar system simulation complete with user accounts and saved solar systems.

# Installation
I'm very new to distributing stuff so until I can figure out setup files and distutils and all that, installation will have to be very manual. Apologies! 

Dependencies:
- Pygame
- cx_Oracle

Oracle Instant Client
- You will need to download and unzip the Oracle Instant Client. This allows the application to connect to the SolarSystemMaker database.
For 32 bit Python use https://drive.google.com/drive/folders/1sAZ-10XQqUXtrd4M8adnmzHdo_rOp_wz?usp=sharing.
For 64 bit Python use https://drive.google.com/drive/folders/1JYQCkZFdkGfP6dyEha_9QE529cbKPfMl?usp=sharing.
- Unzip and open the folder and find the instant client folder within it. Put this folder in the same directory as the SolarSystemMaker files. To start SolarSystemMaker, run main.py.

After installation your directory should look like:

solar-system-maker-main
> main.py
> databaseHandler.py
> objectHandler.py
> userInterface.py
> eventListener.py
> instantclient_19_12
> > etc
> readme, license, etc

**Errors**:
cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 32-bit Oracle Client library: "The specified module could not be found".
This means you have likely installed the instant client incorrectly or not at all. 
- Please check you have downloaded the correct version for your Python installation. 
- Please check that the instant client folder is named "instantclient_19_12" and is in the same directory as the rest of the SolarSystemMaker files. 
- Please check that the instant client folder contains all the necessary files including a folder named "network".
