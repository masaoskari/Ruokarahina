# Ruokarahina
This program implements game called "Ruokarähinä" which is game where different foods are
fighting against each other. The Program asks two user's to give foods which are fighting.
The program finds different food's stats from Finelli API's csv.files: "component_value.csv" 
and "food.csv". These files are downloaded from webpage: "https://fineli.fi/fineli/fi/ohje/19".
These files found from zip-file from that website with heading: "Peruspaketti 1. Sama sisältö 
kuin Fineli verkkopalvelussa (4232 elintarviketta ja 55 ravintotekijää) (zip 1,5 Mt )".
Food's stats are determined by food's nutrition values like below:

health=food's energy (kcal)
attack power=food's carbohydrates (g/100g)
defence=food's proteins (g/100g) //Food objects defense is taken into account to fight in percentages.
delay=fat + carbonhydrates + proteins (tells how fast food can attack)

When the stats are found the program shows how foods are fighting and finally
shows which food was stronger and won the fight. So the player must to guess which food's
stats are that good so that the food will won the other player's food. Is the food, wich delay
is lower, the best? or the food wich contains more energy? You have to find out about it!

The program is made only with Python programmin language and with windows computer. 
The program is easy to use. The user must only download "main.py"-, "component_value.csv"- 
and "food.csv" -files from gitHub, put them to same folder and then run the program. 
Then the program asks guestions and the users can play the game.
