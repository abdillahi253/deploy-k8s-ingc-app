import os
import subprocess, time
import re

def setup():
    print("0️⃣ Configuration de l'environnement...")
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
    print("1️⃣ Installation de k3s...")
    # Vérifier si k3s est déjà installé (kubectl présent et cluster accessible)
    res = subprocess.run("kubectl get nodes", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        print("✅ k3s (ou un cluster Kubernetes) est déjà installé et accessible.")
        return
    # Sinon, installer k3s
    subprocess.run("curl -sfL https://get.k3s.io | sh -", shell=True, check=True)
    time.sleep(30)
    result = subprocess.run("kubectl get nodes", shell=True, check=True, capture_output=True, text=True, env=get_kube_env())
    if "Ready" in result.stdout:
        print("✅ Cluster k3s est installé.")
    else:
        print("❌ Installation de k3s échouée.")

def check_traefik():
    print("3️⃣ Vérification de Traefik...")
    time.sleep(30)  # Attendre un peu pour s'assurer que les ressources sont bien créées
    pod = subprocess.run("sudo kubectl get pods -n kube-system", shell=True, check=True, capture_output=True, text=True, env=get_kube_env())
    svc = subprocess.run("sudo kubectl get svc -n kube-system", shell=True, check=True, capture_output=True, text=True, env=get_kube_env())
    if "traefik" not in pod.stdout or "traefik" not in svc.stdout:
        print("❌ Traefik n'est pas déployé.")
        return None
    print("✅ Traefik est déployé.")
    for line in svc.stdout.splitlines():
        if "traefik" in line:
            print("Ligne Traefik:", line)
            # Recherche tous les NodePorts HTTP (80:xxxxx/TCP)
            matches = re.findall(r'80:(\d+)/TCP', line)
            if matches:
                node_port = matches[0]
                print("NodePort HTTP :", node_port)
                return node_port
            else:
                print("Aucun NodePort HTTP trouvé sur la ligne Traefik.")
                return None
    print("Aucune ligne Traefik trouvée dans les services.")
    return None

def install_helm():
    print("2️⃣ Installation de Helm...")
    # Vérifier si helm est déjà installé
    res = subprocess.run("helm version", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0:
        print("✅ Helm est déjà installé.")
        return
    # Installer Helm via le script officiel
    subprocess.run("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash", shell=True, check=True)
    result = subprocess.run("helm version", shell=True, check=True, capture_output=True, text=True)
    if "version" in result.stdout:
        print("✅ Helm est installé.")
    else:
        print("❌ Installation de Helm échouée.")

def deploy_app():
    print("4️⃣ Déploiement de l'application Color...")
    # Vérifier si le chart Helm est accessible
    show_chart = subprocess.run("helm show chart oci://registry-1.docker.io/abdillahi253/app --version 0.1.0", shell=True, capture_output=True, text=True, env=get_kube_env())
    if show_chart.returncode != 0:
        print("Erreur : le chart Helm n'est pas accessible ou n'existe pas à l'URL spécifiée.")
        print(show_chart.stderr)
        return
    result = subprocess.run("helm upgrade --install color oci://registry-1.docker.io/abdillahi253/app --version 0.1.0", shell=True, capture_output=True, text=True, env=get_kube_env())
    print(result.stderr)
    if result.returncode != 0:
        print("Erreur Helm :", result.stderr)
        return
    time.sleep(30)
    # Récupère le code HTTP et le corps séparément
    cmd = f'curl -s -o /tmp/body -w "%{{http_code}}" http://localhost:{check_traefik()}/color'
    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    http_code = result.stdout.strip()
    with open("/tmp/body", "r") as f:
        body = f.read()
    print("Code HTTP:", http_code)
    if http_code == "200":
        print("✅ L'application est disponible.")
        print("URL d'accès : http://localhost:{port}/color".format(port=check_traefik()))
        print("URL d'accès depuis l'extérieur : http://IP-machine:{port}/color".format(port=check_traefik()))
    else:
        print("❌ L'application n'est pas disponible (code:", http_code, ")")

def get_kube_env():
    env = os.environ.copy()
    env['KUBECONFIG'] = '/etc/rancher/k3s/k3s.yaml'
    return env

def main():
    setup()
    install_k3s()
    install_helm()
    if check_traefik():
        deploy_app()
    else:
        print("Arrêt du script : Traefik ou non disponible.")

if __name__ == "__main__":
    main()