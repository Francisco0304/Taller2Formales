# Función para validar el correo con AFD
def validar_correo(correo):
    estado = 0  # Empezamos en el estado inicial
    for i, char in enumerate(correo):
        if estado == 0:
            # Estado 0: El correo debe comenzar con una letra minúscula
            if char.islower():
                estado = 1
            else:
                return False, "El correo debe comenzar con una letra minúscula."
        elif estado == 1:
            # Estado 1: El correo puede seguir con letras o números
            if char.islower() or char.isdigit():
                estado = 1  # Sigue en el estado 1
            elif char == '@':
                estado = 2  # Al encontrar el '@', pasamos al estado 2
            else:
                return False, "El nombre del usuario solo puede contener letras minúsculas y números."
        elif estado == 2:
            # Estado 2: Después de '@', debe verificar el dominio
            if correo[i:i+15] == 'uptc.edu.co':
                estado = 3  # Cuando se encuentra 'uptc.edu.co', pasamos al estado final
                break
            else:
                return False, "El correo debe terminar con '@uptc.edu.co'."

    # Verificamos que se haya llegado al estado final (estado 3)
    if estado == 3:
        return True, "Correo válido."
    else:
        return False, "El correo debe terminar con '@uptc.edu.co'."

# Función para ingresar y validar correos electrónicos
def solicitar_correo():
    correo = input("Introduce un correo electrónico para validar: ")

    valido, mensaje = validar_correo(correo)

    if valido:
        print(f"{correo} es válido.")
    else:
        print(f"{correo} es inválido. Razón: {mensaje}")

# Continuamente solicita correos hasta que el usuario decida salir
while True:
    solicitar_correo()
    continuar = input("¿Quieres validar otro correo? (s/n): ")
    if continuar.lower() != 's':
        print("Gracias por usar el validador de correos.")
        break
