import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QRadioButton, QSlider, QLabel, QFileDialog)
from PyQt6.QtCore import Qt
from PIL import Image

class ImageConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertidor de Imágenes")
        self.setGeometry(100, 100, 800, 200)

        # Variables
        self.images_to_convert = []
        self.output_folder = ""
        self.formato_seleccionado = "WEBP"  # Por defecto

        # Widget principal y layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Botones de selección
        button_layout = QHBoxLayout()
        self.select_images_btn = QPushButton("Seleccionar Imágenes")
        self.select_images_btn.clicked.connect(self.abrir_dialog)
        button_layout.addWidget(self.select_images_btn)

        self.select_folder_btn = QPushButton("Seleccionar Carpeta de Destino")
        self.select_folder_btn.clicked.connect(self.carpeta_destino)
        button_layout.addWidget(self.select_folder_btn)
        main_layout.addLayout(button_layout)

        # Botón de procesamiento
        self.process_btn = QPushButton("Procesar")
        self.process_btn.clicked.connect(self.procesar_imagenes)
        main_layout.addWidget(self.process_btn)

        # Radio buttons para formatos
        formats_layout = QHBoxLayout()
        self.jpeg_radio = QRadioButton("JPEG")
        self.jpeg_radio.clicked.connect(lambda: self.set_formato("JPEG"))
        formats_layout.addWidget(self.jpeg_radio)

        self.webp_radio = QRadioButton("WEBP")
        self.webp_radio.setChecked(True)  # Seleccionado por defecto
        self.webp_radio.clicked.connect(lambda: self.set_formato("WEBP"))
        formats_layout.addWidget(self.webp_radio)

        self.png_radio = QRadioButton("PNG")
        self.png_radio.clicked.connect(lambda: self.set_formato("PNG"))
        formats_layout.addWidget(self.png_radio)

        self.gif_radio = QRadioButton("GIF")
        self.gif_radio.clicked.connect(lambda: self.set_formato("GIF"))
        formats_layout.addWidget(self.gif_radio)
        main_layout.addLayout(formats_layout)

        # Slider para calidad
        quality_layout = QHBoxLayout()
        quality_label = QLabel("Calidad (solo JPEG):")
        quality_layout.addWidget(quality_label)

        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setMinimum(0)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(50)
        quality_layout.addWidget(self.quality_slider)

        self.quality_value_label = QLabel("50")
        self.quality_slider.valueChanged.connect(lambda: self.quality_value_label.setText(str(self.quality_slider.value())))
        quality_layout.addWidget(self.quality_value_label)
        main_layout.addLayout(quality_layout)

        # Etiqueta de estado
        self.status_label = QLabel("Esperando selección...")
        main_layout.addWidget(self.status_label)

    def abrir_dialog(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Selecciona las imágenes a convertir",
            "", "Images (*.png *.jpeg *.jpg *.gif *.bmp *.webp);;All Files (*.*)"
        )
        if files:
            self.images_to_convert = files
            self.status_label.setText(f"Imágenes seleccionadas: {len(files)}")

    def carpeta_destino(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona la carpeta de destino")
        if folder:
            self.output_folder = folder
            self.status_label.setText(f"Carpeta de destino: {folder}")

    def set_formato(self, formato):
        self.formato_seleccionado = formato

    def procesar_imagenes(self):
        if not self.images_to_convert or not self.output_folder:
            self.status_label.setText("Error: Selecciona imágenes y una carpeta de destino.")
            return

        for image_path in self.images_to_convert:
            try:
                image_name = os.path.splitext(os.path.basename(image_path))[0]
                output_image = f"{self.output_folder}/{image_name}.{self.formato_seleccionado.lower()}"
                self.convert_image(image_path, output_image, self.quality_slider.value())
                self.status_label.setText(f"Convertido: {image_name} a {self.formato_seleccionado}")
            except Exception as e:
                self.status_label.setText(f"Error al convertir {image_name}: {str(e)}")
                break

        self.status_label.setText("Conversión completada.")

    def convert_image(self, input_path, output_path, quality):
        img = Image.open(input_path)
        if output_path.lower().endswith('.jpeg') or output_path.lower().endswith('.jpg'):
            img = img.convert("RGB")
        if output_path.lower().endswith('.jpeg') or output_path.lower().endswith('.jpg'):
            img.save(output_path, quality=quality)
        else:
            img.save(output_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConverter()
    window.show()
    sys.exit(app.exec())