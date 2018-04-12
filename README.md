# Python-2D-Simulation-of-Schrodinger-Equation

Une simulation de l'évolution d'un paquet d'onde gaussien 

## Fonctionnement 

Le programme simule le comportement d'un paquet d'onde gaussien suivant l'équation de Schrödinger. L'algorithme utilisé est la méthode [Alternating direction implicit method](https://en.wikipedia.org/wiki/Alternating_direction_implicit_method). 

## Utilisation 

Pour créer une animation et la stocker dans le ficher *nomDuFichier.mp4*, il faut utiliser la commande suivante : 
```console
python main.py nomDufichier
```
Si l'on veut afficher la densité de probalité et non pas la fonction d'onde complexe, il faut ajouter le flage *--intensity*.
```console
python main.py nomDufichier --intensity
```
