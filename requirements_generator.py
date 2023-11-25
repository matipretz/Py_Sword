import subprocess

# Instala pipreqs y pip-tools si no están instalados
subprocess.run(["pip", "install", "pipreqs"])
subprocess.run(["pip", "install", "pip-tools"])

# Genera el archivo requirements.in usando pipreqs
subprocess.run(["pipreqs", "--savepath=requirements.in"])

# Compila los requisitos usando pip-compile
subprocess.run(["pip-compile"])