def main():

	import sys
	#try:
		# tweak to import sip from PyQt 5.11
		#from PyQt5 import QtCore
		#import sip
		# end of tweak
	from PyQt5 import QtWidgets, uic
	from PyQt5.QtWidgets import QFileDialog
	from caviar import cavity_detect_gui
	#except:
	#	print("It looks like we're missing some libraries here!")
	#	print("Please install PyQt5, scipy, numpy, pyparse, skimage and networkx:")
	#	print("conda install -c conda-forge pyparsing numpy scipy networkx scikit-image pyqt")
	#	sys.exit()

	import os 
	dir_path = os.path.dirname(os.path.realpath(__file__))
	local = os.getcwd()

	qtcreator_file  = os.path.join(dir_path, "cavity.ui") # Enter file here.
	Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


	qtcreator_subcav  = os.path.join(dir_path, "subcavity.ui") # Enter file here.
	Ui_SubCav, QtBaseClass2 = uic.loadUiType(qtcreator_subcav)



	class Cavity(QtWidgets.QWidget, Ui_MainWindow):
		def __init__(self):
			QtWidgets.QMainWindow.__init__(self)
			Ui_MainWindow.__init__(self)
			self.setupUi(self)
			self.run.clicked.connect(self.find_cavities)
			self.button_close.clicked.connect(self.close)
			self.button_browse.clicked.connect(self.getfile)
	
	
		def getfile(self):
			fname = QFileDialog.getOpenFileName(self, 'Open file', 
				'./',"PDB files (*.pdb)")[0]
			self.input_filename.setText((fname))
	
		def find_cavities(self):
			
			try:
				input_filename = self.input_filename.text()
			except:
				input_filename = None
			global code
			if input_filename:
				code = os.path.split(input_filename)[-1]
				sourcedir = os.path.split(input_filename)[0:-1][0]
			else:
				code = self.code.text()
				sourcedir = local
			if not ".pdb" in code:
				code = str(code+".pdb")
			try:
				chain = self.chain_id.text()
				user_chain = True
			except:
				user_chain = False
			exclude_missing = self.exclude_missing.isChecked()
			exclude_interchain = self.exclude_interchain.isChecked()
	
			#try:
			parser = cavity_detect_gui.arguments()
			global args
			if user_chain:
				args = parser.parse_args(["-sourcedir", sourcedir, "-code", code, "-user_chain",
					str(user_chain), "-chain_id", chain,
					"-exclude_missing", str(exclude_missing), "-exclude_interchain", str(exclude_interchain)])
			else:
				args = parser.parse_args(["-sourcedir", sourcedir, "-code", code,
				"-exclude_missing", str(exclude_missing), "-exclude_interchain", str(exclude_interchain)])
			
			global data4subcav
			#try:
				#print(args)
			cavity_detect_gui.run(args)
			report, cavity_file, data4subcav = cavity_detect_gui.run(args)
			#except:
			#	report = self.OutputTextBrowser.setText(f"CAVIAR does not detect any cavity in {code[:-4]} with this set of parameters.\n")
			#	return None
			# Now write the pml file
			from caviar.misc_tools.gen_pmlfile import write_pmlfile
			if self.bypharma.isChecked():
				what = "pharmacophore"
			elif self.byburi.isChecked():
				what = "buriedness"
			elif self.bycav.isChecked():
				what = "bychain"
			else:
				what = None
			abs_cavfile = os.path.join(local, "caviar_out", cavity_file)
			write_pmlfile(cavity_file = abs_cavfile, what = what, outputfile = str(code[:-4]+"_cavities.pml"))
		
			# Print output in results and log
			self.OutputTextBrowser.setText(report)
		
			if self.pymol.isChecked():
				#from shutil import which
				try:
					import pymol
					_file = str(os.path.join(local,str(code[:-4]+"_cavities.pml")))
					pymol.finish_launching(['pymol', _file])
				except:
					try:
						import subprocess
						subprocess.Popen(["pymol "+ os.path.join(local,str(code[:-4]+"_cavities.pml"))], shell=True,
						stdin=None, stdout=None, stderr=True, close_fds=True)
					except:
						self.OutputTextBrowser.append("Could not open PyMOL: please set up a variable 'pymol' in your terminal")
				
			# Here open subcavity windows
			window_subcav = SubCav()
			window_subcav.show()
	
			#except:
			#	self.OutputTextBrowser.setText("Hey! You forgot to give me a PDB file/code :( (mmCIF not yet supported)")
	
	
	class SubCav(QtWidgets.QWidget, Ui_SubCav):
		def __init__(self):
			QtWidgets.QMainWindow.__init__(self)
			Ui_MainWindow.__init__(self)
			self.setupUi(self)
			self.run_subcavs.clicked.connect(self.find_subcavities)
			self.button_close_subcavs.clicked.connect(self.close)
	
	
		def find_subcavities(self):
			try:
				cavID = self.cavID.text()
			except:
				cavID = None
	
			report_subcavs, subcavity_file = cavity_detect_gui.runsubcavities(data4subcav, args, cavid = cavID)
			# Now write the pml file
			from caviar.misc_tools.gen_pmlfile import write_pmlsubcavs
			abs_subcavfile = os.path.join(local, "caviar_out", subcavity_file)
			write_pmlsubcavs(cavity_file = abs_subcavfile, outputfile = str(code[:-4]+"_subcavities.pml"))
		
			# Print output in results and log
			self.output_subcavs.setText(report_subcavs)
		
			if self.pymol_subcavs.isChecked():
				#from shutil import which
				try:
					import pymol
					_file = str(os.path.join(local,str(code[:-4]+"_subcavities.pml")))
					pymol.finish_launching(['pymol', _file])
				except:
					try:
						import subprocess
						subprocess.Popen(["pymol "+ os.path.join(local,str(code[:-4]+"_subcavities.pml"))], shell=True,
						stdin=None, stdout=None, stderr=True, close_fds=True)
					except:
						self.OutputTextBrowser.append("Could not open PyMOL: please set up a variable 'pymol' in your terminal")


	app = QtWidgets.QApplication(sys.argv)
	window_cav = Cavity()
	window_cav.show()
	sys.exit(app.exec_())

if __name__ == "__main__":

	main()
