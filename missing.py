from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import QDir, Qt, QUrl, QSize
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel, 
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar, QMainWindow, QLineEdit)

import os 
import shutil
import csv

# path for the filtering GUI
PATH = '/Users/abbasmammadov/Desktop/filtering_GUI/'

curr_img = 0

all_imgs = list()
with open(PATH + 'totest.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        all_imgs.append(line.strip())

processed_imgs = list()
with open(PATH + 'so_far_processed_images.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        processed_imgs.append(line.strip())

img_names = list()
for img_name in all_imgs:
    if not img_name in processed_imgs:
        img_names.append(img_name)


info_gt = dict()
with open(PATH + 'csv_files/gt_labels.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # if line is first line
        if line.split(',')[0] == 'img_name':
            continue
        info_gt[line.split(',')[0]] = line.split('{')[1].split('}')[0].replace(',', '\n')


info_pred = dict()
with open(PATH + 'csv_files/pred_labels.csv', 'r') as f:
    lines = f.readlines()
    for line in lines:
        # if line is first line
        if line.split(',')[0] == 'img_name':
            continue
        info_pred[line.split(',')[0]] = line.split('{')[1].split('}')[0].replace(',', '\n')


descriptions_with_names = list()

so_far_processed_images = list()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Mismatch Filter")
        
        btnSize = QSize(16, 16)

        self.nextButton = QPushButton("Next")
        self.nextButton.setIconSize(btnSize)
        self.nextButton.clicked.connect(self.next)  

        self.saveSoFarResultsButton = QPushButton("Save So Far Results")
        self.saveSoFarResultsButton.setIconSize(btnSize)
        self.saveSoFarResultsButton.clicked.connect(self.savesofar)
        
        self.groundTruth = QLabel("Ground Truth")
        self.groundTruth.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groundTruth.setFixedWidth(480)
        self.groundTruth.setFixedHeight(480)
        self.groundTruth.setStyleSheet("border: 1px solid black")

        self.gt_labels = QLabel("Ground Truth Labels")
        self.gt_labels.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gt_labels.setFixedWidth(480)
        self.gt_labels.setFixedHeight(120)
        self.gt_labels.setStyleSheet("border: 1px solid black")

        self.rawImg = QLabel("Raw Image")  
        self.rawImg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rawImg.setFixedWidth(480)
        self.rawImg.setFixedHeight(480)
        self.rawImg.setStyleSheet("border: 1px solid black")

        #ask for description of problem to input the text
        self.description = QLineEdit('Add description of problem')
        self.description.setFixedWidth(480)
        self.description.setFixedHeight(120)
        self.description.setStyleSheet("border: 1px solid black")

        self.prediction = QLabel("Prediction")
        self.prediction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prediction.setFixedWidth(480)
        self.prediction.setFixedHeight(480)
        self.prediction.setStyleSheet("border: 1px solid black")

        self.pred_labels = QLabel("Prediction Truth Labels")
        self.pred_labels.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.pred_labels.setFixedWidth(480)
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
        layout_button.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_button.addWidget(self.saveSoFarResultsButton)
        layout_button.setAlignment(Qt.AlignmentFlag.AlignRight)
        

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
        global so_far_processed_images
        
        if curr_img:
            name_of_img = img_names[curr_img-1]
            text = self.description.text()
            descriptions_with_names.append([str(name_of_img), str(text)])

        if curr_img:
            so_far_processed_images.append(img_names[curr_img-1])

        
        
        if curr_img == len(img_names):
            # save descriptions_with_names to csv file
            with open(PATH + 'csv_files/descriptions_with_names.csv', 'a') as f:
                writer = csv.writer(f)
                # writer.writerow(['img_name', 'description'])
                for row in descriptions_with_names:
                    writer.writerow(row)
            # save so_far_processed_images to txt file
            with open(PATH + 'so_far_processed_images.txt', 'a') as f:
                for img_name in so_far_processed_images:
                    f.write(img_name + '\n')
            # close the app
            sys.exit()

        name_of_img = img_names[curr_img]
        self.groundTruth.setPixmap(QPixmap(PATH + 'gt_img/' + name_of_img + '.jpg'))
        self.rawImg.setPixmap(QPixmap(PATH + 'raw_img/' + name_of_img + '.jpg'))
        self.prediction.setPixmap(QPixmap(PATH + 'pred_img/' + name_of_img + '.jpg'))
        self.groundTruth.setScaledContents(True)
        self.rawImg.setScaledContents(True)
        self.prediction.setScaledContents(True)

        self.gt_labels.setText(info_gt[name_of_img])
        self.pred_labels.setText(info_pred[name_of_img])

        self.description.setText('')

        curr_img += 1

    def savesofar(self):
        global so_far_processed_images
        with open(PATH + 'so_far_processed_images.txt', 'a') as f:
            for img in so_far_processed_images:
                f.write(img + '\n')

        global descriptions_with_names
        with open(PATH + 'csv_files/descriptions_with_names.csv', 'a') as f:
            writer = csv.writer(f)
            for row in descriptions_with_names:
                writer.writerow(row)
        
        #close the GUI and exit
        sys.exit()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(600, 400)
    player.show()
    sys.exit(app.exec())