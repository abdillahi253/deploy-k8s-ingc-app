import subprocess, time

def setup():
    print("Configuration de l'environnement...")
    subprocess.run("sudo apt update && sudo apt install -y curl gpg apt-transport-https --yes", shell=True, check=True)

def install_k3s():
    print("Installation de k3s...")
    subprocess.run("sudo curl -sfL https://get.k3s.io | sh -", shell=True, check=True)
    time.sleep(30)
    result = subprocess.run("sudo kubectl get nodes", shell=True, check=True, capture_output=True, text=True)
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
    subprocess.run("curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null", shell=True, check=True)
    subprocess.run("echo \"deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main\" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list", shell=True, check=True)
    subprocess.run("sudo apt update && sudo apt install -y helm", shell=True, check=True)
    result = subprocess.run("helm version", shell=True, check=True, capture_output=True, text=True)
    if "version" in result.stdout:
        print("Helm est installé.")
    else:
        print("Installation de Helm échouée.")

def deploy_app():
    print("Déploiement de l'application Color...")
    subprocess.run("helm upgrade --install color oci://registry-1.docker.io/abdillahi253/app --version 0.1.0", shell=True, check=True)
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