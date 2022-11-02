import cv2 
import numpy as np
import math

# Transforme le texte en une image 8 bits
def text_to_image(texte, img_shape):
    img_b = np.zeros(img_shape) # création d'une image vide avec la meme taille que l'image encoder
    h , w, _ = img_b.shape

    # Taille approximative d'un caractère dans l'image
    char_height = 25
    char_width = 8.5

    org = (0, 20) # position initial du texte sur l'image

    texte_len = len(texte)
    nb_characters= int( w // char_width) # nombre de caractères sur une ligne

    i=0
    while i < texte_len: # tant qu'on a pas écrit l'integratlité du texte sur l'image
        # Dans le cas ou le texte restant à écricre possède moins de caractère que la limite de cactère
        # par ligne imposé on écrit l'intégralité du texte restant sur cette ligne
        if i + nb_characters >= texte_len:
            cv2.putText(img_b, texte[i:], org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            i += nb_characters #on positione l'indice a la fin de la phrase pour stoper la boucle

        else:
            space = nb_characters
            # Dans le cas ou le caractère finissant la ligne n'est pas un espace on retourne au dernier espace
            # existant afin de ne pas couper de mots lors de l'écriture sur cette ligne
            if texte[i + nb_characters] != " ": 
                while texte[i + space] != " " and space != 0:
                    space -= 1

                cv2.putText(img_b, texte[i: i + space + 1], org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                i += space + 1 # on pose l'indice sur le caractère se trouvant après le dernier espace détecté 

            else : # sinon on écrit directement le texte sur la ligne sans modifications 
                cv2.putText(img_b, texte[i: i + nb_characters], org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                i+=nb_characters # on pose l'indice sur le premier caractère non affiché

        org=(org[0], org[1] + char_height) # on effectue un saut a la ligne

    return img_b


# on encode notre image texte sur une image 16 bits
def encrypt_image(texte, img_path):
    img_a = cv2.imread(img_path, cv2.IMREAD_COLOR) # on récupére l'image qui qui contiendra l'encodage
    if img_a is None: 
        print("Image Vide")
        exit()

    img_b = text_to_image(texte, img_a.shape) # on récupère notre image texte

    # on change le format de l'image vers YCrCb et on la convertie en une image 16 bits
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2YCrCb)
    img_a = np.uint16(img_a) * 256
    h , w, _ = img_a.shape

    # on encode notre image sur le canal de la chrominance pixel par pixel
    # chaque valeur du pixel est multiplié par 16 pour correspondre au format 16 bits
    # un bit est aussi ajouté afin de remedier a la marge d'erreur du au changement de format de l'image
    for y in range(h):
        for x in range(w):
            img_a[y][x][2] += img_b[y][x][2] * 16 + 8

    img_a = cv2.cvtColor(img_a, cv2.COLOR_YCrCb2BGR) # on reconverti l'image au format BGR
    cv2.imwrite("encoded_"+img_path[0:-4]+".png", img_a) # on sauvegarde l'image
    return img_a

# Décrypte et récupére l'image texte de l'image 16 bits
def decrypt_image(img_path):
    img_a = cv2.imread(img_path, -1) # on récupère notre image 16 bits
    if img_a is None: 
        print("Image Vide")
        exit()

    img_b = np.zeros(img_a.shape) # on initialise notre image texte
    h, w , _ = img_a.shape # on récupère les dimensions de notre image
    img_a = cv2.cvtColor(img_a, cv2.COLOR_BGR2YCrCb) # on change le format de l'image vers YCrCb

    # On recupère notre image texte pixel par pixel en les remettant en format 8 bit et en les divisant par 16
    # afin de les retrouver dans le format originel le bit ajouter lors de l'encodage prévient de la marge d'erreur
    for y in range(h):
        for x in range(w):
            img_b[y][x][2] = np.uint8(img_a[y][x][2]) // 16 

    return img_b

teste_texte = "Salut Rania j'espere que cv et que ton pc marche bien j'ai le sentiment que tu vas pas etre tres fan de ma solution meme moi jsp si elle est valide vu que je me suis pas fait chier avec les bits de poid faible et de poid fort je suis juste partie du principe que sa va etre gerer automatiquement mais bon au on a truc fonctionelle meme si faudrait que je vois pourquoi y'a cette couleur rouge on dirait un film d'horreur ou le projet d'archi au choix si tu veux essayer de faire ton propre algo qui respecte mieux ses consignes fait toi plaiz bon crg dit moi si tu veux que je t'aide et tu es la meilleur "

img_b = text_to_image(teste_texte, (480, 640, 3))
img_a = encrypt_image(teste_texte, "phone.png")
d_img_b = decrypt_image("encoded_phone.png")
cv2.imshow("text image", img_b)
cv2.imshow("encoded image", img_a)
cv2.imshow("decoded image", d_img_b)
cv2.waitKey(0)
cv2.destroyAllWindows()