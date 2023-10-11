import sys
import os
import pyautogui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox, QFileDialog, QMainWindow, QHBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel



class SelectAreaWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Выберите область для скриншота')
        self.selected_area = None
        self.setWindowOpacity(0.3)
        self.show()


        global layout
        layout = QHBoxLayout()


        self.button = QPushButton("Click", self)
        self.button.setStyleSheet("background-color: rgba(255, 0, 0, 250);")

        self.button.clicked.connect(self.saveArea)
        self.button.show()


    def saveArea(self):
        self.selected_area = self.frameGeometry()
        self.close()


class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('Скриншот-приложение')

        self.save_dir = os.path.expanduser('~')
        self.save_dir_label = QLabel('Папка сохранения скриншотов: ' + self.save_dir)
        self.select_dir_button = QPushButton('Выбрать папку')
        self.select_dir_button.clicked.connect(self.selectDirectory)

        self.select_area_button = QPushButton('Выбрать область скриншота')
        self.select_area_button.clicked.connect(self.selectArea)

        self.screenshot_button = QPushButton('Сделать скриншот')
        self.screenshot_button.clicked.connect(self.takeScreenshot)

        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Имя снимка: ')
        self.line = QLineEdit(self)
        self.line.move(50, 20)
        self.line.resize(200, 32)
        self.nameLabel.move(20, 20)


        layout = QVBoxLayout()
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.line)
        layout.addWidget(self.save_dir_label)
        layout.addWidget(self.select_dir_button)
        layout.addWidget(self.select_area_button)
        layout.addWidget(self.screenshot_button)
        self.setLayout(layout)

    def selectDirectory(self):
        options = QFileDialog.Options()
        selected_dir = QFileDialog.getExistingDirectory(self, "Выбрать папку", options=options)
        if selected_dir:
            self.save_dir = selected_dir
            self.save_dir_label.setText('Папка сохранения скриншотов: ' + self.save_dir)

    def selectArea(self):
        self.select_area_window = SelectAreaWindow(self)
        self.select_area_window.show()

    def takeScreenshot(self):
        if not hasattr(self, 'select_area_window') or not self.select_area_window.selected_area:
            QMessageBox.warning(self, 'Ошибка', 'Выберите область скриншота сначала.')
            return

        screenshot = pyautogui.screenshot(region=(self.select_area_window.selected_area.x(),
                                                  self.select_area_window.selected_area.y(),
                                                  self.select_area_window.selected_area.width(),
                                                  self.select_area_window.selected_area.height()))
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        filename = os.path.join(self.save_dir, f'{self.line.text()}.png')
        screenshot.save(filename)
        QMessageBox.information(self, 'Готово', f'Скриншот сохранен как {filename}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ScreenshotApp()
    ex.show()
    sys.exit(app.exec_())
