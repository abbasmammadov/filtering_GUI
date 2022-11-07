from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import QDir, Qt, QUrl, QSize
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar, QMainWindow, QLineEdit)

import os 
import shutil
import csv

curr_img = 0

img_names = list()
with open('/Users/abbasmammadov/Desktop/PyQt6-missings/totest.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        img_names.append(line.strip())


info_gt = dict()
with open('/Users/abbasmammadov/Desktop/PyQt6-missings/gt_labels.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # if line is first line
        if line.split(',')[0] == 'img_name':
            continue
        info_gt[line.split(',')[0]] = line.split('{')[1].split('}')[0].replace(',', '\n')


info_pred = dict()
with open('/Users/abbasmammadov/Desktop/PyQt6-missings/pred_labels.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # if line is first line
        if line.split(',')[0] == 'img_name':
            continue
        info_pred[line.split(',')[0]] = line.split('{')[1].split('}')[0].replace(',', '\n')


descriptions_with_names = list()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mismatch Filter")
        
        btnSize = QSize(16, 16)

        self.nextButton = QPushButton("Next")
        self.nextButton.setIconSize(btnSize)
        self.nextButton.clicked.connect(self.next)  
        
        self.groundTruth = QLabel("Ground Truth")
        self.groundTruth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groundTruth.setFixedWidth(640)
        self.groundTruth.setFixedHeight(640)
        self.groundTruth.setStyleSheet("border: 1px solid black")

        self.gt_labels = QLabel("Ground Truth Labels")
        self.gt_labels.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gt_labels.setFixedWidth(640)
        self.gt_labels.setFixedHeight(120)
        self.gt_labels.setStyleSheet("border: 1px solid black")

        self.rawImg = QLabel("Raw Image")  
        self.rawImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rawImg.setFixedWidth(640)
        self.rawImg.setFixedHeight(640)
        self.rawImg.setStyleSheet("border: 1px solid black")

        #ask for description of problem to input the text
        self.description = QLineEdit('Add description of problem')
        self.description.setFixedWidth(640)
        self.description.setFixedHeight(120)
        self.description.setStyleSheet("border: 1px solid black")

        self.prediction = QLabel("Prediction")
        self.prediction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prediction.setFixedWidth(640)
        self.prediction.setFixedHeight(640)
        self.prediction.setStyleSheet("border: 1px solid black")

        self.pred_labels = QLabel("Prediction Truth Labels")
        self.pred_labels.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.pred_labels.setFixedWidth(640)
        self.pred_labels.setFixedHeight(120)
        self.pred_labels.setStyleSheet("border: 1px solid black")

        layout_img = QHBoxLayout()
        layout_img.addWidget(self.groundTruth)
        layout_img.addWidget(self.rawImg)
        layout_img.addWidget(self.prediction)

        layout_labels = QHBoxLayout()
        layout_labels.addWidget(self.gt_labels)
        layout_labels.addWidget(self.description)
        layout_labels.addWidget(self.pred_labels)

        layout_button = QHBoxLayout()
        layout_button.addWidget(self.nextButton)
        layout_button.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addLayout(layout_img)
        layout.addLayout(layout_labels)
        layout.addLayout(layout_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def next(self):
        global curr_img
        global descriptions_with_names
        if curr_img:
            name_of_img = img_names[curr_img-1]
            text = self.description.text()
            descriptions_with_names.append([str(name_of_img), str(text)])
        
        
        if curr_img == len(img_names):
            # save descriptions_with_names to csv file
            with open('/Users/abbasmammadov/Desktop/PyQt6-missings/descriptions_with_names.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['img_name', 'description'])
                for row in descriptions_with_names:
                    writer.writerow(row)

        name_of_img = img_names[curr_img]
        self.groundTruth.setPixmap(QPixmap('/Users/abbasmammadov/Desktop/PyQt6-missings/gt_img/' + name_of_img + '.jpg'))
        self.rawImg.setPixmap(QPixmap('/Users/abbasmammadov/Desktop/PyQt6-missings/raw_img/' + name_of_img + '.jpg'))
        self.prediction.setPixmap(QPixmap('/Users/abbasmammadov/Desktop/PyQt6-missings/pred_img/' + name_of_img + '.jpg'))
        self.groundTruth.setScaledContents(True)
        self.rawImg.setScaledContents(True)
        self.prediction.setScaledContents(True)

        self.gt_labels.setText(info_gt[name_of_img])
        self.pred_labels.setText(info_pred[name_of_img])


        self.description.setText('')

        curr_img += 1


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(600, 400)
    player.show()
    sys.exit(app.exec())