import sys
from PyQt5.QtWidgets import QApplication
from Tex2Svg import Tex2Svg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tex2Svg.Tex2Svg()
    sys.exit(app.exec_())