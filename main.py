import sys
from PyQt5.QtWidgets import QApplication
from scaffold_app import ScaffoldApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScaffoldApp()
    ex.show()
    sys.exit(app.exec_())
