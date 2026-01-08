# Labo 00 – Infrastructure (Git, Docker, CI/CD)

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann.

## 🎯 Objectifs d'apprentissage

- Apprendre à créer un projet **Python** conteneurisé avec **Docker** à partir de zéro.
- Apprendre à écrire et exécuter des tests automatisés avec **pytest**.
- Mettre en place un pipeline **CI/CD** avec les ressources à notre disposition.

---

## ⚙️ Setup

Dans ce laboratoire, vous travaillerez sur une application calculatrice. Cette calculatrice est volontairement très simple afin que nous puissions nous concentrer sur la configuration et la structure du projet, ainsi que sur la création d'un pipeline CI/CD.

Vous allez créer la structure du projet vous-même à partir de zéro, en créant le `requirements.txt`, `Dockerfile`, `docker-compose.yml` et `.env`. Chaque activité vous guidera dans une étape de setup, puis l'implémentation. Il est très important de réaliser ce laboratoire car :

- Les concepts que vous apprendrez ici (ex. le setup Python et Docker, les approches de test et déploiement, etc.) vous aideront à mieux comprendre **TOUS** les laboratoires suivants.
- Les concepts architecturaux et les pratiques de développement que vous apprenez ici peuvent être appliqués au projet, **dans n'importe quel langage de programmation ou framework**.

Dans les prochains laboratoires, nous verrons des architectures plus complexes et nous travaillerons avec une variété d'outils logiciels et de concepts architecturaux.

> ⚠️ **ATTENTION** : Si vous ne l'avez pas déjà fait, nous vous recommandons d'installer **VS Code**, **Python 3+**, **Docker Desktop** et **MySQL Workbench** avant de commencer.

> ⚠️ **IMPORTANT** : Avant de commencer le setup et les activités, veuillez lire la documentation architecturale dans le répertoire `/docs/arc42/docs.pdf` pour comprendre quel type d'application nous serons en train de développer.

### 1. Clonez le dépôt

```bash
git clone https://github.com/[votrenom]/log430-labo0
cd log430-labo0
```

### 2. Créez votre fichier requirements.txt

Le fichier `requirements.txt` contient la liste des dépendances Python que vous avez besoin pour exécuter votre projet et qui seront installées via [pip](https://www.w3schools.com/python/python_pip.asp) dans votre environnement. Vous aurez besoin d'une seule dépendance pour ce projet : `pytest` (pour exécuter les tests unitaires). Créez un fichier `requirements.txt` dans le répertoire racine de votre projet :

```sh
pytest>=7.0
```

### 3. Créez votre Dockerfile

Un fichier `Dockerfile` est une recette permettant de créer une image de conteneur Docker. Un conteneur est une machine virtuelle simplifiée qui s'exécutera dans votre environnement de développement local, mais qui peut également s'exécuter dans un environnement de production si vous le souhaitez. Créez un fichier `Dockerfile` dans le répertoire racine de votre projet :

```sh
FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src/
COPY requirements.txt ./
ENV PYTHONPATH=/app/src
RUN pip install --no-cache-dir -r requirements.txt
```

### 4. Créez votre docker-compose.yml

Un fichier `docker-compose.yml` décrit quels conteneurs (également appelés services) seront créés en utilisant votre image de conteneur Docker comme base. Dans notre cas, nous voulons uniquement exécuter notre calculatrice. Créez un fichier `docker-compose.yml` dans le répertoire racine de votre projet :

```yml
services:
  calculator:
    build: .
    volumes:
      - .:/app
    stdin_open: true
    tty: true
```

### 5. Créez votre .env

Un fichier `.env` est utilisé pour garder les variables d'une application qui sont distinctes pour chaque instance et que nous ne voulons pas écrire dans le code pour des raisons de sécurité et de flexibilité. Par exemple, une application de gestion de magasin aura une base de données différente pour chaque magasin, avec un nom d'utilisateur et un mot de passe également distincts et qui ne doivent pas être partagés dans le code. Ici, dans ce très simple cas, nous garderons simplement le nom de l'utilisateur de la calculatrice. Créez un fichier `.env` dans le répertoire racine de votre projet avec une seule ligne :

```sh
CALCULATOR_USERNAME=YourName
```

Une fois le fichier `.env` créé et la variable définie, l'application dans `/src/calculator.py` est déjà préparée pour lire le `.env`, extraire la variable `CALCULATOR_USERNAME` et l'utiliser. Si vous faites votre propre application à partir de zéro, vous devriez écrire vous-même le code pour lire le `.env`, ou utiliser une librairie telle que [dotenv](https://www.geeksforgeeks.org/python/using-python-environment-variables-with-python-dotenv/) pour vous aider.

### 6. Démarrez le conteneur

Dans le terminal, exécutez :

```sh
docker compose build
docker compose up -d
```

Ensuite, cliquez sur votre conteneur dans la liste dans Docker Desktop, sélectionnez l'onglet `Exec` et exécutez :

```sh
python src/calculator.py
```

> 📝 **NOTE** : l'autocomplétion en appuyant sur Tab et les flèches du clavier ne marchent pas dans Docker Desktop, parce qu'il utilise une interface Bash simplifiée. Si vous n'aimez pas cela, vous pouvez également exécuter les commandes via [docker exec](https://docs.docker.com/reference/cli/docker/container/exec/) à partir de votre machine hôte (hors Docker).

---

## 🧪 Activités

### 1. Écrivez les tests

Dans le fichier `test_calculator.py`, écrivez des tests pour les fonctions définies dans `calculator.py`.

```python
def test_addition():
    assert addition(2, 3) == 5
```

Pour lancer les tests :

```bash
pytest
```

> 💡 **Question 1** : Si l'un des tests échoue à cause d'un bug, comment pytest signale-t-il l'erreur et aide-t-il à la localiser ? Rédigez un test qui provoque volontairement une erreur, puis montrez la sortie du terminal obtenue.

### 2. Ajoutez une étape à la pipeline CI (Intégration Continue)

Ajoutez une étape (step) dans `.github/workflows/.github-ci.yml` pour que GitHub exécute les tests automatiquement à chaque push.

> ⚠️ **IMPORTANT** : Il n'est pas recommandé d'écrire les noms d'utilisateur et les mots de passe en « plain text » dans un fichier tel que `.github/workflows/.github-ci.yml`. Veuillez utiliser les [secrets](https://docs.github.com/fr/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets) dans un [environnement GitHub](https://docs.github.com/fr/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments#creating-an-environment) **si vous avez besoin** de gérer des informations d'authentification.

### 3. Versionnez votre code

Si tous les tests passent :

```bash
git add .
git commit -m "Tests pour calculator.py"
git push
```

GitHub exécutera les tests sur son serveur, et ils devront passer également s'ils sont corrects.

> 💡 **Question 2** : Que fait GitHub pendant les étapes de « setup » et « checkout » ? Veuillez inclure la sortie du terminal GitHub CI dans votre réponse.

### 4. Réfléchissez à comment déployer votre code en production

Déployer en production signifie copier votre dépôt et faire le setup de votre application en dehors de votre environnement de développement, dans un autre serveur. Ce serveur pourrait être, par exemple :

- Un serveur physique dans une entreprise/école
- Un serveur en nuage (ex. Azure, AWS, etc.)
- Une machine virtuelle (VM) dans un serveur

Dans le cours LOG430, nous utiliserons des VMs créées dans [LXD](https://canonical.com/lxd), une application de gestion de VMs et conteneurs. Nous utiliserons une instance LXD hébergée par l'école.

### 5. Installez le client LXD

Le client LXD est disponible pour Windows, macOS et Linux.

Installez sur Windows via `chocolatey` :
```sh
choco install lxc
```

Installez sur Windows (WSL) ou Linux via `snap` :
```sh
snap install lxd
```

Installez sur macOS via `brew` :
```sh
brew install lxc
```

Pour ajouter les deux serveurs LXD, connectez-vous au VPN et exécutez :
```sh
lxc remote add fiware-1.logti.etsmtl.ca
lxc remote add fiware-2.logti.etsmtl.ca
```

Ces commandes demanderont un jeton chacune. Demandez votre jeton au chargé de lab.

> 📝 **NOTE** : Ce sont des jetons à usage unique. Par conséquent, lorsqu'une personne intègre un serveur dans son client LXD, le jeton est annulé et ne peut plus être utilisé pour ajouter un second client.

### 6. Créez des VMs dans votre serveur LXD
Pour créer une VM dans le serveur `fiware-1.logti.etsmtl.ca`, par exemple :
```sh
lxc launch images:ubuntu/22.04 vm-test1 --remote fiware-1.logti.etsmtl.ca
```

Remplacez `vm-test1` par le nom que vous voulez donner à votre VM.

#### 6.1. Vérifier la création de la VM

Pour voir la liste de VMs sur le serveur :

```bash
lxc list --remote fiware-1.logti.etsmtl.ca
```

#### 6.2. Obtenir l'adresse IP de la VM

```bash
lxc list --remote fiware-1.logti.etsmtl.ca
```

Notez l'adresse IP de votre VM (colonne IPV4).

Exemple de sortie :
```sh
| vm-test1 | RUNNING | 10.99.0.50 (eth0) | ... |
```

#### 6.3. Configurer SSH dans la VM

Accédez à la VM pour installer et configurer SSH :

```bash
lxc exec vm-test1 --remote fiware-1.logti.etsmtl.ca -- bash
```

Puis à l'intérieur de la VM, exécutez :

```bash
apt update
apt install openssh-server -y
```

#### 6.4. Créer une clé SSH (sur votre machine locale)

Si vous n'avez pas encore de clé SSH :

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/lxd_key
```

Appuyez sur `Enter` pour accepter les paramètres par défaut.

#### 6.5. Copier la clé publique dans la VM

Depuis votre machine locale :

```bash
lxc file push ~/.ssh/lxd_key.pub vm-test1/root/.ssh/authorized_keys --remote fiware-1.logti.etsmtl.ca
```

#### 6.6. Configurer les permissions SSH

À l'intérieur de la VM (via la commande `exec` de l'étape 6.3) :

```bash
chmod 600 ~/.ssh/authorized_keys
systemctl enable ssh
systemctl start ssh
```

#### 6.7. Annexe : commandes utiles pour les serveurs distants

```bash
# Arrêter une VM
lxc stop vm-test1 --remote fiware-1.logti.etsmtl.ca

# Supprimer une VM
lxc delete vm-test1 --remote fiware-1.logti.etsmtl.ca --force

# Démarrer une VM
lxc start vm-test1 --remote fiware-1.logti.etsmtl.ca

# Voir les logs d'une VM
lxc logs vm-test1 --remote fiware-1.logti.etsmtl.ca

# Copier des fichiers vers la VM
lxc file push fichier_local.txt vm-test1/root/ --remote fiware-1.logti.etsmtl.ca

# Copier des fichiers depuis la VM
lxc file pull vm-test1/root/fichier.txt ./fichier.txt --remote fiware-1.logti.etsmtl.ca
```

### 7. Déployez votre application manuellement

Depuis votre machine locale (vous devez être connecté au VPN), exécutez :

```sh
ssh -i ~/.ssh/lxd_key root@<IP_DE_LA_VM>
```

Remplacez `<IP_DE_LA_VM>` par l'adresse IP obtenue à l'étape 6.2. Exemple :

```sh
ssh -i ~/.ssh/lxd_key root@10.99.0.50
```

Une fois que vous êtes connecté, déployez l'application sur la VM manuellement. N'oubliez pas d'installer Python, Docker et toutes les dépendances nécessaires sur la VM :

```sh
git clone https://github.com/[votre-nom]/log430-labo0
cd log430-labo0
```

De plus, voici quelques commandes utiles pour vérifier l'état des ressources :

```sh
free -h   # Vérifier l'utilisation de la RAM
top       # Vérifier l'utilisation du CPU et les processus en cours
df -h     # Vérifier l'espace disque disponible
```

> 📝 **NOTE** : Si vous avez des problèmes de performance avec votre VM (par exemple, une VM lente ou bloquée), essayez de l'arrêter et de la redémarrer, ou de la recréer. Si cela ne fonctionne pas, faites-moi signe.

> 💡 **Question 3** : Quel type d'informations pouvez-vous obtenir via la commande « top » ? Veuillez inclure la sortie du terminal dans votre réponse.

### 8. Automatisez le déploiement continu (CD)

Plusieurs alternatives existent pour le CD : déploiement déclenché par webhooks via SSH, ou via un outil CI/CD (ex. ArgoCD). Cependant, dans ce labo, nous vous recommandons d'utiliser un [GitHub Runner auto-hébergé (self-hosted)](https://docs.github.com/fr/actions/how-tos/manage-runners/self-hosted-runners/add-runners).

Nous vous recommandons le GitHub Runner parce que c'est l'approche plus simple et moins dépendante d'une configuration spécifique de réseau (ex. il n'est pas nécessaire d'ouvrir des ports dans le pare-feu, ou d'utiliser une approche événementielle).

---

## 📦 Livrables

- Code compressé en `.zip` contenant **l'ensemble du code source** du projet Labo 00.
- Rapport `.pdf` répondant aux 3 questions présentées dans ce fichier. Il est **obligatoire** d'ajouter du code ou des sorties de terminal pour illustrer chacune de vos réponses.