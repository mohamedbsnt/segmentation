# Extraction des métriques finales pour créer un tableau complet
import pandas as pd

# Métriques principales extraites du rapport
data = {
    'Architecture': ['Mask R-CNN (RGB)', 'Mask R-CNN (LAB)', 'U-Net++ (RGB)', 'U-Net++ (LAB)'],
    'Dice Score': [0.8405, 0.8237, 0.8050, 0.8064],
    'IoU/Jaccard': [0.7909, 0.7787, 0.7759, 0.7769],
    'Notes': [
        'Baseline RGB - Meilleure performance globale',
        'Canal luminance - Performance équivalente',
        'Architecture double - Supervision profonde',
        'Légèrement supérieur au RGB pour U-Net++'
    ]
}

# Métriques par classe (post-traitement SE)
class_metrics = {
    'Classe': ['Monocouche', 'Agrégation', 'Sphéroïde'],
    'Précision (avant SE)': [0.620, 0.609, 0.788],
    'Précision (après SE)': [0.743, 0.682, 0.827],
    'Rappel': [0.368, 0.854, 0.530],
    'F1-Score (avant SE)': [0.461, 0.711, 0.634],
    'F1-Score (après SE)': [0.492, 0.758, 0.644],
    'Amélioration F1': ['+0.031', '+0.047', '+0.010']
}

# Hyperparamètres optimaux SE
se_params = {
    'Paramètre': ['Population (μ, λ)', 'Sigma initial', 'Nombre d\'itérations', 'Score Fβ final'],
    'Valeur optimale': ['(40, 60)', '0.1', '160', '0.917'],
    'Description': [
        'Parents: 40, Descendants: 60 - Meilleur compromis exploration/exploitation',
        'Force de mutation adaptative - Équilibre optimal',
        'Convergence robuste - Plateau atteint vers 25-30 générations',
        'Performance exceptionnelle sur grilles synthétiques'
    ]
}

# Création des DataFrames
df_main = pd.DataFrame(data)
df_class = pd.DataFrame(class_metrics)
df_se = pd.DataFrame(se_params)

print("=== RÉSULTATS PRINCIPAUX ===")
print(df_main.to_string(index=False))
print("\n=== PERFORMANCES PAR CLASSE (avec amélioration SE) ===")
print(df_class.to_string(index=False))
print("\n=== HYPERPARAMÈTRES STRATÉGIE ÉVOLUTIONNAIRE ===")
print(df_se.to_string(index=False))

# Sauvegarde des résultats
df_main.to_csv('resultats_principaux.csv', index=False)
df_class.to_csv('performances_par_classe.csv', index=False)
df_se.to_csv('hyperparametres_SE.csv', index=False)

print("\n✅ Tableaux sauvegardés en CSV pour intégration dans le fichier .md")
