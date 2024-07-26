import textwrap
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
import random
import datetime
from libs.wavelengths import wavelength
from selectwavelength.wavlength_process import get_absorbance
import math

class PDFReport:

    def __init__(self):
       self.wavelengthFunction = wavelength()
       print(self.wavelengthFunction)

    def create_pdf(self, file_path, Title, User):

        n465 = 161
        n480 = 176
        n500 = 196
        n525 = 221
        n546 = 242
        n565 = 261
        n580 = 276
        n590 = 286
        n660 = 346

        # 50 for 474, 56 for 428, 76 for 535, 97 for 587, 106 for 609, 120 for 600, 143 for 660
        with open("./data/interpolate_muestra.txt", "r") as file:
            lines = file.readlines()
            if n465 <= len(lines):
                db465 = get_absorbance(465)
            if n480 <= len(lines):
                db480 = get_absorbance(480)
            if n500 <= len(lines):
                db500 = get_absorbance(500)
            if n525 <= len(lines):
                db525 = get_absorbance(525)
            if n546 <= len(lines):
                db546 = get_absorbance(546)
            if n565 <= len(lines):
                db565 = get_absorbance(565)
            if n580 <= len(lines):
                db580 = get_absorbance(580)
            if n590 <= len(lines):
                db590 = get_absorbance(590)
            if n660 <= len(lines):
                db660 = get_absorbance(660)
            else:
                print(f"The file has fewer than {n465} lines.")
                
        with open("./data/single_muestra.txt", "r") as file:
            lines = file.readlines()
            maxDBvalue = float("-inf")
            maxnvalue = 0
            for i, line in enumerate(
                lines, start=1
            ):  # use lines instead of file
                value = float(line.strip())
                if value > maxDBvalue:
                    maxDBvalue = float(value)
                    # print(maxDBvalue)
                    maxnvalue = i
            maxNMvalue = int(
                self.wavelengthFunction[maxnvalue - 1]
            )  # get the corresponding nm value

            minDBvalue = float("inf")
            minNMvalue = 0
            for i, line in enumerate(lines, start=1):
                value = float(line.strip())
                if value < minDBvalue:
                    minDBvalue = float(value)
                    # print(minDBvalue)
                    minNMvalue = i
            minNMvalue = int(self.wavelengthFunction[minNMvalue - 1])

            mean = sum([float(line.strip()) for line in lines]) / len(lines)
            variance = sum([(float(line.strip()) - mean) ** 2 for line in lines]) / len(lines)
            standard_deviation = math.sqrt(variance)
            RMS = math.sqrt(sum([float(line.strip()) ** 2 for line in lines]) / len(lines))

            with open("./data/wavelength_muestra.txt", "r") as f:
                wavelengths = [line.strip() for line in f]
            with open("./data/single_muestra.txt", "r") as f:
                absorbances = [line.strip() for line in f]
            with open("./data/interpolate_muestra.txt", "r") as f:
                lines = [line.strip().split(',') for line in f.readlines()]
                interpolate_wavelength, new_absorbances = zip(*[(float(wavelength), float(absorbance)) for wavelength, absorbance in lines])
            weighted_average = sum([float(wavelength) * float(absorbance) for wavelength, absorbance in zip(wavelengths, absorbances)]) / sum([float(absorbance) for absorbance in absorbances])


        # Create a new PDF with Reportlab
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Add a title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30, height - 50, Title + ' Spectrophotometric Report')

        # Add a detailed description
        c.setFont("Helvetica", 12)
        text = 'This spectrophotometer report provides a comprehensive analysis of the sample. It includes the sample\'s absorbance spectrum, a table of absorbance values at specific wavelengths, and a detailed interpretation of the results. The report is designed to provide clear, actionable insights for further research or industrial applications.'
        lines = textwrap.wrap(text, width=100)  # Split the text into lines of up to 60 characters each
        x = 30  # The x-coordinate where the text should start
        y = height - 80  # The y-coordinate where the first line of text should start
        for line in lines:
            c.drawString(x, y, line)
            y -= 14  # Move to the next line

        # Add a table of data
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 150, 'General information:')

        c.setFont("Helvetica", 12)
        c.drawString(30, height - 170, 'Sample Name: ' + Title)
        c.drawString(30, height - 190, 'User: ' + User)
        c.drawString(30, height - 210, 'Manufacturer: UTP')
        c.drawString(30, height - 230, 'Model: UTP-CG-001')
        c.drawString(30, height - 250, 'Serial Number: UTP30032024A')
        c.drawString(30, height - 270, 'Wavelength Range: 340 - 850 nm')
        c.drawString(300, height - 170, 'Baseline Correction: Yes')
        c.drawString(300, height - 190, 'Date: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        c.drawString(300, height - 210, 'Laboratory: Indicasat AIP')
        c.drawString(300, height - 230, 'Location: Panama City, Panama')
        c.drawString(300, height - 250, 'Light Source: High Power LED')
        c.drawString(300, height - 270, 'Detector: CMOS')

        # Add a brief description
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 300, 'Test condition')

        c.setFont("Helvetica", 12)
        c.drawString(30, height - 320, 'Temperature: 25°C') # Add a sensor ?
        c.drawString(30, height - 340, 'Humidity: 50%') # Add a sensor ?
        c.drawString(30, height - 360, 'WL Range: 350 - 750 nm')
        c.drawString(30, height - 380, 'Scan Speed: 39.55 nm/sec')
        c.drawString(30, height - 400, 'Test mode: Single')
        c.drawString(30, height - 420, 'Scan Mode: Absorbance')

        if 0.299 < float(db465) < 0.375 and 0.262 < float(db480) < 0.338 and 0.162 < float(db500) < 0.238 and 0.134 < float(db525) < 0.21 and 0.187 < float(db546) < 0.293 and 0.282 < float(db565) < 0.358 and 0.205 < float(db580) < 0.281 and 0.104 < float(db590) < 0.180:
            # Add a brief description
            c.setFont("Helvetica-Bold", 14)
            c.drawString(300, height - 300, 'Sample Analysis')
            c.setFont("Helvetica", 12)
            c.setFillColorRGB(0, 50, 0)  # Set text color to blue
            c.drawString(300, height - 315, 'No contamination detected')
            c.setFillColorRGB(0, 0, 0)  # Reset text color to black
            if 0.299 < float(db465) < 0.375:
                c.drawString(300, height - 380, f'465nm: {db465:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 380, f'465nm: {db465:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.262 < float(db480) < 0.338:
                c.drawString(300, height - 400, f'480nm: {db480:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 400, f'480nm: {db480:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.162 < float(db500) < 0.238:
                c.drawString(300, height - 420, f'500nm: {db500:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 420, f'500nm: {db500:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.134 < float(db525) < 0.21:
                c.drawString(400, height - 340, f'525nm: {db525:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 340, f'525nm: {db525:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.187 < float(db546) < 0.293:
                c.drawString(400, height - 360, f'546nm: {db546:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 360, f'546nm: {db546:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.282 < float(db565) < 0.358:
                c.drawString(400, height - 380, f'565nm: {db565:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 380, f'565nm: {db565:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.205 < float(db580) < 0.281:
                c.drawString(400, height - 400, f'580nm: {db580:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 400, f'580nm: {db580:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.104 < float(db590) < 0.180:
                c.drawString(400, height - 420, f'590nm: {db590:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 420, f'590nm: {db590:.4f}')
                c.setFillColorRGB(0, 0, 0)
        else:
            # Add a brief description
            c.setFont("Helvetica-Bold", 14)
            c.drawString(300, height - 300, 'Sample Analysis')
            

            c.setFont("Helvetica", 12)
            c.setFillColorRGB(100, 0, 0)  # Set text color to red
            c.drawString(300, height - 315, 'Contamination detected')
            c.setFillColorRGB(0, 0, 0)  # Reset text color to black
            if 0.299 < float(db465) < 0.375:
                c.drawString(300, height - 380, f'465nm: {db465:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 380, f'465nm: {db465:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.262 < float(db480) < 0.338:
                c.drawString(300, height - 400, f'480nm: {db480:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 400, f'480nm: {db480:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.162 < float(db500) < 0.238:
                c.drawString(300, height - 420, f'500nm: {db500:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(300, height - 420, f'500nm: {db500:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.134 < float(db525) < 0.21:
                c.drawString(400, height - 340, f'525nm: {db525:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 340, f'525nm: {db525:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.187 < float(db546) < 0.293:
                c.drawString(400, height - 360, f'546nm: {db546:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 360, f'546nm: {db546:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.282 < float(db565) < 0.358:
                c.drawString(400, height - 380, f'565nm: {db565:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 380, f'565nm: {db565:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.205 < float(db580) < 0.281:
                c.drawString(400, height - 400, f'580nm: {db580:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 400, f'580nm: {db580:.4f}')
                c.setFillColorRGB(0, 0, 0)
            if 0.104 < float(db590) < 0.180:
                c.drawString(400, height - 420, f'590nm: {db590:.4f}')
            else:
                c.setFillColorRGB(100, 0, 0)
                c.drawString(400, height - 420, f'590nm: {db590:.4f}')
                c.setFillColorRGB(0, 0, 0)
    
        # Add a graph
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 450, 'Measured Graph:')
        c.drawImage(ImageReader("./savedata/graph.png"), 30, height - 760, width=500, height=300)
        
        #New page
        c.showPage()
        # Add a title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30, height - 50, 'Parameters: ')
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 80, 'Key Parameters:')
        #Falta
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 100, 'Max dB: ' + str(maxDBvalue))
        c.drawString(30, height - 120, 'Max nm: ' + str(maxNMvalue))
        c.drawString(30, height - 140, 'Min dB: ' + str(minDBvalue))
        c.drawString(30, height - 160, 'Min nm: ' + str(minNMvalue))
        c.drawString(30, height - 200, "Blue's (465nm) dB: " + str(db465))
        c.drawString(30, height - 220, "Green's (525nm) dB: " + str(db525))
        c.drawString(30, height - 240, "Yellow's (580nm) dB: " + str(db580))
        c.drawString(30, height - 260, "Orange's (690nm) dB: " + str(db590))
        c.drawString(30, height - 280, "Red's (660nm) dB: " + str(db660))

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 320, 'Radiometric Parameters:')
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 340, 'Radiant Flux: 1000 rad')
        c.drawString(30, height - 360, 'Radiant Density: 518 rad/mm2')
        c.drawString(30, height - 380, 'Color Rendering: 70')
        c.drawString(30, height - 400, 'Thermal resistance: 1.6 C°/W')
        c.drawString(30, height - 420, 'Radiant Efficacy: 206 rad/W')

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 460, 'Electrical Parameters:')
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 480, 'Voltage: 12 V')
        c.drawString(30, height - 500, 'Current: 3 A')
        c.drawString(30, height - 520, 'Power: 36 W')
        c.drawString(30, height - 540, 'Power Factor: 1.0')
        c.drawString(30, height - 560, 'Frequency: 60 Hz')

        c.setFont("Helvetica-Bold", 14)
        c.drawString(300, height - 80, 'Statistical Parameters:')
        c.setFont("Helvetica", 12)
        c.drawString(300, height - 120, 'Mean: ' + str(mean))
        c.drawString(300, height - 140, 'Standard Deviation: ' + str(standard_deviation))
        c.drawString(300, height - 160, 'Variance: ' + str(variance))
        c.drawString(300, height - 180, 'RMS: ' + str(RMS))
        c.drawString(300, height - 200, 'Weighted Average (nm): ' + str(weighted_average))
        c.drawString(300, height - 220, 'Minimum Value: ' + str(minDBvalue))
        c.drawString(300, height - 240, 'Maximum Value: ' + str(maxDBvalue))
        c.drawString(300, height - 260, 'Number of Values: 445')

        #"colorimetric parameters"
        #"photometric parameters"
        #"electrical parameters"

        #new page
        c.showPage()
        with open("./data/wavelength_muestra.txt", "r") as f:
            wavelengths = [line.strip() for line in f]
        with open("./data/single_muestra.txt", "r") as f:
            absorbances = [line.strip() for line in f]
        with open("./data/baseline_muestra.txt", "r") as f:
            baselines = [line.strip() for line in f]

        # Assuming wavelengths and absorbances are lists
        wavelengths = np.array(wavelengths)
        absorbances = np.array(absorbances)
        baselines = np.array(baselines)

        # Create an array of new x values (i.e., 305, 306, 307, ...)
        new_wavelengths = np.arange(int(wavelengths[0]), int(wavelengths[-1]) + 1)

        # Interpolate the y values
        new_absorbances = np.interp((new_wavelengths.astype(float)), (wavelengths.astype(float)), (absorbances.astype(float)))

        new_baselines = np.interp((new_wavelengths.astype(float)), (wavelengths.astype(float)), (baselines.astype(float)))

        new_wavelengths = [str(i) for i in new_wavelengths]
        new_absorbances = [str(i) for i in new_absorbances]
        new_baselines = [str(i) for i in new_baselines]

        # Add a title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30, height - 50, 'Measured Data: ')

        # Create a table
        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]

        # Iterate over the first 35 values of wavelengths, absorbances, and baselines
        for wl1, abs1, base1 in zip(new_wavelengths[:35], new_absorbances[:35], new_baselines[:35]):
            # Calculate transmittance from new_baselines and absorbance
            try:
                single = round(float(base1) / (10 ** float(abs1)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base1)
            table_data.append([str(wl1), format(float(abs1), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 750)

        print (new_wavelengths[35:70], new_absorbances[35:70], new_baselines[35:70])
        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        # Iterate over the first 35 values of new_wavelengths, absorbances, and new_baselines
        for wl2, abs2, base2 in zip(new_wavelengths[35:70], new_absorbances[35:70], new_baselines[35:70]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base2) / (10 ** float(abs2)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base2)
            table_data.append([str(wl2), format(float(abs2), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 220, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl3, abs3, base3 in zip(new_wavelengths[70:105], new_absorbances[70:105], new_baselines[70:105]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base3) / (10 ** float(abs3)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base3)
            table_data.append([str(wl3), format(float(abs3), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 410, height - 750)

        # New page
        c.showPage()

        # Add a title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30, height - 50, 'Measured Data (cont): ')
        # Create a table
        # Create random data for the table
        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl4, abs4, base4 in zip(new_wavelengths[105:140], new_absorbances[105:140], new_baselines[105:140]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base4) / (10 ** float(abs4)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base4)
            table_data.append([str(wl4), format(float(abs4), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl5, abs5, base5 in zip(new_wavelengths[140:175], new_absorbances[140:175], new_baselines[140:175]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base5) / (10 ** float(abs5)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base5)
            table_data.append([str(wl5), format(float(abs5), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 220, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl6, abs6, base6 in zip(new_wavelengths[175:210], new_absorbances[175:210], new_baselines[175:210]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base6) / (10 ** float(abs6)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base6)
            table_data.append([str(wl6), format(float(abs6), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 410, height - 750)

        # New page
        c.showPage()

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl7, abs7, base7 in zip(new_wavelengths[210:245], new_absorbances[210:245], new_baselines[210:245]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base7) / (10 ** float(abs7)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base7)
            table_data.append([str(wl7), format(float(abs7), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl8, abs8, base8 in zip(new_wavelengths[245:280], new_absorbances[245:280], new_baselines[245:280]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base8) / (10 ** float(abs8)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base8)
            table_data.append([str(wl8), format(float(abs8), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 220, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl9, abs9, base9 in zip(new_wavelengths[280:315], new_absorbances[280:315], new_baselines[280:315]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base9) / (10 ** float(abs9)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base9)
            table_data.append([str(wl9), format(float(abs9), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 410, height - 750)

        # New page
        c.showPage()

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl10, abs10, base10 in zip(new_wavelengths[315:350], new_absorbances[315:350], new_baselines[315:350]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base10) / (10 ** float(abs10)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base10)
            table_data.append([str(wl10), format(float(abs10), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl11, abs11, base11 in zip(new_wavelengths[350:385], new_absorbances[350:385], new_baselines[350:385]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base11) / (10 ** float(abs11)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base11)
            table_data.append([str(wl11), format(float(abs11), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 220, height - 750)

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl12, abs12, base12 in zip(new_wavelengths[385:420], new_absorbances[385:420], new_baselines[385:420]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base12) / (10 ** float(abs12)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base12)
            table_data.append([str(wl12), format(float(abs12), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 410, height - 750)

        # New page
        c.showPage()

        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
        for wl13, abs13, base13 in zip(new_wavelengths[420:445], new_absorbances[420:445], new_baselines[420:445]):
            # Calculate transmittance from new_baselines and new_absorbances
            try:
                single = round(float(base13) / (10 ** float(abs13)), 5)
            except OverflowError:
                single = float('inf')  # or some other value that makes sense in your context
            transmittance = single / float(base13)
            table_data.append([str(wl13), format(float(abs13), '.5f'), format(transmittance, '.5f')])

        # Define column widths
        col_widths = [55, 55, 55]

        # Create the table with adjusted column widths
        table = Table(table_data, colWidths=col_widths)

        # Add style to the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, 'black')
        ]))

        # Draw the table on the canvas
        table.wrapOn(c, width, height)
        table.drawOn(c, 30, height - 750)

        c.save()

    #create_pdf("spectrophotometer_report.pdf")