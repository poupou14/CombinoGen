from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize( "CombinoSource.pyx")
)
setup(
    ext_modules = cythonize( "Match.pyx")
)
setup(
    ext_modules = cythonize( "Grille.pyx")
)
setup(
    ext_modules = cythonize( "CombinoEngine.pyx")
)
setup(
    ext_modules = cythonize( "Bet.pyx")
)

