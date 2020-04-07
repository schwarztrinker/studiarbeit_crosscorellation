import mysql.connector

class Settings:
    """ Contains setting parameters for the cross correlation """
    def __init__(self, plotNormalizedData=False,
                 plotCorrelations=False, 
                 plotNonNormalizedResults=False,
                 plotNormalizedResults=True, # !!  DEFAULT=True
                 subtractMeanFromResult=True, # !!  DEFAULT=True
                 drawResults=False, # Matlab output / if PDF True not needed 
                 exportFilePath="", 
                 exportToPdf=True, ## GENERAL BOOL ABOUT PDF PRINT
                 decidePdfPrinting=True, ## IF BOOL ABOVE then DOUBLE between 0 and 1 in pyhton call
                 saveCrossCorrIndicators=True, #NEEDS TO BE True for SQL OR EXCEL SUMMARY
                 printExcelSummary=False, # EXCEL  SUMMARY EXPORt 
                 exportToMySql=True, # SQL DATABASE EXPORT // CHANGE DB SETTINGS BEFORE EXPORT
                 crossCorrProcessParallelisation=True # Script Runs PDF Plots and Xcorr Calc parallel
                 ):
        # If you want to adjust the settings and plot a lot of 
        # information, it is recommended to disable the pdf generation
        # and only to draw the results. Then choose the settings you need
        # and enable pdf generation again. 
        # Reason: the space on a single PDF page is limited.
        self.plotNormalizedData = plotNormalizedData
        self.plotCorrelations = plotCorrelations
        self.plotNonNormalizedResults = plotNonNormalizedResults
        self.plotNormalizedResults = plotNormalizedResults
        self.subtractMeanFromResult = subtractMeanFromResult
        self.drawResults = drawResults
        self.exportToPdf = exportToPdf
        self.exportFilePath = exportFilePath
        self.decidePdfPrinting = decidePdfPrinting
        self.printExcelSummary = printExcelSummary
        self.exportToMySql = exportToMySql
        self.saveCrossCorrIndicators = saveCrossCorrIndicators
        self.crossCorrProcessParallelisation = crossCorrProcessParallelisation
