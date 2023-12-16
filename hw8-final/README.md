# ME35: Final Project - Extracting the Bone
This is all the code for the final project! The folder is laid out as follows:
- old-versions: Tests or old versions of code for future reference.
## Files on the Raspberry Pi Pico W
- pico-libraries: Files that must be installed on the Pico W to run the main program.
  - Credit to: https://github.com/pedromneto97/AccelStepper-MicroPython for a port of the AccelStepper library (https://www.airspayce.com/mikem/arduino/AccelStepper/) in MicroPython
- picomotors_mqtt: The main program to be named main.py and ran on the Pico W. This controls the motors and recieves messages over mqtt from the PC.
## Files on the PC (PyCharm or some other capable IDE)
- tracking.py: Required to run camera_main.py, this is a library containing all the image processing functions needed.
  - Credit to: https://stackoverflow.com/questions/44588279/find-and-draw-the-largest-contour-in-opencv-on-a-specific-color-python on finding objects of a color. 
- camera_main.py: Main image procesing program to be ran on the computer. Displays a window with live feedback to the user of all tracked objects.
- mosquitto_setup_commands.txt: Contains useful commands to be ran in Microsoft Powershell to run the mqtt broker. Make sure the IP is correctly set.
