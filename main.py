"""
This program implements game called "Ruokarähinä" which is game where different foods are
fighting against each other. The Program asks two user's to give foods which are fighting.
The program finds different food's stats from Finelli API's csv.files: "component_value.csv" 
and "food.csv". These files are downloaded from webpage: "https://fineli.fi/fineli/fi/ohje/19".
These files found from zip-file from that website with heading: "Peruspaketti 1. Sama sisältö 
kuin Fineli verkkopalvelussa (4232 elintarviketta ja 55 ravintotekijää) (zip 1,5 Mt )".
Food's stats are determined by food's nutrition values like below:

health=food's energy (kcal)
attack power=food's carbohydrates (g/100g)
defence=food's proteins (g/100g)
delay=fat + carbonhydrates + proteins (tells how fast food can attack)

When the stats are found the program shows how foods are fighting and finally
shows which food was stronger and won the fight. So the player must to guess which food's
stats are that good so that the food will won the other player's food. Is the food, wich delay is
lower, the best? or the food wich contains more energy? You have to find out about it!

The program is made only with Python programmin language and with windows computer. 
The program is easy to use. The user must only download "main.py"-, 
"component_value.csv"- and "food.csv" -files from gitHub, put them to same folder and then run the program. 
Then the program asks guestions and the users can play the game.

"""
import csv
import time

class Food:
    def __init__(self, id:int, name:str, long_name:str, health :float=0 , attack:float=0, defence:float=0, fat:float=0):
        self.id=id #food id to find food nutrition values from component_value.csv-file
        self.name=name #user given food name
        self.long_name=long_name #longer and more exact name for food (used for printing which foods are fighting)
        self.health=health #Foods energy in kcal/100g
        self.attack=attack #Food's carbohydrates in g/100g
        self.defence=defence #Food's proteins in g/100g. Food objects defence is taken in to account by percents. 
        #The more food has defence the more other food's attack power is lowered (see main function to see more closely how defence is taken in to account).
        self.fat=fat #Food's fat in g/100g
        self.delay=fat+defence+attack #Food's fat + carbonhydrates + proteins which tells how fast food can attack.
        self.time=self.delay #Time which keep a record what is the time when food attacks

    #Method for printing that food stats
    def __str__(self):
        print=f'{self.long_name}\nEnergia {self.health:.2f} kcal\nHiilihydraatit {self.attack:.2f} g\nProteiini {self.defence:.2f} g\nRasva {self.fat:.2f} g\n------------->\nHealth: {self.health:.2f}\nAttack: {self.attack:.2f}\nDefence: {self.defence:.2f}\nDelay: {self.delay:.2f} ({self.attack:.2f} + {self.defence:.2f} + {self.fat:.2f})\n'     
        return print

    #Method to check how different foods are hitting to each other. Uses class attribute health and attack to check that.
    def hit(self, attack:float):
        self.health-=attack
        #Forcing food's health to 0 if it goes to negative number.
        if self.health<0:
            self.health=0

#Function which is used to add foods in program's data structure from given csv.files
def add_food(food_dic, food1):
    #Boolean to explore is food in list
    is_food_in_list=False
    #Food id to find food's nutritional values from "component_value.csv"-file. Food id is both component_value.csv-file's
    #and food.csv-file's row's first element.
    food_id=""
    #More presice food name (for printing)
    food_long_name=""
    #List to save options if there are many foods with the same name
    food_options_list=[]
    #Boolean to check is there many food options with user given food name
    is_options_need=False
    #First file "food.csv" read and exploring is there foods which name is same as food name that the user has given.
    #Checking also that file is read succesful. If not the program gives an error (the error message is below after the except-structure).
    try:
        with open("food.csv") as file:
            for row in csv.reader(file, delimiter=";"):
                food_options=row[1].split(",")
                if food_options[0]==food1:
                    #Saving all options to list
                    food_options_list.append((row[0], row[1]))
                    food_long_name=row[1]
                    food_id=row[0]
            #Exploring is food options needed.
            if len(food_options_list)>1:
                is_options_need=True
            elif len(food_options_list)!=0:
                is_food_in_list=True
            #If options are needed, asking user to give that option number which is the food_id.
            #Loop ends when the user gives correct number. The program gives error message if the user gives unknown value.
            if is_options_need:
                print()
                print(f"Antamallasi ruualla {food1.lower()} on vaihtoehdot:")
                for option in food_options_list:
                    print(f"{option[0]} {option[1]}")
                print()
                desirable_option=input("Kirjoita taisteluun haluamasi vaihtoehdon numero:")
                while True:
                    for option in food_options_list:
                        if option[0]==desirable_option:
                            food_id=option[0]
                            food_long_name=option[1]
                            is_food_in_list=True
                            break
                    if is_food_in_list:
                        break
                    else:
                        print()
                        print("Vaihtoehto ei ollut listalla, kokeile uudestaan.")
                        desirable_option=input("Kirjoita taisteluun haluamasi vaihtoehdon numero:")
    #Error print if the first file is not read succesful                    
    except IOError:
        print("Tiedostoa food.csv ei voitu avata. Varmista, että tiedosto on samassa kansiossa kuin tiedosto main.py ja käynnistä ohjelma uudestaan.")                  
        raise
    #Checking that the second file is read succesful. If not the program gives an error (the error message is below after the except-structure)
    try:
        #Finding food's nutritional values from "component_value.csv"-file based to food's id
        if is_food_in_list:
            with open("component_value.csv") as file2:

                for row2 in csv.reader(file2, delimiter=";"):
                    if row2[0]==food_id:
                        #Getting food nutritional values to variables defined below
                        if row2[1]=="ENERC":
                            health=float(row2[2].replace(",", "."))
                        elif row2[1]=="FAT":
                            fat=float(row2[2].replace(",", "."))
                        elif row2[1]=="PROT":
                            defence=float(row2[2].replace(",", "."))
                        elif row2[1]=="CHOAVL":
                            attack=float(row2[2].replace(",", "."))
                #Making food object and saving food's informations to that program's data structure
                food=Food(food_id, food1, food_long_name, health, attack, defence, fat)
                food_dic[food1]=food
    #Error print if the second file is not read succesful  
    except IOError:
        print("Tiedostoa componen_value.csv ei voitu avata. Varmista, että tiedosto on samassa kansiossa kuin tiedosto main.py ja käynnistä ohjelma uudestaan.")                  
        raise
    #Returning boolean is food succesful added to the food data structure
    return is_food_in_list      
                


#Function that prints what has happened to foods when they are fighting.
#Function also fix that finnish language declensions that come out when printing events
#(There is only some declension fixes in this program. If the program is developed more the coder might add some exstra fixes)
def print_event(food1:Food, food2:Food):
    #Declension fixes:
    food2_name_copy=""
    #For example if food2.name="hampurilainen" fixing that when it is printed program says "hampurilaiselle"
    if food2.name[-3:]=="NEN":
        food2_name_copy=food2.name[0:len(food2.name)-3]+"se"
    #If there is two same consonants at the end of the food name for example "kurkku" program deletes the second one. 
    #Program doesn't do that if foods last character is "I".
    elif food2.name[-2]==food2.name[-3] and food2.name[-1]!="I":
        food2_name_copy=food2.name[0:len(food2.name)-2]+food2.name[-1]
    #If food name's last letter is "E"
    elif food2.name[-1]=="E":
        food2_name_copy=food2.name[0:len(food2.name)-1]+food2.name[-2]+2*food2.name[-1]
    #If food name's last letter is "O" and there is no double consonants at the end off the name
    elif food2.name[-1]=="O" and food2.name[-2]!=food2.name[-3]:
        food2_name_copy=food2.name[0:len(food2.name)-2]+"d"+food2.name[-1]
    #If no fixes needed
    else:
        food2_name_copy=food2.name
    #Printing event by using that food attributes.
    print(f"{food1.time:.2f} s {food1.name.title()} lyö ja tekee {food1.attack*(1-food2.defence/100):.2f} vahinkoa. {food2_name_copy.title()}lle jäi {food2.health:.2f} Health.")

#Programs main function which uses programs Food class and other functions. More details what this function
#does you will find below.
def main():
    #Dictionary where user foods are added
    food_dic={} 

    #Asks user to set two foods which are fighting. Uses function add_food() to do that.
    #If there is no food in the csv.file. The program gives another try.
    #When the two foods are found, the battle will begin.
    while  len(food_dic)!=2:
        food1=input("Anna ruoka:").upper()
        if add_food(food_dic, food1)==False:
            print(f"Ruokaa {food1.lower()} ei löytynyt listasta. Kokeile uudestaan.")
        else:
            while True:
                food2=input("Anna toinen ruoka:").upper()
                if add_food(food_dic, food2)==False:
                    print(f"Ruokaa {food2.lower()} ei löytynyt listasta. Kokeile uudestaan.")
                else:
                    break
    print()
    #Prints these two food stats
    for key in food_dic:
        print(food_dic[key])
        #Little break to user to explore different food stats.
        time.sleep(2)

    #Taking these two foods from the food dictionary and saving them to the variables
    food_obj1=food_dic[food1]
    food_obj2=food_dic[food2]

    
    #Printing these starting taglings
    print(f"{food_obj1.long_name.title()} vs {food_obj2.long_name.title()}")
    print()
    print(f"{food1.title()} Healt: {food_dic[food1].health} {food2.title()} Healt: {food_dic[food2].health}")
    print()
    #Little break
    time.sleep(2.5)
    #Battle begins
    print(f"0 s Taistelu alkaa")
    time.sleep(1)
    #Game loop where program uses class Food to explore how different foods are attacking to each other.
    while food_obj1.health>0 or food_obj2.health>0:
        #if food_obj2 delay is smaller it attacks to food_obj1
        if food_obj1.time>food_obj2.time:
            #Using Food method: hit(self, attack:float) to find out how much food_obj1's health is lowered.
            #Attack (power) is determined by food_obj2's attack power and there is also taken in to account that food_obj1's defence.
            #Food object's defence is taken in to account by percents. The more food has defence the more other food's attack power 
            #(which method hit() uses) is lowered.
            food_obj1.hit(food_obj2.attack*(1-food_obj1.defence/100))
            print_event(food_obj2, food_obj1)
            food_obj2.time+=food_obj2.delay

        elif food_obj2.time>food_obj1.time:
            food_obj2.hit(food_obj1.attack*(1-food_obj2.defence/100))
            print_event(food_obj1, food_obj2)
            food_obj1.time+=food_obj1.delay

        #Checks which food has won the battle.
        if food_obj1.health==0:
            print(f"{food2.title()} voitti taistelun!")
            break
        elif food_obj2.health==0:
            print(f"{food1.title()} voitti taistelun!")
            break
#Starting the program
main()      