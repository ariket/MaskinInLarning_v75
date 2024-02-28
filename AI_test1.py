import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
import numpy



# Läs in historisk data
historical_data = pd.read_csv("./data/modified_data.csv")

# Läs in data för kommande V75 lopp
upcoming_data = pd.read_csv("./data/kommandeV75.csv")
upcoming_data2 = upcoming_data.drop(columns=["racenum","winnernum","horsename","driver","trainer","resrace1","pricesumrace1","resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5"])


# Ta bort eventuella rader med NaN-värden
#historical_data.dropna(inplace=True)

# Välj funktioner (features) och målvariabel (target)
features = historical_data.drop(columns=["racenum","winnernum","winner","horsename","driver","trainer","resrace1","pricesumrace1","resrace2","pricesumrace2","resrace3","pricesumrace3","resrace4","pricesumrace4","resrace5","pricesumrace5"])
target = historical_data['winner']

# Dela upp datat i tränings- och testset
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=42)

# Lista för att spara resultaten
results = {}

# Träna och utvärdera fyra olika regressionsmodeller med Pipeline och andra parametrar
for name, model in [('Random Forest Regression', Pipeline([('scaler', StandardScaler()), ('regressor', RandomForestRegressor(n_estimators=250, random_state=42, max_depth=5))])),
                    #Fungerar dåligt för min data('Neural Networks (Regression)', Pipeline([('scaler', StandardScaler()), ('regressor', MLPRegressor(hidden_layer_sizes=(100, ), activation='relu', solver='adam', max_iter=1000))])),
                    ('Gradient Boosting Regression', Pipeline([('scaler', StandardScaler()), ('regressor', GradientBoostingRegressor(n_estimators=350, random_state=42, learning_rate=0.2, max_depth=6))])),
                    #Fungerar ok men ger samma värden som 'Ridge Regression'('Linear Regression', Pipeline([('scaler', StandardScaler()), ('regressor', LinearRegression())])),
                    #Fungerar dåligt för min data ('Decision Tree Regression', DecisionTreeRegressor(max_depth=5)),
                    ('Ridge Regression', Pipeline([('scaler', StandardScaler()), ('regressor', Ridge(alpha=1.0, fit_intercept=True))])),
                    #Fungerar dåligt för min data('Lasso Regression', Pipeline([('scaler', StandardScaler()), ('regressor', Lasso(alpha=1.0))])),
                    #Fungerar dåligt för min data('Support Vector Machine', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='rbf', C=1, gamma='scale', epsilon=0.3))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Linear Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='linear', C=1.0, epsilon=0.1))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Polynomial Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='poly', degree=3, C=1.0, gamma='scale', epsilon=0.1))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Sigmoid Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='sigmoid', C=0.5, gamma='scale', epsilon=0.3))]))
                    ]:
        
    
    model.fit(X_train, y_train)
   
    upcoming_data[name] = model.predict(upcoming_data2)
    #ingen skillnad mellan score och accuracy_score
    #https://stats.stackexchange.com/questions/354709/sklearn-metrics-accuracy-score-vs-logisticregression-score
    y_pred = model.predict(X_test)
    #mse = mean_squared_error(y_test, y_pred)
    #results[name] = mse
    accuracy = model.score(X_test, y_test)
    #accuracy = model.score(X_train, y_train)

    results[name] = accuracy

# Skriv ut resultaten
#print("Mean Squared Error:")
#for name, mse in results.items():
#    print(f"{name}: {mse}")
print("Accuracy Score:")
for name, accuracy in results.items():
    print(f"{name}: {accuracy}")    


"""
# Gör förutsägelser på kommande V75 lopp med Pipeline och andra parametrar
for name, model in [('Random Forest Regression', Pipeline([('scaler', StandardScaler()), ('regressor', RandomForestRegressor(n_estimators=250, max_depth=5))])),
                    #Fungerar dåligt för min data('Neural Networks (Regression)', Pipeline([('scaler', StandardScaler()), ('regressor', MLPRegressor(hidden_layer_sizes=(100, ), activation='relu', solver='adam', max_iter=1000))])),
                    ('Gradient Boosting Regression', Pipeline([('scaler', StandardScaler()), ('regressor', GradientBoostingRegressor(n_estimators=450, learning_rate=0.2, max_depth=6))])),
                    #Fungerar ok men ger samma värden som 'Ridge Regression'('Linear Regression', Pipeline([('scaler', StandardScaler()), ('regressor', LinearRegression())])),
                    #Fungerar dåligt för min data ('Decision Tree Regression', DecisionTreeRegressor(max_depth=5)),
                    ('Ridge Regression', Pipeline([('scaler', StandardScaler()), ('regressor', Ridge(alpha=1.0, fit_intercept=True))])),
                    #Fungerar dåligt för min data('Lasso Regression', Pipeline([('scaler', StandardScaler()), ('regressor', Lasso(alpha=1.0, fit_intercept=True, normalize=False, precompute=False, copy_X=True, max_iter=1000, tol=0.0001, warm_start=False, positive=False, random_state=None, selection='cyclic'))])),
                    #Fungerar dåligt för min data('Support Vector Machine', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='rbf', C=1, gamma='scale', epsilon=0.1))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Linear Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='linear', C=1.0, epsilon=0.1))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Polynomial Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='poly', degree=3, C=1.0, gamma='scale', epsilon=0.1))])),
                    #Fungerar dåligt för min data('Support Vector Machine (Sigmoid Kernel)', Pipeline([('scaler', StandardScaler()), ('regressor', SVR(kernel='sigmoid', C=0.5, gamma='scale', epsilon=0.1))]))
                    ]:
     
         
    model.fit(features, target)
    upcoming_data[name] = model.predict(upcoming_data2)
"""
# Skriv ut förutsägelserna för kommande V75 lopp
print("\nFörutsägelser för kommande V75 lopp:")
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    
    print(upcoming_data[['horsename','startnum','Random Forest Regression','Gradient Boosting Regression','startnum','Ridge Regression']])