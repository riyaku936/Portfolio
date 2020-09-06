import matplotlib.pyplot as plt
from fhir_parser import FHIR
import os, csv
from krakenio import Client
import datetime
import matplotlib
matplotlib.use("TKAgg")
import sys

def maritalStatus():
    """ plots the overall trends for marital status 
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()

    marital_status = {}
    for patient in patients:
        if str(patient.marital_status) in marital_status:
            marital_status[str(patient.marital_status)] += 1
        else:
            marital_status[str(patient.marital_status)] = 1


    plt.bar(range(len(marital_status)), list(marital_status.values()), align='center')
    plt.xticks(range(len(marital_status)), list(marital_status.keys()))
    plt.show()

def getPatientPageWithPageNumber(i):
    """Gets all patients on page number i
    Args:
        i: page we wish to view
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    specific_patient = fhir.get_patient('8f789d0b-3145-4cf2-8504-13159edaa747')
    first_page_patients = fhir.get_patient_page(i)
    return first_page_patients

def getPatientNumberOnPage(page, patientNumber):
    """ get the patient object given page and patientNumber
    Args:
        page: page we are looking at
        patientNumber: patient number for the patient we are searching for 
    """
    return page[patientNumber]



def getPatientUUIDFromPatientName(patientName):
    """ get the Patient UUID From the Patient Name
    Args:
        patientName : patient for whom we want the uuid
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    for patient in patients:
        if patientName == patient.name.full_name:
            return patient.uuid #need to fix in case they dont enter full name

def getPatientObservationsTypeWithPatientUUID(patientUUID, typeOfObs):
    """ gets Patient Observations Data for a patient. this function does the communication with FHIR
    Args:
        patientUUID : patient UUID for the patient we are searching for
        typeOfObs : type of observation data we want 
    """
    fhir = FHIR()
    observations = fhir.get_patient_observations(patientUUID)
    resultObservationUUID = []
    resultStatus = []
    resultEffectiveDatetime = []
    resultComponents = []
    for observation in observations:
        if observation.type == typeOfObs:
            resultObservationUUID.append(observation.uuid)
            resultStatus.append(observation.status)
            resultEffectiveDatetime.append(observation.effective_datetime)
            resultComponents.append(observation.components)

    return resultObservationUUID, resultStatus, resultEffectiveDatetime, resultComponents

def getObservationData(patientUUID, typeOfObs, dataYouWishToCollect):
    """ gets Patient Observations Data for a patient. this function first handles the case where the user inputted variable has
    an exact match in our records. if it does return else search for a data with a close match.
    Args:
        patientUUID : patient UUID for the patient we are searching for
        typeOfObs : type of data we want (vital signs | lab results)
        dataYouWishToCollect: data of this type we want e.g. for vital signs the dataYouWishToCollect could be heart rate 
    """
    resultFromExactMatch = getObservationDataUsingExactMatch(patientUUID, typeOfObs, dataYouWishToCollect)
    if(len(resultFromExactMatch) != 0):
        return resultFromExactMatch 
    else:
        return getObservationDataUsingIn(patientUUID, typeOfObs, dataYouWishToCollect)


def getObservationDataUsingExactMatch(patientUUID, typeOfObs, dataYouWishToCollect):
    """ gets Patient Observations Data for a patient. this function returns observation data for current patient where there is an exact match 
    between the user inputted field name and the field name present in the records 
    Args:
        patientUUID : patient UUID for the patient we are searching for
        typeOfObs : type of data we want (vital signs | lab results)
        dataYouWishToCollect: data of this type we want e.g. for vital signs the dataYouWishToCollect could be heart rate 
    """
    resultObservationUUID, resultStatus, resultEffectiveDatetime, resultComponents = getPatientObservationsTypeWithPatientUUID(patientUUID,  typeOfObs)
    result = []
    for i in range(0, len(resultComponents)):
        for element in (resultComponents[i]):
            if dataYouWishToCollect.lower() == element.display.lower():
                result.append( (element.display, str(resultEffectiveDatetime[i]) , element.quantity() ) )
    return result

def getObservationDataUsingIn(patientUUID, typeOfObs, dataYouWishToCollect):
    """ gets Patient Observations Data for a patient. this function returns observation data for current patient where there is a close match 
    between the user inputted field name and the field name present in the records 
    Args:
        patientUUID : patient UUID for the patient we are searching for
        typeOfObs : type of data we want (vital signs | lab results)
        dataYouWishToCollect: data of this type we want e.g. for vital signs the dataYouWishToCollect could be heart rate 
    """
    resultObservationUUID, resultStatus, resultEffectiveDatetime, resultComponents = getPatientObservationsTypeWithPatientUUID(patientUUID,  typeOfObs)
    result = []
    for i in range(0, len(resultComponents)):
        for element in (resultComponents[i]):
            if dataYouWishToCollect.lower() in element.display.lower():
                result.append( (element.display, str(resultEffectiveDatetime[i]) , element.quantity() ) )
    return result


def getBasicPatientInfo(patientRecord):
    """ this gets a string containing all the information about the inputted patient 
    Args:
        patientRecord: the patient for whom we are gathering data 
    """

    result = ""
    result = result + "UUID: " + patientRecord.uuid + '\n'
    result = result + "full name: " + str(patientRecord.name.full_name)+ '\n'
    result = result + "telecoms: \n" + str([record.use + ": " + str(record.number) for record in patientRecord.telecoms])+ '\n'
    result = result + "gender: "  + str(patientRecord.gender)+ '\n'
    result = result + "birthdate: " + str(patientRecord.birth_date)+ '\n'
    result = result + "addresses: \n" + str([record.full_address for record in patientRecord.addresses])+ '\n'
    result = result + "marital status: " + str(patientRecord.marital_status)+ '\n'
    result = result + "mutliple birth: " + str(patientRecord.multiple_birth)+ '\n'
    return result

def getAllBasicPatientInfo(patientRecord):
    """ this returns all the patient information back to the user
    Args:
        patientRecord: the patient for whom we are gathering data 
    """
    return patientRecord.uuid, str(patientRecord.name.full_name), str([record.use + ": " + str(record.number) for record in patientRecord.telecoms]), str(patientRecord.gender), str(patientRecord.birth_date), str([record.full_address for record in patientRecord.addresses]), str(patientRecord.marital_status), str(patientRecord.multiple_birth)  

def checkIfPatientExistsAndReturnUUID(patientName):
    """ this checks if patient with inputted name exists and if it does we return an uuid
    Args:
        patientName: the patient name which we need to find in the system 
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()

    listOfPatients = []
    for patient in patients:
        splittedFullName = str(patient.name.full_name).split(' ')
        patientNameSplitted = patientName.split(' ')
        if len(patientNameSplitted ) == 3 : #so full name has been entered
            if(patientName == patient.name.full_name):
                listOfPatients.append((str(patient.name.full_name), patient.uuid, patient))
        elif len(patientNameSplitted ) == 2 : #so only first and last name has been entered
            if(patientNameSplitted[0] == splittedFullName[0] and patientNameSplitted[1] == splittedFullName[1]):
                listOfPatients.append((str(patient.name.full_name), patient.uuid, patient))
        elif len(patientNameSplitted) == 1 : #so only first or last name has been entered
            if(patientNameSplitted[0] == patientName or patientNameSplitted[1] == patientName):
                listOfPatients.append((str(patient.name.full_name), patient.uuid, patient))

    return listOfPatients


def getMostCommonGender():
    """ gets the Most Common Gender
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    countDict = {}
    maximumCount = -1
    maxValue = ""
    for patient in patients:
        gender = patient.gender
        valSet = -1
        currVal = ""
        if gender not in countDict:
            countDict[gender] = 1
            valSet = 1
            currVal  = gender
        else:
            countDict[gender] = countDict[gender] + 1
            valSet = countDict[gender] + 1
            currVal = gender
        if valSet > maximumCount:
            maximumCount = valSet
            maxValue = currVal
    return maxValue

def getMostCommonMaritalStatus():
    """ gets the Most Common Marital Status
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    countDict = {}
    maximumCount = -1
    maxValue = ""
    for patient in patients:
        marital_status = str(patient.marital_status)
        valSet = -1
        currVal = ""
        if marital_status not in countDict:
            countDict[marital_status ] = 1
            valSet = 1
            currVal  = marital_status
        else:
            countDict[marital_status] = countDict[marital_status] + 1
            valSet = countDict[marital_status] + 1
            currVal = marital_status
        if valSet > maximumCount:
            maximumCount = valSet
            maxValue = currVal
    return maxValue


def getMostCommonRace():
    """ gets the Most Common Race
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    countDict = {}
    maximumCount = -1
    maxValue = ""
    for patient in patients:
        race = str(patient.get_extension('us-core-race'))
        valSet = -1
        currVal = ""
        if race not in countDict:
            countDict[race] = 1
            valSet = 1
            currVal  = race
        else:
            countDict[race] = countDict[race] + 1
            valSet = countDict[race] + 1
            currVal = race
        if valSet > maximumCount:
            maximumCount = valSet
            maxValue = currVal
    return maxValue

def getMostCommonEthnicity():
    """ gets the Most Common Ethnicity
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    countDict = {}
    maximumCount = -1
    maxValue = ""
    for patient in patients:
        Ethnicity = str(patient.get_extension('us-core-ethnicity'))
        valSet = -1
        currVal = ""
        if Ethnicity not in countDict:
            countDict[Ethnicity] = 1
            valSet = 1
            currVal  = Ethnicity
        else:
            countDict[Ethnicity] = countDict[Ethnicity] + 1
            valSet = countDict[Ethnicity] + 1
            currVal = Ethnicity
        if valSet > maximumCount:
            maximumCount = valSet
            maxValue = currVal
    return maxValue


def getMostCommonLanguagesSpoken():
    """ gets the Most Common Languages Spoken
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()
    languages = {}
    for patient in patients:
        for language in patient.communications.languages:
            languages.update({language: languages.get(language, 0) + 1})

    zippedList = []
    for langauge in languages.keys():
        zippedList.append((langauge, languages.get(langauge)))

    strResult = [ str(element[0]) + "|" +  str(element[1])  for element in zippedList]
    matplotlib.pyplot.bar(range(len(languages)), list(languages.values()), align='center')
    matplotlib.pyplot.xticks(range(len(languages)), list(languages.keys()), rotation='vertical')
    matplotlib.pyplot.savefig('temp.png')
    api = Client('1fefa2b086a5e2538e4e0499e76b3d7b', '36a93fa9921dff34665b8eaed2aa4913cfbb4b02')

    data = {
                'wait': True
                    }

    result = api.upload('temp.png', data)

    url = result.get('kraked_url')
    return cardsList.putResultsInTable(strResult, "Most Common Languages Spoken", url)




