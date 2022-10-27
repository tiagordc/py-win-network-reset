import sys, re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *

class InterfaceWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Network Interfaces')
        self.setGeometry(200, 200, 400, 400)
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.switchInterface)
        button = QPushButton('Refresh')
        button.clicked.connect(self.updateList)
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Double click to enable/disable:'))
        layout.addWidget(self.list)
        layout.addWidget(button)
        self.setLayout(layout)
        self.updateList()

    def addItem(self):
        list = self.findChild(QListWidget)
        list.addItem('Item5')

    def updateList(self):
        self.list.clear()
        process = QProcess()
        process.start('netsh', ['interface', 'show', 'interface'])
        process.waitForFinished()
        output = process.readAllStandardOutput().data().decode('utf-8').splitlines()[3:-1]
        interfaces = {}
        for line in output:
            match = re.search(r"(\w+)\s{2,}(\w+)\s{2,}(\w+)\s{2,}(.*)", line, re.MULTILINE)
            if match:
                name = match.group(4)
                item = QListWidgetItem(name)
                item.__state__ = match.group(1) == 'Enabled'
                item.setForeground(QColor(0, 160, 0) if item.__state__ else QColor(255, 0, 0))
                self.list.addItem(item)
        self.interfaces = interfaces          

    def switchInterface(self, item):
        interface = item.text()
        if item.__state__:
            QProcess.execute('netsh', ['interface', 'set', 'interface', interface, 'disable'])
        else:
            QProcess.execute('netsh', ['interface', 'set', 'interface', interface, 'enable'])
        self.updateList()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceWindow()
    window.show()
    sys.exit(app.exec_())
