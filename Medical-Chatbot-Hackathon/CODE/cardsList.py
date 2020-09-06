import FHIRFunctions
from CurrentPatientDetails import CurrentPatientDetails





class nameStorage:
  """ This class stores the name of the patient
  """
  name = ""


"""
This class consists of the cards we diplays to the user during the conversion.
  These are the cards we have:
    welcomeCard --> the welcome card displays the welcome page when the user open the chatbot. They can choose b/w getting patient info | do data analysis | learning how the bot works
    dataAnalysisCard --> displays the available data analysis options the user can use
    cardForPatientDataRetrieval --> this card is displayed so the user can choose whether hs/she wants Vital signs, Lab results or Basic Patient Info
    cardForVitalSigns --> this card is displayed so the user can choose a vital sign to display
    cardForLabResults --> this card is displayed so the user can choose a lab result to display
"""

dataAnalysisCard = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Please select the type of data you want:"
            }
          },
        ],
        "suggestions": [
          
          {
            "title": "Marital Status Distrib."
          },
          {
            "title": "Most Common Lang. Spoken"
          },
          {
            "title": "Most Common Gender"
          },
          {
            "title": "Most Common MaritalStatus"
          },
          {
            "title": "Most Common Race"
          },
          {
            "title": "Most Common Ethnicity"
          }
        ],
        "linkOutSuggestion": {
          "destinationName": "Suggestion Link",
          "url": "https://assistant.google.com/"
        }
      }
    }
  }
}

welcomeCard = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "systemIntent": {
        "intent": "actions.intent.OPTION",
        "data": {
          "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
          "carouselSelect": {
            "items": [
              {
                "optionInfo": {
                  "key": "SELECTION_KEY_ONE",
                  "synonyms": [
                    "synonym 1",
                    "synonym 2",
                    "synonym 3"
                  ]
                },
                "description": "",
                "image": {
                  "url": "https://internationalsecurityjournal.com/wp-content/uploads/2019/12/shutterstock_388775896.jpg",
                  "accessibilityText": "Get Patient Details"
                },
                "title": "Get Patient Details"
              },
              {
                "optionInfo": {
                  "key": "SELECTION_KEY_GOOGLE_HOME",
                  "synonyms": [
                    "Google Home Assistant",
                    "Assistant on the Google Home"
                  ]
                },
                "description": "",
                "image": {
                  "url": "https://www.sas.com/en_us/insights/analytics/big-data-analytics/_jcr_content/par/styledcontainer_9ecb/image.img.jpg/1560273307760.jpg",
                  "accessibilityText": "Do Data Analysis"
                },
                "title": "Do Data Analysis"
              },
              {
                "optionInfo": {
                  "key": "SELECTION_KEY_GOOGLE_PIXEL",
                  "synonyms": [
                    "Google Pixel XL",
                    "Pixel",
                    "Pixel XL"
                  ]
                },
                "description": "",
                "image": {
                  "url": "https://cdn.hipwallpaper.com/i/77/18/J1CdRN.jpg",
                  "accessibilityText": "How does this bot work?"
                },
                "title": "How does this bot work?"
              }
            ]
          }
        }
      },
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Welcome to PatientData Bot! \n\nPlease select an option from below. \n\nIf you are new to the Bot select \"How does this bot work?\""
            }
          }
        ]
      }
    }
  }
}


cardForPatientDataRetrieval = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Please select the type of data you want:"
            }
          },
        ],
        "suggestions": [
          {
            "title": "Basic Patient Info"
          },
          {
            "title": "Vital signs"
          },
          {
            "title": "Lab results"
          }
        ],
        "linkOutSuggestion": {
          "destinationName": "Suggestion Link",
          "url": "https://assistant.google.com/"
        }
      }
    }
  }
}

cardForVitalSigns= {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Enter the Vital Sign you need:"
            }
          },
        ],
        "suggestions": [
          {
            "title": "Height"
          },
          {
            "title": "Weight"
          },
          {
            "title": "Heart Rate"
          },
          {
            "title": "Body Mass Index"
          },
          {
            "title": "Blood Pressure"
          },
          {
            "title": "Pain severity"
          }
        ],
        "linkOutSuggestion": {
          "destinationName": "Suggestion Link",
          "url": "https://assistant.google.com/"
        }
      }
    }
  }
}

cardForLabResults= {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Enter the Lab Result you need:"
            }
          },
        ],
        "suggestions": [
          {
            "title": "Hemoglobin"
          },
          
          
          {
            "title": "Total Cholesterol"
          },
          {
            "title": "Erythrocytes [#/volume]"
          },
          {
            "title": "Low Density Lipoprotein"
          },
          {
            "title": "Triglycerides"
          },
          {
            "title": "Hematocrit [Volume Fraction]"
          }
          ,
          {
            "title": "Leukocytes [#/volume]"
          }
          ,
          {
            "title": "Platelet mean volume"
          },
          {
            "title": "High Density Lipoprotein"
          },
          {
            "title": "MCV [Entitic volume]"
          }
          ,
          {
            "title": "MCHC [Mass/volume]"
          },
          {
            "title": "Platelets [#/volume]"
          }
        ],
        "linkOutSuggestion": {
          "destinationName": "Suggestion Link",
          "url": "https://assistant.google.com/"
        }
      }
    }
  }
}


def convertDataToRows(listOfResults, field):
    """ converts the data we are getting into a list of objects that can be displayed as a table.
    Args:
      listOfResults : results we need to plot on table
      field : field we are displaying values for in the table 
    """

    allCells = []
    
    for element in listOfResults:
        elementSeparated = element.split("|")
        newList = {
                  "cells": [
                    {
                      "text": elementSeparated[0]
                    },
                    {
                      "text": elementSeparated[1]
                    }
                  ],
                  "dividerAfter": False
                }
        allCells.append(newList)

    return allCells
    

def putResultsInTableForDoDataAnalysis(listOfResults, field, url):
  """ This function puts the data results from data analysis onto a card with a table. This card also displays the graphical form of the image.
  Args:
    listOfResults: data analysis results to display on a table 
    field: the data analysis quantity we are returning 
    url: the graph that contains the graphical representation of all the results
  """

  resultsTable = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "This is the requested Patient Details" 
            }
          },
          {
            "tableCard": {
              "title": field + " Results",
              "subtitle": "",
              "image": {
                "url": "https://static.vecteezy.com/system/resources/thumbnails/000/260/287/original/financegraph.jpg",
                "accessibilityText": "Image alternate text"
              },
              
              "rows": convertDataToRows(listOfResults, field)
              ,
              "columnProperties": [
                {
                  "header": "Date",
                  "horizontalAlignment": "CENTER"
                },
                {
                  "header": field,
                  "horizontalAlignment": "CENTER"
                }
              ],
              "buttons": [
                {
                  "title": "View Graph of Data",
                  "openUrlAction": {
                    "url": url
                  }
                }
              ]
              
            }
          },

          
          
          {
            "simpleResponse": {
              "textToSpeech": "What would you like to do next?"
            }
          }
        ], 
        "suggestions": [
                          {
                            "title": "Explore More Data"
                          },
                          
                          {
                            "title": "Return to Menu"
                          }
                        ]

        
      }
    }
  }
}
  return resultsTable



def putResultsInTable(listOfResults, field, url, name):
    """ This function puts the patient data into a card with a table. This card also displays the graphical representation of the data.
    Args:
      listOfResults : results to put into table
      field : field we are displaying 
      name : name of the patient whose information we are displaying 
      url: to the image portraying the graphical representation of results
    """

    resultsTable = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "This is the requested Patient Details" 
            }
          },
          {
            "tableCard": {
              "title": field + " Results",
              "subtitle": "Patient Name: " + str(name) ,
              "image": {
                "url": "https://icons.iconarchive.com/icons/dapino/people/512/brown-man-icon.png",
                "accessibilityText": "Image alternate text"
              },
              
              "rows": convertDataToRows(listOfResults, field)
              ,
              "columnProperties": [
                {
                  "header": "Date",
                  "horizontalAlignment": "CENTER"
                },
                {
                  "header": field,
                  "horizontalAlignment": "CENTER"
                }
              ],
              "buttons": [
                {
                  "title": "View Graph of Data",
                  "openUrlAction": {
                    "url": url
                  }
                }
              ]
              
            }
          },

          
          
          {
            "simpleResponse": {
              "textToSpeech": "What would you like to do next?"
            }
          }
        ], 
        "suggestions": [
                          {
                            "title": "More Data on this Patient"
                          },
                          {
                            "title": "Get Data for New Patient"
                          },
                          {
                            "title": "Return to Menu"
                          }
                        ]

        
      }
    }
  }
}
    return resultsTable


def putResultsInTableNoButton(listOfResults, field,  name):
    """ This function puts the patient data into a card with a table. This card does not display the graphical representation of the data.
    Args:
      listOfResults : results to put into table
      field : field we are displaying 
      name : name of the patient whose information we are displaying 
    """

    resultsTable = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "This is the requested Patient Details" 
            }
          },
          {
            "tableCard": {
              "title": field + " Results",
              "subtitle": "Patient Name: " + str(name) ,
              "image": {
                "url": "https://icons.iconarchive.com/icons/dapino/people/512/brown-man-icon.png",
                "accessibilityText": "Image alternate text"
              },
              
              "rows": convertDataToRows(listOfResults, field)
              ,
              "columnProperties": [
                {
                  "header": "Date",
                  "horizontalAlignment": "CENTER"
                },
                {
                  "header": field,
                  "horizontalAlignment": "CENTER"
                }
              ]
              
            }
          },

          
          
          {
            "simpleResponse": {
              "textToSpeech": "What would you like to do next?"
            }
          }
        ], 
        "suggestions": [
                          {
                            "title": "More Data on this Patient"
                          },
                          {
                            "title": "Get Data for New Patient"
                          },
                          {
                            "title": "Return to Menu"
                          }
                        ]

        
      }
    }
  }
}
    return resultsTable



def getPatientDetailsCard(patientObj):
    """ This function returns the card which displays all the basic patient info with all the patient details filled in
    Args:
      patientObj : the patientObj contains all the relevant patient info we need to fill in
    """
    uuid, name, number, gender, birthdate, address, marital_status, multiple_births = FHIRFunctions.getAllBasicPatientInfo(patientObj)
    patientDetailsCard = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "This is the Patient info for " + name
            }
          },
          {
            "tableCard": {
              "title": "Patient Details",
              "subtitle": "Patient: " + name,
              "image": {
                "url": "https://www.pngitem.com/pimgs/m/263-2637044_work-for-my-job-icon-vector-person-png.png",
                "accessibilityText": "person"
              },
              "rows": [
                {
                  "cells": [
                    {
                      "text": "uuid"
                    },
                    {
                      "text": uuid
                    }
                  ],
                  "dividerAfter": False
                },
                {
                  "cells": [
                    {
                      "text": "name"
                    },
                    {
                      "text": name
                    }
                  ],
                  "dividerAfter": True
                },
                {
                  "cells": [
                    {
                      "text": "number"
                    },
                    {
                      "text": number
                    }
                  ]
                },
                {
                  "cells": [
                    {
                      "text": "gender"
                    },
                    {
                      "text": gender
                    }
                  ]
                },
                {
                  "cells": [
                    {
                      "text": "birthdate"
                    },
                    {
                      "text": birthdate
                    }
                  ]
                },
                {
                  "cells": [
                    {
                      "text": "address"
                    },
                    {
                      "text": address
                    }
                  ]
                },
                {
                  "cells": [
                    {
                      "text": "maritalStatus"
                    },
                    {
                      "text": "  " + marital_status
                    }
                  ]
                },
                {
                  "cells": [
                    {
                      "text": "multipleBirths"
                    },
                    {
                      "text": "  " + multiple_births
                    }
                  ]
                }
              ],
              "columnProperties": [
                {
                  "header": "Field",
                  "horizontalAlignment": "CENTER"
                },
                {
                  "header": "Data",
                  "horizontalAlignment": "LEADING"
                }
              ]
            }
          },
           {
            "simpleResponse": {
              "textToSpeech": "What would you like to do next?"
            }
          }
        ], 
        "suggestions": [
                          {
                            "title": "More Data on this Patient"
                          },
                          {
                            "title": "Get Data for New Patient"
                          },
                          {
                            "title": "Return to Menu"
                          }
                        ]
        
      }
    }
  }
}
    return patientDetailsCard


def returnCardForData(url):
    """ returns a sample card displaying the image at the inputted url
    Args:
      url: url to the image we need to display on the card
    """
    cardWithData = {
  "payload": {
    "google": {
      "expectUserResponse": True,
      "richResponse": {
        "items": [
          {
            "simpleResponse": {
              "textToSpeech": "Here's an example of a basic card."
            }
          },
          {
            "basicCard": {
              "title": "Title: this is a title",
              "subtitle": "This is a subtitle",
              "formattedText": "This is a basic card.  Text in a basic card can include \"quotes\" and\n    most other unicode characters including emojis.  Basic cards also support\n    some markdown formatting like *emphasis* or _italics_, **strong** or\n    __bold__, and ***bold itallic*** or ___strong emphasis___ as well as other\n    things like line  \nbreaks",
              "image": {
                "url": url,
                "accessibilityText": "Image alternate text"
              },
              "buttons": [
                {
                  "title": "This is a button",
                  "openUrlAction": {
                    "url": "https://assistant.google.com/"
                  }
                }
              ],
              "imageDisplayOptions": "CROPPED"
            }
          },
          {
            "simpleResponse": {
              "textToSpeech": "Which response would you like to see next?"
            }
          }
        ]
      }
    }
  }
}
    return cardWithData