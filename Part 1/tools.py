import cv2
import numpy as np
from PIL import Image
import re


def int_to_bin(bgr):
    b, g, r = bgr

    return f'{b:08b}', f'{g:08b}', f'{r:08b}'
            
def int_to_bin2(ycrcb):
    y, cr, cb = ycrcb
    return f'{y:016b}', f'{cr:016b}', f'{cb:016b}'

def bin_to_int(bgr):
    b, g, r = bgr
    return (int(b, 2),
            int(g, 2),
            int(r, 2))

def bin_to_int2(bgr):
    return (int(bgr, 2))

def merge_bgr(ycrcb, bgr):
    y, cr, cb = ycrcb
    b, g, r = bgr

    bgr = (y[0:8] + b[0:],
            cr[0:8] + g[0:],
            cb[0:8] + r[0:],
        )
    return bgr


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

        cv2.imwrite(f'res1/{texte}.png',img_b)

    return img_b

def encrypt(text, img_path):
    #convertir l'image principale et transformer son espace de couleurs
    img1 = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img1 = np.uint16(img1)*255
    img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2YCrCb)
    #cv2.imwrite('ycbcr.png',img1)
    if img1 is None: 
        print("image empty")
    else:
        text_to_image(text, img1.shape)
        img2 = cv2.imread(f'res1/{text}.png',cv2.IMREAD_COLOR)
        # Create a new image 
        new_image = img1
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                ycrcb = int_to_bin2(img1[i, j])
                bgr_text = int_to_bin(img2[i, j])
                # Merge the two pixels and convert it to a integer tupleshape
                bgr = merge_bgr(ycrcb, bgr_text)
                #for it in bgr:
                #    if not (re.fullmatch('[0]+', it[8:])):
                #        print(new_image[i, j])
                new_image[i, j] = bin_to_int(bgr) 

        new_image = cv2.cvtColor(new_image,cv2.COLOR_YCrCb2BGR)
        cv2.imwrite('res1/Final.png',new_image)

    return new_image


def decrypt(new_img_path):
    img = cv2.imread(new_img_path, -1)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    # Create the new image and load the pixel map
    new_image = np.zeros((img.shape[0],img.shape[1]), np.uint8)


    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            y, cr, cb = int_to_bin2(img[i, j])
            # Extract the last 8 bits (corresponding to the hidden image)
            ycrcb = (y[8:])
            if (re.fullmatch('[1]+', ycrcb)):
                new_image[i, j] = 0
            else:
            # Convert it to an integer tuple
                new_image[i, j] = bin_to_int2(ycrcb)

    cv2.imwrite('res1/Unmerged-Image.png',new_image)
    return new_image



if __name__ == '__main__':

    encrypt('Ran', 'res1/th.jpg')
    decrypt('res1/Final.png')






