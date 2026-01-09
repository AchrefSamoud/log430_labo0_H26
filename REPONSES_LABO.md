# Réponses aux questions du Laboratoire 0

**Étudiant** : Achref Samoud  
**Date** : 8 janvier 2026  
**Cours** : LOG430 - Architecture logicielle

---

## Question 1 : Sortie de pytest en cas d'erreur

Pour démontrer la sortie de pytest en cas d'erreur, je vais créer un test qui échoue volontairement.

### Test modifié avec une erreur volontaire

Modifions temporairement le fichier `src/tests/test_calculator.py` pour qu'un test échoue :

```python
def test_addition_fail():
    calc = Calculator()
    result = calc.addition(2, 2)
    assert result == 5  # Erreur volontaire : 2+2 ne fait pas 5
```

### Sortie de pytest avec l'erreur

```bash
$ docker-compose exec -T calculator pytest src/tests/ -v

============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 -- /usr/local/bin/python3.11
cachedir: .pytest_cache
rootdir: /app
configfile: pyproject.toml
collecting ... collected 8 items

src/tests/test_calculator.py::test_app PASSED                            [ 12%]
src/tests/test_calculator.py::test_addition PASSED                       [ 25%]
src/tests/test_calculator.py::test_addition_fail FAILED                  [ 37%]
src/tests/test_calculator.py::test_subtraction PASSED                    [ 50%]
src/tests/test_calculator.py::test_multiplication PASSED                 [ 62%]
src/tests/test_calculator.py::test_division PASSED                       [ 75%]
src/tests/test_calculator.py::test_division_by_zero PASSED               [ 87%]
src/tests/test_calculator.py::test_last_result PASSED                    [100%]

=================================== FAILURES ===================================
________________________________ test_addition_fail ____________________________

    def test_addition_fail():
        calc = Calculator()
        result = calc.addition(2, 2)
>       assert result == 5
E       assert 4 == 5

src/tests/test_calculator.py:18: AssertionError
=========================== short test summary info ============================
FAILED src/tests/test_calculator.py::test_addition_fail - assert 4 == 5
========================= 1 failed, 7 passed in 0.06s ==========================
```

### Analyse de la sortie d'erreur

Pytest fournit plusieurs informations importantes :

1. **Section FAILURES** : Montre le détail de chaque test échoué
2. **Ligne du fichier** : `src/tests/test_calculator.py:18` indique exactement où l'erreur s'est produite
3. **Type d'erreur** : `AssertionError` - l'assertion a échoué
4. **Valeurs comparées** : `assert 4 == 5` montre la valeur réelle (4) vs la valeur attendue (5)
5. **Résumé** : `1 failed, 7 passed in 0.06s` donne un aperçu rapide du résultat

---

## Question 2 : Sortie de GitHub Actions pour les tests

### Workflow CI/CD configuré

Le fichier `.github/workflows/ci.yml` exécute automatiquement les tests à chaque push :

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: pytest src/tests/ -v
```

### Sortie de GitHub Actions (tests réussis)

```
Run pytest src/tests/ -v
============================= test session starts ==============================
platform linux -- Python 3.11.10, pytest-9.0.2, pluggy-1.6.0 -- /opt/hostedrunner/Python/3.11.10/x64/bin/python
cachedir: .pytest_cache
rootdir: /home/runner/work/log430_labo0_H26/log430_labo0_H26
configfile: pyproject.toml
collecting ... collected 7 items

src/tests/test_calculator.py::test_app PASSED                            [ 14%]
src/tests/test_calculator.py::test_addition PASSED                       [ 28%]
src/tests/test_calculator.py::test_subtraction PASSED                    [ 42%]
src/tests/test_calculator.py::test_multiplication PASSED                 [ 57%]
src/tests/test_calculator.py::test_division PASSED                       [ 71%]
src/tests/test_calculator.py::test_division_by_zero PASSED               [ 85%]
src/tests/test_calculator.py::test_last_result PASSED                    [100%]

============================== 7 passed in 0.03s ===============================
```

### Informations affichées par GitHub Actions

- **Environnement** : `ubuntu-latest` avec Python 3.11.10
- **Chemin Python** : `/opt/hostedrunner/Python/3.11.10/x64/bin/python`
- **Répertoire de travail** : `/home/runner/work/log430_labo0_H26/log430_labo0_H26`
- **Statut de chaque test** : PASSED/FAILED avec pourcentage de progression
- **Temps d'exécution** : 0.03s (très rapide dans l'environnement GitHub)
- **Badge de statut** : ✅ All checks have passed (visible dans le PR/commit)

---

## Question 3 : Sortie de la commande `top` dans la VM

### Commande exécutée

```bash
lxc exec fiware-1:vm-achref-log430 -- top -b -n 1
```

### Sortie de la commande top

```
top - 19:17:13 up 11 min,  0 users,  load average: 0.00, 0.02, 0.00
Tasks:  79 total,   1 running,  78 sleeping,   0 stopped,   0 zombie
%Cpu(s):  6.2 us,  0.0 sy,  0.0 ni, 93.8 id,  0.0 wa,  0.0 hi,  0.0 si, 0.0 st
MiB Mem :   3649.5 total,   2258.3 free,    189.0 used,   1202.1 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   3393.6 avail Mem

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
   2311 root      20   0   10768   3820   3212 R   6.2   0.1   0:00.01 top
      1 root      20   0  167328  12976   8464 S   0.0   0.3   0:03.47 systemd
    214 root      20   0 1239648  16608  11840 S   0.0   0.4   0:00.76 dockerd
    396 root      20   0 1251796  35524  23144 S   0.0   1.0   0:00.42 containerd
   1373 root      20   0 1728744  50940  35812 S   0.0   1.4   0:00.32 dockerd
   1687 root      20   0 1922192  79736  56352 S   0.0   2.1   0:04.23 containerd-shim
```

### Analyse des informations

**Ressources système** :
- **Uptime** : 11 minutes (VM récemment créée)
- **Load average** : 0.00, 0.02, 0.00 (charge très faible, système inactif)
- **Mémoire** : 3649.5 MB total, 2258.3 MB libre (61% libre)
- **Swap** : 0 MB (pas de swap configuré dans la VM)
- **CPU** : 93.8% idle (système très peu utilisé)

**Processus Docker actifs** :
- **PID 214** : `dockerd` - Docker daemon
- **PID 396** : `containerd` - Container runtime
- **PID 1373** : `dockerd` (processus secondaire)
- **PID 1687** : `containerd-shim` - Gère le conteneur de la calculatrice

**Utilisation mémoire** :
- `containerd-shim` : 79.7 MB (2.1% RAM) - gère le conteneur calculator
- `dockerd` : 35.5 MB (1.0% RAM)

**Observations** :
- La VM utilise très peu de ressources (< 200 MB RAM utilisée pour le système)
- Docker et ses processus sont actifs et fonctionnels
- Le conteneur de la calculatrice est géré par `containerd-shim`
- Aucun problème de ressources détecté

---

## Conclusion

✅ **Tous les tests passent** dans les environnements suivants :
1. Localement avec Docker (7/7 tests)
2. GitHub Actions CI/CD (7/7 tests)
3. VM LXD sur fiware-1 avec Docker (7/7 tests)

✅ **Configuration réussie** :
- Application Python avec pytest
- Docker et docker-compose
- GitHub Actions workflow
- VM LXD (VIRTUAL-MACHINE) avec Docker fonctionnel

✅ **Documentation complète** :
- FEEDBACK_README.md documente tous les problèmes et solutions
- Toutes les erreurs du README ont été identifiées et corrigées
