from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QTextEdit, QFileDialog, QScrollBar, QComboBox, QColorDialog, QCheckBox, QSlider
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import QtWidgets, uic
from fpdf import FPDF
import pyqtgraph.exporters
import pyqtgraph as pg
import pandas as pd
import statistics
import os
import numpy as np
import main

def Exporter(self):

    #if there is signal ?
    if not self.curves_1 and not self.curves_2:
        # This message appears if there is no signal to EXPORT
        QtWidgets.QMessageBox.warning(self, 'Warning', 'You have to plot a signal first')
    else:
        FolderPath = QFileDialog.getSaveFileName(None, str('Save the signal file'), None, str("PDF FIles(*.pdf)"))
        if FolderPath != '':
            pdf = FPDF()

            # for graph1 check first if there is atleast one signal running
            if self.curves_1:
                pdf.add_page()
                # Effective page width
                epw = pdf.w - 2*pdf.l_margin
                # distribute the table on 6 columns
                column_width = epw/6

                pdf.set_font('Arial', 'B', 20)
                pdf.cell(70)
                pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')
                pdf.ln(20)

                #        w    h             border  postion allignment 
                pdf.cell(50, 10, 'Graph 1', 0, 0, 'C')
                pdf.ln(20)

                ex3 = pg.exporters.ImageExporter(self.ui.graph1.plotItem)
                ex3.export('img/graph1.png')
                #                        x   y   w    h
                pdf.image('img/graph1.png', 20, 50, 150, 100)
                pdf.ln(120)

                pdf.cell(50, 10, 'Statistics data',0,0, 'C')
                pdf.set_font('Arial', 'B', 10)
                pdf.ln(20)

                # Text height is the same as current font size
                text_height = pdf.font_size

                # declare an array of the arrays.  Also we declared the size
                data = [['', 'Max', 'Min', 'Mean', 'Std_Dev', 'Duration'], [], [], []]
                # add rows while there are signals

                # This loop to draw the rest of the rows and to get the varibles to fill the table
                for channel_name, channel_values in self.channel_data.items():
                    if channel_values['graph_number'] == 1:
                        print(channel_name)
                        current_data = []
                        current_data.append(channel_name)
                        current_data.append(round(np.amax(channel_values['amplitude']), 4))
                        current_data.append(round(np.amin(channel_values['amplitude']), 4))
                        current_data.append(round(np.mean(channel_values['amplitude']), 4))
                        current_data.append(round(np.std(channel_values['amplitude']), 4))
                        current_data.append(round(np.amax(channel_values['time']), 4))
                        data.append(current_data)
                        print("current_data ",current_data)

                # This 2 loops draw the Table
                for row in data:
                    for datum in row:
                        if datum == row[0]:
                            pdf.set_fill_color(200, 200, 200)
                            pdf.cell(column_width, 3*text_height,str(datum), border=1, fill=True)

                        elif row == data[0]:
                            pdf.set_fill_color(200, 200, 200)
                            pdf.cell(column_width, 3*text_height,str(datum), border=1, fill=True)
                        else:
                            pdf.cell(column_width, 3*text_height,str(datum), border=1)
                    pdf.ln(2.7)

            # for graph2 check first if there is atleast one signal running
            if self.curves_2:
                pdf.add_page()
                # Effective page width
                epw = pdf.w - 2*pdf.l_margin
                # distribute the table on 6 columns
                column_width = epw/6

                pdf.set_font('Arial', 'B', 20)
                img2_y = 30
                if not self.curves_1:
                    pdf.cell(70)
                    pdf.cell(50, 10, 'Signal Viewer Report', 0, 0, 'C')
                    pdf.ln(20)
                    img2_y = 50

                #        w    h             border  postion allignment 
                pdf.cell(50, 10, 'Graph 2', 0, 0, 'C')
                pdf.ln(20)

                ex3 = pg.exporters.ImageExporter(self.ui.graph2.plotItem)
                ex3.export('img/graph2.png')
                #                            x   y   w    h
                pdf.image('img/graph2.png', 20, img2_y, 150, 100)
                pdf.ln(120)

                pdf.cell(50, 10, 'Statistics data',0,0, 'C')
                pdf.set_font('Arial', 'B', 10)
                pdf.ln(20)

                # Text height is the same as current font size
                text_height = pdf.font_size

                # declare an array of the arrays.  Also we declared the size
                data = [['', 'Max', 'Min', 'Mean', 'Std_Dev', 'Duration'], [], [], []]
                # add rows while there are signals

                # This loop to draw the rest of the rows and to get the varibles to fill the table
                for channel_name, channel_values in self.channel_data.items():
                    if channel_values['graph_number'] == 2:
                        print(channel_name)
                        current_data = []
                        current_data.append(channel_name)
                        current_data.append(round(np.amax(channel_values['amplitude']), 4))
                        current_data.append(round(np.amin(channel_values['amplitude']), 4))
                        current_data.append(round(np.mean(channel_values['amplitude']), 4))
                        current_data.append(round(np.std(channel_values['amplitude']), 4))
                        current_data.append(round(np.amax(channel_values['time']), 4))
                        data.append(current_data)
                        print("current_data ",current_data)

                # This 2 loops draw the Table
                for row in data:
                    for datum in row:
                        if datum == row[0]:
                            pdf.set_fill_color(200, 200, 200)
                            pdf.cell(column_width, 3*text_height,str(datum), border=1, fill=True)

                        elif row == data[0]:
                            pdf.set_fill_color(200, 200, 200)
                            pdf.cell(column_width, 3*text_height,str(datum), border=1, fill=True)
                        else:
                            pdf.cell(column_width, 3*text_height,str(datum), border=1)
                    pdf.ln(2.7)

            # Exporting the Pdf
            pdf.output(str(FolderPath[0]))

            # This message appears when the pdf is EXPORTED
            QtWidgets.QMessageBox.information(self, 'Done', 'PDF has been created successfully!')