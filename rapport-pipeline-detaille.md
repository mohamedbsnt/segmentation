# Algorithme génétique et apprentissage profond pour l’amélioration de la localisation des sphéroïdes cellulaires in vitro

## Résumé
Projet de Master : "Algorithme génétique et apprentissage profond pour l’amélioration de la localisation des sphéroïdes cellulaires in vitro" — Université Mohammed V de Rabat, 2024.

Objectif : Développer un pipeline automatisé basé sur Deep Learning (Mask R-CNN, U-Net++) couplé à une stratégie d’optimisation évolutionnaire (SE) pour la segmentation, la classification et la localisation des sphéroïdes cellulaires à partir d’images de culture 3D.


## Pipeline Global et Architecture

Le pipeline est fondé sur l’**hybridation Deep Learning + Optimisation évolutionnaire** :

### 1. Préparation et annotation des données
- Dataset Figshare (264 images microscopiques MCF10A, 768x768 px)
- 3 classes (monocouche, agrégation, sphéroïde) avec masques segmentés, format COCO
- Split : train (70%), val (15%), test (15%)
- Augmentations : flips, rotations, affinités, bruit, transformation luminance (Lab)

### 2. Apprentissage profond
#### Mask R-CNN
- Modèle de segmentation d’instances
- Backbone ResNet50 + FPN
- Entraîné sur RGB puis sur canal luminance LAB (pseudo-RGB)

#### U-Net++
- Double architecture : un modèle multiclasse (monocouche + agrégation, softmax) ; un binaire (sphéroïde, sigmoid)
- Backbone RegNetY-120 pré-entraîné
- Supervision profonde, fusion par priorité des masques prédits

### 3. Génération de grilles synthétiques
- Création virtuelle de plaques 20×20 pour évaluer robustesse du pipeline

### 4. Prédiction et Post-traitement
- Application des modèles sur grilles synthétiques et images test
- Post-traitement par stratégie évolutionnaire (SE)
  - Extraction de la grille par détection de lignes (Canny, Hough)
  - Optimisation adaptative des paramètres (rotation, échelle, translation)
  - Fonction de fitness : minimisation de l’erreur (Score Fβ)
- Filtrage : sélection du meilleur masque par cellule (pondération centricité/aire)

### 5. Évaluation
- Précision, rappel, F1-Score, métriques Dice, IoU, score Fβ sur chaque classe


## Résultats Finaux

### 1. Résultats principaux (ensemble Test)
| Architecture      | Dice Score | IoU/Jaccard | Remarque                                   |
|------------------|-----------|-------------|---------------------------------------------|
| Mask R-CNN (RGB) |   0.8405  |   0.7909    | Baseline, meilleure performance globale     |
| Mask R-CNN (LAB) |   0.8237  |   0.7787    | Luminance, robuste pour sphéroïdes         |
| U-Net++ (RGB)    |   0.8050  |   0.7759    | Architecture double, supervision profonde   |
| U-Net++ (LAB)    |   0.8064  |   0.7769    | Légère amélioration sur objets compacts     |


### 2. Performances par classe (post-filtrage SE)
| Classe      | Précision (avant) | Précision (après) | Rappel | F1-Score (avant) | F1-Score (après) | Gain F1 |
|-------------|------------------|-------------------|--------|------------------|------------------|---------|
| Monocouche | 0.620            | 0.743             | 0.368  | 0.461            | 0.492            | +0.031  |
| Agrégation | 0.609            | 0.682             | 0.854  | 0.711            | 0.758            | +0.047  |
| Sphéroïde   | 0.788            | 0.827             | 0.530  | 0.634            | 0.644            | +0.010  |

> Le filtrage SE améliore systématiquement la précision, réduit les faux positifs et renforce la robustesse des segmentations pour toute structure.

### 3. Hyperparamètres SE (Optimisation post-traitement)
| Paramètre             | Valeur optimale | Description                                             |
|----------------------|-----------------|---------------------------------------------------------|
| Population (μ, λ)    | (40, 60)        | Meilleur compromis exploration/exploitation             |
| Sigma initial        | 0.1             | Force de mutation adaptative - Équilibre optimal         |
| Nombre d’itérations  | 160             | Convergence robuste (~25-30 générations atteignent un plateau) |
| Score Fβ final       | 0.917           | Score exceptionnel sur grilles synthétiques              |


## Visualisations clé :
<img width="526" height="509" alt="visualisation " src="https://github.com/user-attachments/assets/7d09143c-40c5-432e-bae9-00953f9bdef4" />

- **Architecture globale** du pipeline et interactions entre modules
- **Qualité des segmentations** :
  - [Masque prédit Mask R-CNN sur image de sphéroïde][11]
  - [Détection de grille optimisée par SE et superposition sur ground truth][13]
  - [Comparaison prédiction brute vs filtrée après SE][13]
 
<img width="2670" height="916" alt="comparison_overlays (4)" src="https://github.com/user-attachments/assets/9e4d3f0d-ad4c-4646-8b07-d8097a93e183" />

- **Exemple du pipeline** : de l’image brute à la grille finale validée


## Analyse & Discussion

- Mask R-CNN démontre une **supériorité systématique** pour la segmentation d’instances ; le canal luminance améliore la robustesse pour les objets sphériques mais reste instable pour d’autres classes.
- U-Net++ est solide pour les structures compactes mais échoue sur la monocouche (F1-score très faible voire nul sur monocouche en LAB).
- **Stratégie évolutionnaire** : clé pour l’optimisation spatiale, la réduction de bruit et le filtrage cellulaire sur grille ; permet un alignement précis et une élimination des artefacts même en présence de données incomplètes.

> **Limites** : dataset de taille modeste, déséquilibre inter-classes, variabilité expérimentale ; perspectives : enrichissement automatique annotations, hybridation d’architectures, optimisation multi-objectifs, intégration de données temporelles.


## Structure modulaire du code
```plaintext
├── data/           # Données sources, annotations COCO, preprocessing
├── models/         # Implémentations Mask R-CNN & U-Net++
├── training/       # Scripts d’apprentissage et validation
├── evolutionary/   # SE : grid extraction, optimisation, filtrage
├── evaluation/     # Métriques, scripts d’analyse et visualisation
├── utils/          # Fonctions utilitaires (I/O, affichage, métriques)
└── experiments/    # Résultats, checkpoints, journalisation
```


## Conclusion
L’approche hybride Deep Learning + stratégies évolutionnaires, validée sur un jeu de données public complexe, prouve sa robustesse et son efficacité pour la segmentation automatique, la classification et la localisation spatiale fine de sphéroïdes cellulaires. Cette méthodologie ouvre des **perspectives concrètes** en criblage pharmacologique automatisé, médecine régénérative et bioanalyse haut débit.


---
Fichier rédigé pour portfolio GitHub.

**Auteur : Mohamed Boussount – Master FIMATH 2024, Université Mohammed V de Rabat.**
