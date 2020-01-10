from setuptools import setup, find_namespace_packages

with open("README.MD", "r") as fh:
	long_description = fh.read()

setup(
	name="cavitome_gui",
	version="1.0",
	entry_points = {
        'console_scripts': [ 'cavitome_gui=cavitome_gui.gui:main']
        },
    author="Jean-Remy Marchand",
	author_email="jeanremy.marchand@gmail.com",
	description="A GUI for the automatic detection of protein cavities and their segmentation in subcavities",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jr-marchand/cavitome",

	# When your source code is in a subdirectory under the project root, e.g.
	# `cavitome_gui/`, it is necessary to specify the `package_dir` argument.
	package_dir={'':'src'},	# tell distutils packages are under cavitome_gui

	# You can just specify package directories manually here if your project is
	# simple. Or you can use find_packages().
	#
	# Alternatively, if you just want to distribute a single Python file, use
	# the `py_modules` argument instead as follows, which will expect a file
	# called `my_module.py` to exist:
	#
	#	py_modules=["my_module"],
	packages=find_namespace_packages(where='src'), # include all packages under cavitome_gui

	#package_data={'':['cavitome_gui/*ui', "cavitome_gui/prody_parser/utilities/datafiles/mod_res_map.dat",
	#"cavitome_gui/misc_tools/tabu_lists/tabu*", 'cavitome_gui/cavity_identification/vdw_size_atoms.dat']},
	include_package_data=True,

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
