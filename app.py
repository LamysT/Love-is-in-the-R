import os
import random #pour la création du message
import smtplib #pour l'envoi par email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template,request,redirect,url_for 


sujets = [
    "Ton sourire", "Ton regard", "Ta voix", "Ta présence", "Ta douceur", 
    "Ton rire", "Ton amour", "Chaque mot de toi", "Ton existence", 
    "Chaque instant avec toi", "Ton air mystérieux", "Chaque pensée de toi", 
    "Être avec toi", "Penser à toi", "T'avoir près de moi"
]
verbes = [
    "illumine", "ensoleille", "réchauffe", "adoucit", "apaise", 
    "embellit", "fait vibrer", "calme", "fait fondre", 
    "transforme", "donne un sens à", "apporte de la magie à", 
    "ajoute de la tendresse à", "met des paillettes dans"
]
compléments = [
    "ma journée", "mon petit cœur", "ma vie entière", "mes pensées", 
    "mes rêves", "mon monde", "mon âme", "mes nuits", "ma vie",
    "tout mon être", "mon quotidien", 
    "mon univers"
]
emojis=["✨","💖","💕","💗","🍫","🦋","🎬","🌸","🌷", "🌙 ","⭐","🫶","🧸","☁️"]

def generer_message():
    S=random.choice(sujets)
    V=random.choice(verbes)
    C=random.choice(compléments)
    E=random.choice(emojis)
    return f"{S} {V} {C} {E}"

email_expediteur="a2cbc4001@smtp-brevo.com"
mdp=os.environ.get("MAIL_KEY")

def envoyer_email(destinataire,message_contenu):
    #on préparer l'enveloppe qui contient le message
    msg=MIMEMultipart()
    #comme écrire l'expéditeur,destinataire et objet sur l'enveloppe
    msg['From']="luv.is.in.the.r@hotmail.com"
    msg['To']=destinataire
    msg['Subject']="Un ptit message pour toi...✨"

    #on met le message dedans
    msg.attach(MIMEText(message_contenu,'plain', 'utf-8'))
    #connexion au serveur et envoi
    try:
        with smtplib.SMTP('smtp-relay.brevo.com',587) as serveur:
         serveur.set_debuglevel(1)  # ← active le debug
         serveur.starttls() #securisation de la connexion
         serveur.login(email_expediteur,mdp) #identification
         serveur.send_message(msg) #envoi définitif
        print("Mail envoyé avec succès ✓ ")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi :{e}")   
        return False

app = Flask(__name__)

@app.route('/')
def index():
    # Générer un nouveau message à chaque chargement
    message = generer_message()
    return render_template('index.html', message=message)

@app.route('/envoyer', methods=['POST'])
def envoyer():
    destinataire = request.form.get('email_utilisateur')
    message_a_envoyer = request.form.get('message_a_envoyer')
    
    
    succes = envoyer_email(destinataire, message_a_envoyer)
    
    if succes:
        return "<script>alert('Message envoyé avec amour !💌'); window.location.href='/';</script>"
    else:
        return "<script>alert('Oups, petit souci technique...❌'); window.location.href='/';</script>"


if __name__ == '__main__':
    app.run(debug=True)