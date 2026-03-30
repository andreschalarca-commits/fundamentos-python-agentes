#Solución Taller Semana 3: Forjando las Herramientas (Refactorización y Blindaje)
##Andrés Felipe Chalarca Rueda.
####Convertir el código en un sistema de herramientas (Tools) tipadas y seguras.

# --- IMPORTACIÓN DE HERRAMIENTAS ---

from datetime import datetime #Le pido a Python que me preste las funciones para manejar fechas y poder usar datetime.now(). El "Reloj".
import sys #Importamos 'sys' para poder cerrar el proceso de forma segura con sys.exit(). El "Interruptor del Sistema".
from typing import List, Dict, Optional #Le pido a Python las "etiquetas de calidad" para avisar qué tipo de datos guardaremos y evitar confusiones.

# --- DEFINCIÓN DEL CONTRATO DE MEMORIA (TYPE ALIASING) ---

#Usamos "Alias" (apodos para los datos) porque en la IA es vital que los datos tengan siempre la misma forma. Usamos PascalCase.
##"Recuerdo" será un solo mensaje.
##"MemoriaAgente" será el cuaderno completo con todos los recuerdos.
Recuerdo = Dict[str, str]
MemoriaAgente = List[Recuerdo]

# --- REFACTORIZACIÓN (CREACIÓN DE TOOLS) "CAJAS DE HERRAMIENTAS" ---

def gestionar_historial(accion: str, memoria: MemoriaAgente, palabra_clave: Optional[str] = None) -> str:
    """
    TOOL A: Esta herramienta se encarga de organizar el historial.
    Es una 'función pura': Procesa la información y la devueñve en texto, sin imprimir nada en la pantalla.
    """
    if accion == "all":
        if not memoria: return "La memoria está vacía."
        #Construirmos un reporte línea por línea.
        resultado = "\n---------- REVISIÓN TOTAL DE MEMORÍA ----------\n"
        for item in memoria:
            resultado += f"[{item['timestamp']}] {item['rol']}: {item['descripcion']}\n"
        return resultado
    
    elif accion == "clear":
        memoria.clear() #Vaciamos la lista por completo.
        return "[Sistema]: memoria reseteada correctamente."
    
    elif accion == "search" and palabra_clave:
        #Buscamos coincidencias usando una lista rápida (list comprehension)
        encontrados = [r for r in memoria if palabra_clave in r["descripcion"].lower() or palabra_clave in r["cmd"].lower()] 
        if not encontrados:
            return f"No encontré registros con la palabra: '{palabra_clave}'."
        
        res = f"\n---------- Resultado para: '{palabra_clave}' ----------\n"
        for r in encontrados:
            res += f" > [{r['timestamp']}] {r['rol']}: {r['descripcion']}\n"
        return res
    
    return "Acción de historial no reconocida."

def contar_letras(texto: str) -> str:
    """
    TOOL B: Cuenta vocales y consonantes de forma automática y ordenada.
    """
    texto_limpio = texto.strip().lower()
    #Usamos filtros rápidos para seprar letras
    vocales = [l for l in texto_limpio if l in "aeiouáéíóú"]
    consonantes = [l for l in texto_limpio if l.isalpha() and l not in "aeiouáéíóú"]

    return (f"Resultados para '{texto_limpio}':\n"
            f"- Vocales: {len(vocales)}\n"
            f"- Consonantes: {len(consonantes)}\n"
            f"- Total caracteres: {len(texto_limpio)}")

def realizar_calculo(n1: float, operacion: str, n2: float) -> str:
    """
    TOOL B: Es la calculadora del agente. Recibe números y devuelve el resultado en texto.
    """
    if operacion == "+": return str(n1 + n2)
    elif operacion == "-": return str(n1 - n2)
    elif operacion == "*": return str(n1 * n2)
    elif operacion == "/":
        if n2 == 0: return "Error: No se puede dividir por cero."
        return str(n1 / n2)
    return "Error: Operador no reconocido."

def obtener_fecha_sistema(rol: str) -> str:
    """
    TOOL B: Consulta la fecha actual. Aplica el 'blindaje' lanzando un error su el usuio no tiene permisos.
    """
    if rol != "admin":
        #El error nace aquí (raise) y viaja hacia el bloque 'except' del bucle principal.
        raise PermissionError("Privilegios insuficientes: Sólo administradores pueden ver la fecha.")
    
    ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"Hoy es: {ahora}"

def validar_seguridad_clave(clave: str, usuario: str) -> str:
    """
    TOOL B: Verifica si una constraseña cumple con las políticas de la empresa.
    """
    if len(clave) < 8:
        return "X Rechazado: La clave debe tener al menos 8 caracteres."
    if clave == usuario:
        return "X Rechazado: La clave no puede ser igual al nombre de usuario."

    return "Exitosa: la clave cumple con las políticas de seguridad."

def ejecutar_ping() -> str:
    """
    TOOL B: Una herramienta simple de diagnótico.
    """
    return "Se envió un ping y el sistema respondió: pong!" 

# --- LÓGICA PRINCIPAL (EL CEREBRO DEL AGENTE) ---

print("---------- Iniciando el pseudoagente estilo consola (blindado) ----------")

historial_chat: MemoriaAgente = [] #Lista vacía que servirá como BD temporal de la sesión.
rol_usuario = ""
usuario_login = "" #Guardaremos aquí el usuario con el que se autenticó
acceso_concedido = False

for i in range(3):
    u = input("Usuario: ").strip().lower() #Eliminamos espacios en blanco y llevamos todo a minúsculas para que el ingreso no falle por ingresos accidentales.
    p = input("Contraseña: ").strip() #Eliminamos espacios en blanco.
    if (u == "admin" and p == "1234") or (u == "invitado" and p == "0000"):
        rol_usuario = "admin" if u == "admin" else "invitado"
        usuario_login = u #Recordamos el usuario.
        acceso_concedido = True
        print(f"---------- Acceso concedido como {rol_usuario.upper()} ---------")
        break #Se rompe el bucle porque ya ingresó.
    print(f"----- [Error] Credenciales incorrectas. Intento {i+1} de 3. ----- ")

if not acceso_concedido:
    print("----- [Alerta] Usuario bloqueado. Cerrando sistema -----")
    sys.exit() #Aquí el programa muere. Nada de lo que esté abajo se ejecutará.

# --- BUCLE DE OPERACIÓN (BLINDADO) ---

while True:
    try:
        entrada = input(f"\n{usuario_login}@PseudoAgente>: ").strip().lower() #Agregamos un salto de línea '\n' y eliminamos espacios en blanco y llevamos todo a minúsculas.
        if not entrada: continue

        partes = entrada.split() #Separar el comando de los posibles argumentos como ('all' o 'clear').
        cmd = partes[0]
        mensaje_log = "" #Variable para redactar el reporte de lo que sucedió en el turno y que irá al historial

        if cmd == "salir":
            print("---- [Sistema] Agente apagado. Vuelva pronto. -----")
            mensaje_log = "Se ha solicitado finalizar la sesión."
            break #Se rompe porque el usuario decidió salir

        elif cmd == "ping":
            mensaje_log = ejecutar_ping()
            print(mensaje_log)
        
        elif cmd == "fecha_hoy":
            #Intentamos usar la herramienta; si falla, el 'except PermissionError' nos captura.
            resultado = obtener_fecha_sistema(rol_usuario)
            print(resultado)
            mensaje_log = resultado

        elif cmd == "contar":
            frase = input("Ingrese una palabra o frase: ")
            mensaje_log = contar_letras(frase)
            print(mensaje_log)

        elif cmd == "validar_pass":
            nueva_p = input("Ingrese su nueva contraseña: ")
            mensaje_log = validar_seguridad_clave(nueva_p, usuario_login)
            print(mensaje_log)

        elif cmd == "calculadora":
            #Capturamos errores de escritura del usuario.
            try:
                n1 = float(input("Digite primer número: "))
                op = input("Digite la operación (+, -, *, /): ")
                n2 = float(input("Digite segundo número: "))
                mensaje_log = f"Resultado: {realizar_calculo(n1, op, n2)}"
                print(mensaje_log)
            except ValueError:
                mensaje_log = "[Error] El usuario no ingresó números válidos."
                print(f"X {mensaje_log}") 

        elif cmd == "historial":
            sub = partes[1] if len(partes) > 1 else "search"
            palabra = input("Palabra a buscar: ").lower() if sub == "search" else None #None = 'vacío' o 'nada'.
            mensaje_log = gestionar_historial(sub, historial_chat, palabra)
            print(mensaje_log)

        else:
            mensaje_log = f"Comando desconocido: {cmd}"
            print(mensaje_log)

        #Registro en memoria.
        historial_chat.append({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": cmd,
            "rol": rol_usuario,
            "descripcion": mensaje_log
        })

    except PermissionError as e:
        print(f" ALERTA DE SEGURIDAD: {e}")
        historial_chat.append({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "cmd": "fecha_hoy",
            "rol": rol_usuario,
            "descripcion": f"FALLO DE SEGURIDAD: {e}"
        })
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")

print("---------- Proceso Finalizado ----------")