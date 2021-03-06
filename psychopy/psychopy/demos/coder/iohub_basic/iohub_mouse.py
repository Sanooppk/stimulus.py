# -*- coding: utf-8 -*-
"""
Demo of basic mouse handling from the ioHub (a separate asynchronous process for
fetching and processing events from hardware; mice, keyboards, eyetrackers).

Inital Version: May 6th, 2013, Sol Simpson
Abbrieviated: May 2013, Jon Peirce
"""
import sys

from psychopy import visual,core
from psychopy.iohub import launchHubServer

# create the process that will run in the background polling devices
io=launchHubServer()

# some default devices have been created that can now be used
display = io.devices.display
keyboard = io.devices.keyboard
mouse=io.devices.mouse

# Hide the 'system mouse cursor'.
mouse.setSystemCursorVisibility(False)

# We can use display to find info for the Window creation, like the resolution
# (which means PsychoPy won't warn you that the fullscreen does not match your requested size)
display_resolution=display.getPixelResolution()

# ioHub currently supports the use of a single full-screen PsychoPy Window
window=visual.Window(display_resolution,
                        units='pix',
                        fullscr=True, allowGUI=False,
                        screen=0
                        )

# Create some psychopy visual stim. This is identical to how you would do so normally.
fixSpot = visual.PatchStim(window,tex="none", mask="gauss",
                    pos=(0,0), size=(30,30),color='black', autoLog=False)
grating = visual.PatchStim(window,pos=(300,0),
                    tex="sin",mask="gauss",
                    color=[1.0,0.5,-1.0],
                    size=(150.0,150.0), sf=(0.01,0.0),
                    autoLog=False)
message = visual.TextStim(window,pos=(0.0,-(display_resolution[1]/2-140)),alignHoriz='center',
                    alignVert='center',height=40,
                    text='move=mv-spot, left-drag=SF, right-drag=mv-grating, scroll=ori',
                    autoLog=False,wrapWidth=display_resolution[0]*.9)

last_wheelPosY=0

# Run the example until the 'q' or 'ESCAPE' key is pressed
#
while True:
    # Get the current mouse position
    # posDelta is the change in position *since the last call*
    position, posDelta = mouse.getPositionAndDelta()
    mouse_dX,mouse_dY=posDelta

    # Get the current state of each of the Mouse Buttons
    left_button, middle_button, right_button = mouse.getCurrentButtonStates()

    # If the left button is pressed, change the grating's spatial frequency
    if left_button:
        grating.setSF(mouse_dX/5000.0, '+')
    elif right_button:
        grating.setPos(position)

    # If no buttons are pressed on the Mouse, move the position of the mouse cursor.
    if True not in (left_button, middle_button, right_button):
        fixSpot.setPos(position)

    if sys.platform == 'darwin':
        # On OS X, both x and y mouse wheel events can be detected, assuming the mouse being used
        # supported 2D mouse wheel motion.
        wheelPosX,wheelPosY = mouse.getScroll()
    else:
        # On Windows and Linux, only vertical (Y) wheel position is supported.
        wheelPosY = mouse.getScroll()

    # keep track of the wheel position 'delta' since the last frame.
    wheel_dY=wheelPosY-last_wheelPosY
    last_wheelPosY=wheelPosY

    # Change the orientation of the visual grating based on any vertical mouse wheel movement.
    grating.setOri(wheel_dY*5, '+')

    # Advance 0.05 cycles per frame.
    grating.setPhase(0.05, '+')

    # Redraw the stim for this frame.
    fixSpot.draw()
    grating.draw()
    message.draw()
    window.flip()#redraw the buffer

    # Handle key presses each frame. Since no event type is being given
    # to the getEvents() method, all KeyboardEvent types will be
    # returned (KeyboardPressEvent, KeyboardReleaseEvent, KeyboardCharEvent),
    # and used in this evaluation.
    #
    for event in keyboard.getEvents():
        # Check if we should quit
        # Note that the keyboard events in iohub are case-sensitive (shift-q means "Q")
        if event.key in ['ESCAPE','q']:
            io.quit()
            core.quit()

    # Clear out events that were not accessed this frame.
    io.clearEvents()

#
## End of Example
#