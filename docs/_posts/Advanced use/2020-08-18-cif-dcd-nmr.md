---
layout: post
title: "NMR models, mmCIF files, and DCD trajectory files parsers"
category: advanced-use
author: jr
short-description: CAVIAR is now able to process frames from MD trajectories, and structures from cryoEM in mmCIF format 
---

-----

News from mid August 2020: I just added parsers for iterating through all NMR models in a PDB file, reading mmCIF files and DCD trajectory files from MD simulations.  

##### Disclaimers
- These functionalities are excluded from the caviar_gui and restricted to the command line tool.  
- A maximum grid size parameter has been set up. The default is 10 million grid points, which represent about 12 gb of max memory usage for the cavity detection algorithm. Therefore, some very large mmCIF structures might be rejected by default: in that case, be sure to have a lot of RAM available, and increase the 'size_limit' parameter in a [custom configuration file]({{ site.baseurl }}{% link _posts/Advanced use/2020-04-22-configuration.md %})).  

##### mmCIF
A command line option has been added to request parsing an mmCIF file. This option is ```-cif```.  
If the option -cif is set to true, CAVIAR looks for a .cif file in -sourcedir, or downloads it from the RCSB PDB. In that case, even if a PDB file exists, it will download the file in **CIF** format.  
If the option -cif is not set, CAVIAR *can also end up parsing a CIF file*. The new behavior is that CAVIAR will first look for a PDB file on RCSB PDB webservers, and if it does not find it, it will look for a CIF file corresponding to this code.  
Metadata is not parsed (yet) for mmCIF files.  

Example usage:  
```caviar -cif True -code 4qsr``` will work on 4qsr with the mmCIF file format rather than the PDB format. The value of this is actually lower than using the PDB format, as long as I did not implement a mmCIF header metadata parser.
```caviar -cif True -code 6zme -custom_config conf.cfg``` will work on 6zme, which exists only in mmCIF format. The file ```conf.cfg``` needs to contain ```size_limit: 30000000```, and the computer on which calculations happen need to have probably more than 30 gb of RAM for such a huge structure (size of the box of roughly 300\*300\*300 Angstroms!!).  

##### DCD molecular dynamics trajectories
All frames of a DCD trajectory file can be processed iteratively. Each frame gets its own report and its own PDB file containing its cavities/subcavities. That can take a lot of disk space, so be sure to preprocess the trajectory files beforehand! CAVIAR does not, and may never, contain advanced functionalities for MD trajectories. For easing the analysis, it is advisable to align the frames beforehand and filter them in some ways. For example, one can cluster the frame and limit the analysis to the cluster representatives. I can also heavily recommend the wonderful methods of Vitalis and coworkers to identify metastable states in MD trajectories and plot them as so-called "SAPPHIRE plots" ([ref 1, figures 1 and 2](https://www.nature.com/articles/srep06264), [ref 2, figures 6, 8 and 10](https://pubs.acs.org/doi/10.1021/acs.jctc.5b00618), and [tutorial](http://campari.sourceforge.net/V3/tutorial11.html)).  
 <br>
Two arguments are needed for DCD trajectory files: the pdb file needs to be given (via -code) as reference coordinates, and -dcd is used to input the DCD file containing the frames (with path, if in another directory).  

Example usage:  
```caviar caviar -dcd mdm2.dcd -code mdm2.pdb -sourcedir ./``` will use the structure file mdm2.pdb in the local working directory as template for the frames of mdm2.dcd (also, in that case in the local working directory, otherwise the path needs to be specified alongside the file name). The two example files mdm2.dcd and mdm2.pdb can be found on [ProDy servers](http://prody.csb.pitt.edu/tutorials/trajectory_analysis/trajectory_analysis_files.tgz).

The output tables will now contain an additional tag for easing the analysis in the PDB_chain field. In this case, it contains PDBname_chain_f{nb}, where {nb} is the frame number starting from 1.  
Example:   
<blockquote>
PDB_chain    CavID Ligab  Score  Size Hydrophob InterCh  AltLoc Miss  Subcavs
mdm2_P_f1      1    0.8    0.4    44     84%       0       0     0       1
PDB_chain    CavID SubCavID Size Hydrophob. Polar  Neg   Pos  Other
mdm2_P_f1      1      1      44     84%      9%     0%    0%    7%

mdm2_f2 does not have a cavity
mdm2_f3 does not have a cavity
PDB_chain    CavID Ligab  Score  Size Hydrophob InterCh  AltLoc Miss  Subcavs
mdm2_P_f4      1    0.8    1.4   125     74%       0       0     0       2
PDB_chain    CavID SubCavID Size Hydrophob. Polar  Neg   Pos  Other
mdm2_P_f4      1      1      32     78%      22%    0%    0%    0%
mdm2_P_f4      1      2      93     73%      18%    0%    0%    9%
</blockquote>
<br>
The DCD file parser was developped by the ProDy team and tested for 32-bit DCD files (CHARMM format DCD file, also NAMD 2.1 and later, but not X-PLOR format DCD files or NAMD 2.0 and earlier).  

##### NMR structures
All models of the NMR PDB file are investigated iteratively, similarly to what happens with a DCD trajectory.  
A report is printed out for each model, as well as corresponding PDB file containing cavities/subpockets.  
Nothing particular needs to be done for this scenario, CAVIAR detects automatically the NMR tag in the metadata of the PDB file and sets up the routines for analyzing all models. The output resembles the tables copied in the DCD paragraph.  

<br><br><br>
A huge thanks to the [ProDy team](https://github.com/prody/ProDy). The parsers relies on their software, they are doing an amazing job.  