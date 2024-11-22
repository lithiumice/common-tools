import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QListWidget, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel, QSlider, QLineEdit, QListWidgetItem)
# from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtGui import QPixmap, QImage, QIcon  # 添加 QIcon
from PyQt6.QtCore import Qt, QSize
from PIL import Image
import io

class ImageListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setIconSize(QSize(100, 100))

    def dropEvent(self, event):
        super().dropEvent(event)
        self.parent().parent().update_preview()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Concatenator")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        self.select_button = QPushButton("Select Images")
        self.select_button.clicked.connect(self.select_images)
        left_layout.addWidget(self.select_button)

        self.image_list = ImageListWidget()
        left_layout.addWidget(self.image_list)

        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setRange(0, 100)
        self.interval_slider.setValue(10)
        self.interval_slider.valueChanged.connect(self.update_preview)
        left_layout.addWidget(QLabel("Interval:"))
        left_layout.addWidget(self.interval_slider)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Enter width (px)")
        self.width_input.textChanged.connect(self.update_preview)
        left_layout.addWidget(QLabel("Output Width:"))
        left_layout.addWidget(self.width_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_image)
        left_layout.addWidget(self.save_button)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.preview_label)

        main_widget = QWidget()
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.images = []
        
        
    def select_images(self):
        file_dialog = QFileDialog()
        image_files, _ = file_dialog.getOpenFileNames(self, "Select Images", "", "Image Files (*.png *.jpg *.bmp)")
        
        self.image_list.clear()
        self.images = []
        
        for file in image_files:
            image = Image.open(file)
            # 把image缩小到宽度为100 pixels， 高度等比例缩放
            image.thumbnail((100, 100 * image.size[1] // image.size[0]))
            self.images.append(image)
            pixmap = QPixmap(file)
            icon = QIcon(pixmap)  # 创建 QIcon 对象
            item = QListWidgetItem()
            item.setIcon(icon)  # 使用 QIcon 对象
            item.setText(file.split('/')[-1])
            self.image_list.addItem(item)
        
        self.update_preview()
        
    def update_preview(self):
        if not self.images:
            return

        interval = self.interval_slider.value()
        try:
            output_width = int(self.width_input.text())
        except ValueError:
            output_width = 500  # Default width if input is invalid

        total_height = sum(int(output_width * img.size[1] / img.size[0]) for img in self.images) + interval * (len(self.images) - 1)
        result = Image.new('RGB', (output_width, total_height), (255, 255, 255))

        y_offset = 0
        for img in self.images:
            resized_img = img.copy()
            resized_img.thumbnail((output_width, output_width * img.size[1] // img.size[0]))
            result.paste(resized_img, (0, y_offset))
            y_offset += resized_img.size[1] + interval

        buffer = io.BytesIO()
        result.save(buffer, format="PNG")
        qt_image = QImage.fromData(buffer.getvalue())
        pixmap = QPixmap.fromImage(qt_image)
        
        scaled_pixmap = pixmap.scaledToWidth(self.preview_label.width(), Qt.TransformationMode.SmoothTransformation)
        self.preview_label.setPixmap(scaled_pixmap)

    def save_image(self):
        if not self.images:
            return

        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "Save Image", "", "PNG Files (*.png)")
        
        if save_path:
            interval = self.interval_slider.value()
            try:
                output_width = int(self.width_input.text())
            except ValueError:
                output_width = 500  # Default width if input is invalid

            total_height = sum(int(output_width * img.size[1] / img.size[0]) for img in self.images) + interval * (len(self.images) - 1)
            result = Image.new('RGB', (output_width, total_height), (255, 255, 255))

            y_offset = 0
            for img in self.images:
                resized_img = img.copy()
                resized_img.thumbnail((output_width, output_width * img.size[1] // img.size[0]))
                result.paste(resized_img, (0, y_offset))
                y_offset += resized_img.size[1] + interval

            result.save(save_path, "PNG")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())