# "Contrôle Dimensionnel"
# Cours : Traitement des signaux et données - EPHEC
# Professeurs : Arnaud DEWULF, Stéphanie GUÉRIT
# Étudiants : Dylan FÉRON, Noé LIBON, Mounir JEBBARI, Amaury GROTARD
# Année académique : 2023 - 2024

import cv2
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


def charger_image():
    chemin_image = filedialog.askopenfilename(title="Sélectionner une image", initialdir="images", filetypes=[("Fichiers PNG", "*.png"), ("Fichiers JPG", "*.jpg")])
    return cv2.imread(chemin_image)

def afficher_image(ax, image, title):
    ax.clear()
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax.set_title(title)
    ax.axis('off')
    canvas.draw()

def comparer_images():
    global image_reference, image_compare

    # Convertir les images en niveaux de gris
    image_gris_ref = cv2.cvtColor(image_reference, cv2.COLOR_BGR2GRAY)
    image_gris_cmp = cv2.cvtColor(image_compare, cv2.COLOR_BGR2GRAY)


    # Détection des contours avec l'algorithme de Canny
    seuil_bas = 50
    seuil_haut = 150

    edges_ref = cv2.Canny(image_gris_ref, seuil_bas, seuil_haut)
    edges_cmp = cv2.Canny(image_gris_cmp, seuil_bas, seuil_haut)

    # Trouver les contours dans l'image
    contours_ref, _ = cv2.findContours(edges_ref, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_cmp, _ = cv2.findContours(edges_cmp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sélectionner le contour avec la plus grande aire (supposant que c'est la plaque)
    contour_plaque_ref = max(contours_ref, key=cv2.contourArea)
    contour_plaque_cmp = max(contours_cmp, key=cv2.contourArea)

    # Calculer le périmètre du contour de la plaque
    perimetre_plaque_ref = cv2.arcLength(contour_plaque_ref, True)
    perimetre_plaque_cmp = cv2.arcLength(contour_plaque_cmp, True)

    # Echelle : périmètre feuille A4 = 101.4 cm ou 6950 pixels sur l'image
    perimetre_en_cm_ref = round(perimetre_plaque_ref / 68.5, 1)
    perimetre_en_cm_cmp = round(perimetre_plaque_cmp / 68.5, 1)

    # Comparer les tailles des deux plaques
    if abs(perimetre_en_cm_ref - perimetre_en_cm_cmp) <= 0.2:
        comparaison = "Les deux plaques sont de taille égale."
    elif perimetre_en_cm_ref > perimetre_en_cm_cmp:
        comparaison = "La première plaque est plus grande que la deuxième."
    elif perimetre_en_cm_ref < perimetre_en_cm_cmp:
        comparaison = "La deuxième plaque est plus grande que la première."


    # Trouver les contours internes
    contours_internes_ref, _ = cv2.findContours(edges_ref.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_internes_cmp, _ = cv2.findContours(edges_cmp.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    image_reference = cv2.drawContours(image_reference, contours_internes_ref, -1, (0, 255, 0), 2)
    image_compare = cv2.drawContours(image_compare, contours_internes_cmp, -1, (0, 255, 0), 2)

    # Filtrer les contours internes en fonction de l'aire et de la forme
    aire_plaque_ref = cv2.contourArea(contour_plaque_ref)
    aire_plaque_cmp = cv2.contourArea(contour_plaque_cmp)


    # Trouver les trous
    for contour_interne_ref in contours_internes_ref:
        aire_contour_interne_ref = cv2.contourArea(contour_interne_ref)
        if 0.001 * aire_plaque_ref < aire_contour_interne_ref < 0.5 * aire_plaque_ref:
            if cv2.pointPolygonTest(contour_plaque_ref, (int(contour_interne_ref[0][0][0]), int(contour_interne_ref[0][0][1])), False) == 1.0:
                trou1 = "Trou détecté!"
                break
            else:
                trou1 = "Pas de trou détecté!"
        else:
            trou1 = "Pas de trou détecté!"

    for contour_interne_cmp in contours_internes_cmp:
        aire_contour_interne_cmp = cv2.contourArea(contour_interne_cmp)
        if 0.001 * aire_plaque_cmp < aire_contour_interne_cmp < 0.5 * aire_plaque_cmp:
            if cv2.pointPolygonTest(contour_plaque_cmp, (int(contour_interne_cmp[0][0][0]), int(contour_interne_cmp[0][0][1])), False) == 1.0:
                trou2 = "Trou détecté!"
                break
            else:
                trou2 = "Pas de trou détecté!"
        else:
            trou2 = "Pas de trou détecté!"
        

    # Afficher les résultats
    afficher_image(ax1, image_reference, f'Plaque de référence\nPérimètre : {perimetre_en_cm_ref} cm \n{trou1}')
    afficher_image(ax2, image_compare, f'Plaque à comparer\nPérimètre : {perimetre_en_cm_cmp} cm \n{trou2}')
    label_resultat.config(text=comparaison)

def selectionner_image_reference():
    global image_reference
    image_reference = charger_image()
    afficher_image(ax1, image_reference, 'Plaque de référence')

def selectionner_image_compare():
    global image_compare
    image_compare = charger_image()
    afficher_image(ax2, image_compare, 'Plaque à comparer')

# Initialiser l'interface graphique
root = tk.Tk()
root.title("Comparateur de Plaques")

# Variables globales pour stocker les images
image_reference = None
image_compare = None

# Boutons pour charger les images
btn_reference = tk.Button(root, text="Sélectionner la plaque de référence", command=selectionner_image_reference)
btn_reference.pack(pady=10)

btn_compare = tk.Button(root, text="Sélectionner la plaque à comparer", command=selectionner_image_compare)
btn_compare.pack(pady=10)

btn_comparer = tk.Button(root, text="Comparer les plaques", command=comparer_images)
btn_comparer.pack(pady=10)

# Figures pour afficher les images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))

# Zone de texte pour afficher le résultat de la comparaison
label_resultat = tk.Label(root, text="", font=("Helvetica", 12))
label_resultat.pack(pady=10)

# Intégration des figures Matplotlib dans Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Démarrer l'interface graphique
root.mainloop()
