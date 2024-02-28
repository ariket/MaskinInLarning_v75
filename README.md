# Pythonprogrammering för AI - IT-högskolan

Projektarbete: Maskininlärning/AI för att lösa ett på förhand givet problem.

Projektdefinition: Ett Python program som genom maskininärning förutspår sannolikheten för vilka hästar som komer att vinna på V75 kommande helg.

-------------------------------------------------------------------------------------------------------------------------------------------

Bibliotekt som jag använt för att samla in data:
bs4 BeautifulSoup		#Beautiful Soup is a Python library for pulling data out of HTML and XML files.
				#Web Scraping with Beautiful Soup.

selenium webdriver	        #Selenium driver is an automated testing framework used for the validation of websites (and web applications).
                                #The selenium package is used to automate web browser interaction from Python.

Selenium Webdreiver fungerar bäst ihop med webläsaren Chrome, vill man absolut inte använda chrome så måste koden ändras på två ställen,
man måste då kommentera bort "driver = webdriver.Chrome()" och istället aktivera EDGE eller Firefox i kodraderna precis under.

Bibliotekt som jag använt för maskininlärningen:
pandas				#pandas aims to be the fundamental high-level building block for doing practical, real world data analysis in Python. 
				#Additionally, it has the broader goal of becoming the most powerful and flexible open source data analysis / 
				#manipulation tool available in any language.

scikit-learn			#Simple and efficient tools for predictive data analysis
				#Accessible to everybody, and reusable in various contexts
				#Built on NumPy, SciPy, and matplotlib

-----------------------------------------------------------------------------------------------------------------------------------------------

Jag har laddat hem data för cirka 500 travlopp som gått det senaste året i Sverige. Det är denna datan jag ska använda mig av i projektet.
Jag har städat upp datan så den är korrekt utan tomma fält m.m. och jag har modifierat fälten jag ska använda till att endast vara numeriska. 
Kvaliteten på datan bedöms som högkvalitativ och kvantiteten på datan bör också vara tillräcklig för att kunna få ett bra slutreslutat. 
Jag kommer troligen inte att använda alla fält i datan jag laddat hem.

Datan har färdiga svar, som ju är vinnaren av travloppen så min data är av typen "labeled data".
Jag kommer således använda mig av "supervised learning" i min träningsmodell och det är ju ett klassificeringsproblem eftersom målvaribeln är
1 för vinnande häst och 0 för övriga hästar i ett lopp. Dock vill jag få ut den procentuella sannolikheten för att en häst vinner så jag kommer att 
använda mig av "predict_proba" i "scikit-learn" paktet och datan jag har är icke-linjär.

Min träningsmodell/träningsplattform använder sig av "Random Forest","Gradient Boosting" och "Decision Tree" modeller för att få fram ett så bra resultat som möjligt..

Problemet jag ska försöka att lösa är således att med högsta möjliga precision försöka hitta vinnaren i ett lopp, 
i mitt fall är då vinnaren en travhäst i ett V75 lopp.
------------------------------------------------------------------------------------------------------------------------------------------------

AI_projekt_resultat.py är slutredovisningen av detta projekt.

------------------------------------------------------------------------------------------------------------------------------------------------
/Ari Ketola