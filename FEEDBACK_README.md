# Retour sur les instructions du README - Étape 6 (Création de VM LXD)

**Étudiant** : Achref Samoud  
**Date** : 8 janvier 2026  
**Section problématique** : Étape 6 - Créer des VMs dans votre serveur LXD

---

## 🐛 Problèmes rencontrés

### 1. Syntaxe de la commande incorrecte dans le README

**Commande donnée dans le README** :
```bash
lxc launch images:ubuntu/22.04 vm-test1 --remote fiware-1.logti.etsmtl.ca
```

**Problème** :
- La syntaxe avec `--remote` ne fonctionne pas avec la version LXD installée
- Erreur : `Error: unknown flag: --remote`

**Solution qui fonctionne** :
```bash
lxc launch ubuntu:22.04 fiware-1:vm-test1
```

---

### 2. Configuration du profil par défaut manquante

**Problème** :
Le profil `default` du projet `log430-student-1` n'a pas de configuration de base (pas de device root, pas de limite mémoire), ce qui empêche la création de VMs.

**Erreurs rencontrées** :
```
Error: Failed instance creation: Failed checking if instance creation allowed: 
Failed getting usage of project entities: Failed getting root disk device for 
instance "vm-achref-log430" in project "log430-student-1": No root device could be found
```

```
Error: Failed instance creation: Failed checking if instance creation allowed: 
Failed getting usage of project entities: Instance "vm-achref-log430" in project 
"log430-student-1" has no "limits.memory" config, either directly or via a profile
```

**Configuration nécessaire AVANT de créer une VM** :

```bash
# 1. Ajouter un device root au profil
lxc profile device add fiware-1:default root disk path=/ pool=default size=20GB

# 2. Définir une limite de mémoire
lxc profile set fiware-1:default limits.memory=4GB

# 3. Ensuite créer la VM
lxc launch ubuntu:22.04 fiware-1:vm-test1
```

---

### 3. Syntaxe pour lister les VMs

**Commande donnée dans le README** :
```bash
lxc list --remote fiware-1.logti.etsmtl.ca
```

**Problème** :
- Le flag `--remote` n'est pas supporté

**Solution qui fonctionne** :
```bash
lxc list fiware-1:
```

---

## ✅ Commandes corrigées - Section complète

### Étape 6 : Créer des VMs dans votre serveur LXD

#### 6.0. Configuration du profil (NOUVELLE ÉTAPE REQUISE)

Avant de créer une VM, vous devez configurer le profil par défaut :

```bash
# Ajouter un device root avec la taille souhaitée
lxc profile device add fiware-1:default root disk path=/ pool=default size=20GB

# Définir une limite de mémoire (4GB recommandé, max 8GB selon quotas)
lxc profile set fiware-1:default limits.memory=4GB
```

#### 6.1. Créer une VM

Pour créer une VM dans le serveur `fiware-1.logti.etsmtl.ca` :

```bash
lxc launch ubuntu:22.04 fiware-1:vm-test1
```

Remplacez `vm-test1` par le nom que vous voulez donner à votre VM.

#### 6.2. Vérifier la création de la VM

Pour voir la liste de VMs sur le serveur :

```bash
lxc list fiware-1:
```

#### 6.3. Obtenir l'adresse IP de la VM

```bash
lxc list fiware-1:
```

Notez l'adresse IP de votre VM (colonne IPV4). Cela peut prendre quelques secondes après la création.

Exemple de sortie :
```
+----------+---------+----------------+------+-----------+-----------+
| NAME     | STATE   | IPV4           | IPV6 | TYPE      | SNAPSHOTS |
+----------+---------+----------------+------+-----------+-----------+
| vm-test1 | RUNNING | 10.99.0.50     |      | CONTAINER | 0         |
+----------+---------+----------------+------+-----------+-----------+
```

---

## � Problème avec la connexion SSH (Étape 6.2 et 7)

### 4. L'IP de la VM n'est pas accessible directement via SSH

**Problème** :
L'adresse IP affichée par `lxc list fiware-1:` (ex: 192.168.1.34) est une IP locale au réseau du serveur LXD distant. Elle n'est pas accessible directement depuis votre machine locale (WSL).

**Erreur rencontrée** :
```bash
ssh -i ~/.ssh/lxd_key root@192.168.1.34
ssh: connect to host 192.168.1.34 port 22: Connection timed out
```

**Solutions testées** :

1. **Proxy device (ÉCHOUÉ)** : Les proxy devices sont interdits par le projet LXD pour des raisons de sécurité :
   ```bash
   lxc config device add fiware-1:vm-achref-log430 ssh-proxy proxy listen=tcp:0.0.0.0:10022 connect=tcp:192.168.1.34:22
   # Error: Proxy devices are forbidden
   ```

2. **Solution fonctionnelle** : Utiliser `lxc exec` pour accéder à la VM au lieu de SSH direct :
   ```bash
   lxc exec fiware-1:vm-achref-log430 -- bash
   ```

**Impact sur le README** :
- L'étape 7 demande d'utiliser SSH (`ssh -i ~/.ssh/lxd_key root@<IP_DE_LA_VM>`), mais cela ne fonctionne pas avec la configuration actuelle du serveur LXD
- La configuration SSH (étapes 6.3 à 6.6) peut être conservée pour référence, mais n'est pas utilisable dans ce contexte
- **Recommandation** : Remplacer dans l'étape 7 la commande SSH par `lxc exec fiware-1:<nom-vm> -- bash`

---

## �📊 Informations sur les quotas du projet

Les étudiants ont les limites suivantes sur leur projet :

- **Stockage total** : 50GB
- **RAM maximale** : 8GB
- **Nombre de VMs** : 1 maximum
- **Nombre de conteneurs** : 10 maximum

Ces informations peuvent être vérifiées avec :
```bash
lxc project show fiware-1:log430-student-1
```

---

## 💡 Recommandations

1. Ajouter la section 6.0 (Configuration du profil) dans le README **avant** l'étape de création de VM
2. Corriger toutes les syntaxes `--remote` par la syntaxe avec `:`
3. Changer `images:ubuntu/22.04` par `ubuntu:22.04`
4. Documenter les quotas disponibles pour que les étudiants sachent quelle taille allouer
5. Préciser que la configuration du profil est une étape **unique** à faire une seule fois
6. **Clarifier l'étape 7** : Remplacer `ssh -i ~/.ssh/lxd_key root@<IP_DE_LA_VM>` par `lxc exec fiware-1:<nom-vm> -- bash` car l'IP locale de la VM n'est pas accessible directement
7. Expliquer que SSH est configuré pour une utilisation future (déploiement automatisé) mais que `lxc exec` doit être utilisé pour le déploiement manuel
8. **CRITIQUE** : Documenter que `lxc launch` crée par défaut un **CONTAINER**, pas une VM. Pour Docker, il faut **ABSOLUMENT** utiliser le flag `--vm` : `lxc launch ubuntu:22.04 fiware-1:vm-test1 --vm`
9. Ajouter l'étape de configuration réseau : après création de la VM, ajouter `eth0` au profil default ou directement à la VM pour qu'elle obtienne une IP

---

## 🔧 Commandes testées et fonctionnelles

```bash
# Lister les serveurs distants configurés
lxc remote list

# Voir le profil par défaut
lxc profile show fiware-1:default

# Configurer le profil (une seule fois)
lxc profile device add fiware-1:default root disk path=/ pool=default size=20GB
lxc profile set fiware-1:default limits.memory=4GB

# Créer et démarrer une VM
lxc launch ubuntu:22.04 fiware-1:vm-test1

# Ajouter une interface réseau à la VM
lxc config device add fiware-1:vm-test1 eth0 nic nictype=bridged parent=lxdbr0

# Redémarrer la VM pour appliquer les changements réseau
lxc restart fiware-1:vm-test1

# Lister les VMs
lxc list fiware-1:

# Accéder à la VM (à utiliser au lieu de SSH)
lxc exec fiware-1:vm-test1 -- bash

# Arrêter une VM
lxc stop fiware-1:vm-test1

# Démarrer une VM
lxc start fiware-1:vm-test1

# Supprimer une VM
lxc delete fiware-1:vm-test1 --force

# Copier des fichiers vers la VM
lxc file push fichier_local.txt fiware-1:vm-test1/root/

# Copier la clé SSH (étape 6.5)
lxc file push ~/.ssh/lxd_key.pub fiware-1:vm-test1/root/.ssh/authorized_keys

# Exécuter une commande dans la VM sans entrer en mode interactif
lxc exec fiware-1:vm-test1 -- chmod 600 /root/.ssh/authorized_keys
```

---

## 🐳 Problème critique : CONTAINER vs VIRTUAL-MACHINE pour Docker

### 5. Docker ne fonctionne PAS dans un conteneur LXC

**Problème découvert** :
La commande `lxc launch ubuntu:22.04 fiware-1:vm-test1` crée un **CONTAINER** (TYPE=CONTAINER), pas une machine virtuelle. Docker ne peut pas fonctionner dans un conteneur LXC à cause des restrictions de cgroups.

**Erreur rencontrée lors du test Docker** :
```bash
docker run hello-world
# docker: Error response from daemon: OCI runtime create failed: 
# runc create failed: unable to start container process: error during 
# container init: error mounting "cgroup" to rootfs at "/sys/fs/cgroup": 
# mount cgroup:/sys/fs/cgroup/systemd (via /proc/self/fd/7), 
# flags: 0xf, data: name=systemd: permission denied: unknown.
```

**Solution CRITIQUE** :
Il faut utiliser le flag `--vm` pour créer une vraie machine virtuelle :

```bash
# ❌ MAUVAIS - Crée un CONTAINER (Docker ne fonctionnera pas)
lxc launch ubuntu:22.04 fiware-1:vm-test1

# ✅ CORRECT - Crée une VIRTUAL-MACHINE (Docker fonctionne)
lxc launch ubuntu:22.04 fiware-1:vm-test1 --vm
```

**Vérification du type** :
```bash
lxc list fiware-1:
# Colonne TYPE doit afficher "VIRTUAL-MACHINE", pas "CONTAINER"
```

**Étapes de correction si vous avez créé un conteneur par erreur** :
```bash
# Supprimer le conteneur
lxc delete fiware-1:vm-test1 --force

# Recréer en tant que VM
lxc launch ubuntu:22.04 fiware-1:vm-test1 --vm
```

---

## 🌐 Configuration réseau manquante

### 6. La VM créée n'a pas de configuration réseau par défaut

**Problème** :
Après création de la VM avec `--vm`, celle-ci n'a pas d'interface réseau et n'obtient pas d'IP :

```bash
lxc list fiware-1:
# IPV4 = vide, IPV6 = vide
```

**Solution - Ajouter une interface réseau** :

Option A : Ajouter au profil default (recommandé, s'applique à toutes les futures VMs) :
```bash
lxc profile device add fiware-1:default eth0 nic nictype=bridged parent=lxdbr0
lxc restart fiware-1:vm-test1
```

Option B : Ajouter directement à la VM :
```bash
lxc config device add fiware-1:vm-test1 eth0 nic nictype=bridged parent=lxdbr0
lxc restart fiware-1:vm-test1
```

**Vérification** :
Après redémarrage (attendre 30-40 secondes), la VM devrait avoir une IP :
```bash
lxc list fiware-1:
# IPV4 = 192.168.1.xxx (enp5s0)
```

---

## ✅ Déploiement Docker réussi dans la VM

### Résumé des étapes qui ont fonctionné :

1. **Créer la VM avec --vm** :
   ```bash
   lxc launch ubuntu:22.04 fiware-1:vm-achref-log430 --vm
   ```

2. **Ajouter l'interface réseau au profil** :
   ```bash
   lxc profile device add fiware-1:default eth0 nic nictype=bridged parent=lxdbr0
   lxc restart fiware-1:vm-achref-log430
   ```

3. **Installer Docker et Git** :
   ```bash
   lxc exec fiware-1:vm-achref-log430 -- bash -c "apt update ; apt install -y git docker.io docker-compose"
   ```

4. **Cloner le repository** :
   ```bash
   lxc exec fiware-1:vm-achref-log430 -- bash -c "cd ~ ; git clone https://github.com/AchrefSamoud/log430_labo0_H26.git"
   ```

5. **Builder et lancer l'application** :
   ```bash
   lxc exec fiware-1:vm-achref-log430 -- bash -c "cd ~/log430_labo0_H26 ; docker-compose build"
   lxc exec fiware-1:vm-achref-log430 -- bash -c "cd ~/log430_labo0_H26 ; docker-compose up -d"
   ```

6. **Tester l'application** :
   ```bash
   lxc exec fiware-1:vm-achref-log430 -- bash -c "cd ~/log430_labo0_H26 ; docker-compose exec -T calculator pytest src/tests/ -v"
   ```

**Résultat** : ✅ 7 tests passed in 0.05s

```
