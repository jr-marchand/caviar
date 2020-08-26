from setuptools import setup, find_namespace_packages, Extension
from os.path import join, isfile
import platform, os


with open("README.MD", "r") as fh:
	long_description = fh.read()




####### FROM ProDy ######
from glob import glob
tntDir = join('src', 'caviar', 'prody_parser', 'utilities', 'tnt')

import numpy as np

EXTENSIONS = [
    Extension('caviar.prody_parser.kdtree._CKDTree',
              sources = [join('src', 'caviar', 'prody_parser', 'kdtree', 'KDTree.c'),
              join('src', 'caviar', 'prody_parser', 'kdtree', 'KDTreemodule.c')],
              include_dirs=[join(np.get_include(), 'numpy'), np.get_include()]),
    Extension('caviar.prody_parser.proteins.ccealign',
              sources = [join('src', 'caviar', 'prody_parser', 'proteins', 'ccealign', 'ccealignmodule.cpp')],
              include_dirs=[tntDir], language='c++')
]


####### END ProDy ######

setup(
	name="caviar",
	version="1.1.0",
	entry_points = {
        'console_scripts': [ 'caviar_gui=caviar.gui:main', 'caviar=caviar.caviar:main']
        },
    author="Jean-Remy Marchand",
	author_email="jeanremy.marchand@gmail.com",
	description="A toolkit for the automatic detection of protein cavities and their segmentation in subcavities",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jr-marchand/CAVIAR",

	# When your source code is in a subdirectory under the project root, e.g.
	# `caviar_gui/`, it is necessary to specify the `package_dir` argument.
	package_dir={'':'src'},	# tell distutils packages are under caviar_gui

	# You can just specify package directories manually here if your project is
	# simple. Or you can use find_packages().
	#
	# Alternatively, if you just want to distribute a single Python file, use
	# the `py_modules` argument instead as follows, which will expect a file
	# called `my_module.py` to exist:
	#
	#	py_modules=["my_module"],
	packages=find_namespace_packages(where='src'), # include all packages under caviar_gui

	#package_data={'':['caviar_gui/*ui', "caviar_gui/caviar.prody_parser_parser/utilities/datafiles/mod_res_map.dat",
	#"caviar_gui/misc_tools/tabu_lists/tabu*", 'caviar_gui/cavity_identification/vdw_size_atoms.dat']},
	include_package_data=True,
	ext_modules=EXTENSIONS,

	#install_requires=['numpy>=1.17.3',
	#'scipy>=1.3.1',
	#'networkx>=2.3',
	#'scikit-image>=0.16.2',
	##'PyQt5-sip==4.19.19',
	##'sip==4.19.8',
	#'PyQt5==5.9.2',
	#'pyparsing>=2.4.2'],
	classifiers=[
	"Programming Language :: Python :: 3",
	"License :: OSI Approved :: MIT License",
	"Operating System :: OS Independent",
	],

	#setup_requires=['pytest-runner'],
	#tests_require=['pytest'],
)
