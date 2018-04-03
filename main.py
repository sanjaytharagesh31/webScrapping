#python script to extract the status of trains from Ettimadai to Coimbatore Jn 
import datetime
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from prettytable import PrettyTable

train = ["56712", "66606", "56604", "56650", "66608", "66604", "56324"]
#onStation = "ETMD"
date = str(datetime.today())
todayDate = date[8:10]+"/"+date[5:7]+"/"+date[:4]
t = PrettyTable (["Train", "Expc Arrival", "Last Station", "Updated on" ])
t.align["Train"] = "l"
t.align["Expc Arrival"] = "l"
t.align["Last Station"] = "l"
t.align["Updated on"] = "l"
def getStatus():
  for i in train:
    url = "https://enquiry.indianrail.gov.in/xyzabc/SelectedDateOfTrain?trainNo="+i+"&startDate="+todayDate+"&journeyStn=ETMD&journeyDate="+todayDate+"&boardDeboard=0&langFile=props.en-us"
    page = requests.get(url)
    page_content = BeautifulSoup(page.content,'html.parser')

    req_div = page_content.findAll('div', class_="w3-padding-small w3-margin-top w3-border w3-border-grey w3-round")
    if (len(req_div)>0):
      side_one = req_div[0].findAll('table')

      arrival_td = side_one[2].tbody.tr.findAll('td')
      arrival_time = arrival_td[1].text.strip()
      side_two = req_div[1].findAll('table')

      curstation_tr = side_two[0].tbody.findAll('tr')
      curstation_td = curstation_tr[1].findAll('td')
      curstation_id = curstation_td[1].text.strip()
      curstation_deptime_td = curstation_tr[2].findAll('td')
      curstation_deptime_id = curstation_deptime_td[1].text.strip()

      req_lastupdated = page_content.findAll('div', class_="w3-padding-small w3-border w3-border-grey w3-round")
      last_updatetime_td = req_lastupdated[0].div.table.tbody.tr.findAll('td')
      last_updatetime_id = last_updatetime_td[1].text.strip()


      t.add_row([i, arrival_time, curstation_id, last_updatetime_id])
    else:
      t.add_row([i, "NA", "NA", "NA"])

print ("Current Status of trains from Ettimadai to Coimbatore Jn")
getStatus()
    
print (t)
