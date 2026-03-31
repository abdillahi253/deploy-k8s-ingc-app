import os
import subprocess, time

def setup():
    print("Configuration de l'environnement...")
    # Vérifier si curl, gpg et apt-transport-https sont installés
    missing = []
    for pkg in ["curl", "gpg", "apt-transport-https"]:
        res = subprocess.run(f"dpkg -s {pkg}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if res.returncode != 0:
            missing.append(pkg)
    if missing:
        print(f"Installation des paquets manquants : {' '.join(missing)}")
        subprocess.run(f"sudo apt update && sudo apt install -y {' '.join(missing)}", shell=True, check=True)
    else:
        print("Tous les paquets nécessaires sont déjà installés.")

def install_k3s():
    print("Installation de k3s...")
    # Vérifier si k3s est déjà installé (kubectl présent et cluster accessible)
    res = subprocess.run("kubectl get nodes", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        print("k3s (ou un cluster Kubernetes) est déjà installé et accessible.")
        return
    # Sinon, installer k3s
    subprocess.run("curl -sfL https://get.k3s.io | sh -", shell=True, check=True)
    time.sleep(30)
    # Exporter le KUBECONFIG pour k3s (pour tous les shells)
    os.environ['KUBECONFIG'] = '/etc/rancher/k3s/k3s.yaml'
    result = subprocess.run("kubectl get nodes", shell=True, check=True, capture_output=True, text=True)
    if "Ready" in result.stdout:
        print("Cluster k3s est installé.")
    else:
        print("Installation de k3s échouée.")

def check_traefik():
    print("Vérification de Traefik...")
    pod = subprocess.run("sudo kubectl get pods -n kube-system", shell=True, check=True, capture_output=True, text=True)
    svc = subprocess.run("sudo kubectl get svc -n kube-system", shell=True, check=True, capture_output=True, text=True)
    if "traefik" in pod.stdout and "traefik" in svc.stdout:
        print("Traefik est déployé.")
        # Chercher la ligne traefik dans svc.stdout et retourner le port exposé
        for line in svc.stdout.splitlines():
            if "traefik" in line:
                print("Ligne Traefik:", line)
                parts = line.split()
                if len(parts) > 4:
                    print("Port exposé par Traefik:", parts[4])
                    return parts[4]
        return None
    else:
        print("Traefik n'est pas déployé.")
        return None

def install_helm():
    print("Installation de Helm...")
    # Vérifier si helm est déjà installé
    res = subprocess.run("helm version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        print("Helm est déjà installé.")
        return
    # Installer Helm via le script officiel
    subprocess.run("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash", shell=True, check=True)
    result = subprocess.run("helm version", shell=True, check=True, capture_output=True, text=True)
    if "version" in result.stdout:
        print("Helm est installé.")
    else:
        print("Installation de Helm échouée.")

def deploy_app():
    print("Déploiement de l'application Color...")
    # Vérifier si le chart Helm est accessible
    show_chart = subprocess.run("helm show chart oci://registry-1.docker.io/abdillahi253/app --version 0.1.0", shell=True, capture_output=True, text=True)
    if show_chart.returncode != 0:
        print("Erreur : le chart Helm n'est pas accessible ou n'existe pas à l'URL spécifiée.")
        print(show_chart.stderr)
        return
    result = subprocess.run("helm upgrade --install color oci://registry-1.docker.io/abdillahi253/app --version 0.1.0", shell=True, capture_output=True, text=True)
    print(result.stderr)
    if result.returncode != 0:
        print("Erreur Helm :", result.stderr)
        return
    time.sleep(30)
    port = check_traefik()
    if port:
        # Récupère le code HTTP et le corps séparément
        cmd = f'curl -s -o /tmp/body -w "%{{http_code}}" http://localhost:{port}/color'
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        http_code = result.stdout.strip()
        with open("/tmp/body", "r") as f:
            body = f.read()
        print("Code HTTP:", http_code)
        print("Réponse de l'application Color:", body)
        if http_code == "200":
            print("L'application est disponible.")
        else:
            print("L'application n'est pas disponible (code:", http_code, ")")
    else:
        print("Impossible de vérifier l'application Color car Traefik n'est pas disponible.")

def main():
    setup()
    install_k3s()
    check_traefik()
    install_helm()
    deploy_app()

if __name__ == "__main__":
    main()