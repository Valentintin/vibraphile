from flask import request


def sendFormConnexion(request_ : request):
    mail = request_.form['mail']
    password = request_.form['password']
    print(f"voici le mail : {mail} et le mot de passe : {password}")
