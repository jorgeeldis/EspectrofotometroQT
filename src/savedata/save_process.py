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

        self.name = QLabel("Sample:")
        self.layout.addWidget(self.name)
        self.nameLineEdit = QLineEdit(self)
        self.layout.addWidget(self.nameLineEdit)

        self.name = QLabel("User:")
        self.layout.addWidget(self.name)
        self.nameLineEdit = QLineEdit(self)
        self.layout.addWidget(self.nameLineEdit)

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
        if self.saveDataTypeComboBox.currentText() == "TXT":
            save_data_type = "TXT"
        elif self.saveDataTypeComboBox.currentText() == "PDF":
            save_data_type = "PDF"
        elif self.saveDataTypeComboBox.currentText() == "CSV":
            save_data_type = "CSV"
        elif self.saveDataTypeComboBox.currentText() == "XLSX":
            save_data_type = "XLSX"
        print(f"Saving settings: Save data type = {save_data_type}")
        # Add code here to save the settings...