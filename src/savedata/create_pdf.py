from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.tables import TableStyle
import random

def create_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Add a title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, 'Spectrophotometer Report')

    # Add a brief description
    c.setFont("Helvetica", 14)
    c.drawString(30, height - 80, 'This is a sample spectrophotometer report.')

    # Add a table of data
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 120, 'Data Table:')
    c.drawString(30, height - 140, 'Sample Name: Sample 1')
    c.drawString(30, height - 160, 'User: John Doe')
    c.drawString(30, height - 180, 'Manufacturer')
    c.drawString(30, height - 200, 'Model')
    c.drawString(30, height - 220, 'Serial Number')
    c.drawString(30, height - 240, 'Wavelength Range: 300 - 750 nm')
    c.drawString(300, height - 120, 'Date: 2021-01-01')
    c.drawString(300, height - 140, 'Baseline Correction: Yes')
    c.drawString(300, height - 160, 'Date: 2021-01-01')
    c.drawString(300, height - 180, 'Laboratory: Indicasat AIP')
    c.drawString(300, height - 200, 'Location: Panama City, Panama')
    c.drawString(300, height - 220, 'Light Source: Tungsten Lamp')
    c.drawString(300, height - 240, 'Detector: Photodiode')

    # Add a brief description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 280, 'Test condition')

    c.setFont("Helvetica", 12)
    c.drawString(30, height - 300, 'Temperature: 25°C')
    c.drawString(30, height - 320, 'Humidity: 50%')
    c.drawString(30, height - 340, 'WL Range: 300 - 750 nm')
    c.drawString(30, height - 360, 'Scan Speed: 100 nm/sec')
    c.drawString(30, height - 380, 'Test mode: Single')
    c.drawString(30, height - 400, 'Scan Mode: Absorbance')
   
    # Add a graph
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 440, 'Graph:')
    c.drawImage(ImageReader("graph.png"), 30, height - 750, width=500, height=300)

    #New page
    c.showPage()
    # Add a title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, 'Parameters: ')
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 80, 'Statistical Parameters:')
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 100, 'Mean: 0.5')
    c.drawString(30, height - 120, 'Standard Deviation: 0.1')
    c.drawString(30, height - 140, 'Variance: 0.01')
    c.drawString(30, height - 160, 'Skewness: 0.0')
    c.drawString(30, height - 180, 'Kurtosis: 0.0')
    c.drawString(30, height - 200, 'Median: 0.5')
    c.drawString(30, height - 220, 'Mode: 0.5')
    c.drawString(30, height - 240, 'Range: 0.9')
    c.drawString(30, height - 260, 'Minimum: 0.1')
    c.drawString(30, height - 280, 'Maximum: 1.0')

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 320, 'Photometric Parameters:')
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 340, 'Luminous Flux: 1000 lm')
    c.drawString(30, height - 360, 'Luminous Intensity: 100 cd')
    c.drawString(30, height - 380, 'Luminance: 100 cd/m2')
    c.drawString(30, height - 400, 'Illuminance: 100 lux')
    c.drawString(30, height - 420, 'Luminous Efficacy: 10 lm/W')

    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 460, 'Electrical Parameters:')
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 480, 'Voltage: 120 V')
    c.drawString(30, height - 500, 'Current: 1 A')
    c.drawString(30, height - 520, 'Power: 100 W')
    c.drawString(30, height - 540, 'Power Factor: 0.9')
    c.drawString(30, height - 560, 'Frequency: 60 Hz')

    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, height - 80, 'Colorimetric Parameters:')
    c.setFont("Helvetica", 12)
    c.drawString(300, height - 100, 'Chromaticity Coordinate (X-axis): 0.30053')
    c.drawString(300, height - 120, 'Chromaticity Coordinate (Y-axis): 0.3205')
    c.drawString(300, height - 140, 'CCT: 7015K')
    c.drawString(300, height - 160, 'Prcp WL: - Ld: 485.6nm')
    c.drawString(300, height - 180, 'Purity: 10.5%')
    c.drawString(300, height - 200, 'Peak WL: - Lp: 570.0nm')
    c.drawString(300, height - 220, 'FWHM: 570.0nm')
    c.drawString(300, height - 240, 'Ratio (Red): 13.9%')
    c.drawString(300, height - 260, 'Ratio (Green): 86.1%')
    c.drawString(300, height - 280, 'Ratio (Blue): 0.0%')
    c.drawString(300, height - 300, 'Render Index (Ra): 0.0')
    c.drawString(300, height - 320, 'EEI: 0.00015')
    c.drawString(300, height - 340, 'R1: 88')
    c.drawString(300, height - 360, 'R2: 0.0')
    c.drawString(300, height - 380, 'R3: 0.0')
    c.drawString(300, height - 400, 'R4: 0.0')
    c.drawString(300, height - 420, 'R5: 0.0')
    c.drawString(300, height - 440, 'R6: 0.0')
    c.drawString(300, height - 460, 'R7: 0.0')
    c.drawString(300, height - 480, 'R8: 0.0')
    c.drawString(300, height - 500, 'R9: 0.0')
    c.drawString(300, height - 520, 'R10: 0.0')
    c.drawString(300, height - 540, 'R11: 0.0')
    c.drawString(300, height - 560, 'R12: 0.0')
    c.drawString(300, height - 580, 'R13: 0.0')
    c.drawString(300, height - 600, 'R14: 0.0')
    c.drawString(300, height - 620, 'R15: 0.0')


    #"colorimetric parameters"
    #"photometric parameters"
    #"electrical parameters"

    #new page
    c.showPage()
    # Add a title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, height - 50, 'Measured Data: ')
    # Create a table
    # Create random data for the table
    table_data = [['WL (nm)', 'Abs (dB)', 'T (I/Io)']]
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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
    for i in range(35):  # Generating 10 rows of random data
        wavelength = random.randint(300, 750)
        absorbance = round(random.uniform(0.1, 2.0), 2)
        transmittance = round(random.uniform(5, 95), 2)
        table_data.append([str(wavelength), str(absorbance), str(transmittance)])

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

    c.save()

create_pdf("spectrophotometer_report.pdf")