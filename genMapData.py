import pandas as pd
import pandas as pd

nationWideActive = 0
nationWideClosed = 0
activeStates = []
closedStates = []

states = [
['Alabama','AL',0,0],
['Alaska','AK',0,0],
['Arizona','AZ',0,0],
['Arkansas','AR',0,0],
['California','CA',0,0],
['Colorado','CO',0,0],
['Connecticut','CT',0,0],
['Delaware','DE',0,0],
['District of Columbia','DC',0,0],
['Florida','FL',0,0],
['Georgia','GA',0,0],
['Hawaii','HI',0,0],
['Idaho','ID',0,0],
['Illinois','IL',0,0],
['Indiana','IN',0,0],
['Iowa','IA',0,0],
['Kansas','KS',0,0],
['Kentucky','KY',0,0],
['Louisiana','LA',0,0],

['Maine','ME',0,0],
['Maryland','MD',0,0],
['Massachusetts','MA',0,0],
['Michigan','MI',0,0],
['Minnesota','MN',0,0],
['Mississippi','MS',0,0],
['Missouri','MO',0,0],
['Montana','MT',0,0],
['Nebraska','Ne',0,0],
['Nevada','NV',0,0],
['Missouri','MO',0,0],
['Montana','MT',0,0],
['Nebraska','NE',0,0],
['Nevada','NV',0,0],
['New Hampshire','NH',0,0],
['New Jersey','NJ',0,0],
['New Mexico','NM',0,0],
['New York','NY',0,0],
['North Carolina','NC',0,0],
['North Dakota','ND',0,0],
['Ohio','OH',0,0],
['Oklahoma','OK',0,0],
['Oregon','OR',0,0],
['Pennsylvania','PA',0,0],
['Puerto Rico','PR',0,0],
['Rhode Island','RI',0,0],
['South Carolina','SC',0,0],
['South Dakota','SD',0,0],
['Tennessee','TN',0,0],
['Texas','TX',0,0],
['Utah','UT',0,0],
['Vermont','VT',0,0],
['Virginia','VA',0,0],
['Washington','WA',0,0],
['West Virginia','WV',0,0],
['Wisconsin','WI',0,0],
['Wyoming','WY',0,0],
]

def convert():
    with open("./hi.json") as f:
        temp = pd.read_json(f)
        temp.to_csv("hicsv.csv", index=False)
convert() 
                
def readCSV2():
    with open("hicsv.csv") as df:
        for i in df[df.columns[23]]:
            state = df[df.columns[3]]
            if str(i) == "Active Recall":
                activeStates.append(state)
            elif str(i) == "Closed Recall":
                closedStates.append(state)
 
def readCSV2():
    with open("hicsv.csv", encoding = "utf8") as df:
        temp = pd.read_csv(df)
        for i in temp[temp.columns[23]]:
            state = temp[temp.columns[3]]
            if str(i) == "Active Recall":
                activeStates.append(state)
            elif str(i) == "Closed Recall":
                closedStates.append(state)
                
def readCSV():
    with open("hicsv.csv", encoding = "utf8") as df:
        temp = pd.read_csv(df)
        #print(temp.columns)
        x = temp.loc[:, "field_recall_type"]
        #print(dir(x))
        state = temp.loc[:, "field_states"]
        #print(dir(y))
        print(x, state)
        for i in x:
            if str(x[i].at['field_recall_type']) == 'Active Recall':
                activeStates.append(state)
            elif str(x[i].at['field_recall_type']) == 'Closed Recall':
                closedStates.append(state)
            elif str(x[i].at['field_recall_type']) == 'Public Health Alert':
                continue
                
def writeActive():
    for x in activeStates:
        if type(x) != float:
            if "Nationwide" in x:
                nationWideActive += 1
            else:
                for i in range(len(states)):
                    states[i][2] = x.count()
                    for stateName in x:
                        states[i][2] += 1
                        

readCSV()
#writeActive()
print(states)