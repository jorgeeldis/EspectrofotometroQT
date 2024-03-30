class SpecificValues:
    def __init__(self):
        pass

    def set_specific_values(self, specific_values):

        if self.progressBar.value() == 100:
            n450 = 56  # replace with the line number you want to read
            n435 = 50
            n500 = 76
            n550 = 97
            n570 = 106
            n600 = 120
            n650 = 143
            # 50 for 435, 56 for 450, 76 for 500, 97 for 550, 106 for 570, 120 for 600, 143 for 650
            with open("./data/single_muestra.txt", "r") as file:
                lines = file.readlines()
                if n450 <= len(lines):
                    db450 = lines[n450 - 1].strip()
                if n435 <= len(lines):
                    db435 = lines[n435 - 1].strip()
                if n500 <= len(lines):
                    db500 = lines[n500 - 1].strip()
                if n550 <= len(lines):
                    db550 = lines[n550 - 1].strip()
                if n570 <= len(lines):
                    db570 = lines[n570 - 1].strip()
                if n600 <= len(lines):
                    db600 = lines[n600 - 1].strip()
                if n650 <= len(lines):
                    db650 = lines[n650 - 1].strip()
                else:
                    print(f"The file has fewer than {n450} lines.")

                maxDBvalue = float("-inf")
                maxnvalue = 0
                for i, line in enumerate(lines, start=1):  # use lines instead of file
                    value = float(line.strip())
                    if value > maxDBvalue:
                        maxDBvalue = float(value)
                        print(maxDBvalue)
                        maxnvalue = i
                maxNMvalue = int(
                    self.wavelength[maxnvalue - 1]
                )  # get the corresponding nm value

                minDBvalue = float("inf")
                minNMvalue = 0
                for i, line in enumerate(lines, start=1):
                    value = float(line.strip())
                    if value < minDBvalue:
                        minDBvalue = float(value)
                        print(minDBvalue)
                        minNMvalue = i
                minNMvalue = int(self.wavelength[minNMvalue - 1])

            self.specificLabel.setText("Key Values (dB):")
            self.db450Label.setText(
                "450nm: " + str("{:.2f}".format(float(db450))) + "dB"
            )
            self.db435Label.setText(
                "435nm: " + str("{:.2f}".format(float(db435))) + "dB"
            )
            self.db500Label.setText(
                "500nm: " + str("{:.2f}".format(float(db500))) + "dB"
            )
            self.db550Label.setText(
                "550nm: " + str("{:.2f}".format(float(db550))) + "dB"
            )
            self.db570Label.setText(
                "570nm: " + str("{:.2f}".format(float(db570))) + "dB"
            )
            self.db600Label.setText(
                "600nm: " + str("{:.2f}".format(float(db600))) + "dB"
            )
            self.db650Label.setText(
                "650nm: " + str("{:.2f}".format(float(db650))) + "dB"
            )
            self.maxDBLabel.setText(
                "Max dB: " + str("{:.2f}".format(float(maxDBvalue))) + "dB"
            )
            self.maxNMLabel.setText("Max nm: " + str(maxNMvalue) + "nm")
            self.minDBLabel.setText(
                "Min dB: " + str("{:.2f}".format(float(minDBvalue))) + "dB"
            )
            self.minNMLabel.setText("Min nm: " + str(minNMvalue) + "nm")
            self.btnBaseline.setEnabled(True)
            self.btnSingle.setEnabled(True)
            self.btnContinuous.setEnabled(True)
            self.btnSaveData.setEnabled(True)
            self.btnSettings.setEnabled(True)
            self.btnWavelength.setEnabled(True)
