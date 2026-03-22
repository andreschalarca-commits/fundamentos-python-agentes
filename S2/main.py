#Solución Taller Semana 2: Motor de Búsqueda del Agente.
##Andrés Felipe Chalarca Rueda.
###Implementación de memoria (listas/diccionarios) y motor de búsqueda.


from datetime import datetime #Le pido a Python que me preste las funciones para manejar fechas y poder usar datetime.now().
import sys #Importamos 'sys' para poder cerrar el proceso de forma segura con sys.exit().
print("---------- Iniciando el pseudoagente estilo consola ----------") #Mejora visual tomada de la solución de Mishelle.

#Iventario de memoria (taller 2).
historial_chat = [] #Creamos lista vacía que servirá como BD temporal de la sesión.

#Fase 1: Login con roles (taller 1).
intentos = 0
acceso_concedido = False
rol_usuario = ""
usuario_login = "" #Guardaremos aquí el usuario con el que se autenticó

#Usamos un bucle para dar los 3 intentos antes de bloquear al usuario.
#Recorremos del 1 al 3 con un bucle. Cada vuelta es un intento de login.
#Pedimos usuario y contraseña en cada intento.
while intentos < 3:
    usuario = input("Usuario: ").strip().lower() #Eliminamos espacios en blanco y llevamos todo a minúsculas para que el ingreso no falle por ingresos accidentales.
    contraseña = input("Contraseña: ").strip() #Eliminamos espacios en blanco.
    
    if usuario == "admin" and contraseña == "1234":
        print("----- [Sistema] Acceso concedido >>> Bienvenido Administrador. -----")
        rol_usuario = "admin"
        usuario_login = usuario #Recordamos el usuario.
        acceso_concedido = True
        break #Se rompe el bucle porque ya ingresó.
    elif usuario == "invitado" and contraseña == "0000":
        print("----- [Sistema] Acceso concedido >>> Bienvenido Invitado. -----")
        rol_usuario = "invitado"
        usuario_login = usuario #Recordamos el usuario.
        acceso_concedido = True
        break #Se rompe el bucle porque ya ingresó.
    else:
        intentos += 1
        print(f"----- [Error] Credenciales incorrectas. {intentos} de 3. ----- ") #Usamos f-string porque no será un texto estático, será dinámico.
        
#Si se cumplen los 3 intentos, cerramos el programa con sys.exit() para matar el proceso inmediatamente.
if not acceso_concedido:
    print("----- [Alerta] Usuario bloqueado. Cerrando sistema -----")
    sys.exit() #Aquí el programa muere. Nada de lo que esté abajo se ejecutará.
    
#Fase del agente activo: El Agente con motor de búsqueda (taller 1 y 2).
while acceso_concedido:
    #Capturamos la entrada completa en la variable 'entrada_usuario' para procesarla antes de decidir qué comando ejecutar. 
    entrada_usuario = input(f"\n{usuario_login}@PseudoAgente>: ").strip().lower() #Agregamos un salto de línea '\n' y eliminamos espacios en blanco y llevamos todo a minúsculas.

    #Usamos .split() para separar el comando de los posibles argumentos como ('all' o 'clear').
    #Esto divide "historial all" en una lista: ["historial", "all"].
    partes = entrada_usuario.split()

    #Verificamos si el usuario escribió algo para evitar que el programa "crashee" (se cierre con error).
    cmd = partes[0] if len(partes) > 0 else "" #str vacío = texto vacío.
    #El 'sub_cmd' sería la segunda palabra (ej: 'all'), si no existe, lo dejamos como None.
    sub_cmd = partes[1] if len(partes) > 1 else None #None = 'vacío' o 'nada'.

    #Creamos una variable para redactar el reporte de lo que sucedió en el turno y que irá al historial.
    mensaje_log = ""

    if cmd == "salir":
        print("---- [Sistema] Agente apagado. Vuelva pronto. -----")
        mensaje_log = "Se ha solicitado finalizar la sesión."
        break #Se rompe porque el usuario decidió salir
    
    elif cmd == "ping":
        print("pong!")
        mensaje_log = "Se ha enviado un ping y de respuesta se devolvió un pong."
        
    elif cmd == "contar":
        palabra = input("Ingrese una palabra o frase: ").strip().lower() #Eliminamos espacios en blanco y llevamos todo a minúsculas
        tot_letras = len(palabra) #Usamos len() para contar los caracteres (el 'largo' del texto)
        tot_vocales = 0
        tot_cons = 0
        
        #Recorremos letra por letra (p) dentro de la palabra.
        for p in palabra:
            if p in "aeiouáéíóú":
                tot_vocales += 1
            #Usamos .isalpha() para contar solo letras reales, ignorando números o símbolos >>> Mejora aplicada.
            elif p.isalpha():
                tot_cons += 1
        print(f"Palabra ingresada: {palabra}")
        print(f"Total de vocales: {tot_vocales}")
        print(f"Total de consonantes: {tot_cons}")
        print(f"Total de caracteres ingresados: {tot_letras}")
        mensaje_log = f"""Se ha solicitado el conteo de la palabra o frase {palabra}, dando como resultado:
        Vocales: {tot_vocales}
        Consonantes: {tot_cons}
        Total: {tot_letras}"""
            
    elif cmd == "fecha_hoy":
        #Validamos que el usuario sea 'admin': Solo el administrador puede ver la fecha del sistema.
        if rol_usuario == "admin":
            ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Nueva variable para mejorar el formato con .strftime().
            print(f"Hoy es: {ahora}") #Usamos f-string porque no será un texto estático, será dinámico.
            mensaje_log = f"Se ha consultado la fecha/hora: {ahora}." 
        else:
            print("----- [Acceso Denegado] Requiere privilegios de Administrador. -----")
            mensaje_log = "[Acceso Denegado] Usuario sin privilegios intentó ver la fecha."
    
    elif cmd == "validar_pass":
        nueva_clave = input("Ingrese su nueva contraseña: ")
        
        #Aplicamos reglas de negocio con lógica booleana
        #Usamos len() para contar los caracteres (el 'largo' del texto)
        if len(nueva_clave) < 8:
            print("----- [Sistema] Rechazado: La clave debe tener al menos 8 caracteres. -----")
            mensaje_log = "[Rechazado] Usuario ingresó una clave con menos de 8 caracteres."
        elif nueva_clave == usuario_login: #'usuario_login' es la variable que guardamos en el login
            print("----- [Sistema] Rechazado: La clave no puede ser igual a tu nombre de usuario. -----")
            mensaje_log = "[Rechazado] Usuario ingresó el nombre de usuario como clave."
        else:
            print("----- [Sistema] Éxitoso: La nueva clave cumple con las políticas de seguridad. -----")
            mensaje_log = "[Exitoso] Usuario ingresó nueva clave con políticas correctas."      
    
    elif cmd == "calculadora":
        #Por defecto, todo lo que entra por el teclado (input) es tratado como texto (str).
        #Usaremos float() porque si el usuario ingresa decimales (10.5) y usamos int(), el programa va a fallar. En este caso float() nos permite decimales y cálculos reales.
        #Quité las tíldes de las variables para evitar errores
        #Usamos una mejora respecto a la entrega anterior con 'try', 'continue' y 'except' (plan de contigencia 'ValueError'). Por si el usuario escribe letras dónde deberían ir números.
        try:
            numero1 = float(input("Digite primer número: "))
            operacion = input("Digite la operación (+, -, *, /): ").strip() #Eliminamos espacios en blanco
            numero2 = float(input("Digite segundo número: ")) 
            resultado = ""

            if operacion == "+": resultado = numero1 + numero2
            elif operacion == "-": resultado = numero1 - numero2
            elif operacion == "*": resultado = numero1 * numero2
            elif operacion == "/":
                #Validación para no dividir por cero
                if numero2 != 0: resultado = numero1 / numero2
                else: 
                    print("----- Error: No se puede dividir por cero. -----")
                    mensaje_log = "[Error] Se ha solicitado dividir por cero."
                    continue
            else:
                print("----- Error: Operador no reconocido. Use +, -, *, /. -----")
                mensaje_log = "[Error] De entrada de operación no valida."
                continue        
                    
            print(f"Resultado: {resultado}") #Usamos f-string porque no será un texto estático, será dinámico. 
            mensaje_log = f"Cálculo: {numero1} {operacion} {numero2} = {resultado}"
            
        except ValueError:
            print("----- Error: Ingrese sólo valores numéricos. -----")
            mensaje_log = "[Error] De entrada numérica."
            
    elif cmd == "historial":
        #Caso 1: Mostrar todo el inventario de memoria.
        if sub_cmd == "all":
            print("\n---------- REVISIÓN TOTAL DE MEMORIA ----------") #Agregamos un salto de línea '\n'
            for item in historial_chat:
                print(f"[{item['timestamp']}] {item['rol']}: {item['descripcion']}.")
            
            mensaje_log = "Se visualizó el historial completo"
        
        #Caso2: Vaciar el inventario (borrar lista).
        elif sub_cmd == "clear":
            historial_chat.clear() #Eliminamos todo
            print("----- [Sistema]: Memoria reseteada correctamente. -----")
            mensaje_log = "Se vació el historial del chat."
        
        #Caso 3: Motor de búsqueda (cuando no se usa 'all' ni 'clear').
        else:
            key = input("Ingrese la palabra clave a buscar: ").strip().lower() #Eliminamos espacios en blanco y llevamos a minúsculas.
            encontrados = 0
            print(f"\n---------- Resultados para la búsqueda: '{key}'. ----------") #Agregamos un salto de línea '\n'

            #Para saber si la palabra está 'dentro' del mensaje, usamos el operador 'in', que busca sub-cadenas en Python.
            #Resolvimos las variantes (all/clear) con .split() para separar el comando del argumento.
            for recuerdo in historial_chat:
                #Comparamos todo en minúsculas (.lower()) para el reto eutagógico.
                if key in recuerdo["descripcion"].lower():
                    print(f" > [{recuerdo['timestamp']}] {recuerdo['rol']}: {recuerdo['descripcion']}.")
                    encontrados += 1

            if encontrados == 0:
                print("PseudoAgente>: No encontré registros con esa palabra.")
            
            mensaje_log = f"Búsqueda de '{key}' en memoria. Concidencias: {encontrados}."

    else:
        print("------ Comando desconocido. Intente de nuevo -----")
        mensaje_log = f"Intento de comando inexsistente: {cmd}"
    
    #Paso final del proceso: Registro en log.
    #Creamos un diccionario con la "foto" de lo que acaba de pasar.
    log_actual = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "cmd": cmd,
        "rol": rol_usuario,
        "descripcion": mensaje_log
    }
    #Guardamos este diccionario en nuestra lista de historial (memoria).
    historial_chat.append(log_actual)

