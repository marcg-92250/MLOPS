# Deployment Strategies: Canary vs Blue/Green

## Canary Deployment

### Principe

Le **canary deployment** (déploiement canari) est une stratégie où on déploie progressivement une nouvelle version en la testant d'abord sur un petit pourcentage du trafic.

### Comment ça marche

1. La **version actuelle** (current) gère la majorité du trafic
2. La **nouvelle version** (canary) reçoit un petit pourcentage du trafic (ex: 10%)
3. On monitore les métriques de la version canary
4. Si tout va bien, on augmente progressivement le pourcentage
5. Si problème, on peut rapidement revenir à 100% sur la version actuelle

### Exemple

```
Étape 1: 90% current, 10% canary
Étape 2: 70% current, 30% canary
Étape 3: 50% current, 50% canary
Étape 4: 0% current, 100% canary (nouvelle version devient current)
```

### Avantages

✅ **Risque limité**: Seul un petit pourcentage d'utilisateurs est affecté  
✅ **Détection rapide**: On peut identifier les problèmes avant déploiement complet  
✅ **Rollback facile**: Juste réduire le pourcentage à 0%  
✅ **A/B testing**: Permet de comparer les performances  
✅ **Progressif**: Augmentation graduelle du trafic  

### Inconvénients

❌ Complexe à implémenter  
❌ Nécessite du monitoring en temps réel  
❌ Deux versions actives simultanément (consomme plus de ressources)  
❌ Gestion de l'état si les versions sont incompatibles  

### Cas d'usage idéaux

- Systèmes à fort trafic
- Modifications critiques
- Nouveaux modèles ML à valider
- Environnements de production sensibles

---

## Blue/Green Deployment

### Principe

Le **blue/green deployment** maintient deux environnements identiques: un actif (blue) et un inactif (green).

### Comment ça marche

1. **Blue** (environnement actuel) gère 100% du trafic
2. On déploie la nouvelle version sur **Green** (inactif)
3. On teste Green en interne
4. **Switch instantané**: On bascule tout le trafic de Blue vers Green
5. Blue devient l'environnement de secours

### Exemple

```
État initial: Blue (v1) → 100% trafic, Green (vide) → 0% trafic
Déploiement: Blue (v1) → 100% trafic, Green (v2) → 0% trafic (tests)
Switch:      Blue (v1) → 0% trafic, Green (v2) → 100% trafic
```

### Avantages

✅ **Switch instantané**: Basculement immédiat  
✅ **Rollback simple**: Re-switch vers Blue  
✅ **Tests complets**: Green peut être testé avant switch  
✅ **Zéro downtime**: Pas d'interruption de service  
✅ **Plus simple**: Pas de gestion de pourcentage  

### Inconvénients

❌ **Coût**: Nécessite le double de ressources  
❌ **Tout ou rien**: Pas de déploiement progressif  
❌ **Synchronisation**: Gestion de l'état et des bases de données  
❌ **Tests en prod**: Difficile de tester avec du vrai trafic avant switch  

### Cas d'usage idéaux

- Déploiements ponctuels
- Systèmes avec peu de trafic
- Besoins de rollback rapide
- Budget infrastructure disponible

---

## Comparaison

| Critère | Canary | Blue/Green |
|---------|--------|------------|
| **Basculement** | Progressif (10% → 50% → 100%) | Instantané (0% → 100%) |
| **Risque** | Faible (affecte peu d'utilisateurs) | Moyen (affecte tous) |
| **Rollback** | Immédiat (réduire %) | Immédiat (re-switch) |
| **Ressources** | 2 versions actives partiellement | 2 environnements complets |
| **Complexité** | Élevée (routing + monitoring) | Moyenne (switch) |
| **Monitoring** | Essentiel en temps réel | Important mais moins critique |
| **A/B Testing** | Oui, natif | Non, nécessite des outils |

---

## Similitudes

1. **Zéro downtime**: Les deux permettent des déploiements sans interruption
2. **Rollback rapide**: Retour arrière possible rapidement
3. **Deux versions**: Les deux maintiennent l'ancienne et la nouvelle version
4. **Testing en production**: Possibilité de tester avec du vrai trafic

---

## Différences clés

### 1. Granularité du contrôle

- **Canary**: Contrôle fin du pourcentage (1%, 5%, 10%, etc.)
- **Blue/Green**: Tout ou rien (0% ou 100%)

### 2. Vitesse de déploiement

- **Canary**: Progressif sur plusieurs heures/jours
- **Blue/Green**: Instantané

### 3. Exposition au risque

- **Canary**: Exposition limitée et contrôlée
- **Blue/Green**: Tous les utilisateurs basculent en même temps

### 4. Utilisation des ressources

- **Canary**: Partage des ressources selon le pourcentage
- **Blue/Green**: Double infrastructure complète

---

## Quand utiliser quoi?

### Choisir Canary si:

- Vous avez un fort trafic
- Vous voulez valider progressivement
- Vous avez besoin de métriques comparatives
- Le risque doit être minimisé au maximum

### Choisir Blue/Green si:

- Vous avez peu de trafic
- Vous voulez un déploiement simple
- Le rollback doit être instantané
- Vous avez le budget infrastructure

---

## Dans le contexte ML

### Canary pour ML

Idéal pour les modèles ML car:
- Permet de comparer les performances des modèles
- Réduit le risque d'un mauvais modèle
- Facilite l'A/B testing des prédictions
- **C'est ce qu'on implémente dans ce projet!**

### Blue/Green pour ML

Utile quand:
- Changement majeur d'architecture
- Nouveau preprocessing
- Migration de framework

---

## Implémentation dans ce projet (Part 3)

Notre implémentation Canary:

```python
# Deux modèles chargés
current_model  # Version stable (production)
next_model     # Version candidate

# Prédiction avec probabilité p
if random() < p:
    prediction = current_model.predict(X)
else:
    prediction = next_model.predict(X)

# Endpoints
/update-model        # Met à jour next_model
/accept-next-model   # next_model devient current_model
/set-canary-ratio    # Ajuste le pourcentage p
```

Cela permet de tester prudemment de nouveaux modèles en production!

