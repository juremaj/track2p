The first thing to know is that we assume that each of the recording is same length, imaging frequency, number of planes and number of channels (otherwise might not work, or we cant guarantee).

After activating the GUI through `python -m track2p` the user should navigate to the 'Run' tab on the top left of the window and select 'Run track2p algorithm' from the dropdown menu. This will open a pop-up window that will allow the user to set the paths to suite2p datasets and to set the algorithm parameters (see an example below). For each parameter, a brief explanation of what is expected by the user is displayed next to the input box or input button. 

![ex_popup_runtrack2p.png](docs/media/plots/ex_popup_runtrack2p.png) 

- Iscell_thr input textobox: the user must enter the threshold used to filter suite2p outputs (based on suite2p classifier probability in iscell.npy). The default value is 0.5.
- Reg_chan input textbox : the user must enter which channel to use for day-to-day registration (0-> functional 1-> anatomical (if available)). The default value is 0.
- Import directory button : the user have to import the directory containing subfolders of different recordings for the same mouse (each subfolder contains a ‘suite2p’ folder in default suite2p output format). Once imported, the directory path will be displayed (Imported directory: directory path) and all subfolders in the directory are displayed in the left-hand box (in alphabetical order). Next, the user must press -> to add the file to the list of paths to use for track2p in the right-hand box. Warning: to avoid mismatch between ordered recording days and days that are displayed in the gui, the user should list the subfolders from oldest to most recent recording day in the right-hand box, so that the first day of recording (oldest day) correspond to the first day in the gui and so on.
- Save path button : the user must import the parent folder in which he desires to put a track2p subfolder containing outputs of the algorithm. 
- Run button: it allows the user to launch the track2p algorithm and initiates the terminal that displays messages informing about the algorithm's progress.

When the algorithm is finished, another pop-up window will appear, asking the user if they want to visualise the outputs in the GUI. If the user click on yes, all vizualizations will be displayed (see visualisations section). 
