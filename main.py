from ui import *
from backgroundMusic import *

if __name__ == "__main__":
    # Create the PyQt5 app
    app = QApplication(sys.argv)

    # Create the window
    window = Window()
    window.show()

    # Run the app
    sys.exit(app.exec_())

    # window.update_background("3_normal.png")




