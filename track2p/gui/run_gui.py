from PyQt5.QtWidgets import QApplication
import time 
from track2p.gui.main_wd import MainWindow
from track2p.gui.t2p_wd import NewWindow

if __name__ == '__main__':
    start_time = time.time()

    app = QApplication([])
    mainWindow = MainWindow()
    end_time = time.time()
    print(f"Application took {end_time - start_time} seconds to open.")
    app.exec_()
    