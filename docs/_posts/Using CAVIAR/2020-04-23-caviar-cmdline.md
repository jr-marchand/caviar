---
layout: post
title: "Command line use"
category: using-caviar
author: jr
short-description: Batch use 
---

-----

Once you have installed CAVIAR and activated the environment ([--> installation <--]({% link _posts/Using CAVIAR/2020-04-24-installation.md %})), you can call the command line instance of CAVIAR simply with:  
```caviar -h```

This will trigger the presentation of the tool. The most basic use only requires a PDB code:  
```caviar -code 1dwc```

### Terminal output
The output is visualized in the terminal as a table. The first table contains the list of identified cavities, ranked by cavity score.  



| PDB_chain | CavID  | Ligab.  |  Score |  Size | Hydrophob | Interchain | AltLocs | MissAtoms |
| --------- |------- | ------- | ------ | ----- | --------- | ---------- | ------- | ------ |
| 1dwc_H    |     1  |   0.6   |   3.7  | 333   |   39%     |     0      |    0    |    0   |
| 1dwc_H    |     2  |   0.2   |   0.9  |   51  |   10%     |     0      |    0    |    0   |
| 1dwc_H    |     3  |   0.8   |   0.6  |   63  |   56%     |     0      |    0    |    0   |
{:.table.table-scroll}
   

- PDB_chain = PDB code underscore chain identifier (here, PDB 1dwc, chain H)
- CavID = cavity identifier
- Ligab. = ligandability estimator
  - [0.0 - 0.2] = likely hard to ligand  
  - [0.4 - 0.6] = not conclusive  
  - [0.8 - 1.0] = probably easy to ligand
- Score = cavity score, scales with size and buriedness: the bigger and the more buried, the higher the score.  
- Hydrophob = hydrophobicity, count of aliphatic+aromatic grid points / total number of grid points.  
- Interchain = is the cavity in between two protein chains? (Boolean) Some interfaces are spurious (crystal contacts), some are productive (biological interfaces). Please keep that in mind when analysing the results.  
- AltLocs = Does the cavity contain residues alternate locations? (Boolean)  
- MissAtoms = Does the cavity contain missing atoms or residues? (Boolean) We advise to be very careful with cavities containing missing atoms, as they may be very noisy or even spurious.


### Generated files
In addition, CAVIAR generates by default a certain number of files in the working directory:

<blockquote>
<p>
|-- . <br>
|-- 1dwc_cavities.pml<br>
|-- 1dwc_subcavities.pml<br>
|-- caviar_out/<br>
&nbsp;&nbsp;&nbsp;&nbsp;|-- 1dwc_cavs.pdb<br>
&nbsp;&nbsp;&nbsp;&nbsp;|-- 1dwc_subcavs.pdb
</p>
</blockquote>



The two \*.pml files are pymol session files to automatically open and visualize the PDB file and its cavities or subcavities, respectively. The folder caviar_out/ contains the original PDB file with at the end, the cavities with the residue name GRI and the subcavities as SUB. Cavities contain as b factor the buriedness for each cavity grid point (from 8 to 14, with 14 being the most buried) and as occupancy field the pharmacophore type of the grid point, i.e., the chemical type of the closest atom of the protein. By default, the coloring of cavities is one color per cavity, but this can be changed for a coloring by buriedness or pharmacophore types, with a legend (cf command line arguments section). Cavities are ordered as in the printout, with the first cavity being represented in the PDB file as resname GRI, chain A, residue index 1. The second cavity is GRI A 2, and so forth.  
Subcavities are ordered iteratively and correspond to the cavities they come from, but we have to separate both the different cavities *and* the different subcavities. Therefore, subcavity 1 of cavity 1 is represented as resname SUB, chain A, residue index 1. Subcavity 2 of cavity 1 is SUB A 2. Subcavity 1 of cavity 2 is SUB B 1.  
To come back to our example with 1dwc, it contains three cavities, represented in the PDB file as residue name "GRI" (default for any cavity), chain identifier A (default for any cavity) and residue indices 1, 2 and 3 (identifies the 3 cavities as different).  
The first cavity (resname GRI, chain A, resid 1) contains 4 subcavities. These 4 subcavities are named resname SUB (default for any subcavity), chain A (identifies the first cavity), residue identifiers 1 to 4 (identifies the 4 subcavities of said cavity).  


### Command line arguments

```caviar``` handles both command line arguments and the use of parameter/configuration files.  
We already saw one command line argument earlier: ```-code``` option to specify a PDB code.  

- ```-code``` will download the file from the RCSB PDB if it is not present in ```-sourcedir```.  
- ```-sourcedir``` is the folder in which the PDB file is, in case you already downloaded it.  
- ```-what``` defines what objects to select from the PDB file: all protein chains (keyword "allproteins"), just the longest chain ("longestchain"), or the longest chain plus contacting chains at 5A (longestandcontacting).   
- ```-chain_id``` permits to select a priori a certain protein chain or more than one protein chains. For example, if you want to select the chain A, simply define ```-chain_id A```, but if you want to investigate chains A and B, specify both as ```-chain_id AB```.  
- ```-color_cavs_by``` defines the coloring scheme mentioned a bit before. Generates a pymol \*.pml file that colors cavity by cavity ID (default, "bychain"), by buriedness ("buriedness"), or by corresponding protein pharmacophore type ("pharmacophore").  
- ```-subcavs_decomp``` to inactivate the subcavities decomposition (boolean).  
- ```-out``` to define an output path (default: ./caviar_out/).  
- ```-v``` to activate verbosity.  
- ```-preset_config``` gives the choice between three presets default configuration: search for cavities and decompose them into subcavities (default, "default"), only search for cavities ("cavities_only"), or only export subcavities ("subcavities_only").  

### Configuration file 

```caviar``` can take as unique argument, or in addition to command line arguments, a configuration file containing any of the parameters.

- ```-custom_config``` gives the possibility to use a custom configuration file created by the user.  

This file needs to follow the standard set by [--> configparse <--](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure).

<blockquote><p>
[Simple Values]<br>
key=value<br>
spaces in keys=allowed<br>
spaces in values=allowed as well<br>
spaces around the delimiter = obviously<br>
you can also use : to delimit keys from values<br>
<br>
[All Values Are Strings]<br>
values like this: 1000000<br>
or this: 3.14159265359<br>
are they treated as numbers? : no<br>
integers, floats and booleans are held as: strings<br>
can use the API to get converted values directly: true<br>
<br>
[Multiline Values]<br>
chorus: I'm a lumberjack, and I'm okay<br>
    I sleep all night and I work all day<br>
<br>
[No Values]<br>
key_without_value<br>
empty string value here =<br>
<br>
[You can use comments]<br>
# like this<br>
; or this<br>
<br>
# By default only in an empty line.<br>
# Inline comments can be harmful because they prevent users<br>
# from using the delimiting characters as parts of values.<br>
# That being said, this can be customized.<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;[Sections Can Be Indented]<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;can_values_be_as_well = True<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;does_that_mean_anything_special = False<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;purpose = formatting for readability<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;multiline_values = are<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;handled just fine as<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;long as they are indented<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;deeper than the first line<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;of a value<br>
&nbsp;&nbsp;&nbsp;&nbsp;# Did I mention we can indent comments, too?<br>
</p>
</blockquote>

Many parameters can be set in the configuration file and can be found in the advanced use section (```link it once it's written!```).


### Final wrapping up example 

Now let us make a final example combining all of the above. We want to check only subcavities of PDB 1dwc (human Thrombin (protease), in complex with an inhibitor), present in chain H, output in the folder "~/thrombin_caviar_out/" and we have already downloaded the PDB at ~/1dwc.pdb.  
```caviar -code 1dwc -sourcedir ~/ -chain_id H -preset_config subcavities_only -out ~/thrombin_caviar_out/ ```

This is equivalent to the following:  
```caviar -custom_config ~/custom_config.cfg```  

where ~/custom_config.cfg is:
<blockquote><p>
### Example of custom parameter file for CAVIAR ###  <br>
 <br>
[custom] # At least one section header is necessary, the name does not matter <br>
 <br>
 &nbsp;&nbsp;sourcedir: ~/    # Source directory, otherwise downloads file  <br>
 &nbsp;&nbsp;code: 1dwc       # PDB Code (no default)  <br>
 &nbsp;&nbsp;chain_id: H      # Protein chain identifier of interest<br>
 &nbsp;&nbsp;preset_config subcavities_only  # We want only subcavities<br>
 &nbsp;&nbsp;out: ~/thrombin_caviar_out/ # Path/to/outfolder<br>
</p>
</blockquote>
