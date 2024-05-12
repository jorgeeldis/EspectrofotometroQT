import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox, QGraphicsView, QMessageBox
from ui.main_window_ui import Ui_MainWindow
from pyqtgraph.exporters import CSVExporter
from pyqtgraph.exporters import SVGExporter
from pyqtgraph.exporters import ImageExporter
from PyQt5.QtCore import pyqtSignal
from .create_pdf import PDFReport
from .upload_file import upload
from PyQt5 import QtCore, QtGui, QtWidgets

class SaveWindow(QMainWindow, Ui_MainWindow):
    saveSettingsRequested = pyqtSignal(tuple)
    def __init__(self, parent=None,  graphWidget=None, ):
        super(SaveWindow, self).__init__(parent)
        self.graphWidget = graphWidget
        #self.wavelengthFunction = wavelengthFunction()
        self.setWindowTitle("Save Data")

        # Create a central widget to hold the layout and widgets
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create a layout
        self.layout = QVBoxLayout(self.centralWidget)

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(15)  # Set the font size to 24 points

        self.sample = QLabel("Sample: ")
        self.sample.setFont(font)
        self.layout.addWidget(self.sample)
        self.sampleLineEdit = QLineEdit(self)
        self.sampleLineEdit.setFont(font)
        self.layout.addWidget(self.sampleLineEdit)

        self.user = QLabel("User: ")
        self.user.setFont(font)
        self.layout.addWidget(self.user)
        self.userLineEdit = QLineEdit(self)
        self.userLineEdit.setFont(font)
        self.layout.addWidget(self.userLineEdit)

        self.saveDataType = QLabel("Export as:")
        self.saveDataType.setFont(font)
        self.layout.addWidget(self.saveDataType)
        self.saveDataTypeComboBox = QComboBox(self)
        self.saveDataTypeComboBox.setFont(font)
        self.saveDataTypeComboBox.addItems(["PDF", "CSV", "SVG", "PNG"])
        self.layout.addWidget(self.saveDataTypeComboBox)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.setFont(font)  # Set the font for the button
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)

        self.message = QLabel("No saved data.")
        self.message.setFont(font)
        self.layout.addWidget(self.message)


    def saveSettings(self):
        # Save the settings
        if self.saveDataTypeComboBox.currentText() == "PDF":
            self.save_as_pdf()
        elif self.saveDataTypeComboBox.currentText() == "CSV":
            self.save_as_csv()
        elif self.saveDataTypeComboBox.currentText() == "SVG":
            self.save_as_svg()
        elif self.saveDataTypeComboBox.currentText() == "PNG":
            self.save_as_png()

    def save_as_pdf(self):
        # Add code here to save as PDF...
        print("Saving as PDF...")

        plot_item = self.graphWidget.getPlotItem()
        exporter = ImageExporter(plot_item)
        exporter.export("./savedata/graph.png")

        filename = f"./savedata/{self.sampleLineEdit.text()}.pdf"  # Combine the sample name and the extension into a single string
        title = f"{self.sampleLineEdit.text()}"
        user = f"{self.userLineEdit.text()}"
        pdf_obj = PDFReport()
        pdf_obj.create_pdf(filename, title, user)
        print("Report saved.")
        self.message.setText("Report saved.")
        upload(filename)

    def save_as_csv(self):
        # Add code here to save as CSV...
        old_filename = "./data/interpolate_muestra.txt"
        new_filename = f"./data/{self.sampleLineEdit.text()}.csv"  # New filename
        os.rename(old_filename, new_filename)  # Rename the file
        print("Data saved as CSV.")
        self.message.setText("Data saved as CSV.")
        upload(new_filename)  # Upload the renamed file

    def save_as_svg(self):
        # Add code here to save as SVG...
        print("Saving as SVG...")
        plot_item = self.graphWidget.getPlotItem()
        exporter = SVGExporter(plot_item)
        filename = f"{self.sampleLineEdit.text()}.svg"  # Combine the sample name and the extension into a single string
        exporter.export(filename)
        print("Data saved as SVG.")
        self.message.setText("Graph saved as SVG.")
        upload(filename)

    def save_as_png(self):
        # Add code here to save as PNG...
        print("Saving as PNG...")
        plot_item = self.graphWidget.getPlotItem()
        exporter = ImageExporter(plot_item)
        filename = f"{self.sampleLineEdit.text()}.png"  # Combine the sample name and the extension into a single string
        exporter.export(filename)
        print("Data saved as PNG.")
        self.message.setText("Graph saved as PNG.")
        upload(filename)
