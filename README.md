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
    Automatically test your functions to see if you have changed their behavior by mistake!
    <br />
<!--
    <a href="https://github.com/NicolasMICAUX/autotestreg"><strong>Explore the docs »</strong></a>
-->
    <br />
    <br />
    <a href="https://github.com/NicolasMICAUX/autotestreg">View Demo</a>
    ·
    <a href="https://github.com/NicolasMICAUX/autotestreg/issues">Report Bug</a>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [Screen Shot][product-screenshot] -->
Have you ever spent hours reworking someone else's code, trying not to break anything, only to realize at the last moment that something doesn't work anymore, but not knowing at which step you introduced the bug? So frustrating!

AutoTest!Reg allows you to automatically track the code you are working on and not introduce any regression, without writing a single test!

<!-- GETTING STARTED -->
## Getting Started
Using AutoTest!Reg requires no effort at all!

Install AutoTest!Reg with pip :
```sh
pip install autotestreg
```

Import AutoTest!Reg into your tests, adding this line:
```python
import autotestreg
```

To follow a function `my_func`, this code is all you need:
```python
from autotestreg import autotest_func

def my_func():
    ...

autotest_func(my_func)
```

To track an entire module `mypackage`, with all the functions and methods it contains:
```python
from autotestreg import autotest_module
import mypackage

autotest_module(mypackage)
```

<!-- USAGE EXAMPLES -->
## Next
If no regression was introduced when you modified the code, your tests will pass.

Otherwise, AutoTest!Reg will give you the function whose behavior was changed.

## Advanced usage
You can use AutoTest!Reg as a pre-commit hook:  
1. Create some test files using `autotestreg` (e.g. `some_tests.py`)
  - This file must contain at the top `from autotestreg import set_interactive` and `set_interactive(False)`
2. Modify the pre-commit hook script: `touch .git/hooks/pre-commit`
3. Add this inside:
```bash
#!/bin/sh
# Dont forget to activate your env if needed.
python some_tests.py
```
4. Make the pre-commit file executable: `chmod +x .git/hooks/pre-commit`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing
_(Section in english)_  
I want to add a lot of functionnalities to this project, but I don't have much time to work on it. Contributions are welcome!  

To install in dev mode, use `pip install -e .`

<!-- ROADMAP-->
### Roadmap/todo
<!-- table with columns : task, importance, difficulty, status, description -->
| Task | Importance | Difficulty | Contributor on it | Description  |
|:-----|------------|------------|-------------------|:-------------|
|      | ./5        | ./5        | NOBODY            | _e.g._ : ... |

Non-Code contribution :

| Task | Importance | Difficulty | Contributor on it | Description  |
|:-----|------------|------------|-------------------|:-------------|
|      | ./5        | ./5        | NOBODY            | _e.g._ : ... |


_For every todo, just click on the link to find the discussion where I describe how I would do it._  
See the [open issues](https://github.com/NicolasMICAUX/autotestreg/issues) for a full list of proposed features (and known issues).

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


## Authors
This library was created by [Nicolas MICAUX](https://github.com/NicolasMICAUX).


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
[//]: # ([linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555)
[//]: # ([linkedin-url]: https://linkedin.com/in/othneildrew)
[product-screenshot]: images/screenshot.png

