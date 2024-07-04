from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar los mensajes

import re #Expresiones regulares --> Empatar con un patrón de texto
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        #data = {diccionario con toda la info del objeto}
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    #Método que crea un nuevo registro
    @classmethod
    def save(cls, form):
        #form = {"first_name": "Elena", "last_name": "De Troya"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL("foro_publicaciones").query_db(query, form) #Regresar el ID del nuevo registro

    #Método que regresa objeto de Usuario en base a e-mail
    @classmethod
    def get_by_email(cls, form):
        #form = {"email": "elena@cd.com", "password": "hola123"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form) #Regresa Lista de Diccionarios

        if len(result) < 1: #Revisa que mi lista esté vacia
            return False
        else:
            #Me regresa 1 registro
            #result = [ {"id:1", "first_name": "Elena", "last_name": "De Troya"...} ]
            user = cls(result[0]) #User({"id": 1, "first_name": "Elena", "last_name": "De Troya"...})
            return user
    
    #Método que valide la info que recibimos del form
    @staticmethod
    def validate_user(form):
        #form = {diccionario con toda la info del formulario}
        is_valid = True

        #Validamos que el nombre tenga al menos 2 caracteres
        if len(form["first_name"]) < 2:
            flash("First name must have at least 2 chars", "register") #(mensaje, categoria)
            is_valid = False

        #Validamos que el apellido tenga al menos 2 caracteres
        if len(form["last_name"]) < 2:
            flash("Last name must have at least 2 chars", "register")
            is_valid = False

        if len(form["password"]) <6:
            flash("Password must have at least 6 chars", "register")
            is_valid = False

        #Validar que el correo sea único
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL("foro_publicaciones").query_db(query, form) # Lista de diccionarios
        if len(result)>= 1:
            #Si existe ese correo en mi BDs
            flash("E-mail already registered", "register")
            is_valid = False

        #Verificamos que las contraseñas coincidan
        if form["password"] != form["confirm"]:
            flash("Password do not match", "register")
            is_valid = False

        if not EMAIL_REGEX.match(form["email"]): #match --> compara una expresió regular con un texto
            flash("E-mail not valid", "register")
            is_valid = False

        return is_valid 
    
    @classmethod
    def get_by_id(cls, data):
        #data = {"id: 1"}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('foro_publicaciones').query_db(query,data) #Lista de 1 diccionario --> indice 0
        user = cls(result[0])
        return user