import cv2
import numpy as np
import random


TXT_BITS=8

def convertir_texte(text):
    text_bit = []
    for char in text:
        c = ord(char) #get the unicode
        bins = list(bin(c).replace("0b", "")) #get list of binary bits
        if len(bins) < TXT_BITS: #si la longueur du texte est inf à 8, on rajoute un padding de 00 jusquau caracteres 
            text_bit +=(['0']*(TXT_BITS - len(bins)) + bins)
        else:
            text_bit +=(bins)        
    return text_bit


def decrypt(img_path):

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    if img is None : 
        print("Image Vide")
    else:
        bits = []
        for num in img.reshape(-1): 
            img_bin = list(bin(num).replace("0b", "")) #get the binary form of our number
            bit = img_bin[-1] #on prend le dernier bit 
            bits.append(bit)   
        #extraction de texte
        low, high = 0, TXT_BITS
        string = ''
        length = len(bits)
        while high < length:
            string += chr(int("".join(bits[low:high]), 2))
            low += TXT_BITS
            high += TXT_BITS
    return string


    

def encrypt(text, img_path, new_path):

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2YCrCb)
    img = np.uint16(img) * 255
    h, w , c = img.shape
    if img is None: 
        print("Image Vide")
    if len(text)+1 > h*w : 
        raise ValueError()
    else:
        text_bit = convertir_texte(text)
        img_flat = img.ravel() #passage par adresse pour modifier les bits
        for i, bit in enumerate(text_bit): #on change les bits du poids faible del'img
            img_bin = list(bin(img_flat[i]).replace("0b", "")) #convert our image to binaries
            img_bin[-1] = bit #rajouter notre texte dans le bit du poids faible
            img_flat[i] =  int("".join(img_bin),2) #merge
        img = cv2.cvtColor(img,cv2.COLOR_YCrCb2BGR)
        cv2.imwrite(new_path, img)
    return img


if __name__ == '__main__':
    img = encrypt('Rania','phone.png',"new.png")
    string = decrypt('new.png')
    print(string)

    #img_b, img_g, img_r = np.zeros(img.shape, img.dtype), np.zeros(img.shape, img.dtype), np.zeros(img.shape, img.dtype)
    #img_b[:,:,0] = img[:,:,0]
    #img_g[:,:,1] = img[:,:,1]
    #img_r[:,:,2] = img[:,:,2]
#
    #ret, bw= cv2.threshold(img,127,255, cv2.THRESH_BINARY) 
#
    #cv2.imshow('binary',img)
#
#
    #cv2.waitKey(0)  
    #cv2.destroyAllWindows()






