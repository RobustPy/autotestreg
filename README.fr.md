<a name="readme-top"></a>
[![Contributors][contributors-shield]][contributors-url]<!--[![Forks][forks-shield]][forks-url]-->
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]<!--[![MIT License][license-shield]][license-url]--><!--[![LinkedIn][linkedin-shield]][linkedin-url]-->
[![PyPi version][pypi-shield]][pypi-url]<!--[![Python 2][python2-shield]][python-url]-->
[![Python 3][python3-shield]][python-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/NicolasMICAUX/autotestreg">
    <img src="https://raw.githubusercontent.com/NicolasMICAUX/autotestreg/main/images/logo.png" alt="Logo" width="182" height="143">
  </a>
  <h3 align="center">AutoTest!Reg</h3>
  <p align="center">
Tester automatiquement vos fonctions pour voir si vous avez modifié leur comportement par erreur.<br/>
<!--
    <a href="https://github.com/NicolasMICAUX/autotestreg"><strong>Explorer la documentation »</strong></a>
-->
    <br/><br/>
    <a href="https://github.com/NicolasMICAUX/autotestreg">Voir la démo</a>
    ·
    <a href="https://github.com/NicolasMICAUX/autotestreg/issues">Report Bug</a>
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## Introduction
<!-- [Screen Shot][product-screenshot] -->
Avez vous déjà passé des heures à retravailler le code de quelqu'un d'autre en essayant de ne rien casser, pour vous rendre compte au dernier moment que quelque chose ne marche plus, mais sans savoir à quelle étape vous avez introduit le bug ? Tellement frustrant !

AutoTest!Reg vous permets de suivre automatiquement le code que vous travaillez et de n'introduire aucune régression, sans écrire un seul test !

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>

<!-- GETTING STARTED -->
## Pour commencer
Utiliser AutoTest!Reg ne recquiert quasiment aucun effort.

Installer AutoTest!Reg avec pip :
```sh
pip install autotestreg
```

Importer AutoTest!Reg dans vos tests, en ajoutant cette ligne :
```python
import autotestreg
```

Pour suivre une fonction `my_func`, ce code suffit:
```python
from autotestreg import autotest_func

def my_func():
    ...

autotest_func(my_func)
```

Pour suivre un module entier `mypackage`, avec toutes les fonctions et méthodes qu'il contient:
```python
from autotestreg import autotest_module
import mypackage

autotest_module(mypackage)
```

<p align="right">(<a href="#readme-top">retour en haut</a>)</p>


## Ensuite
Si aucune régression n'a été introduite quand vous modifier le code, vos tests passeront avec succès.

Sinon, AutoTest!Reg vous donnera la fonction dont le comportement a été modifié.
<!-- # todo : GIVE EXAMPLE HERE -->

<!-- 
## Fonctionnalités avancées
<p align="right">(<a href="#readme-top">back to top</a>)</p>
-->


## Usage avancé
Vous pouvez utiliser AutoTest!Reg comme un pre-commit hook:
1. Créez des fichiers de test en utilisant `autotestreg` (par exemple `some_tests.py`)
  - Ce fichier doit contenir en haut `from autotestreg import set_interactive` et `set_interactive(False)`
2. Modifiez le script de pre-commit hook: `touch .git/hooks/pre-commit`
3. Ajoutez ceci à l'intérieur:
```bash
#!/bin/sh
# N'oubliez pas d'activer votre env si nécessaire.
python some_tests.py
```
4. Rendez le fichier pre-commit exécutable: `chmod +x .git/hooks/pre-commit`

<!-- CONTRIBUTING -->
## Contributing
_(Section in english)_  
I want to add a lot of functionnalities to this project, but I don't have much time to work on it. Contributions are welcome!  

<!--
### Roadmap/todo
| Task | Importance | Difficulty | Contributor on it | Description  |
|:-----|------------|------------|-------------------|:-------------|
|      | ./5        | ./5        | NOBODY            | _e.g._ : ... |

Non-Code contribution :

| Task | Importance | Difficulty | Contributor on it | Description  |
|:-----|------------|------------|-------------------|:-------------|
|      | ./5        | ./5        | NOBODY            | _e.g._ : ... |


_For every todo, just click on the link to find the discussion where I describe how I would do it._  
See the [open issues](https://github.com/NicolasMICAUX/autotestreg/issues) for a full list of proposed features (and known issues).
-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### How to contribute
Contributing is an awesome way to learn, inspire, and help others. Any contributions you make are **greatly appreciated**, even if it's just about styling and best practices.

If you have a suggestion that would make this project better, please fork the repo and create a pull request.  
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/YourAmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Auteurs
Cette librairie a été crée par [Nicolas MICAUX](https://github.com/NicolasMICAUX).



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/NicolasMICAUX/autotestreg.svg?style=for-the-badge
[contributors-url]: https://github.com/NicolasMICAUX/autotestreg/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/NicolasMICAUX/autotestreg.svg?style=for-the-badge
[stars-url]: https://github.com/NicolasMICAUX/autotestreg/stargazers
[issues-shield]: https://img.shields.io/github/issues/NicolasMICAUX/autotestreg.svg?style=for-the-badge
[issues-url]: https://github.com/NicolasMICAUX/autotestreg/issues
[pypi-shield]: https://img.shields.io/pypi/v/autotestreg.svg?style=for-the-badge
[pypi-url]: https://pypi.org/project/autotestreg/
[python2-shield]: https://img.shields.io/badge/python-2.7+-blue.svg?style=for-the-badge
[python3-shield]: https://img.shields.io/badge/python-3.5+-blue.svg?style=for-the-badge
[python-url]: https://www.python.org/downloads/

[//]: # ([license-shield]: https://img.shields.io/github/license/NicolasMICAUX/autotestreg.svg?style=for-the-badge)
[//]: # ([license-url]: https://github.com/NicolasMICAUX/autotestreg/blob/master/LICENSE.txt)
[//]: # ([product-screenshot]: images/screenshot.png)

