from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import QDir, Qt, QUrl, QSize
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar, QMainWindow)

import os 
import shutil

curr_img = 0

img_names = list()
with open('/Users/abbasmammadov/Desktop/PyQt6-missings/totest.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        img_names.append(line.strip())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mismatch Filter")
        
        btnSize = QSize(16, 16)

        self.nextButton = QPushButton("Next")
        self.nextButton.setIconSize(btnSize)
        self.nextButton.clicked.connect(self.next)

        self.removeButton = QPushButton("Remove")
        self.removeButton.setIconSize(btnSize)
        self.removeButton.clicked.connect(self.remove)
        
        
        self.groundTruth = QLabel("Ground Truth")
        self.groundTruth.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.groundTruth.setFixedWidth(640)
        self.groundTruth.setFixedHeight(640)
        self.groundTruth.setStyleSheet("border: 1px solid black")

        self.prediction = QLabel("Prediction")
        self.prediction.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.prediction.setFixedWidth(640)
        self.prediction.setFixedHeight(640)
        self.prediction.setStyleSheet("border: 1px solid black")

        layout_img = QHBoxLayout()
        layout_img.addWidget(self.groundTruth)
        layout_img.addWidget(self.prediction)

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.removeButton)
        layout_button.addWidget(self.nextButton)

        layout = QVBoxLayout()
        layout.addLayout(layout_img)
        layout.addLayout(layout_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def next(self):
        global curr_img
        name_of_img = img_names[curr_img]
        self.groundTruth.setPixmap(QPixmap('/Users/abbasmammadov/Desktop/PyQt6-missings/gt_img/' + name_of_img + '.jpg'))
        self.prediction.setPixmap(QPixmap('/Users/abbasmammadov/Desktop/PyQt6-missings/pred_img/' + name_of_img + '.jpg'))
        self.groundTruth.setScaledContents(True)
        self.prediction.setScaledContents(True)
        curr_img += 1

    
    def remove(self):
        print("Play button clicked")




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(600, 400)
    player.show()
    sys.exit(app.exec())