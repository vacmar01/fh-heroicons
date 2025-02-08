# fh-heroicons

Any use of the code retrieved from [heroicons.com](https://heroicons.com/) is subject to the terms of the Heroicons license, found [here](https://github.com/tailwindlabs/heroicons/blob/master/LICENSE).

-----

This is a small library that let's you use `heroicons` as FastHTML `ft` components: 

* Only saves the icons you use
* Icons are downloaded on the first use and cached locally in your working directory. 
* full customization through css


## Installation

```bash
pip install git+https://github.com/vacmar01/fh-heroicons.git
```

## Usage

```python
from fh_heroicons import Heroicon

Heroicon("academic-cap", style="color: red")
```

You can pass any valid heroicon icon name to `Heroicon`. A full searchable list of icons can be found [here](https://heroicons.com/).

You can also specify which variant of the icons (`outline` or `solid`, default to `outline`) you want by adding the `variant` attribute to `Heroicon`. 

```python
Heroicon("academic-cap", variant="solid")
```

## Caveat
This is very much wip as well as my first python library ever. So please treat it gently. 

## License

The library is distributed under the MIT LICENSE.