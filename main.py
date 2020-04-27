import time
import numpy as np
from Scraper import Scraper
from tensorflow import keras

nn = keras.models.load_model("model.h5")


color = -1
bet_amount = 2

scraper = Scraper()

username = input("Username: ")
password = input("Password: ")

print("authorization is {}".format(scraper.login(username, password)))
time.sleep(5)
scraper.close_modal()

rolled = int(input("Last rolled: "))

while True:
    time.sleep(1)
    data = scraper.get_values()

    print("Data {}".format(data))

    if data:
        if data[0]:
            if int(data[0]) == 0:
                rolled = 0
            elif int(data[0]) > 7:
                rolled = 2
            elif int(data[0]) <= 7:
                rolled = 1

            if color != -1:
                if color == rolled:
                    bet_amount = 2
                else:
                    bet_amount *= 2

            time.sleep(5)

            color = nn.predict([[data[1]]])
            color = np.argmax(color)

            if scraper.make_bet(bet_amount,color):
                print("betted")
            else:
                print("couldnt make a bet")

            print("bet amount {}".format(bet_amount))
            print("color predicted {}".format(color))