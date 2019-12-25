# Slic3r profile comparer
Ever got a new profile and wandered what exactly is different in it compared to a stock profile or a different profile? Looking through INI files is not particularly easy, so here's a simple (and crude) tool that will display those differences for you.

## Installing
1. Make sure your system has python 3 installed. You will need TK (tkinter) support for GUI version, but it is being installed by default.
2. Git clone repository, or download as zip
3. Navigate to directory and install dependencies - ```pip install -r requirements.txt``` or ```pip install -r requirements_gui.txt``` for gui version
4. Run it - ```python compare.py``` or ```python gui.py```

## Using
### CLI version
1. Add a new profile using full path for file, unless it's located in the same directory. For example ```add C:\Users\abc\Documents\prusa_profile_comparison\PrusaProfile.ini``` 
Note that you can import multiple profile files.
2. Display all the available profiles - ```print```
3. Compare 2 profiles, for example ```compare printer:Original Prusa i3 MK3S MMU2S Single to printer:Original Prusa i3 MK3S MMU2S 0.6 nozzle```
### GUI version
1. Import profile - click Browse, select file and click Open
Note that you can import multiple profile files.
2. Select profiles to compare in both dropdown windows, click submit for each one. Make sure profiles are displayed in their respective windows.
3. Click Compare button to compare profiles and display difference.