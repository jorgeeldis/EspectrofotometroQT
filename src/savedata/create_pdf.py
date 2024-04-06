import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
import random
import datetime
from libs.wavelengths import wavelength

class PDFReport:

    def __init__(self):
       self.wavelengthFunction = wavelength()
       print(self.wavelengthFunction)

    def create_pdf(self, file_path, Title, User):

        db428 = 47  # replace with the line number you want to read
        db474 = 66
        db535 = 91
        db587 = 114
        db609 = 124
        db660 = 148

        n428 = 47  # replace with the line number you want to read
        n474 = 66
        n535 = 91
        n587 = 114
        n609 = 124
        n660 = 148
        # 50 for 474, 56 for 428, 76 for 535, 97 for 587, 106 for 609, 120 for 600, 143 for 660
        with open("./data/single_muestra.txt", "r") as file:
            lines = file.readlines()
            if n428 <= len(lines):
                db428 = lines[n428 - 1].strip()
            if n474 <= len(lines):
                db474 = lines[n474 - 1].strip()
            if n535 <= len(lines):
                db535 = lines[n535 - 1].strip()
            if n587 <= len(lines):
                db587 = lines[n587 - 1].strip()
            if n609 <= len(lines):
                db609 = lines[n609 - 1].strip()
            if n660 <= len(lines):
                db660 = lines[n660 - 1].strip()
            else:
                print(f"The file has fewer than {n428} lines.")

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
        c.drawString(30, height - 180, "Violet's (428nm) dB: " + str(db428))
        c.drawString(30, height - 200, "Blue's (474nm) dB: " + str(db474))
        c.drawString(30, height - 220, "Green's (535nm) dB: " + str(db535))
        c.drawString(30, height - 240, "Yellow's (587nm) dB: " + str(db587))
        c.drawString(30, height - 260, "Orange's (609nm) dB: " + str(db609))
        c.drawString(30, height - 280, "Red's (660nm) dB: " + str(db660))

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 320, 'Photometric Parameters:')
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 340, 'Luminous Flux: 1000 lm')
        c.drawString(30, height - 360, 'Luminous Density: 518 lm/mm2')
        c.drawString(30, height - 380, 'Color Rendering: 70')
        c.drawString(30, height - 400, 'Thermal resistance: 1.6 C°/W')
        c.drawString(30, height - 420, 'Luminous Efficacy: 206 lm/W')

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, height - 460, 'Electrical Parameters:')
        c.setFont("Helvetica", 12)
        c.drawString(30, height - 480, 'Voltage: 12 V')
        c.drawString(30, height - 500, 'Current: 3 A')
        c.drawString(30, height - 520, 'Power: 36 W')
        c.drawString(30, height - 540, 'Power Factor: 1.0')
        c.drawString(30, height - 560, 'Frequency: 60 Hz')

        c.setFont("Helvetica-Bold", 14)
        c.drawString(300, height - 80, 'Colorimetric Parameters:')
        #Falta
        c.setFont("Helvetica", 12)
        c.drawString(300, height - 100, 'Chromaticity Coordinate (X-axis): 0.30053') #!
        c.drawString(300, height - 120, 'Chromaticity Coordinate (Y-axis): 0.3205') #!
        c.drawString(300, height - 140, 'CCT: 7015K') #!
        c.drawString(300, height - 160, 'Prcp WL: - Ld: ' + str(minNMvalue) + 'nm')
        c.drawString(300, height - 180, 'Purity: 10.5%') #!
        c.drawString(300, height - 200, 'Peak WL: - Lp: ' + str(maxNMvalue) + 'nm')
        c.drawString(300, height - 220, 'FWHM: 12.0nm') #!
        c.drawString(300, height - 240, 'Ratio (Red): 13.9%') #!
        c.drawString(300, height - 260, 'Ratio (Green): 86.1%') #!
        c.drawString(300, height - 280, 'Ratio (Blue): 0.0%') #!
        c.drawString(300, height - 300, 'Render Index (Ra): 0.0') #!
        c.drawString(300, height - 320, 'EEI: 0.00015') #!
        c.drawString(300, height - 340, 'R1: 88') #!
        c.drawString(300, height - 360, 'R2: 0.0') #!
        c.drawString(300, height - 380, 'R3: 0.0') #!
        c.drawString(300, height - 400, 'R4: 0.0') #!
        c.drawString(300, height - 420, 'R5: 0.0') #!
        c.drawString(300, height - 440, 'R6: 0.0') #!
        c.drawString(300, height - 460, 'R7: 0.0') #!
        c.drawString(300, height - 480, 'R8: 0.0') #!
        c.drawString(300, height - 500, 'R9: 0.0')#!
        c.drawString(300, height - 520, 'R10: 0.0')#!
        c.drawString(300, height - 540, 'R11: 0.0')#!
        c.drawString(300, height - 560, 'R12: 0.0')#!
        c.drawString(300, height - 580, 'R13: 0.0')#!
        c.drawString(300, height - 600, 'R14: 0.0')#!
        c.drawString(300, height - 620, 'R15: 0.0')#!


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

        # Add a title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(30, height - 50, 'Measured Data: ')

        # Create a table
        table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]

        # Iterate over the first 35 values of wavelengths, absorbances, and baselines
        for wavelength, absorbance, baseline in zip(wavelengths[:35], absorbances[:35], baselines[:35]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        # Iterate over the first 35 values of wavelengths, absorbances, and baselines
        for wavelength, absorbance, baseline in zip(wavelengths[35:70], absorbances[35:70], baselines[35:70]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        for wavelength, absorbance, baseline in zip(wavelengths[70:105], absorbances[70:105], baselines[70:105]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        for wavelength, absorbance, baseline in zip(wavelengths[105:140], absorbances[105:140], baselines[105:140]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        for wavelength, absorbance, baseline in zip(wavelengths[140:175], absorbances[140:175], baselines[140:175]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        for wavelength, absorbance, baseline in zip(wavelengths[175:198], absorbances[175:198], baselines[175:198]):
            # Calculate transmittance from baseline and absorbance
            single = float(baseline)/ (10 ** float(absorbance))
            transmittance = single / float(baseline)
            table_data.append([str(wavelength), format(float(absorbance), '.5f'), format(transmittance, '.5f')])

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
        table.drawOn(c, 410, height - 515)

        c.save()

    #create_pdf("spectrophotometer_report.pdf")