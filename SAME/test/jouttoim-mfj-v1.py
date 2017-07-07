#version 2.0 based more on the openbabel code rather than pybel. Files are
#prepared in one step instead of two. Faster? 
import glob, os, io, pybel, openbabel, time, string


#Set working Directory
#mydir='C:\\Users\\Paolo\\Desktop\\Projects\\Kendra'
#mydir='C:\\Users\\Paolo\\Desktop\\Projects\\Porpheryn\\Gaussian Outputs'
#mydir='C:\\Users\\Paolo\\Desktop\\Projects\\Photolysis\\Theoretical\\Rebeca'
#mydir='C:\\Users\\Paolo\\Desktop\\Projects\\Photolysis\\Theoretical\\Expanded Series\\log out'
mydir='Users\\carlosacosta\\Desktop\Chemistry Software\\test'
#mydir='C:\\Users\\Paolo\\Desktop\\Projects\\Other\\Coaltar\\log out'

chargeline='Atomic charges from electrostatic potential' #identifies where the charges are printed in jag

with open('IMoS.cla','r') as file: #Base IMoS file. Set run parameters in this file.
	imos=file.readlines()
	file.close()

os.chdir(mydir)

failed=[]
obConversion = openbabel.OBConversion()
obConversion.SetInAndOutFormats("jout", "xyz")
mol = openbabel.OBMol()


count=0
for filename in glob.glob("*.out"):
	with open(filename,'r') as myfile:
		test=(list(myfile)[-1])
		myfile.close()
	if test.split()[2]=='completed':
		obConversion.ReadFile(mol, filename)
		ycoor,xcoor,zcoor,atom=[],[],[],[]
		charge, chargeloc=[],[]
		for obatom in openbabel.OBMolAtomIter(mol):
			ycoor.append(obatom.y())
			xcoor.append(obatom.x())
			zcoor.append(obatom.z())
			atom.append(int(obatom.GetAtomicMass()))
		 
		atoms=len(ycoor)
		with open (filename,'r') as myfile:
			jagfile=myfile.readlines()
			for i, line in enumerate(jagfile,1):
				if chargeline in line:
					chargeloc.append(int(i))
			for ii in range (chargeloc[0]-1, chargeloc[0]+(atoms/5+1)*3+1):
				temp=jagfile[ii].split()
				for iii, val in enumerate(temp):
					try:
						charge.append(float(val))
					except:
						pass
			myfile.close()
		mfj=[]
		for x in range (2,atoms+2):
			mfj.append('      '+str(xcoor[x-2])+'     '+str(ycoor[x-2])+'     '+str(zcoor[x-2])+'     '+str(atom[x-2])+'     '+str(charge[x-2])+'\n')
		totalcharge=round(sum(charge))
		mfj[0]=str(os.path.splitext(filename)[0])+'\n'+'1\n'+str(atoms)+'\n'
		mfj[1]='ang \ncalc \n'+str(totalcharge)+'\n'
		IMoSin=os.path.splitext(filename)[0]+'.mfj'
		
		with open (IMoSin, 'w') as myfile3:
			myfile3.writelines(mfj)
			myfile3.close()

			outname=os.path.splitext(filename)[0]+'.IMO' #new extension for imos out files
		imos[1]=str(IMoSin)+"  "+"\savefolder\\"+str(outname)+"         N2\n"			
		imos[12]="Mweight " + str(int(mol.GetMolWt()))+"\n"
		with open('IMoS-Copy('+str(count)+').cla','w') as file:
			file.writelines(imos)
			count+=1

	else:
		failed.append(filename+'\n')

with open ('Failed_Jobs.txt','w') as fjobs:
	fjobs.writelines(failed)



