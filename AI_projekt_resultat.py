import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import balanced_accuracy_score
from sklearn import tree
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.svm import SVC
from sklearn.naive_bayes import CategoricalNB
from sklearn.neural_network import BernoulliRBM
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeClassifier

# Läs in historisk data:
data = pd.read_csv("./data/modified_data.csv")
# Läs in prediktion data:
preddata = pd.read_csv("./data/kommandeV75.csv")

# Förbered attribut. ta bort(drop) "playpercent", om du vill använda modellen utan att ta hänsyn till hur mycket en häst är spelad.
#Tar bort variabler som inte bedöms relevanta för att erhålla bästa möjliga resultat.
Xpred = preddata.drop(columns=["playpercent","racenum","winnernum","horsename","driver","trainer","resrace1","pricesumrace1",
                               "resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5"])  


# Förbered attribut och målvariabel
X = data.drop(columns=["winner","playpercent","racenum","winnernum","horsename","driver","trainer","resrace1","pricesumrace1",
                       "resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5"]) 
y = data["winner"]  # Målvariabel: Har värde 1 eller 0, 1 om hästen vann annars 0.

# Dela upp data i tränings- och testuppsättningar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

                                                                                           
# Tränar flera modeller och använder summan av alla prediktioner i slutresultet.          # Jag har provat flera algoritmer(modeller) från
models = {                                                                                # scikit men fått bäst resultat med dessa 3:
  "Random Forest": RandomForestClassifier(max_depth=5,n_estimators=225, random_state=42),
  "Gradient Boosting": GradientBoostingClassifier(n_estimators=275, random_state=42),
  "Decision Tree": tree.DecisionTreeClassifier(max_depth=5,random_state=42)
}


sumDict = {}    # addera sannolikhet för att häst vinner i sumDict
modelNumber = 0
for model_name, model in models.items():
    
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid')
    calibrated_model.fit(X_train, y_train)

    # Gör prediktioner på testuppsättningen för att få träffsäkerheten på modellen.
    y_pred_proba = calibrated_model.predict_proba(X_test)
    # Gör prediktioner på min prediktion data
    yy_pred_proba = calibrated_model.predict_proba(Xpred)
    #print(yy_pred_proba)
 
    v75lopp = {}
    horsenum = 1
    racenum = 1
    for i, (prob, startnum) in enumerate(zip(yy_pred_proba, Xpred['startnum'])):
        
        
        #print(f"Horse {i+1}: {prob[1]*100:.2f}% chance to win, startnum: {startnum}")
        if startnum < horsenum: #new racenum
            racenum += 1
        v75lopp[int(f"{racenum}{startnum}")] = round(prob[1]*100,1)
        if modelNumber == 0:
          sumDict[int(f"{racenum}{startnum}")] = round(prob[1]*100,2)
        else:
          tempPercent = sumDict[int(f"{racenum}{startnum}")]
          sumDict[int(f"{racenum}{startnum}")] = round(round(prob[1]*100,2) + tempPercent,1)
        horsenum = startnum
    modelNumber += 1              

    print(f"Modell: {model_name}")
    # Utvärdera modellen med "balanced_accuracy_score"
    accuracy = balanced_accuracy_score(y_test, y_pred_proba.argmax(axis=1))
    print(f"Träffsäkerhet: {accuracy:.2f}\n")

v75lopp = dict(sumDict)
sorted_dict = dict(sorted(v75lopp.items(), key=lambda item: (int(str(item[0])[0]), -item[1])))

if str(list(sorted_dict)[-1])[0] == 8: #För v86, 8 lopp
  printList = ["Lopp 1:         Lopp 2:         Lopp 3:         Lopp 4:         Lopp 5:         Lopp 6:         Lopp 7:         Lopp 8:","","","","","","","","","","","","","","",""]
else:
  printList = ["Lopp 1:         Lopp 2:         Lopp 3:         Lopp 4:         Lopp 5:         Lopp 6:         Lopp 7:                ","","","","","","","","","","","","","","",""]

racenum = "1"
Listindex = 0
print("________________________________________________________________________________________________________________________________\n")
print("Första siffran i respektive lopp anger hästnummer och" +
      " andra siffran anger vinstchansen(ju större siffa ju större vinstchans).\n" +
      "\n                                           ***Lycka till i veckans v75!!!***")
print("________________________________________________________________________________________________________________________________")
for horseNum, percent in sorted_dict.items():     
  if racenum != str(horseNum)[0]:
    # print(f"Lopp {str(horseNum)[0]}:")
    while Listindex < 15:
        printList[Listindex + 1] = printList[Listindex + 1] + "                "
        Listindex += 1

    Listindex = 1
  
  else:
      Listindex += 1
  printList[Listindex] = printList[Listindex] + ("{} \t{}\t".format(str(horseNum)[1:], percent))
  #print("{}\t{}".format(str(horseNum)[1:], percent))
  racenum = str(horseNum)[0]

#Printar ut resultatet
i = 0
while i < 15:  
  print(printList[i])
  i += 1  
print("________________________________________________________________________________________________________________________________")