import requests
import logging
import time

logging.basicConfig(filename='myapp.log', level=logging.INFO)


def dowload_one_match_data(number, year):
    filename_tpd = str (number) + "_tpd.pdf"
    filename_lu = str (number) + "_lu.pdf"
    filename_ts = str (number) + "_ts.pdf"

    url_tpd = "https://www.uefa.com/newsfiles/UCL/" + str(year)+ '/' + filename_tpd
    url_lu = "https://www.uefa.com/newsfiles/UCL/" + str(year)+ '/' + filename_lu
    url_ts = "https://www.uefa.com/newsfiles/UCL/" + str(year)+ '/' + filename_ts

    response_tpd = requests.get(url_tpd)
    response = requests.head(url_tpd)
    file_size = int(response.headers.get('Content-Length', 0))

    if file_size > 700:
        logging.info(f" {number} szamu fajl merete eleg nagy, ezert letoltom")
        #print(str(number) + " szamu fájl merete eleg nagy, ezert letoltom")
        response_lu = requests.get(url_lu)
        response_ts = requests.get(url_ts)
        with open('data/' + str(year) + '/' + filename_lu, "wb") as f:
            f.write(response_lu.content)
        with open('data/' + str(year) + '/' + filename_tpd, "wb") as f:
            f.write(response_tpd.content)
        with open('data/' + str(year) + '/' + filename_ts, "wb") as f:
            f.write(response_ts.content)
    else:
        logging.info(f" {number} szamu fajl merete kicsi, ezert  nem tortenik letoltes.")


year =2020
beg=2027013
nbeg=2029656
end=2030150

for i in range(nbeg,end):
    print(i)
    dowload_one_match_data(i,year)
    time.sleep(1)