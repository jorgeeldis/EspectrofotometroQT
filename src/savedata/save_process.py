from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox, QGraphicsView, QMessageBox
from ui.main_window_ui import Ui_MainWindow
from pyqtgraph.exporters import CSVExporter
from pyqtgraph.exporters import SVGExporter
from pyqtgraph.exporters import ImageExporter
from PyQt5.QtCore import pyqtSignal
from .create_pdf import PDFReport

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

        self.sample = QLabel("Sample: ")
        self.layout.addWidget(self.sample)
        self.sampleLineEdit = QLineEdit(self)
        self.layout.addWidget(self.sampleLineEdit)

        self.user = QLabel("User: ")
        self.layout.addWidget(self.user)
        self.userLineEdit = QLineEdit(self)
        self.layout.addWidget(self.userLineEdit)

        self.saveDataType = QLabel("Export as:")
        self.layout.addWidget(self.saveDataType)
        self.saveDataTypeComboBox = QComboBox(self)
        self.saveDataTypeComboBox.addItems(["PDF", "CSV", "SVG", "PNG"])
        self.layout.addWidget(self.saveDataTypeComboBox)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)

        self.message = QLabel("No saved data.")
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

    def save_as_csv(self):
        # Add code here to save as CSV...
        plot_item = self.graphWidget.getPlotItem()
        exporter = CSVExporter(plot_item)
        filename = f"{self.sampleLineEdit.text()}.csv"  # Combine the sample name and the extension into a single string
        exporter.export(filename)
        print("Data saved as CSV.")
        self.message.setText("Data saved as CSV.")

    def save_as_svg(self):
        # Add code here to save as SVG...
        print("Saving as SVG...")
        plot_item = self.graphWidget.getPlotItem()
        exporter = SVGExporter(plot_item)
        filename = f"{self.sampleLineEdit.text()}.svg"  # Combine the sample name and the extension into a single string
        exporter.export(filename)
        print("Data saved as SVG.")
        self.message.setText("Graph saved as SVG.")

    def save_as_png(self):
        # Add code here to save as PNG...
        print("Saving as PNG...")
        plot_item = self.graphWidget.getPlotItem()
        exporter = ImageExporter(plot_item)
        filename = f"{self.sampleLineEdit.text()}.png"  # Combine the sample name and the extension into a single string
        exporter.export(filename)
        print("Data saved as PNG.")
        self.message.setText("Graph saved as PNG.")
