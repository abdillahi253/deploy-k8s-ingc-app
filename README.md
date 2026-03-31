# 🚀 deploy-k8s-ingc-app

> **Sujet d’Entretien Technique** — Déploiement d’un Cluster Kubernetes + Ingress + Application Color

---

## 🛠️ Stack choisie

- **k3s** : Kubernetes léger, rapide à installer .
- **Traefik** : Ingress moderne, simple à configurer pour exposer les apps.
- **Helm** : Déploiement et gestion d’apps Kubernetes via des charts.
- **Python** : Automatisation du déploiement, script simple et portable.

➡️ Cette stack permet un déploiement Kubernetes automatisé, reproductible et accessible à tous.

---

## ⚡ Prérequis

- Système Linux (Debian/Ubuntu recommandé)
- Accès sudo
- Python 3.x installé
- Connexion Internet

---

## ▶️ Utilisation

1. Clone ce dépôt ou copie le script sur ta machine.
2. Rends le script exécutable si besoin :
   ```sh
   chmod +x full_script.py
   ```
3. Exécute le script avec Python :
   ```sh
   sudo python3 full_script.py
   ```

---

## 🌐 Accès à l'application

- **En local** : ouvre l’URL locale affichée à la fin du script dans ton navigateur.
- **À distance** : remplace "localhost" par l’adresse IP de la machine pour accéder à l’application depuis un autre appareil.

---

## 📦 Chart Helm de l'application

- Chart Helm public : [oci://registry-1.docker.io/abdillahi253/app](https://hub.docker.com/r/abdillahi253/app)

Pour l'utiliser directement :
```sh
helm upgrade --install color oci://registry-1.docker.io/abdillahi253/app --version 0.1.0
```

---

## ✨ Fonctionnalités

- Installe les dépendances système nécessaires (`curl`, `gpg`, etc.)
- Installe k3s (Kubernetes léger)
- Vérifie la présence de Traefik dans le cluster
- Installe Helm (gestionnaire de packages Kubernetes)
- Déploie une application Helm (`color`) depuis Docker Hub
- Vérifie l’accessibilité de l’application via Traefik

---

## 🧩 Structure du script

- `setup()` : Installe les paquets système nécessaires.
- `install_k3s()` : Installe k3s et vérifie le cluster.
- `check_traefik()` : Vérifie que Traefik est bien déployé et récupère le port exposé.
- `install_helm()` : Installe Helm.
- `deploy_app()` : Déploie l’application et vérifie son accessibilité via HTTP.
- `main()` : Enchaîne toutes les étapes.

---

## 🏗️ Architecture du déploiement

```
[Utilisateur]
    |
    v
[Script Python] --(kubectl/helm)--> [Cluster k3s]
    |                                 |
    |                                 v
    |                        [Traefik Ingress]
    |                                 |
    |                                 v
    |                        [App Color déployée]
    |                                 |
    +-----------------------> [Accès HTTP/NodePort]
```

- Le script automatise l’installation de k3s, Traefik et l’application via Helm.
- Traefik expose l’application sur un NodePort accessible en local ou à distance.
- L’utilisateur interagit uniquement avec le script et l’URL générée.

---

## ⚠️ Avertissement

Ce script modifie le système (installation de paquets, k3s, etc.) et doit être lancé avec des droits administrateur.
