class Nodo:
    def __init__(self, pregunta=None, si=None, no=None):
        self.pregunta = pregunta
        self.si = si
        self.no = no

def guardar_arbol(raiz, archivo):
    with open(archivo, 'w') as f:
        f.write("Preorder: " + preorder(raiz) + "\n")
        f.write("Inorder: " + inorder(raiz) + "\n")
        f.write("Postorder: " + postorder(raiz) + "\n")

def preorder(raiz):
    if raiz is None:
        return ''
    return raiz.pregunta + ' ' + preorder(raiz.si) + ' ' + preorder(raiz.no)

def inorder(raiz):
    if raiz is None:
        return ''
    return inorder(raiz.si) + ' ' + raiz.pregunta + ' ' + inorder(raiz.no)

def postorder(raiz):
    if raiz is None:
        return ''
    return postorder(raiz.si) + ' ' + postorder(raiz.no) + ' ' + raiz.pregunta

def cargar_arbol_desde_archivo(archivo):
    with open(archivo, 'r') as f:
        contenido = f.readlines()
        preorder_str = contenido[0].split(' ')[1].strip()
        inorder_str = contenido[1].split(' ')[1].strip()
        postorder_str = contenido[2].split(' ')[1].strip()
    preorder_lista = preorder_str.split(' ')
    inorder_lista = inorder_str.split(' ')
    postorder_lista = postorder_str.split(' ')
    return construir_arbol(preorder_lista, inorder_lista, postorder_lista)

def construir_arbol(preorder, inorder, postorder):
    if not preorder:
        return None
    raiz = Nodo(preorder[0])
    raiz_index = inorder.index(raiz.pregunta)
    raiz.si = construir_arbol(preorder[1:1+raiz_index], inorder[:raiz_index], postorder[:raiz_index])
    raiz.no = construir_arbol(preorder[1+raiz_index:], inorder[raiz_index+1:], postorder[raiz_index:-1])
    return raiz

def jugar_juego(raiz):
    print("¡Bienvenido al juego de adivinanzas!")
    print("Piensa en algo, y yo trataré de adivinarlo.")
    nodo_actual = raiz
    while nodo_actual.si and nodo_actual.no:
        respuesta = input(nodo_actual.pregunta + " (s/n): ").lower()
        while respuesta not in ['s', 'n']:
            respuesta = input("¡Ups! Parece que no entendí, por favor responde 's' para sí o 'n' para no: ").lower()
        if respuesta == 's':
            nodo_actual = nodo_actual.si
        else:
            nodo_actual = nodo_actual.no
    adivinanza = nodo_actual.pregunta
    respuesta = input(f"¿Es {adivinanza} lo que estabas pensando? (s/n): ").lower()
    while respuesta not in ['s', 'n']:
        respuesta = input("¡Vaya! Me he enredado, por favor responde 's' para sí o 'n' para no: ").lower()
    if respuesta == 's':
        print("¡Adiviné! ¡Soy un genio!")
    else:
        objeto = input("¡Oh no! ¿Qué estabas pensando? ")
        pregunta_nueva = input(f"¡Vaya! No lo había adivinado... ¿Qué pregunta distinguiría {objeto} de {adivinanza}? ")
        respuesta_nueva = input(f"¿Cuál es la respuesta para {objeto}? (s/n): ").lower()
        while respuesta_nueva not in ['s', 'n']:
            respuesta_nueva = input("¡Lo siento, no te entendí! Responde 's' para sí o 'n' para no: ").lower()
        if respuesta_nueva == 's':
            nodo_actual.si = Nodo(objeto)
            nodo_actual.no = Nodo(adivinanza)
            print("¡Qué divertido! ¡Aprendí algo nuevo!")
        else:
            nodo_actual.si = Nodo(adivinanza)
            nodo_actual.no = Nodo(objeto)
            print("¡Ahora sí! ¡Seré mejor la próxima vez!")

def agregar_pregunta(raiz):
    print("\n¡Vamos a agregar una nueva pregunta para hacer el juego más emocionante!")
    pregunta = input("¿Qué pregunta distinguiría entre dos objetos o animales? ")
    respuesta = input(f"¿Cuál es la respuesta para {pregunta}? (s/n): ").lower()
    while respuesta not in ['s', 'n']:
        respuesta = input("¡Vaya! Me he enredado, por favor responde 's' para sí o 'n' para no: ").lower()
    if respuesta == 's':
        objeto = input("¿Qué objeto o animal tenías en mente? ")
        pregunta_nueva = input(f"¿Qué pregunta distinguiría {objeto} de {raiz.pregunta}? ")
        raiz.pregunta = pregunta_nueva
        raiz.si = Nodo(pregunta, Nodo(objeto), Nodo(raiz.pregunta))
    else:
        objeto = input("¿Qué objeto o animal tenías en mente? ")
        pregunta_nueva = input(f"¿Qué pregunta distinguiría {raiz.pregunta} de {objeto}? ")
        raiz.pregunta = pregunta_nueva
        raiz.no = Nodo(pregunta, Nodo(raiz.pregunta), Nodo(objeto))
    print("\n¡Perfecto! ¡El juego ahora es aún más emocionante!")

def jugar_de_nuevo(raiz):
    jugar = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
    if jugar == 's':
        jugar_juego(raiz)
        jugar_de_nuevo(raiz)
    elif jugar == 'n':
        print("\n¡Gracias por jugar! ¡Hasta la próxima!")

def main():
    archivo = "arbol.txt"  # Nombre del archivo externo

    opcion = input("¿Quieres cargar un árbol desde un archivo externo? (s/n): ").lower()
    if opcion == 's':
        raiz = cargar_arbol_desde_archivo(archivo)
    else:
        # Construir el árbol de adivinanzas
        raiz = Nodo("¿Es un animal?")
        raiz.si = Nodo("¿Tiene patas?")
        raiz.no = Nodo("¿Es un objeto?")
        raiz.si.si = Nodo("Perro")
        raiz.si.no = Nodo("Gato")
        raiz.no.si = Nodo("Teléfono")
        raiz.no.no = Nodo("Lámpara")

    jugar_juego(raiz)

    opcion = input("\n¿Quieres agregar una nueva pregunta para hacer el juego más divertido? (s/n): ").lower()
    if opcion == 's':
        agregar_pregunta(raiz)

    guardar_arbol(raiz, archivo)

    jugar_de_nuevo(raiz)

if __name__ == "__main__":
    main()
#Iván Ordoñez 1567523

