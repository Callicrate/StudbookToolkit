import os, sys, inspect

# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../3rdParty")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
