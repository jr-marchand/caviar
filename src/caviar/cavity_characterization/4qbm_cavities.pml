load /home/marchje7/cavities/cavitome_gui/cavitome_gui/src/caviar_gui/cavity_characterization//caviar_out/4qbm_cavs.pdb
set sphere_scale, 0.1
center resname GRI and resid 1 ; zoom center, 15
spectrum b, blue_white_red, selection = resname GRI, minimum=8, maximum=14
sele middle, b < 3 and resname GRI
color yellow, middle
