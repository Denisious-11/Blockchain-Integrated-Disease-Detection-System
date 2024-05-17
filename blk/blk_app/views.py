from django.shortcuts import render
from .models import *
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
import re
import os
from .vals import *
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage

from datetime import date
from datetime import datetime
from blockchain import *
import ipfshttpclient
import numpy as np
from tensorflow.keras.models import load_model
import pickle


# Load the saved model
model_saved = load_model('prediction_model.h5')
with open('label_encoder.pkl', 'rb') as f:
	label_encoder = pickle.load(f)


allopathy_treatments = {
	"Hepatitis A": "Symptomatic treatment, rest, fluids, and sometimes antiviral medications",
	"Dimorphic hemorrhoids (piles)": "High-fiber diet, topical treatments, minimally invasive procedures, surgery in severe cases",
	"Arthritis": "Nonsteroidal anti-inflammatory drugs (NSAIDs), disease-modifying antirheumatic drugs (DMARDs), biologic response modifiers, physical therapy",
	"Fungal infection": "Antifungal medications (oral or topical)",
	"Alcoholic hepatitis": "Alcohol cessation, supportive care, corticosteroids in severe cases",
	"Cervical spondylosis": "Pain relievers, muscle relaxants, physical therapy, cervical collars, surgery in severe cases",
	"AIDS": "Antiretroviral therapy (ART)",
	"Impetigo": "Topical or oral antibiotics",
	"Hyperthyroidism": "Antithyroid medications, radioactive iodine therapy, beta blockers",
	"Paralysis (brain hemorrhage)": "Rehabilitation therapy, medication to prevent blood clots, surgery in some cases",
	"Vertigo (Paroxysmal positional vertigo)": "Epley maneuver, balance training exercises, medications to control symptoms",
	"Hypothyroidism": "Levothyroxine (thyroid hormone replacement)",
	"Pneumonia": "Antibiotics, cough medicine, fever reducers, oxygen therapy in severe cases",
	"Osteoarthritis": "Pain relievers, physical therapy, corticosteroid injections, joint replacement surgery in severe cases",
	"Hepatitis B": "Antiviral medications, interferon injections, liver transplant in severe cases",
	"Chickenpox": "Symptomatic treatment, antiviral medications in some cases",
	"Varicose veins": "Compression stockings, lifestyle changes, vein procedures",
	"Allergy": "Antihistamines, decongestants, allergy shots in severe cases",
	"Malaria": "Antimalarial medications",
	"Typhoid": "Antibiotics, supportive care, fluid replacement therapy",
	"Hepatitis E": "Supportive care, avoiding alcohol, rest",
	"Hypertension": "Lifestyle changes, diuretics, ACE inhibitors, beta blockers, calcium channel blockers",
	"Bronchial asthma": "Bronchodilators (inhalers), corticosteroids, leukotriene modifiers, allergy medications",
	"Hepatitis D": "No specific antiviral treatment; management of complications",
	"Urinary tract infection": "Antibiotics, increased fluid intake",
	"Psoriasis": "Topical treatments, phototherapy, oral medications, biologic drugs",
	"Chronic cholestasis": "Medications to relieve itching, ursodeoxycholic acid, liver transplant in severe cases",
	"Peptic ulcer disease": "Proton pump inhibitors, antibiotics (if caused by H. pylori infection), antacids",
	"GERD (Gastroesophageal reflux disease)": "Antacids, proton pump inhibitors, lifestyle changes",
	"Drug reaction": "Discontinuation of the offending medication, supportive care, sometimes steroids or antihistamines",
	"Acne": "Topical treatments (e.g., benzoyl peroxide, retinoids), oral antibiotics, hormonal therapy, isotretinoin in severe cases",
	"Heart attack": "Aspirin, thrombolytics, beta blockers, ACE inhibitors, statins, angioplasty, bypass surgery",
	"Diabetes": "Insulin therapy, oral medications (e.g., metformin, sulfonylureas), lifestyle changes",
	"Common Cold": "Symptomatic treatment (rest, fluids, over-the-counter cold medications)",
	"Hepatitis C": "Antiviral medications (e.g., direct-acting antivirals), liver transplant in severe cases",
	"Tuberculosis": "Antibiotics (usually a combination), directly observed therapy (DOT)",
	"Migraine": "Pain relievers, triptans, preventive medications (e.g., beta blockers, anticonvulsants)",
	"Jaundice": "Treatment of underlying cause, supportive care, phototherapy in newborns",
	"Hypoglycemia": "Glucose or sugar intake, glucagon injection in severe cases",
	"Gastroenteritis": "Symptomatic treatment (fluids, electrolytes), sometimes antibiotics in bacterial cases",
	"Dengue": "Supportive care (fluids, rest, pain relievers), sometimes hospitalization in severe cases"
}




homeopathy_treatments = {
	"Hepatitis A": "Chelidonium, Bryonia, Nux vomica",
	"Dimorphic hemorrhoids (piles)": "Aesculus hippocastanum, Collinsonia, Hamamelis",
	"Arthritis": "Rhus tox, Bryonia, Calcarea fluorica",
	"Fungal infection": "Thuja, Sulphur, Graphites",
	"Alcoholic hepatitis": "Lycopodium, Carduus marianus, Chelidonium",
	"Cervical spondylosis": "Ruta, Calcarea fluorica, Cimicifuga",
	"AIDS": "Natrum muriaticum, Thuja, Arsenicum album",
	"Impetigo": "Arsenicum album, Hepar sulph, Silicea",
	"Hyperthyroidism": "Lachesis, Thyroidinum, Iodum",
	"Paralysis (brain hemorrhage)": "Arnica, Gelsemium, Lachesis",
	"Vertigo (Paroxysmal positional vertigo)": "Conium, Cocculus, Bryonia",
	"Hypothyroidism": "Calcarea carbonica, Sepia, Lycopodium",
	"Pneumonia": "Antimonium tart, Bryonia, Phosphorus",
	"Osteoarthritis": "Rhus tox, Bryonia, Calcarea fluorica",
	"Hepatitis B": "Chelidonium, Lycopodium, Carduus marianus",
	"Chickenpox": "Antimonium tart, Rhus tox, Belladonna",
	"Varicose veins": "Hamamelis, Pulsatilla, Calcarea fluorica",
	"Allergy": "Allium cepa, Natrum mur, Arsenicum album",
	"Malaria": "China officinalis, Arsenicum album, Nux vomica",
	"Typhoid": "Baptisia, Arsenicum album, Rhus tox",
	"Hepatitis E": "Chelidonium, Bryonia, Nux vomica",
	"Hypertension": "Natrum muriaticum, Belladonna, Glonoinum",
	"Bronchial asthma": "Arsenicum album, Sambucus, Natrum sulph",
	"Hepatitis D": "Chelidonium, Lycopodium, Carduus marianus",
	"Urinary tract infection": "Cantharis, Apis mellifica, Sarsaparilla",
	"Psoriasis": "Arsenicum album, Graphites, Sulphur",
	"Chronic cholestasis": "Chelidonium, Carduus marianus, Lycopodium",
	"Peptic ulcer disease": "Nux vomica, Arsenicum album, Lycopodium",
	"GERD (Gastroesophageal reflux disease)": "Nux vomica, Pulsatilla, Carbo veg",
	"Drug reaction": "Apis mellifica, Arsenicum album, Sulphur",
	"Acne": "Hepar sulph, Kali bromatum, Berberis aquifolium",
	"Heart attack": "Arnica, Cactus, Crataegus",
	"Diabetes": "Syzygium, Uranium nitricum, Phosphoric acid",
	"Common Cold": "Aconite, Allium cepa, Gelsemium",
	"Hepatitis C": "Chelidonium, Lycopodium, Carduus marianus",
	"Tuberculosis": "Arsenicum album, Phosphorus, Tuberculinum",
	"Migraine": "Belladonna, Iris versicolor, Spigelia",
	"Jaundice": "Chelidonium, Lycopodium, Carduus marianus",
	"Hypoglycemia": "Syzygium, Uranium nitricum, Phosphoric acid",
	"Gastroenteritis": "Arsenicum album, Podophyllum, Veratrum album",
	"Dengue": "Eupatorium perfoliatum, Arsenicum album, China officinalis"
}




ayurveda_treatments = {
	"Hepatitis A": "Ayurvedic herbs like Kutki (Picrorhiza kurroa), Bhumiamalaki (Phyllanthus niruri), Amalaki (Emblica officinalis), supportive therapy like liver detoxification (Panchakarma), dietary changes",
	"Dimorphic hemorrhoids (piles)": "Ayurvedic herbs like Triphala, Arshoghni vati, Kankayan vati, dietary changes including increased fiber intake, lifestyle modifications",
	"Arthritis": "Ayurvedic herbs like Ashwagandha (Withania somnifera), Guggul (Commiphora wightii), Shallaki (Boswellia serrata), Panchakarma therapies, dietary changes according to Dosha imbalance",
	"Fungal infection": "Ayurvedic herbs like Neem (Azadirachta indica), Haridra (Curcuma longa), Gandhak rasayan, Triphala, maintaining hygiene",
	"Alcoholic hepatitis": "Ayurvedic herbs like Bhumyamalaki (Phyllanthus niruri), Punarnava (Boerhavia diffusa), Katuki (Picrorhiza kurroa), strict abstinence from alcohol, liver detoxification therapies",
	"Cervical spondylosis": "Ayurvedic herbs like Shallaki (Boswellia serrata), Ashwagandha (Withania somnifera), Guggulu (Commiphora wightii), Panchakarma therapies like Greeva basti, dietary changes",
	"AIDS": "Ayurvedic herbs to boost immunity like Guduchi (Tinospora cordifolia), Amalaki (Emblica officinalis), Ashwagandha (Withania somnifera), supportive care to manage symptoms",
	"Impetigo": "Ayurvedic herbs with antibacterial properties like Neem (Azadirachta indica), Haridra (Curcuma longa), Khadir (Acacia catechu), maintaining hygiene",
	"Hyperthyroidism": "Ayurvedic herbs like Guggulu (Commiphora wightii), Brahmi (Bacopa monnieri), Jatamansi (Nardostachys jatamansi), dietary changes according to Dosha imbalance",
	"Paralysis (brain hemorrhage)": "Ayurvedic herbs for nerve regeneration like Ashwagandha (Withania somnifera), Brahmi (Bacopa monnieri), Panchakarma therapies like Abhyanga, Basti",
	"Vertigo (Paroxysmal positional vertigo)": "Ayurvedic herbs for balancing Doshas like Brahmi (Bacopa monnieri), Shankhpushpi (Convolvulus pluricaulis), lifestyle modifications, dietary changes",
	"Hypothyroidism": "Ayurvedic herbs to stimulate thyroid function like Guggulu (Commiphora wightii), Kanchanar guggulu, Ashwagandha (Withania somnifera), dietary changes according to Dosha imbalance",
	"Pneumonia": "Ayurvedic herbs for respiratory health like Tulsi (Ocimum sanctum), Pippali (Piper longum), Kantakari (Solanum xanthocarpum), supportive care including rest and hydration",
	"Osteoarthritis": "Ayurvedic herbs with anti-inflammatory properties like Shallaki (Boswellia serrata), Guggulu (Commiphora wightii), Maharasnadi kwath, Panchakarma therapies like Janu basti",
	"Hepatitis B": "Ayurvedic herbs like Kutki (Picrorhiza kurroa), Bhumi Amalaki (Phyllanthus niruri), supportive liver detoxification therapies, strict abstinence from alcohol",
	"Chickenpox": "Ayurvedic herbs to boost immunity like Guduchi (Tinospora cordifolia), Amalaki (Emblica officinalis), supportive care to manage symptoms",
	"Varicose veins": "Ayurvedic herbs for strengthening blood vessels like Triphala, Guggulu (Commiphora wightii), lifestyle modifications including regular exercise and avoiding prolonged standing",
	"Allergy": "Ayurvedic herbs with anti-allergic properties like Haridra (Curcuma longa), Neem (Azadirachta indica), supportive therapies to balance Doshas",
	"Malaria": "Ayurvedic herbs with antimalarial properties like Tulsi (Ocimum sanctum), Neem (Azadirachta indica), Papaya leaf extract, supportive care including hydration and rest",
	"Typhoid": "Ayurvedic herbs with antibacterial properties like Kutaja (Holarrhena antidysenterica), Dhataki (Woodfordia fruticosa), supportive care including hydration and rest",
	"Hepatitis E": "Ayurvedic herbs like Bhumi Amalaki (Phyllanthus niruri), Kutki (Picrorhiza kurroa), supportive liver detoxification therapies, strict abstinence from alcohol",
	"Hypertension": "Ayurvedic herbs for managing blood pressure like Arjuna (Terminalia arjuna), Brahmi (Bacopa monnieri), lifestyle modifications including stress management and dietary changes",
	"Bronchial asthma": "Ayurvedic herbs for respiratory health like Vasa (Adhatoda vasica), Tulsi (Ocimum sanctum), Pippali (Piper longum), Panchakarma therapies like Vamana",
	"Hepatitis D": "Ayurvedic herbs for liver support like Bhumi Amalaki (Phyllanthus niruri), Kutki (Picrorhiza kurroa), supportive liver detoxification therapies, strict abstinence from alcohol",
	"Urinary tract infection": "Ayurvedic herbs with diuretic and antibacterial properties like Gokshura (Tribulus terrestris), Chandan (Santalum album), supportive care including hydration",
	"Psoriasis": "Ayurvedic herbs for skin health like Neem (Azadirachta indica), Turmeric (Curcuma longa), Guduchi (Tinospora cordifolia), Panchakarma therapies like Virechana",
	"Chronic cholestasis": "Ayurvedic herbs for liver support like Bhumi Amalaki (Phyllanthus niruri), Kutki (Picrorhiza kurroa), supportive liver detoxification therapies, strict abstinence from alcohol",
	"Peptic ulcer disease": "Ayurvedic herbs for gastrointestinal health like Licorice (Glycyrrhiza glabra), Haritaki (Terminalia chebula), supportive care including dietary changes and stress management",
	"GERD (Gastroesophageal reflux disease)": "Ayurvedic herbs for digestive health like Trikatu (combination of Ginger, Long pepper, and Black pepper), Yashtimadhu (Glycyrrhiza glabra), dietary changes",
	"Drug reaction": "Ayurvedic herbs for detoxification like Guduchi (Tinospora cordifolia), Amalaki (Emblica officinalis), supportive care including hydration and rest, avoiding the offending drug",
	"Acne": "Ayurvedic herbs for skin health like Neem (Azadirachta indica), Haridra (Curcuma longa), Manjistha (Rubia cordifolia), dietary changes according to Dosha imbalance",
	"Heart attack": "Ayurvedic herbs for heart health like Arjuna (Terminalia arjuna), Punarnava (Boerhavia diffusa), supportive care including lifestyle changes, stress management, and dietary changes",
	"Diabetes": "Ayurvedic herbs for managing blood sugar levels like Gurmar (Gymnema sylvestre), Bitter gourd (Momordica charantia), lifestyle modifications including diet and exercise, stress management",
	"Common Cold": "Ayurvedic herbs to boost immunity and relieve symptoms like Tulsi (Ocimum sanctum), Ginger (Zingiber officinale), Pepper (Piper nigrum), supportive care including rest and hydration",
	"Hepatitis C": "Ayurvedic herbs for liver support like Bhumi Amalaki (Phyllanthus niruri), Kutki (Picrorhiza kurroa), supportive liver detoxification therapies, strict abstinence from alcohol",
	"Tuberculosis": "Ayurvedic herbs for respiratory health like Vasaka (Adhatoda vasica), Kantakari (Solanum xanthocarpum), supportive care including rest, nutrition, and fresh air",
	"Migraine": "Ayurvedic herbs for managing headaches and stress like Brahmi (Bacopa monnieri), Shankhpushpi (Convolvulus pluricaulis), lifestyle modifications including stress management, diet, and sleep hygiene",
	"Jaundice": "Ayurvedic herbs for liver support and detoxification like Bhumi Amalaki (Phyllanthus niruri), Kutki (Picrorhiza kurroa), supportive care including hydration, rest, and dietary changes",
	"Hypoglycemia": "Ayurvedic herbs to balance blood sugar levels like Ashwagandha (Withania somnifera), Shatavari (Asparagus racemosus), supportive care including consumption of natural sugars like honey or fruit juice",
	"Gastroenteritis": "Ayurvedic herbs for gastrointestinal health like Dhanyaka (Coriandrum sativum), Musta (Cyperus rotundus), supportive care including hydration, dietary changes, and rest",
	"Dengue": "Ayurvedic herbs to boost immunity and support recovery like Giloy (Tinospora cordifolia), Papaya leaf extract, supportive care including hydration, rest, and managing symptoms"
}




# Create your views here.

@never_cache
def show_index(request):
	return render(request, "index.html", {})


@never_cache
def logout(request):
	if 'uid' in request.session:
		del request.session['uid']
		del request.session['username']
	return render(request,'index.html')

def register(request):
	username=request.POST.get("username")
	password=request.POST.get("password")
	mobile=request.POST.get("mobile")
	p_address=request.POST.get("p_address")

	print(username,password,mobile,p_address)

	if not verify_adr(p_address):
		return HttpResponse("<script>alert('Public Key does not belong to blockchain');window.location.href='/show_index/';</script>")
	else:

		obj10=Requests.objects.filter(mobile=mobile,username=username,password=password,p_address=p_address)
		co=obj10.count()
		if co==1:
			return HttpResponse("<script>alert('Request is in Pending list');window.location.href='/show_index/'</script>")

		else:
			obj1=Requests(mobile=mobile,username=username,password=password,p_address=p_address)
			obj1.save()
			return HttpResponse("<script>alert('Request sent, Wait For Approval');window.location.href='/show_index/'</script>")




def check_login(request):
	username = request.POST.get("username")
	password = request.POST.get("password")

	if username == 'admin' and password == 'admin':
		request.session["uid"] = "admin"
		request.session["username"]="admin"
		return HttpResponse("<script>alert('Admin Login Successful');window.location.href='/show_home_admin/'</script>")
	else:

		obj2=Patient.objects.filter(username=username,password=password)
		c2=obj2.count()
		if c2==1:
			ob9=Patient.objects.get(username=username,password=password)
			request.session["uid"] = ob9.u_id
			request.session["username"]=ob9.username
			return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_patient/'</script>")
		else:
			return HttpResponse("<script>alert('Invalid');window.location.href='/show_index/'</script>")


@never_cache
###############ADMIN START
def show_home_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		return render(request,'home_admin.html') 
	else:
		return render(request,'index.html')


@never_cache
def display_test_page(request):
	if 'uid' in request.session:
		return render(request,'display_test_page.html') 
	else:
		return render(request,'index.html')

@never_cache
def show_request_admin(request):
	if 'uid' in request.session:
		print(request.session['uid'])
		req_list=Requests.objects.all()
		if not req_list:
			return HttpResponse("<script>alert('No Request Pending');window.location.href='/show_home_admin/'</script>")
		else:
			return render(request,'view_request_admin.html',{'req': req_list}) 
	else:
		return render(request,'index.html')


@never_cache
def show_users_admin(request):
	if 'uid' in request.session:
		print("hai---------------")
		obj=get_patients()
		# req_list=Patient.objects.all()
		return render(request,'show_users_admin.html',{'req': obj}) 
	else:
		return render(request,'index.html')


@never_cache
def show_history_admin(request):
	if 'uid' in request.session:
		obj=get_records()
		# req_list=Record.objects.all()
		# if not req_list:
		# 	return HttpResponse("<script>alert('History Empty');window.location.href='/show_home_admin/'</script>")
		# else:
		return render(request,'show_history_admin.html',{'req': obj}) 
	else:
		return render(request,'index.html')


def approve(request):
	r_id=request.POST.get('r_id')
	username=request.POST.get('username')
	password=request.POST.get('password')
	mobile=request.POST.get('mobile')
	p_address=request.POST.get('p_address')

	obj1=Patient(mobile=mobile,username=username,password=password,p_address=p_address)
	obj1.save()
	obj2=Patient.objects.get(mobile=mobile,username=username,password=password,p_address=p_address)
	user_id=obj2.u_id
	print("User id : ",user_id)
	add_patient1(user_id,username,password,mobile,p_address)

	obj3=Requests.objects.get(r_id=int(r_id))
	obj3.delete()
	return HttpResponse("<script>alert('Approved Successfully');window.location.href='/show_request_admin/'</script>")

def reject(request):
	r_id=request.POST.get('r_id')
	obj1=Requests.objects.get(r_id=int(r_id))
	obj1.delete()
	return HttpResponse("<script>alert('Rejected');window.location.href='/show_request_admin/'</script>")


@never_cache
def show_home_patient(request):
	if 'uid' in request.session:
		username=request.session['username']
		return render(request,'home_patient.html',{'username':username}) 
	else:
		return render(request,'index.html')


def get_pred(data):

	# Split the input data string by commas and convert it into a list of integers
	input_= [int(x) for x in data.split(',')]

	# Convert the list into a NumPy array and reshape it
	processed_data = np.array(input_).reshape(1, 131, 1)

	# Make predictions using the model
	predictions = model_saved.predict(processed_data)

	# Get the predicted class index
	predicted_class_index = np.argmax(predictions)
	class_name = label_encoder.inverse_transform([predicted_class_index])[0]

	print("\n Class Name : ",class_name)

	allopathy_treatment = allopathy_treatments[class_name]
	homeopathy_treatment = homeopathy_treatments[class_name]
	ayurveda_treatment = ayurveda_treatments[class_name]

	return class_name, allopathy_treatment, homeopathy_treatment, ayurveda_treatment


def do_prediction(request):
	data = request.POST.get("inputText")
	print(data)
	username=request.session['username']
	class_name, allopathy_treatment, homeopathy_treatment, ayurveda_treatment = get_pred(data)

	now = datetime.now()
	time = now.strftime("%H:%M:%S")
	print("Current Time =", time)
	print(type(time))

	today = date.today()
	current_date = today.strftime("%d/%m/%Y")
	print("date =",current_date)
	print(type(current_date))

	blk1=Record(username=username,c_date=current_date,c_time=time,result=class_name)
	blk1.save()
	obj2=Record.objects.get(username=username,c_date=current_date,c_time=time,result=class_name)
	record_id=obj2.r_id
	print("record_id id : ",record_id)
	add_record1(record_id,username,current_date,time,class_name)

	return render(request, 'prediction_result.html', {'class_name': class_name,
													  'allopathy_treatment': allopathy_treatment,
													  'homeopathy_treatment': homeopathy_treatment,
													  'ayurveda_treatment': ayurveda_treatment})
