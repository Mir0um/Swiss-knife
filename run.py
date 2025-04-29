# ██████╗ ██╗   ██╗███╗   ██╗   ██████╗ ██╗   ██╗
# ██╔══██╗██║   ██║████╗  ██║   ██╔══██╗╚██╗ ██╔╝
# ██████╔╝██║   ██║██╔██╗ ██║   ██████╔╝ ╚████╔╝ 
# ██╔══██╗██║   ██║██║╚██╗██║   ██╔═══╝   ╚██╔╝  
# ██║  ██║╚██████╔╝██║ ╚████║██╗██║        ██║   
# ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝        ╚═╝   
#           run.py V1.0.1 27/03/2025

import subprocess
import sys
import os
import json
import subprocess
import configparser
import psutil

class Color:
    resetcolor = "\033[0m"

    @staticmethod
    def rgbcode(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def clear_terminal():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_rgb(text, r, g, b):
        return f"{Color.rgbcode(r, g, b)}{text}{Color.resetcolor}"


def _create_venv():
    """Crée l'environnement virtuel s'il n'existe pas et retourne le chemin du nouvel exécutable Python."""
    new_env = False
    if not os.path.exists(".venv"):
        subprocess.run(
            [sys.executable, "-m", "venv", "--symlinks", ".venv"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        new_env = True
    # Détermine le chemin de l'exécutable Python dans le venv
    if os.name == "nt":
        new_python = os.path.join(".venv", "Scripts", "python.exe")
    else:
        new_python = os.path.join(".venv", "bin", "python")
    print(Color.print_rgb(f"{'[INFO]':-<10} Nouvel exécutable Python dans .'venv' : {new_python}",128, 192, 255))
    return new_python, new_env


def _maj_pip_si_dispo(python_executable):
    r = subprocess.run([python_executable, "-m", "pip", "index", "versions", "pip", "--disable-pip-version-check", "--format=json"], capture_output=True, text=True)
    if r.returncode == 0:
        latest = json.loads(r.stdout)["versions"][0]
        current = subprocess.run([python_executable, "-m", "pip", "--version"], capture_output=True, text=True).stdout.split()[1]
        if latest != current:
            print(f"{'[UPDATE]':-<10} Mise à jour de pip.")
            subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    else:
        print(Color.print_rgb(f"{'[OK]':-<10} pip est à jour.",128,255,128))


def _portis():
    config = configparser.ConfigParser()
    config.read(".streamlit/config.toml")

    return config.get("server", "port").split("#")[0].replace(" ","")


def _runinport(port_recherche):
    resultats = []

    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == int(port_recherche):
            pid = conn.pid
            if pid:
                try:
                    proc = psutil.Process(pid)
                    resultats.append(proc.name())
                
                except psutil.NoSuchProcess:
                    continue

    return ",".join(set(resultats))

def check_and_install_requirements(python_executable):
    """Vérifie et installe les packages depuis requirements.txt avec l'exécutable du venv."""
    requirements_path = os.path.join("requirements.txt")
    if not os.path.exists(requirements_path):
        print(Color.print_rgb(f"{'[ERROR]':-<10} requirements.txt non trouvé à {requirements_path}.",255,128,128))
        input("Appuyez sur Entrée pour quitter...")
        sys.exit(1)

    package_installed = False

    with open(requirements_path, "r") as f:
        nb_libs = sum(1 for _ in f)
    
    with open(requirements_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue            
            i += 1
            parts = line.split("==")
            package_name = parts[0].strip()
            version = parts[1].strip() if len(parts) > 1 else None

            try:
                result = subprocess.run([python_executable, "-m", "pip", "show", package_name],
                                        capture_output=True, text=True, check=True)
                if version:
                    installed_version_line = [l for l in result.stdout.splitlines() if l.startswith("Version:")]
                    if installed_version_line:
                        installed_version = installed_version_line[0].split(":")[1].strip()
                        if installed_version != version:
                            print(f"{'[UPDATE]':-<10} {i}/{nb_libs} Mise à jour de {package_name} vers la version {version}")
                            subprocess.run([python_executable, "-m", "pip", "install", "--upgrade", f"{package_name}=={version}"], check=True, capture_output=True) # Capture output
                        else:
                            print(Color.print_rgb(f"{'[OK]':-<10} {i}/{nb_libs} '{package_name}' en version '{version}' est déjà installé.",128,255,128))
                    else:
                        print(Color.print_rgb(f"{'[WARNING]':-<10} Impossible de déterminer la version installée de {package_name}.",255,192,0))
                else:
                    print(Color.print_rgb(f"{'[OK]':-<10} {package_name} est déjà installé.",128,255,128))
            except subprocess.CalledProcessError:
                if version:
                    print(Color.print_rgb(f"{'[INSTALL]':-<10} {i}/{nb_libs} Installation de '{package_name}' en version '{version}'",255,255,128))
                    subprocess.run([python_executable, "-m", "pip", "install", f"{package_name}=={version}"], check=True, capture_output=True)  # Capture output
                else:
                    print(Color.print_rgb(f"{'[INSTALL]':-<10}  {i}/{nb_libs} Installation de {package_name}",255,255,128))
                    subprocess.run([python_executable, "-m", "pip", "install", package_name], check=True, capture_output=True)  # Capture output
                package_installed = True

    if package_installed:
        print(Color.print_rgb(f"{'[INFO]':-<10} Vérification des requirements terminée.",128, 192, 255))
        #input("Appuyez sur Entrée pour continuer...")

def run_streamlit_app(python_executable):
    """Lance l'application Streamlit avec l'exécutable du venv."""


    print(f"=======================================================================")
    print(f"    Information : La fenêtre de commande reste ouverte car elle héberge")
    print(f"    l'application Swiss-knife en cours d'exécution.")
    print(f"    Ne la fermez pas tant que vous n'avez pas terminé l'usage l'application.")
    print(f"    Pour interagir avec l'application, ouvrez votre navigateur et")
    print(f"    accédez à l'URL suivante : {Color.print_rgb(f'http://localhost:{port}/',128,128,255)}")
    print(f"=======================================================================")
    
    subprocess.run([python_executable, "-m", "streamlit", "run", "main.py"], capture_output=True, text=True, check=True)

if __name__ == "__main__":
    # Se placer dans le dossier du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system('title Swiss-knife')
    
    Color.clear_terminal()

    print(Color.print_rgb("Checking for Python...",128,255,128))
    print(Color.print_rgb(f"{'[OK]':-<10} Python installation found.",128,255,128))
    if not os.path.exists(".venv"):
        print(Color.print_rgb(f"{'[INFO]':-<10} Premier démarrage détecté. ",255,192,0))
        print(Color.print_rgb(f"{'[INFO]':-<10} Création de l'environnement virtuel '.venv'... ",128, 192, 255) +  Color.print_rgb("(Cette operation peu prendre pluseure minutes.)",255,192,192))
        new_python, new_env = _create_venv()
        _maj_pip_si_dispo(new_python)
        check_and_install_requirements(new_python)
       
        # Le script se ranlance avec le nouvelle python du .venv
        subprocess.run([new_python] + sys.argv, check=True)
        sys.exit() 
    else:

        port = _portis()

        # netstat -ano
        
        runinport =   _runinport(port)

        if bool(runinport):
            runinport =   _runinport(port)
            input(Color.print_rgb(f"{'[ERROR]':-<10} L'aplication {runinport} est deja lancer sur le port:{port}.",255,128,128))
        else:
            new_python = os.path.join(".venv", "Scripts", "python.exe")
            _maj_pip_si_dispo(new_python)
            check_and_install_requirements(new_python)
            Color.clear_terminal()
            run_streamlit_app(os.path.join(".venv", "Scripts", "python.exe"))
            sys.exit() 
