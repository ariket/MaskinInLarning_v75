import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split



# Läs in historisk data från "historisk_data.csv"
data = pd.read_csv("./data/modified_data.csv")

# Förbered attribut och målvariabel
X = data.drop(columns=["racenum","winner","horsename","driver","trainer"])  # Alla attribut utom "winner","horsename","driver","trainer"
y = data["winner"]  # Målvariabel: 1

# Dela upp data i tränings- och testuppsättningar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definiera parametrar att testa
param_grid = {
    'n_estimators': [100, 200, 300]
}

# Grid Search för Random Forest Classifier
rf_model = RandomForestClassifier(random_state=42)
rf_grid_search = GridSearchCV(rf_model, param_grid, cv=5)
rf_grid_search.fit(X_train, y_train)

# Grid Search för Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(random_state=42)
gb_grid_search = GridSearchCV(gb_model, param_grid, cv=5)
gb_grid_search.fit(X_train, y_train)

# Bästa parametrar för varje modell
print("Bästa n_estimators för Random Forest:", rf_grid_search.best_params_['n_estimators'])
print("Bästa n_estimators för Gradient Boosting:", gb_grid_search.best_params_['n_estimators'])

#Bästa n_estimators för Random Forest: 200-225
#Bästa n_estimators för Gradient Boosting: 250-300

"""

Random Forest Classifier:
Testa olika värden för n_estimators, till exempel 50, 100, 200, 300, etc.
Utvärdera modellen med hjälp av en lämplig prestandametrik (t.ex. träffsäkerhet, AUC, F1-score).
Välj det värde för n_estimators som ger bäst prestanda.
Gradient Boosting Classifier:
På liknande sätt, testa olika värden för n_estimators.
Utvärdera modellen med samma prestandametrik som ovan.
Välj det optimala värdet för n_estimators.
Det är viktigt att notera att det inte finns en absolut “bästa” siffra för n_estimators.
Det beror på specifika data och problem.
"""
