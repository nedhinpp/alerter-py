from django.core.management.base import BaseCommand
import requests
import datetime
from alert_app.models import *
import json

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        districts = ['305','297','302','308','303','295']
        ditrict_chat_ids={'305': '@c0vidVaccine','297': '@c0vidVaccineKannur','295': '@c0vidVaccineKasaragod','303': '@c0vidVaccineThrissur','308': '@c0vidVaccinePalakkad','302': '@c0vidVaccineMalappuram'}
        for x in districts:
        	res = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+str(x)+"&date="+str(date))
        	data = res.json()
        	l = len(data.get('centers'))
        	for center in data.get('centers'):
        		for session in center.get('sessions'):
        			if session.get('available_capacity') != 0:
        				a = [center['center_id'], session['date'], session['min_age_limit'], session['vaccine']]
        				b = "-".join([str(x) for x in a ])
        				if not NotifyData.objects.filter(data=b).exists():
        					new_ob = NotifyData.objects.create(data=b)
        					new_ob.save()
        					# txt = "Vaccination center available <br>"+ str(center['name']) +"<br> "+ str(center['address']) +"<br> Vaccine : "+ str(session['vaccine'])+"<br> Age : "+str(session['min_age_limit'])+"<br> Total "+str(session['available_capacity'])+" slots are available on "+str(session['date'])+"<br> (Dose 1 : "+str(session['available_capacity_dose1'])+" , Dose 2 : "+str(session['available_capacity_dose2'])+") <br>coWin : https://selfregistration.cowin.gov.in"
        					txt = "*Vaccination center available* \n \n*"+ str(center['name']) +"*\n"+ str(center['address']) +"\nVaccine : *"+ str(session['vaccine'])+"*\nAge : *"+str(session['min_age_limit'])+" %2B * \nTotal *"+str(session['available_capacity'])+"* slots are available on *"+str(session['date'])+"*\n(Dose 1 : "+str(session['available_capacity_dose1'])+" , Dose 2 : "+str(session['available_capacity_dose2'])+") \n \nCoWin : https://selfregistration.cowin.gov.in"
        					response = requests.post("https://api.telegram.org/bot1860148922:AAHdt2gJdjl6kQT15lcxzbM-63ZJRTp4_Ps/sendMessage?chat_id="+ditrict_chat_ids[x]+"&text="+txt+"&parse_mode=Markdown")
        					print(response.json())
        NotifyData.objects.filter(created_at__lte=(datetime.datetime.now() - datetime.timedelta(hours = 1))).delete()



