from psychopy.localization import _translate

code = 2001

descr = _translate("Stimulus is being rendered smaller than a pixel")

help = """
Check the units and the size of your stimulus carefully. If your stimulus is 
set to draw with a size (or letter height) of 0.1 and the units are set to be
pixels then your stimulus will be smaller than a pixel and it won't be visible.
"""
