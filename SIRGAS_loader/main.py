


"""from sirgas_downloader import sirgas_downloader
test_obj = sirgas_downloader()

saved_file_name = test_obj.download(test_obj.multianual_coord_url)
decompressed_crd_file = test_obj.decompress(saved_file_name)    

df = read_sirgas_dataframe(decompressed_crd_file)
df.plot()"""

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5 import uic

# Only needed for access to command line arguments
import sys


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('plot.ui', self) # Load the .ui file

if __name__ == "__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    qapp.exec()
