import sys
from PyQt5.QtWidgets import QApplication
from ui_module import InfusionForm

def main():
    app = QApplication(sys.argv)
    form = InfusionForm()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()