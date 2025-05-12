from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cy_game_logic",
    ext_modules=cythonize("cy_game_logic.pyx", compiler_directives={"language_level": "3"}),
    zip_safe=False,
)
