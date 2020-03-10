import crosscorrelation.settings as crossSettings
import crosscorrelation.functions_crosscorrelation as fcc
import analysationrequest.request as catData

from analysationrequest.request import AnalysationRequest

import xlsxwriter


def extractValueFromMetaDataDictionary(metadataDictionary: {}, key):
    return metadataDictionary.get(key, '')

def writeExcelBeginning(worksheet, name):
    worksheet.write("A1", name)


def executeCrossCorrelationForDatasets(datasets: catData.AnalysationRequest, secondsWindow, autoTrashPdfs):
    """ Iterates the datasets and calaculates the cross correlation
        for suitable sequences """   
   
    for dataset in datasets:
        if len(dataset.sequences) >= 2:
            print("\nCrosscorrelation for file", dataset.fileName)

            workbook = xlsxwriter.Workbook( dataset.fileName + "SUMMARY.xlsx")
            worksheet = workbook.add_worksheet()

            writeExcelBeginning(worksheet, "Summary for:" + dataset.fileName)

            machineNameArray= []

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


                    titlePostfixFirstString = 'S:' + startTime + ' ' + titlePostfixFirst
                    titlePostfixSecondString = titlePostfixSecond + ' E:' +endTime



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
                    PeakScore, ymax, timeGap = fcc.crossCorrelation(firstSequence, secondSequence,
                                         correlationSettings, str(titlePostfixFirstString), str(titlePostfixSecondString), secondsWindow, autoTrashPdfs, worksheet)

                    
                    machineNameArray.append([titlePostfixFirst, titlePostfixSecond, PeakScore, ymax, timeGap])
            ### EXCEL SUMMARY! 

            data_format_green = workbook.add_format({'bg_color': '#32CD32'})
            data_format_lightgreen = workbook.add_format({'bg_color': '#98FB98'})
            data_format_grey = workbook.add_format({'bg_color': '#A0A0A0'})
                 
            row= 2
            col = 0
            headline = ["Machine 1", "Machine 2", "Score", "Ymax", "TimeGap"]

            for data in (headline):
                worksheet.write(row, col, data, data_format_grey)
                col +=1
            
            row = 2
            col = 0    

            lastMachineName = ""

            for machineNameone, machineNametwo, score, ymax, timeGap in (machineNameArray):
                if ymax <= 0.1:
                    continue
                if lastMachineName != machineNameone:
                    row +=1
                lastMachineName = machineNameone
                worksheet.write(row, col, machineNameone)
                worksheet.write(row, col + 1, machineNametwo)
                worksheet.write(row, col + 2, score)
                worksheet.write(row, col + 3, ymax)
                worksheet.write(row, col + 4, timeGap)

                if float(score) >= 0.2:
                    worksheet.write(row, col + 2, score, data_format_lightgreen)
                if float(score) >= 0.4:
                    worksheet.write(row, col + 2, score, data_format_green)
                row += 1

            workbook.close()
            
