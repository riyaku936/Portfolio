# import flask dependencies
from flask import Flask, request, make_response, jsonify, render_template
from pydialogflow_fulfillment import DialogflowResponse
import os
import FHIRFunctions, CurrentPatientDetails, cardsList
import datetime
import matplotlib
from krakenio import Client
import re
from fhir_parser import FHIR


# initialize the flask app
app = Flask(__name__)

nameWeAreCurrentlyDealingWith = ""
uuidWeAreDealingWith = ""
patientWeAreDealingWith = None

def getMostCommonLanguagesSpoken():
    """ analyses all patient records to find most common language spoken
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
    if os.path.isfile('temp2.png'):
        os.remove('temp2.png')
    matplotlib.pyplot.savefig('temp2.png')
    api = Client('1fefa2b086a5e2538e4e0499e76b3d7b', '36a93fa9921dff34665b8eaed2aa4913cfbb4b02')

    data = {
                'wait': True
                    }
    result = api.upload('temp2.png', data)
    url = result.get('kraked_url')
    return cardsList.putResultsInTableForDoDataAnalysis(strResult, "Most Common Languages Spoken", url)


def maritalStatusDistribution():
    """ analyses all patient records to find marital status distribution
    """
    fhir = FHIR()
    patients = fhir.get_all_patients()

    marital_status = {}
    for patient in patients:
        if str(patient.marital_status) in marital_status:
            marital_status[str(patient.marital_status)] += 1
        else:
            marital_status[str(patient.marital_status)] = 1

    zippedList = []
    for status in marital_status.keys():
        zippedList.append((status, marital_status.get(status)))

    strResult = [ str(element[0]) + "|" +  str(element[1])  for element in zippedList]

    matplotlib.pyplot.bar(range(len(marital_status)), list(marital_status.values()), align='center')
    matplotlib.pyplot.xticks(range(len(marital_status)), list(marital_status.keys()))
    if os.path.isfile('temp1.png'):
        os.remove('temp1.png')
    matplotlib.pyplot.savefig('temp1.png')
    api = Client('1fefa2b086a5e2538e4e0499e76b3d7b', '36a93fa9921dff34665b8eaed2aa4913cfbb4b02')

    data = {
                'wait': True
                    }

    result = api.upload('temp1.png', data)

    url = result.get('kraked_url')
    return cardsList.putResultsInTableForDoDataAnalysis(strResult, "Marital Status Spread", url)

def processWhenNameHasBeenEntered(queryText):
        """ returns the right response once a patient name is inputted by the user
        """
        listOfPatientDetails = FHIRFunctions.checkIfPatientExistsAndReturnUUID(queryText)
        if(len(listOfPatientDetails) > 1):
            namesToPost = ""
            counter = 0
            for name in listOfPatientDetails:
                namesToPost = counter + ". " + name[0] + namesToPost
                counter = counter+1
            return {'fulfillmentText': 'Please select a name by entering a number ' + namesToPost}
        elif len(listOfPatientDetails) == 1:
            CurrentPatientDetails.nameWeAreCurrentlyDealingWith, CurrentPatientDetails.uuidWeAreDealingWith, CurrentPatientDetails.patientWeAreDealingWith = listOfPatientDetails[0]
            cardsList.nameStorage.name = listOfPatientDetails[0][0]
            return cardsList.cardForPatientDataRetrieval
        else:
            return {'fulfillmentText': 'A patient with this name does not exist in our records'}


def processTheTypesOfDataSelected(QueryFromDialogFlow):
        """ returns the right response once the user has selected the type of data (pateint data | vital signs | lab results) they want for the current patient 
        """
     # need to put option in case they type in text back and dont write number
        numberSelected = QueryFromDialogFlow.get('parameters').get('number')[0]
        if(numberSelected == 1.0): # return back basic info about patient 
            #resultToSendBack = FHIRFunctions.getBasicPatientInfo(CurrentPatientDetails.patientWeAreDealingWith)
            return cardsList.getPatientDetailsCard(CurrentPatientDetails.patientWeAreDealingWith)#{'fulfillmentText': 'Patient Details for ' + CurrentPatientDetails.patientWeAreDealingWith.name.full_name + '\n' + resultToSendBack}
        elif (numberSelected == 2.0):
            CurrentPatientDetails.lastSelected = "vital-signs"
            return {'fulfillmentText': 'Enter the Vital Sign you need for ' + CurrentPatientDetails.patientWeAreDealingWith.name.full_name}
        elif (numberSelected == 3.0):
            CurrentPatientDetails.lastSelected = "survey"
            return {'fulfillmentText': 'Enter the Lab result you need for ' + CurrentPatientDetails.patientWeAreDealingWith.name.full_name}
        elif (numberSelected == 4.0):
            CurrentPatientDetails.lastSelected = "laboratory"
            return {'fulfillmentText': 'Enter the Parameter you need for ' + CurrentPatientDetails.patientWeAreDealingWith.name.full_name}

def processUnknowIntent(QueryFromDialogFlow):
       """ returns the right response once the user has selected the specific data they want e.g. for vital sign they selected heart rate then it comes here
       """
       listResult = FHIRFunctions.getObservationData(CurrentPatientDetails.uuidWeAreDealingWith, CurrentPatientDetails.lastSelected, QueryFromDialogFlow.get('queryText'))
       if(len(listResult) == 0):
           return {'fulfillmentText': 'Sorry could you enter that again?'}
       else:
           yLabel = listResult[0][0]
           xLabel = "Date Recorded"
           xAndYData = [ (element[1], element[2]) for element in listResult]
           xAndYData.sort(key=lambda x: x[0])
           strResult = [ str(element[0]) + "|" +  str(element[1])  for element in xAndYData]
           try:
            xData = [datetime.datetime.strptime(element[0][:-15], '%Y-%m-%d') for element in xAndYData]
            yData = [float(re.sub('[^0-9]','', element[1])) for element in xAndYData]
            
            matplotlib.pyplot.plot(xData, yData, 'r--')
            matplotlib.pyplot.ylabel(yLabel)
            matplotlib.pyplot.xlabel(xLabel)
            for xy in zip(xData,yData):                                       # <--
                    matplotlib.pyplot.annotate('(%s)' % xy[1], xy=xy, textcoords='data')
            if os.path.isfile('temp3.png'):
                    os.remove('temp3.png')
            matplotlib.pyplot.savefig('temp3.png')
            api = Client('1fefa2b086a5e2538e4e0499e76b3d7b', '36a93fa9921dff34665b8eaed2aa4913cfbb4b02')

            data = {
                'wait': True
                    }
            result = api.upload('temp3.png', data)
            url = result.get('kraked_url')
            return cardsList.putResultsInTable(strResult, listResult[0][0], url, CurrentPatientDetails.patientWeAreDealingWith.name) #{'fulfillmentText': strResult + '\nPlease select choose to select the type of data you want : 1) Basic Patient Info 2) Vital signs 3) Lab results 4) Other'}
           except:
               return cardsList.putResultsInTableNoButton(strResult, listResult[0][0],  CurrentPatientDetails.patientWeAreDealingWith.name) #{'fulfillmentText': strResult + '\nPlease select choose to select the type of data you want : 1) Basic Patient Info 2) Vital signs 3) Lab results 4) Other'}



# default route
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('test.html')

# function for responses
def results():
    """ This function recieves the responses from the user 
    """
    req = request.get_json(force=True)

    QueryFromDialogFlow = req.get('queryResult')
    
    queryText = QueryFromDialogFlow.get('queryText')
    intent = QueryFromDialogFlow.get('action')

    if intent == "input.welcome" or intent == "getMenu":
      return cardsList.welcomeCard
    if ("\'query\': \'Get Patient Details\'" in str(req)):
      return {'fulfillmentText': 'Please enter the Patient Name'}
    if "\'query\': \'Do Data Analysis\'" in str(req)  or "\'query\': \'Explore More Data\'" in str(req):
        return cardsList.dataAnalysisCard
    if("\'query\': \'Most Common Gender\'" in str(req)):
        return {'fulfillmentText': 'This is the Most Common Gender: ' + str(FHIRFunctions.getMostCommonGender())}
    if("\'query\': \'Most Common MaritalStatus\'" in str(req)):
        return {'fulfillmentText': 'This is the Most Common Marital Status: ' + str(FHIRFunctions.getMostCommonMaritalStatus())}
    if("\'query\': \'Most Common Race\'" in str(req)):
        return {'fulfillmentText': 'This is the Most Common Race: ' + str(FHIRFunctions.getMostCommonRace())}
    if("\'query\': \'Most Common Ethnicity\'" in str(req)):
        return {'fulfillmentText': 'This is the Most Common Ethnicity: ' + str(FHIRFunctions.getMostCommonEthnicity())}
    if intent == "startNewPatient":
        return {'fulfillmentText': 'Please enter the Patient Name'}
    if intent == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom":
        return processWhenNameHasBeenEntered(queryText)
    if intent == "DefaultWelcomeIntent.DefaultWelcomeIntent-custom.DefaultWelcomeIntent-custom-selectnumber":
       return processTheTypesOfDataSelected(QueryFromDialogFlow)
    if intent == "getBasicPatientInfo":
        return cardsList.getPatientDetailsCard(CurrentPatientDetails.patientWeAreDealingWith)#{'fulfillmentText': 'Patient Details for ' + CurrentPatientDetails.patientWeAreDealingWith.name.full_name + '\n' + resultToSendBack}
    if intent == "getVitalSign":
        CurrentPatientDetails.lastSelected = "vital-signs"
        return cardsList.cardForVitalSigns
    if intent == "getLabResults":
        CurrentPatientDetails.lastSelected = "laboratory"
        return cardsList.cardForLabResults
    if  intent == "MostCommonLang.Spoken":
        return getMostCommonLanguagesSpoken()
    if intent == "MaritalStatusSpread":
        return maritalStatusDistribution()
    if intent == "moreDataOnThisPatient":
        return cardsList.cardForPatientDataRetrieval
    if QueryFromDialogFlow.get('action') == "input.unknown":
        return processUnknowIntent(QueryFromDialogFlow)
       




# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(results())

# run the app
if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'), 
            port=int(os.getenv('PORT', 8000)))