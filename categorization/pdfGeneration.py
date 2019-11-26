from matplotlib.gridspec import GridSpec
from matplotlib.font_manager import FontProperties
import analysationrequest.request as catData
import matplotlib.pyplot as plt

MARKERSIZE = 3
FREQUENCY_PLOT_COLOR = '#23a877'
BALANCE_PLOT_COLOR = '#4286f4'
# Set the following parameter to True if you want to plot
# big sequences. PDF files of big sequences will take their time to load.
# If you use rasterization, the resolution of the plot will be lower.
RASTERIZE_PLOTS = True


def generatePdfsForDataset(data: catData.AnalysationRequest, drawResults=False):
    """ Generate the pdfs for a dataset. """
    for sequenceIndex, sequence in enumerate(data.sequences):
        print("Generating pdf reports for",
              data.fileName, "Sequence", sequenceIndex)
        plt.close("all")

        generateSummaryPdf(sequenceIndex, sequence, data, drawResults)
        generateSubSequenceFrequencyInfoPdf(sequenceIndex, data, drawResults)
        generateSubSequenceBalanceInfoPdf(sequenceIndex, data, drawResults)
        if drawResults:
            plt.show()


def resolveFrequencyValueToDescriptiveString(value):
    """ Resolve a frequency value to a more descriptive string. """
    if value <= 0.25:
        return "Niederfrequent"
    if value > 0.25 and value < 0.75:
        return "Mittelfrequent"
    if value >= 0.75:
        return "Hochfrequent"
    return "Unbekannt"


def resolveBalanceValueToDescriptiveString(value):
    """ Resolve a balance value to a more descriptive string. """
    if value >= 0.4 and value <= 0.6:
        return "Ausgeglichen"
    if value < 0.4 or value > 0.6:
        return "Unausgeglichen"
    return "Unbekannt"


def generateSubSequenceBalanceInfoPdf(sequenceIndex,
                                      data: catData.AnalysationRequest,
                                      drawResults: bool):
    """ Generate a pdf containing the balances for the sub sequences. """

    subSequenceBalances = data.subSequenceBalances[sequenceIndex]

    numberOfNeededRows = len(subSequenceBalances)
    if numberOfNeededRows == 0:
        return

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(numberOfNeededRows, 1, figure=figure)

    currentRowIndex = 0
    for key, values in subSequenceBalances.items():
        ax = figure.add_subplot(gs[currentRowIndex])
        currentRowIndex += 1
        ax.plot(values,
                '.-',
                color=BALANCE_PLOT_COLOR,
                rasterized=RASTERIZE_PLOTS,
                linewidth=0.25)
        ax.set_title(str(key) + "er Sub-Sequenzen")
        ax.set_xlabel('Sub-Sequenz')
        ax.set_ylabel('Balance')
        ax.set_ylim(-0.05, 1.1)

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv", "_SubSequences_Balances_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    
    if drawResults:
        figure.canvas.set_window_title(exportPath) 
        plt.draw()
    else:
        plt.close(figure)


def generateSubSequenceFrequencyInfoPdf(sequenceIndex,
                                        data: catData.AnalysationRequest,
                                        drawResults: bool):
    """ Generate a pdf containing the frequencies for the sub sequences. """

    subSequenceFrequencies = data.subSequenceFrequencyResults[sequenceIndex]
    
    numberOfNeededRows = len(subSequenceFrequencies)
    if numberOfNeededRows == 0:
        return

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(numberOfNeededRows, 1, figure=figure)

    currentRowIndex = 0
    for key, values in subSequenceFrequencies.items():
        ax = figure.add_subplot(gs[currentRowIndex])
        currentRowIndex += 1
        ax.plot(values,
                '.-',
                color=FREQUENCY_PLOT_COLOR,
                rasterized=RASTERIZE_PLOTS,
                linewidth=0.25)
        ax.set_title(str(key) + "er Sub-Sequenzen")
        ax.set_xlabel('Sub-Sequenz')
        ax.set_ylabel('Frequenz')
        ax.set_ylim(-0.05, 1.1)

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv", "_SubSequences_Frequency_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')

    if drawResults:
        figure.canvas.set_window_title(exportPath) 
        plt.draw()
    else:
        plt.close(figure)


def extractValueFromMetaDataDictionary(metadataDictionary: {}, key):
    return metadataDictionary.get(key, '')


def generateSummaryPdf(sequenceIndex, sequence,
                       data: catData.AnalysationRequest,
                       drawResults: bool):
    """ Generate a summary pdf for a sequnce in a given data file. """

    figure = plt.figure(constrained_layout=True)
    gs = GridSpec(3, 1, figure=figure)
    # plot sequence
    axes = figure.add_subplot(gs[0])
    axes.plot(sequence,
              'r.',
              markersize=MARKERSIZE,
              rasterized=RASTERIZE_PLOTS)
    # Extract meta data:
    metaDataInfo = data.metadataDictionaries[sequenceIndex]
    titlePostfix = \
        extractValueFromMetaDataDictionary(metaDataInfo, 'Machine')

    startTime = extractValueFromMetaDataDictionary(metaDataInfo, 'Start')
    endTime = extractValueFromMetaDataDictionary(metaDataInfo, 'End')

    if(startTime != ''):
        titlePostfix = titlePostfix + ' Start: ' + startTime

    if(endTime != ''):
        titlePostfix = titlePostfix + ' End: ' + endTime

    intervalPostfix = \
        extractValueFromMetaDataDictionary(metaDataInfo, 'Interval')

    if(intervalPostfix != ''):
        intervalPostfix = '(Interval ' + intervalPostfix + ')'

    axes.set_title("Sequenz " + titlePostfix)
    axes.set_xlabel('Index ' + intervalPostfix)
    axes.set_ylabel('Wert')
    axes.set_ylim(-0.05, 1.1)

    # The middle row is empty and used as a separator between the subfigures.

    # plot summary
    axes = figure.add_subplot(gs[2])
    axes.axis('off')
    axes.axis('tight')
    axes.set_title("Sequenzeigenschaften")
    columns = ('Eigenschaft', 'Wert')
    tableData = []
    # Write Length into the table
    tableData.append(["Länge", len(sequence)])
    frequencyString = str(data.frequencyResults[sequenceIndex]) + ' - ' + \
        resolveFrequencyValueToDescriptiveString(
            data.frequencyResults[sequenceIndex])

    # Write Frequency into the table
    tableData.append(["Frequenz", frequencyString])
    balanceString = str(data.balances[sequenceIndex]) + " - " + \
        resolveBalanceValueToDescriptiveString(data.balances[sequenceIndex])

    # Write Balance into the table
    tableData.append(["Balance", balanceString])
    table = axes.table(cellText=tableData, colLabels=columns,
                       loc='center', cellLoc="left", colLoc="left")

    # Set first row (header) text to bold
    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    # Export the pdf
    exportPath = data.fileName.replace(
        ".csv",  "_Sequence_" + str(sequenceIndex) + ".pdf")
    figure.savefig(exportPath, bbox_inches='tight')
    if drawResults:
        figure.canvas.set_window_title(exportPath) 
        plt.draw()
    else:
        plt.close(figure)
