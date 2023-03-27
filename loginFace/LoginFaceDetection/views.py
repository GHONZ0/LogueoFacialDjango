from email import message
from fileinput import filename
from multiprocessing import context
import re
from cv2 import *
import cv2
import os
import imutils
from django.shortcuts import render, HttpResponse
from requests import request

from LoginFaceDetection import models
from .forms import FormRegisterForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from werkzeug.utils import secure_filename
from LoginFaceDetection.models import users


# Create your views here.
# ------------- VISTA PARA MOSTRAR EL HTML DEL HOME ---------------
def home(request):
    return render(request, "home.html")

# ------------ VISTA PARA EL MENU DE INICIO DE SESION -------------
# mostrar el view del menu de logueo
def menuLogueo(request):
    return render(request, 'menuLogueo.html')

#tradicional
def loguear(request):
    return render(request, "login.html")

# facial
def loguear_facial(request):
    return render(request, 'login_facial.html')

# ----------- VISTA PARA EL MENU DE REGISTRO ------------
# mostrar el view del menu de registro
def reg_menu(request):
    return render(request, 'register_menu.html')

#----------------------------------------------------------#

# mostrar el view registro tradicional
def registrarse(request):
    return render(request, "register.html")

# proceso de registro de sesión
def proceso_register(request):
    form = FormRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()		
        messages.success(request, 'Te has registrado correctamente.')
        form = FormRegisterForm()
    else:
        messages.error(request, 'No se ha podido registrar su cuenta.')
    context = {'form': form }  
    return render(request, "register.html", context)

#-----------------------------------------------------------------------------------#

# mostrar el view registro facial
def register_facial(request):
    return render(request, 'register_facial.html')

# proceso de registro facial
def cap_face(request):
    if request.method == "POST":
        
        username = request.POST.get("usuario", None)
        password = request.POST.get("password", None)

        #capturando el rostro
        cap = cv2.VideoCapture(0)

        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        count = 0

        while True:
            
            ret, frame = cap.read()
            if ret == False: break
            frame =  imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()

            faces = faceClassif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(username+'.jpg'.format(count),rostro)
                count = count + 1
            cv2.imshow('frame',frame)

            k =  cv2.waitKey(1)
            if k == 27 or count >= 1:
                break

        cap.release()
        cv2.destroyAllWindows()

        upload = users(usuario=username, password=password)
        upload.save() 
            
        messages.success(request, 'Te has registrado correctamente.')
    return render(request, 'register_facial.html')
    #message.success(request, 'Foto tomada')

# ---------------- PROCESO DE INCIO DE SESION --------------

# inicio de sesión tradicional
@csrf_exempt
def procesar_sesion(request):

    if request.method == "POST":

        user = request.POST["user_name"]
        password = request.POST["user_password"]
        fn_user = secure_filename(user)
        fn_pass = secure_filename(password)

        usuario = users.objects.filter(usuario=fn_user, password=fn_pass)

        if usuario:
            
            contexto = {'usuario':usuario}
            return render(request, 'portal.html', contexto)
        else:
            
            messages.error(request, 'Algo falló, intenta de nuevo.')
            return render(request, 'login.html')

# inicio de sesión facial
@csrf_exempt
def facial_log(request):
    if request.method == "POST":
        
        username = request.POST.get("user_name", None)

        #capturando el rostro
        cap = cv2.VideoCapture(0)

        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        count = 0

        while True:
            
            ret, frame = cap.read()
            if ret == False: break
            frame =  imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()

            faces = faceClassif.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                rostro = auxFrame[y:y+h,x:x+w]
                rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(username+"LOG.jpg".format(count),rostro)
                count = count + 1
            cv2.imshow('frame',frame)

            k =  cv2.waitKey(1)
            if k == 27 or count >= 1:
                break

        cap.release()
        cv2.destroyAllWindows()
# función para la comparación de imágenes
    def orb_sim(image_1, image_2):
        #creamos el objeto de comparación
        orb = cv2.ORB_create()
        #creamos los descriptores y extraemos los puntos claves
        kpA, dA = orb.detectAndCompute(image_1, None)
        kpB, dB = orb.detectAndCompute(image_2, None)

        #creación del comparador de fuerza
        cF = cv2.BFMatcher (cv2.NORM_HAMMING, crossCheck = True)

        #aplicamos el comparador a los descriptores 
        matches = cF.match(dA, dB)

        #Extraemos las regiones similares en base a los puntos claves
        similar_regions = [i for i in matches if i.distance < 70]
        if len(matches) == 0:
            return 0
        #retornamos el porcentaje
        return len(similar_regions)/len(matches)

    # mandamos la imagenes y llamamos la función de comparación
    #importar la lista de archivos con la libreria os
    im_archivos = os.listdir()
    if username+".jpg" in im_archivos:
        face_reg = cv2.imread(username+".jpg", 0)
        face_log = cv2.imread(username+"LOG.jpg", 0)
        sem = orb_sim(face_reg, face_log)
        if sem >= 0.98:
            return render(request, 'portal.html')
        else:
            messages.error(request, 'Intente nuevamente o inicie sesion tradicional.')
            return render(request, 'login_facial.html')
    else:
        messages.error(request, 'Usuario inexistente/Sin registro facial.')
        return render(request, 'login_facial.html')

#------------------------------ FIN -----------------------------------#
