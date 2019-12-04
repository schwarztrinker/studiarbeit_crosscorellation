import crosscorrelation.settings as crossSettings
import crosscorrelation.functions_crosscorrelation as fcc
import analysationrequest.request as catData

from analysationrequest.request import AnalysationRequest

def extractValueFromMetaDataDictionary(metadataDictionary: {}, key):
    return metadataDictionary.get(key, '')

def executeCrossCorrelationForDatasets(datasets: catData.AnalysationRequest, secondsWindow, autoTrashPdfs):
    """ Iterates the datasets and calaculates the cross correlation
        for suitable sequences """   
   
    for dataset in datasets:
        if len(dataset.sequences) >= 2:
            print("\nCrosscorrelation for file", dataset.fileName)
            for firstIndex, firstSequence in enumerate(dataset.sequences):
                for secondIdx, secondSequence in enumerate(dataset.sequences):
                    if secondIdx <= firstIndex:
                        continue
                    # Only sequences with the same length can be used:
                    if len(firstSequence) != len(secondSequence):
                        print(dataset.fileName,
                              "Cross-Correlation between sequence",
                              str(firstIndex), "and",
                              str(secondIdx),
                              "ignored. Sequence-Length not equal!")
                        continue
                    # Print information and create the export file path:
                    metaDataInfo = dataset.metadataDictionaries[firstIndex]
                    titlePostfixFirst = \
                            extractValueFromMetaDataDictionary(metaDataInfo, 'Machine')
                    metaDataInfo = dataset.metadataDictionaries[secondIdx]
                    titlePostfixSecond = \
                            extractValueFromMetaDataDictionary(metaDataInfo, 'Machine')

                    startTime = extractValueFromMetaDataDictionary(metaDataInfo, 'Start')
                    endTime = extractValueFromMetaDataDictionary(metaDataInfo, 'End')

                    print(dataset.fileName,
                          "exporting Cross-Correlation between sequence",
                          str(titlePostfixFirst), "and", str(titlePostfixSecond))
                    exportPath = dataset.fileName.replace(
                        ".csv",  "_CrossCorrelation_Sequence_" +
                        str(titlePostfixFirst)
                        + "_Sequence_" + str(titlePostfixSecond) + '_' +str(startTime) +".pdf")


                    titlePostfixFirst = 'S:' + startTime + ' ' + titlePostfixFirst
                    titlePostfixSecond = titlePostfixSecond + ' E:' +endTime



                    # If you want to adjust the settings and plot a lot of 
                    # information, it is recommended to disable the pdf generation
                    # and only to draw the results. Then choose the settings you need
                    # and enable pdf generation again. 
                    # Reason: the space on a single PDF page is limited.
                    correlationSettings = crossSettings.Settings()
                    correlationSettings.exportToPdf = True
                    correlationSettings.exportFilePath = exportPath
                    correlationSettings.drawResults = False
                    # Execute the cross correlation:
                    fcc.crossCorrelation(firstSequence, secondSequence,
                                         correlationSettings, str(titlePostfixFirst), str(titlePostfixSecond), secondsWindow, autoTrashPdfs)
