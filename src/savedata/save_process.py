from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox

class SaveWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SaveWindow, self).__init__(parent)
        self.setWindowTitle("Save Data")

        # Create a central widget to hold the layout and widgets
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create a layout
        self.layout = QVBoxLayout(self.centralWidget)

        self.saveDataType = QLabel("Save as:")
        self.layout.addWidget(self.saveDataType)
        self.saveDataTypeComboBox = QComboBox(self)
        self.saveDataTypeComboBox.addItems(["TXT", "PDF", "CSV", "XLSX"])
        self.layout.addWidget(self.saveDataTypeComboBox)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)

    def saveSettings(self):
        # Save the settings
        save_data_type = self.saveDataTypeComboBox.currentText()
        print(f"Saving settings: Save data type = {save_data_type}")
        # Add code here to save the settings...