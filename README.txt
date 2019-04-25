First, run the installModule.py script and install corresponding modules through the Module Manager, follow instructions on Terminal/Command Prompt. Module Manager by Austin Schick.

After installing modules, in order to run the program, open the Game.py and run the script

If you wish to install modules on your own use the following after: sudo pip3 install

pyglet
numpy
numpy-stl

If you wish to play over LAN (sockets), then ONE PLAYER should run the file 'server.py' and use the HOST IP address that it prints; instruct the other player to use this IP address as well.


If the graphics are initially too big for the screen (meaning you can only see the bottom left corner of the screen),
then follow these instructions:

Within the 'game.py' file, within the Window class, there are two functions:
 
setd3d(self)      and           set2d(self)

Within these functions there should be an identical line:

	glViewport(0, 0, width*2, height*2)


For both set3d and set2d, change this line to say the following:

	glViewport(0, 0, width, height)


After this change is made, save the file and run the game file. This should have fixed the problem.

Enjoy!
