import subprocess
import os
import time

def uninstall_app():
    print("1️⃣ Désinstallation de l'application Helm...")
    result = subprocess.run("helm uninstall color", shell=True, capture_output=True, text=True, env=get_kube_env())
    if result.returncode == 0:
        print("✅ Application 'color' désinstallée.")
    else:
        print("ℹ️ L'application 'color' n'était peut-être pas installée ou une erreur est survenue.")
        print(result.stderr)

def uninstall_helm():
    print("2️⃣ Désinstallation de Helm...")
    # Supprimer le binaire helm
    result = subprocess.run("sudo rm -f /usr/local/bin/helm", shell=True)
    if result.returncode == 0:
        print("✅ Helm désinstallé.")
    else:
        print("ℹ️ Helm n'était peut-être pas installé ou une erreur est survenue.")
    # Supprimer les fichiers de configuration Helm
    subprocess.run("rm -rf ~/.config/helm ~/.cache/helm ~/.local/share/helm", shell=True)

def uninstall_k3s():
    print("3️⃣ Désinstallation de k3s...")
    # Utilise le script officiel de désinstallation
    result = subprocess.run("/usr/local/bin/k3s-uninstall.sh", shell=True)
    if result.returncode == 0:
        print("✅ k3s désinstallé.")
    else:
        print("ℹ️ k3s n'était peut-être pas installé ou une erreur est survenue.")

def get_kube_env():
    env = os.environ.copy()
    env['KUBECONFIG'] = '/etc/rancher/k3s/k3s.yaml'
    return env

def main():
    uninstall_app()
    uninstall_helm()
    uninstall_k3s()

if __name__ == "__main__":
    main()
