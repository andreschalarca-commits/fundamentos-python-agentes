#Solución Taller Semana 1: El Núcleo del Agente y Control de Acceso
##Andrés Felipe Chalarca Rueda

#Le pido a Python que me preste las funciones para manejar fechas y poder usar datetime.now()

from datetime import datetime

#Fase 1: Login con roles
intentos = 0
acceso_concedido = False
rol_usuario = ""
usuario_login = "" #Guardaremos aquí el usuario con el que se autenticó

#Usamos un bucle para dar los 3 intentos antes de bloquear al usuario.
#Recorremos del 1 al 3 con un bucle. Cada vuelta es un intento de login.
#Pedimos usuario y contraseña en cada intento.
while intentos < 3:
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    
    if usuario == "admin" and contraseña == "1234":
        print("----- Bienvenido Administrador. -----")
        rol_usuario = "admin"
        usuario_login = usuario #Recordamos el usuario
        acceso_concedido = True
        break #Se rompe el bucle porque ya ingresó
    elif usuario == "invitado" and contraseña == "0000":
        print("----- Bienvenido Invitado. -----")
        rol_usuario = "invitado"
        usuario_login = usuario #Recordamos el usuario
        acceso_concedido = True
        break #Se rompe el bucle porque ya ingresó
    else:
        intentos += 1
        print(f"----- Error. Intento {intentos} de 3. ----- ") #Usamos f-string porque no será un texto estático, será dinámico.
        
#Si se cumplen los 3 intentos, cerramos el programa
if not acceso_concedido:
    print("----- [Alerta] Usuario bloqueado. Cerrando sistema -----")
    exit() #Detenemos todo el programa
    
#Fase 2 y 3: El Agente
while acceso_concedido:
    cmd = input("Agente>: ").lower() #Llevamos todo a minúsculas
    
    if cmd == "salir":
        print("---- Agente apagado. Vuelva pronto. -----")
        break #Se rompe porque el usuario decidió salir
    
    elif cmd == "ping":
        print("pong!")
        
    elif cmd == "contar":
        palabra = input("Ingrese una palabra o frase: ").lower() #Llevamos todo a minúsculas
        tot_letras = len(palabra) #Usamos len() para contar los caracteres (el 'largo' del texto)
        tot_vocales = 0
        tot_cons = 0
        
        for p in palabra:
            if p in "aeiouáéíóú":
                tot_vocales += 1
            else:
                tot_cons += 1
        print(f"Palabra ingresada: {palabra}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de letras ingresada: {tot_letras}")
            
    elif cmd == "fecha_hoy":
        if rol_usuario == "admin":
            print(f"Hoy es: {datetime.now()}") #Usamos f-string porque no será un texto estático, será dinámico.
        else:
            print("----- [Acceso Denegado] Requiere privilegios de Administrador. -----")
    
    elif cmd == "validar_pass":
        nueva_clave = input("Ingrese su nueva contraseña: ")
        
        #Aplicamos reglas de negocio con lógica booleana
        #Usamos len() para contar los caracteres (el 'largo' del texto)
        if len(nueva_clave) < 8:
            print("----- Rechazado: La clave debe tener al menos 8 caracteres. -----")
        elif nueva_clave == usuario_login: #'usuario_login' es la variable que guardamos en el login
            print("----- Rechazado: La clave no puede ser igual a tu nombre de usuario. -----")
        else:
            print("----- Éxitoso: La nueva clave cumple con las políticas de seuridad. -----")      
    
    elif cmd == "calculadora":
        #Por defecto, todo lo que entra por el teclado (input) es tratado como texto (str).
        #Usaremos float() porque si el usuario ingresa decimales (10.5) y usamos int(), el programa va a fallar. En este caso float() nos permite decimales y cálculos reales.
        número1 = float(input("Digite primer número: "))
        operación = input("Digite la operación (+, -, *, /): ")
        número2 = float(input("Digite segundo número: "))
        
        #Usamos f-string porque no será un texto estático, será dinámico. 
        if operación == "+": print(f"Resultado: {número1 + número2}")
        elif operación == "-": print(f"Resultado: {número1 - número2}")
        elif operación == "*": print(f"Resultado: {número1 * número2}")
        elif operación == "/":
            if número2 != 0: #Validación para no dividir por cero
                print(f"Resultado: {número1 / número2}")
            else:
                print("----- Error: No se puede dividir por cero. -----")
        else:
            print("----- Error: Operador no reconocido. Use +, -, *, /. -----")
    
    else:
        print("------ Comando desconocido. Intente de nuevo -----")
