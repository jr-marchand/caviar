"""
Module for generating a .pml file from the caviar GUI.
"""


def write_pmlfile(cavity_file, what = None, outputfile = "visualize_cavities.pml"):

	output = ""
	###### COMMON ######
	# Load file, make the spheres smaller for nicer visualization, zoom and center on the first cavity
	output+=str(f"load {cavity_file}\nset sphere_scale, 0.1\ncenter resname GRI and resid 1 ; zoom center, 15\n")
	
	###### BY BURIEDNESS ######
	if what == "buriedness":
		output+=str(f"spectrum b, blue_white_red, selection = resname GRI, minimum=8, maximum=14\n"
		f"sele middle, b < 3 and resname GRI\n"
		f"color yellow, middle\n")
	
	###### BY PHARMACOPHORE ######
	elif what == "pharmacophore":
		output+=str(f"# Select the different pharmacophoric groups \n"
		f"sele aliphatic, resn GRI and q <1.1 and q >0.9\n"
		f"sele aromatic, resn GRI and q <2.1 and q >1.9\n"
		f"sele donor, resn GRI and q <3.1 and q >2.9\n"
		f"sele acceptor, resn GRI and q <4.1 and q >3.9\n"
		f"sele doneptor, resn GRI and q <5.1 and q >4.9\n"
		f"sele negative, resn GRI and q <6.1 and q >5.9\n"
		f"sele positive, resn GRI and q <7.1 and q >6.9\n"
		f"sele cys, resn GRI and q <8.1 and q >7.9\n"
		f"sele his, resn GRI and q <9.1 and q >8.9\n"
		f"sele metal, resn GRI and q <10.1 and q >9.9\n"
		f"sele none_, resn GRI and q < 0.01\n"
		f"# Color the different pharmacophoric groups \n"
		f"color grey, aliphatic\n"
		f"color palecyan, aromatic\n"
		f"color blue, donor\n"
		f"color red, acceptor\n"
		f"color green, doneptor\n"
		f"color firebrick, negative\n"
		f"color purple, negative\n"
		f"color yellow, cys\n"
		f"color brown, his\n"
		f"color pink, metal\n"
		f"color black, none_\n")
	
	###### BY CHAIN ######
	elif what == "bychain":
		output+=str(f"util.chainbow('resname GRI')\n")

	a = open(outputfile, "w")
	a.write(output)
	a.close()

	return None


def write_pmlsubcavs(cavity_file, outputfile = "visualize_subcavs.pml"):
	output = ""
	###### COMMON ######
	# Load file, make the spheres smaller for nicer visualization, zoom and center on the first cavity
	output+=str(f"load {cavity_file}\nset sphere_scale, 0.1\ncenter resname GRI and resid 1 ; zoom center, 15\n")
	output+=str(f"spectrum resi,  2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21, resname SUB\n")

	a = open(outputfile, "w")
	a.write(output)
	a.close()

	return None
