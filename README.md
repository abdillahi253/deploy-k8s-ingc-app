# deploy-k8s-ingc-app
Sujet d’Entretien Technique — Déploiement d’un Cluster Kubernetes + Ingress + Application Color

# Script de Déploiement Kubernetes avec k3s, Traefik et Helm

Ce script Python automatise l’installation d’un cluster k3s, la vérification de Traefik, l’installation de Helm et le déploiement d’une application via Helm.

## Prérequis

- Système Linux (Debian/Ubuntu recommandé)
- Accès sudo
- Python 3.x installé
- Connexion Internet

## Fonctionnalités

- Installe les dépendances système nécessaires (`curl`, `gpg`, etc.)
- Installe k3s (Kubernetes léger)
- Vérifie la présence de Traefik dans le cluster
- Installe Helm (gestionnaire de packages Kubernetes)
- Déploie une application Helm (`color`) depuis Docker Hub
- Vérifie l’accessibilité de l’application via Traefik

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

## Structure du script

- `setup()` : Installe les paquets système nécessaires.
- `install_k3s()` : Installe k3s et vérifie le cluster.
- `check_traefik()` : Vérifie que Traefik est bien déployé et récupère le port exposé.
- `install_helm()` : Installe Helm.
- `deploy_app()` : Déploie l’application et vérifie son accessibilité via HTTP.
- `main()` : Enchaîne toutes les étapes.

## Personnalisation

- Modifie l’URL du chart Helm ou le nom de l’application selon tes besoins.
- Adapte les ports ou les ressources si nécessaire.

## Avertissement

Ce script modifie le système (installation de paquets, k3s, etc.) et doit être lancé avec des droits administrateur.
