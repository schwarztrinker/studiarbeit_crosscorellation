import crosscorrelation.settings as crossSettings
import crosscorrelation.functions_crosscorrelation as fcc
import analysationrequest.request as catData

from analysationrequest.request import AnalysationRequest
import mysql.connector
import xlsxwriter

import os

import multiprocessing

from datetime import datetime



def extractValueFromMetaDataDictionary(metadataDictionary: {}, key):
    return metadataDictionary.get(key, '')

def writeExcelBeginning(worksheet, name):
    worksheet.write("A1", name)


def executeCrossCorrelationForDatasets(datasets: catData.AnalysationRequest, secondsWindow, autoTrashPdfs, tableName):
    """ Iterates the datasets and calaculates the cross correlation
        for suitable sequences """  
    correlationSettings = crossSettings.Settings()


    machineNameArray = []
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    for dataset in datasets:
        if len(dataset.sequences) >= 2:
            print("\nCrosscorrelation for file", dataset.fileName)

            for i in range(os.cpu_count()): 
                print('registering process %d' % i)
            
            pool = multiprocessing.Pool()
            
            count = 0
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
                    pool.apply_async(execute, args=(dataset, secondsWindow, autoTrashPdfs, tableName, firstIndex, secondIdx, firstSequence, secondSequence, return_dict, count))
                    count +=1
                    
            
            pool.close()
            pool.join()

    if correlationSettings.saveCrossCorrIndicators:
        machineNameArray= return_dict.values()

    ######## DATA EXPORTS IN EXCEL OR SQL DATABASE
    if correlationSettings.printExcelSummary:
        excelExport(dataset.fileName, machineNameArray)

    if correlationSettings.exportToMySql:
        #TRY : DATABASE ERROR
        try:
            sqlExport(tableName, machineNameArray)
            pass
        except mysql.connector.Error as err:
            print("Database Export Error: {}".format(err))



def execute(dataset, secondsWindow, autoTrashPdfs, tableName, firstIndex, secondIdx, firstSequence, secondSequence, return_dict, count): 
    
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
                            correlationSettings, str(titlePostfixFirstString), str(titlePostfixSecondString), secondsWindow, autoTrashPdfs)


    ### Export Date and Times for SQL Export! 
    datetime_objectStart = datetime.strptime(startTime, '%Y-%m-%d-%H-%M-%S')
    datetime_objectEnd = datetime.strptime(endTime, '%Y-%m-%d-%H-%M-%S')
    date = str(datetime_objectStart.date())
    timeStart = str(datetime_objectStart.time())
    timeEnd = str(datetime_objectEnd.time())
    
    if correlationSettings.saveCrossCorrIndicators:
        return_dict[count] = [str(titlePostfixFirst), str(titlePostfixSecond), PeakScore, ymax, timeGap, secondsWindow, date, timeStart, timeEnd]


def sqlExport(tableName, machineNameArray):
    print("---- SQL export ----") 

    #SQL INJECT
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="crosscorr")

    mycursor = mydb.cursor()

    for machineNameone, machineNametwo, score, ymax, timeGap, secondsWindow, date, timeStart, timeEnd in machineNameArray:
        ## CHECK IF TABLE EXIST
        mycursor.execute("CREATE TABLE IF NOT EXISTS "+tableName+"(machine1 varchar(255), machine2 varchar(255), score double, ymax double, timeGap int, timeWindow int, timeDate date, startTime TIME(0), endTime TIME(0))")
        
        ## CHECK IF ROW ALREADY EXISTS   !!!!!!!!!!!(SCORING AND XCORR COULD HAVE CHANGED refresh for SCORE AND YMAX NEEDED)
        mycursor.execute("SELECT EXISTS(Select * from "+tableName+" WHERE machine1='"+machineNameone+"' AND machine2='"+machineNametwo+"' AND score="+ str(score)+" AND ymax="+str(ymax)+" AND timeWindow="+ str(secondsWindow)+" AND timeDate='"+date+"' AND startTime='"+timeStart+"' AND endTime='"+timeEnd+"')")
        rowAlreadyExisting = mycursor.fetchall()
        print(rowAlreadyExisting[0][0])
        
        if str(rowAlreadyExisting[0][0]) == "0":  
            ## INSERT THE ROW 
            mycursor.execute("INSERT INTO "+tableName+"(machine1, machine2, score, ymax, timeGap, timeWindow, timeDate, startTime, endTime) VALUES ('"+machineNameone+"', '"+machineNametwo+"', "+ str(score)+", "+str(ymax)+", "+str(timeGap)+", "+ str(secondsWindow)+", '"+date+"', '"+timeStart+"','"+timeEnd+"')")
            ## REPLACE THE ROW WITH NEW CALCULATED SCORE ETC
        else: print("row already exists")
    
    mydb.commit()

    mydb.close()



def excelExport(fileName, machineNameArray):
    workbook = xlsxwriter.Workbook(fileName + "SUMMARY.xlsx")
    worksheet = workbook.add_worksheet()

    writeExcelBeginning(worksheet, "Summary for:" + fileName)

    ### EXCEL SUMMARY! 

    data_format_green = workbook.add_format({'bg_color': '#32CD32'})
    data_format_lightgreen = workbook.add_format({'bg_color': '#98FB98'})
    data_format_grey = workbook.add_format({'bg_color': '#A0A0A0'})
            
    row= 2
    col = 0
    headline = ["Machine 1", "Machine 2", "Score", "Ymax", "TimeGap", "secondsWindow", "date", "startTime", "endTime"]

    for data in (headline):
        worksheet.write(row, col, data, data_format_grey)
        col +=1
    
    row = 2
    col = 0    

    lastMachineName = ""

    for machineNameone, machineNametwo, score, ymax, timeGap, secondsWindow, date, startTime, endTime in (machineNameArray):
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
        worksheet.write(row, col + 5, secondsWindow)
        worksheet.write(row, col + 6, date)
        worksheet.write(row, col + 7, startTime)
        worksheet.write(row, col + 8, endTime)

        if float(score) >= 0.2:
            worksheet.write(row, col + 2, score, data_format_lightgreen)
        if float(score) >= 0.4:
            worksheet.write(row, col + 2, score, data_format_green)
        row += 1

    workbook.close()