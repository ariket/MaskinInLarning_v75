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
from sklearn.svm import NuSVC
from sklearn.naive_bayes import CategoricalNB
from sklearn.neural_network import BernoulliRBM

#https://stats.stackexchange.com/questions/254638/should-i-choose-random-forest-regressor-or-classifier

# addera sannoliket för att häst vinner i sumDict
sumDict = {}

# Läs in historisk data:
data = pd.read_csv("./data/modified_data.csv")
# Läs in prediktion data:
preddata = pd.read_csv("./data/kommandeV75.csv")

# Förbered attribut. Drop "playpercent", if you dont want to use data about how much a horse is played.
Xpred = preddata.drop(columns=["racenum","horsename","driver","trainer"])  # Alla attribut utom "winnernum","horsename","driver","trainer"

# Förbered attribut och målvariabel
X = data.drop(columns=["racenum","winner","horsename","driver","trainer"])  # Alla attribut utom "winner","horsename","driver","trainer"
y = data["winner"]  # Målvariabel: 1

# Dela upp data i tränings- och testuppsättningar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Träna flera modeller
models = {
 # BRA   "Random Forest": RandomForestClassifier(max_depth=5,n_estimators=225, random_state=42),
#BRA  "Gradient Boosting": GradientBoostingClassifier(n_estimators=275, random_state=42),
  "Decision Tree": tree.DecisionTreeClassifier(max_depth=5,random_state=42)
}

modelNumber = 0
for model_name, model in models.items():
    
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid')
    calibrated_model.fit(X_train, y_train)

    # Gör prediktioner på testuppsättningen
    y_pred_proba = calibrated_model.predict_proba(X_test)
    yy_pred_proba = calibrated_model.predict_proba(Xpred)

    print(yy_pred_proba)

    # Skriv ut sannolikheten för varje häst att vinna
    print(f"Modell: {model_name}")
    #  for i, prob in enumerate(yy_pred_proba):
    #      print(f"Häst {i+1}: {prob[1]*100:.2f}% chans att vinna")
    v75lopp = {}
    horsenum = 1
    racenum = 1
    for i, (prob, startnum) in enumerate(zip(yy_pred_proba, Xpred['startnum'])):
        
        
        print(f"Horse {i+1}: {prob[1]*100:.2f}% chance to win, startnum: {startnum}")
        if startnum < horsenum: #new racenum
            racenum += 1
        v75lopp[int(f"{racenum}{startnum}")] = round(prob[1]*100,1)
        horsenum = startnum

    # Utvärdera modellen (kan anpassas för fler metriker)
    accuracy = balanced_accuracy_score(y_test, y_pred_proba.argmax(axis=1))
    print(f"Träffsäkerhet: {accuracy:.2f}\n")

    sorted_dict = dict(sorted(v75lopp.items(), key=lambda item: (int(str(item[0])[0]), -item[1])))
    
   
    

    printList = ["Lopp 1:         Lopp 2:         Lopp 3:         Lopp 4:         Lopp 5:         Lopp 6:         Lopp 7:         Lopp 8:","","","","","","","","","","","","","","",""]

    racenum = "1"
    Listindex = 0
    print("Första siffran i respektive lopp anger hästnummer och andra siffran vinstchansen i procent.")
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

    i = 0
    while i < 15:  
      print(printList[i])
      i += 1  

    modelNumber += 1    