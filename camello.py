
#Juego del Camello.
#Solo debes elegir la opción según tu criterio
#Buenas Suerte

import random

print("Bienvenido al juego del Camello !!!")
print("Has robado un Camello para atravesar el Gran Desierto del Bahara")
print("Los nativos quieren que les devuelvas su Camello y salen en tu persecución !!")
print("Tu misión sobrevivir al desierto y correr más que los nativos")
print()

hecho = False
distancia_recorrida = 0
distancia_nativos = -20
cansancio_camello = 0
tragos = 6
max_cantimplora = 5
sed = 0
oasis = random.randint(0, 20)

while not hecho:
    suerte = random.randint(0, 20)
    if suerte == oasis:
        print("HAS ENCONTRADO UN OASIS...!!!!!")
        print("Ya no tienes sed")
        print("tu camello ha descansado")
        sed = 0
        cansancio_camello = 0

    if distancia_recorrida >= 200:
        print("HAS LLEGADO A TU DESTINO !!!  ENHORABUENA !!!")
        print("------------ FIN EL JUEGO ---------------")
        break

    if sed > 6:
        print("HAS MUERTO DE SED!!!")
        hecho = True
        break

    if cansancio_camello > 8:
        print("TU CAMELLO HA MUERTO !!!")
        hecho = True
        break

    if not hecho and distancia_nativos >= 0:
        print("LOS NATIVOS TE HAN CAPTURADO....")
        print(" ------- FIN DEL JUEGO--------")
        hecho = True
        break

    if not hecho and cansancio_camello > 5:
        print("Tu camello se esta cansando !!!")
        print()

    if not hecho and sed > 4 :
        print("Estas SEDIENTO !!!")
        print()

    print("A. Beber de la cantimplora.")
    print("B. Velocidad moderada hacia adelante.")
    print("C. A toda velocidad hacia adelante.")
    print("D. Parar y Descansar.")
    print("E. Comprueba tu ESTADO.")
    print("Q. Salir.")
    print()

    opcion = input("¿Que opción eliges? : ").upper()
    print()
    if opcion == "Q":
        hecho = True
    elif opcion == "E":
        print(f"Distancia Recorrida: {distancia_recorrida} Km")
        print(f"Veces que puedes beber de la cantimplora: {tragos}, llevas {6 - tragos}")
        print(f"Los Nativos están a {distancia_nativos * (-1)} Km")
        print(f"Cansancio del Camello (0-5): {cansancio_camello}")
        print()
    elif opcion == "D":
        cansancio_camello = 0
        distancia_nativos += random.randint(7, 10)
        print("El Camello parece estar agradecido.")
        print(f"...Pero los nativos están ahora a {(distancia_nativos) * -1} km")
        print()
    elif opcion == "C":
        distancia_recorrida += random.randint(20, 50)
        sed += 1
        cansancio_camello += random.randint(1, 3)
        distancia_nativos += random.randint(3, 5)
        print(f"Has recorrido en total {distancia_recorrida} Km.")
    elif opcion == "B":
        distancia_recorrida += random.randint(15, 20)
        sed += 1
        cansancio_camello += 1
        print(f"Has recorrido en total {distancia_recorrida} Km.")
    elif opcion == "A":
        if tragos <= 0:
            print("NO QUEDA AGUA.....")
        else:
            tragos -= 1
            sed = 0

