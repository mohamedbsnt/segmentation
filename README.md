# segmentation
localization and segmentation instances

Détection et Segmentation de Sphéroïdes Cellulaires avec Deep Learning
Ce projet met en œuvre et compare plusieurs approches de Deep Learning pour la détection et la segmentation automatiques de sphéroïdes cellulaires à différents stades de formation (monocouche, agrégation, sphéroïde final). L'objectif est de reproduire et d'évaluer les techniques décrites dans l'article scientifique Evolutionary Grid Optimization and Deep Learning for Improved In Vitro Cellular Spheroid Localization.
Le code explore deux architectures de modèles principales : Mask R-CNN pour la segmentation d'instance et Unet++ pour la segmentation sémantique. Chaque modèle est entraîné et évalué selon deux stratégies de traitement d'image :
Images RGB brutes : Utilisation directe des images couleur.
Canal de Luminance (LAB) : Conversion des images dans l'espace colorimétrique LAB et utilisation exclusive du canal de Luminance (L) pour l'entraînement, afin de réduire l'impact des variations d'éclairage.
Objectifs du Projet
Automatiser l'analyse : Remplacer l'analyse manuelle, longue et subjective, des cultures de sphéroïdes par un système de détection automatique, rapide et reproductible.
Quantifier les stades de formation : Identifier et segmenter précisément chaque type d'objet (monocouche, agrégation, sphéroïde) pour permettre une analyse quantitative de la croissance cellulaire.
Comparer les architectures de modèles : Évaluer les performances de Mask R-CNN et d'Unet++ pour cette tâche spécifique.
Évaluer l'impact de la luminance : Déterminer si l'utilisation du canal de luminance de l'espace LAB améliore la robustesse et la précision des modèles par rapport aux images RGB standard.
Méthodologie
Le projet est structuré autour de deux approches de segmentation complémentaires.
1. Segmentation d'Instance avec Mask R-CNN

  
   ![spheroide_maskrcnn](https://github.com/user-attachments/assets/44bd6d06-1226-420b-9e6f-9aa51ba9dfce)

 
Objectif : Détecter chaque objet individuellement dans l'image, lui assigner une classe (monocouche, agrégation, sphéroïde) et générer un masque de segmentation précis pour chacun. C'est idéal pour compter les objets et analyser leurs propriétés individuelles.
Architecture : Le modèle Mask R-CNN est utilisé avec un backbone ResNet50-FPN pré-entraîné sur COCO. Les têtes de classification et de masquage ont été ré-entraînées pour nos 3 classes spécifiques (+ 1 pour le fond).

![segmentation_biniare_unet++](https://github.com/user-attachments/assets/0cda122a-01bf-4da1-95cd-a6a8014b2ce4)

Entraînement :
Version RGB : Le modèle est entraîné directement sur les images couleur.
Version LAB : Les images sont converties en espace LAB, et le canal de luminance (L) est dupliqué sur 3 canaux pour servModel,Luminance Conversion,Dice,Jaccard
Mask R-CNN,yes,0.9558463096618652,0.9154267907142639
Unet++,yes,0.36221417784690857,0.221160888671875
Mask R-CNN,no,0.8491584658622742,0.737858772277832
Unet++,no,0.6892058849334717,0.52579265832901

[comparaison_unet_maskrcnn_rgb_luminance.csv](https://github.com/user-attachments/files/21023918/comparaison_unet_maskrcnn_rgb_luminance.csv)

ir d'entrée au modèle.
Évaluation : Les performances sont mesurées à l'aide de la métrique mAP (mean Average Precision), qui évalue la qualité des boîtes englobantes et des masques.
2. Segmentation Sémantique avec Unet++
Objectif : Classifier chaque pixel de l'image en lui attribuant une des classes cibles. Cette approche est puissante pour obtenir une carte de segmentation complète de l'image. Pour gérer la complexité des objets, une stratégie de fusion a été adoptée.
Architecture : Deux modèles Unet++ avec un encodeur timm-regnety_120 sont utilisés :
Modèle Multiclasse : Entraîné à segmenter les classes "monocouche" et "agrégation" (avec une sortie softmax).
Modèle Binaire : Spécifiquement entraîné à segmenter la classe "sphéroïde" (avec une sortie sigmoid).
Fusion des prédictions (Logique XOR) : Les prédictions des deux modèles sont combinées. Un pixel est classé comme "sphéroïde" uniquement s'il est détecté par le modèle binaire ET qu'il n'est pas déjà classé comme "monocouche" ou "agrégation" par le modèle multiclasse. Cela permet de gérer efficacement les superpositions.
Entraînement : Comme pour Mask R-CNN, deux versions sont entraînées (RGB et LAB).
Évaluation : Les performances sont mesurées à l'aide des coefficients Dice et Jaccard (IoU), qui comparent les masques prédits aux masques de vérité terrain au niveau du pixel.
Comment Utiliser ce Projet
Configuration : Assurez-vous que les dépendances listées dans requirements.txt sont installées.
Données : Organisez vos données (images et annotations COCO) en suivant la structure de dossiers attendue par les scripts. Mettez à jour les chemins d'accès dans les fichiers de configuration.

Entraînement :

Pour entraîner le modèle Mask R-CNN (RGB), exécutez le script train_maskrcnn_rgb.py.
Pour entraîner le modèle Mask R-CNN (Luminance), exécutez train_maskrcnn_lab.py.
Les scripts d'entraînement pour Unet++ suivent une logique similaire.
Évaluation : Utilisez les notebooks ou scripts d'évaluation pour calculer les métriques de performance sur le jeu de test et générer des visualisations.
Résultats et Conclusion
Les résultats des deux approches sont comparés dans les rapports d'évaluation. L'analyse montre que :
Mask R-CNN excelle dans la détection d'instances distinctes, ce qui est crucial pour le comptage.
L'approche Unet++ fusionnée fournit une carte de segmentation sémantique complète et robuste.
L'utilisation du canal de luminance (LAB) a montré une amélioration de la performance dans certains cas, confirmant les observations de l'article de recherche et suggérant une meilleure robustesse aux variations d'éclairage.
Ce projet constitue une base solide pour le développement d'outils d'analyse d'images automatisés en biologie cellulaire.

