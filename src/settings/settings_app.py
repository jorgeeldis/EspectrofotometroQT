from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox

class SettingsWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Settings")

        # Create a central widget to hold the layout and widgets
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create a layout
        self.layout = QVBoxLayout(self.centralWidget)

        # Create a label and line edit for each setting
        self.wavelengthLabel = QLabel("Wavelength file:")
        self.layout.addWidget(self.wavelengthLabel)
        self.wavelengthLineEdit = QLineEdit(self)
        self.layout.addWidget(self.wavelengthLineEdit)

        # Add more settings here...
        # Change color of graph
        # Create a combo box for selecting the graph color
        self.graphColorLabel = QLabel("Graph color:")
        self.layout.addWidget(self.graphColorLabel)
        self.graphColorComboBox = QComboBox(self)
        self.graphColorComboBox.addItems(["Red", "Green", "Blue"])  # Add more colors as needed
        self.layout.addWidget(self.graphColorComboBox)

        # Create a spin box for selecting the font size
        self.fontSizeLabel = QLabel("Font size:")
        self.layout.addWidget(self.fontSizeLabel)
        self.fontSizeSpinBox = QSpinBox(self)
        self.fontSizeSpinBox.setRange(8, 72)  # Set the range of font sizes
        self.layout.addWidget(self.fontSizeSpinBox)

        self.graphType = QLabel("Graph type:")
        self.layout.addWidget(self.graphType)
        self.graphTypeComboBox = QComboBox(self)
        self.graphTypeComboBox.addItems(["Line", "Bar", "Scatter"])
        self.layout.addWidget(self.graphTypeComboBox)

        self.mathGraphType = QLabel("Math graph type:")
        self.layout.addWidget(self.mathGraphType)
        self.mathGraphTypeComboBox = QComboBox(self)
        self.mathGraphTypeComboBox.addItems(["Lineal", "Logarithmic"])
        self.layout.addWidget(self.mathGraphTypeComboBox)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveSettings)
        self.layout.addWidget(self.saveButton)

    def saveSettings(self):
        # Save the settings
        wavelength_file = self.wavelengthLineEdit.text()
        graph_color = self.graphColorComboBox.currentText()
        font_size = self.fontSizeSpinBox.value()
        print(f"Saving settings: Wavelength file = {wavelength_file}, Graph color = {graph_color}, Font size = {font_size}")
        # Add code here to save the settings...