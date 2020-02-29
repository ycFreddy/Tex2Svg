import sys
from io import BytesIO
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QMainWindow, QApplication, QColorDialog, QPushButton, QLineEdit, QLabel, QFileDialog, QGridLayout, QWidget


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Tex2Svg'
        self.setFixedSize(500, 150)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setAutoFillBackground(True)
        p = self.palette()
        bgcolor = QColor(60, 207, 175)
        p.setColor(self.backgroundRole(), bgcolor)
        self.setPalette(p)
        self.setStyleSheet("QLabel, QMessageBox, QPushButton {background-color:rgb(60,207,175); color:rgb(45, 53, 142)}")

        wid = QWidget(self)
        self.setCentralWidget(wid)
        self.grid = QGridLayout()
        wid.setLayout(self.grid)

        self.colbut = QPushButton('Choose a color', self)
        self.colbut.resize(self.width()*2/5-30, 40)
        self.colbut.clicked.connect(self.col)
        self.grid.addWidget(self.colbut, 0, 0)

        self.colorbox = QLineEdit(self)
        self.colorbox.resize(70, 40)
        self.grid.addWidget(self.colorbox, 0, 1)

        self.labfont = QLabel("Size:", self)
        self.labfont.setAlignment(Qt.AlignCenter)
        self.labfont.resize(40, 40)
        self.grid.addWidget(self.labfont, 0, 2)

        self.fontbox = QLineEdit(self)
        self.fontbox.resize(40, 40)
        self.grid.addWidget(self.fontbox, 0, 4)

        self.labbox = QLabel("Tex/Latex Formula", self)
        self.labbox.setAlignment(Qt.AlignCenter)
        self.labbox.resize(450, 20)
        self.grid.addWidget(self.labbox, 1, 0, 1, 5)

        self.textbox = QLineEdit(self)
        self.textbox.resize(450, 40)
        self.grid.addWidget(self.textbox, 2, 0, 1, 5)

        self.button = QPushButton('SVG image', self)
        self.button.resize(200, 40)
        self.button.clicked.connect(self.on_click)
        self.grid.addWidget(self.button, 3, 0, 1, 2)

        self.savbut = QPushButton('Save',self)
        self.savbut.resize(100, 40)
        self.savbut.clicked.connect(self.save)
        self.grid.addWidget(self.savbut, 3, 3, 1, 2)

        self.show()

    def col(self):
        self.colorbox.setText(str(QColorDialog.getColor().name()))

    def trace(self):
        plt.rc('mathtext', fontset='cm')
        fig = plt.figure(figsize=(1, 1))
        fig.text(0, 0, r'${}$'.format(self.textbox.text()), color=self.colorbox.text(), fontsize=self.fontbox.text())
        output = BytesIO()
        fig.savefig(output, dpi=400, transparent=True, format='svg', bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        output.seek(0)
        return output.read()

    def on_click(self):
        svg = QSvgWidget()
        svg.renderer().load(self.trace())
        svg.setWindowTitle("SVG Picture")
        svg.show()

    def save(self):
        pic = QFileDialog.getSaveFileName(self, 'Save File', '.svg')
        with open(pic[0], 'wb') as f:
            f.write(self.trace())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())