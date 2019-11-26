class Settings:
    """ Contains setting parameters for the cross correlation """
    def __init__(self, plotNormalizedData=False,
                 plotCorrelations=False, plotNonNormalizedResults=False,
                 plotNormalizedResults=True, subtractMeanFromResult=True,
                 drawResults=False, exportToPdf=False,
                 exportFilePath=""):
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
