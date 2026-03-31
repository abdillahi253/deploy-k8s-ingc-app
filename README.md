# deploy-k8s-ingc-app
Sujet d’Entretien Technique — Déploiement d’un Cluster Kubernetes + Ingress + Application Color

# Script de Déploiement Kubernetes avec k3s, Traefik et Helm

Ce script Python automatise l’installation d’un cluster k3s, la vérification de Traefik, l’installation de Helm et le déploiement d’une application via Helm.

## Stack choisie et justification

- **k3s** : Distribution Kubernetes légère, idéale pour les environnements de développement ou les machines à ressources limitées. Installation rapide et maintenance simplifiée.
- **Traefik** : Ingress Controller moderne, facile à configurer, qui permet d'exposer les applications Kubernetes en HTTP/HTTPS avec gestion automatique des routes.
- **Helm** : Gestionnaire de packages Kubernetes, facilite le déploiement, la mise à jour et la gestion des applications complexes via des charts.
- **Python** : Utilisé pour l'automatisation du déploiement grâce à sa simplicité d'écriture de scripts et sa portabilité.

Ce choix permet d'automatiser rapidement la mise en place d'un cluster Kubernetes fonctionnel, d'exposer facilement les applications, et de garantir une reproductibilité des déploiements.

## Prérequis

- Système Linux (Debian/Ubuntu recommandé)
- Accès sudo
- Python 3.x installé
- Connexion Internet

## Utilisation

1. Clone ce dépôt ou copie le script sur ta machine.
2. Rends le script exécutable si besoin :
   ```sh
   chmod +x deploy.py
   ```
3. Exécute le script avec Python :
   ```sh
   sudo python3 deploy.py
   ```

## Accès à l'application

- En local : ouvre l’URL locale affichée à la fin du script dans ton navigateur.
- À distance : remplace "localhost" par l’adresse IP de la machine pour accéder à l’application depuis un autre appareil.

## Chart Helm de l'application

- Chart Helm public : [oci://registry-1.docker.io/abdillahi253/app](https://hub.docker.com/r/abdillahi253/app)

Pour l'utiliser directement :
```sh
helm upgrade --install color oci://registry-1.docker.io/abdillahi253/app --version 0.1.0
```

## Fonctionnalités

- Installe les dépendances système nécessaires (`curl`, `gpg`, etc.)
- Installe k3s (Kubernetes léger)
- Vérifie la présence de Traefik dans le cluster
- Installe Helm (gestionnaire de packages Kubernetes)
- Déploie une application Helm (`color`) depuis Docker Hub
- Vérifie l’accessibilité de l’application via Traefik

## Structure du script

- `setup()` : Installe les paquets système nécessaires.
- `install_k3s()` : Installe k3s et vérifie le cluster.
- `check_traefik()` : Vérifie que Traefik est bien déployé et récupère le port exposé.
- `install_helm()` : Installe Helm.
- `deploy_app()` : Déploie l’application et vérifie son accessibilité via HTTP.
- `main()` : Enchaîne toutes les étapes.

## Avertissement

Ce script modifie le système (installation de paquets, k3s, etc.) et doit être lancé avec des droits administrateur.
