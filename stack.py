# Purpose: Stack layout example
from PyQt5.QtWidgets import QWidget, QLabel,QProgressBar,QApplication,QBoxLayout
class main(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.showFullScreen()
        layout=QBoxLayout(QBoxLayout.TopToBottom)
        layout.setContentsMargins(0,0,0,0)
        firstLabel=QLabel("First Label")
        firstBar=QProgressBar()
        secondLabel=QLabel("Second Label")
        secondBar=QProgressBar()
        layout.addWidget(firstLabel)
        layout.addWidget(firstBar)
        layout.addWidget(secondLabel)
        layout.addWidget(secondBar)
        self.setLayout(layout)
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())