#Compile files 
import sqltool as sql
import os,glob, openbabel

if __name__ == '__main__':
	dbname='SMILESDB.sqlite'
	sqltool=sql.utilities()
	conn, cur= sqltool.connect(dbname)
	
	mol = openbabel.OBMol() #Prepare variables for later
	obConversion2 = openbabel.OBConversion()
	obConversion2.SetInAndOutFormats("jout", "smi")
	
	numtoa=dict()
	numtoa['12']='C'
	numtoa['16']='O'
	numtoa['14']='N'
	numtoa['1']='H'
	
	for filename in glob.glob('*.IMO'): #find theoretical mobility and ccs
		with open (filename,'r') as myfile:
			mobval=(list(myfile)[-1].split())
			TCCS=float(mobval[0])
			TKo=float(mobval[2])
			myfile.close()
		mfjfile=os.path.splitext(filename)[0]+'.mfj'
		with open (mfjfile,'r') as myfile: #find energy, geometry and charges
			info=myfile.readlines()
			myfile.close()
		FORMULA,count,energy,method,basisset=info[0].split('_')
		x,y,z,a,cgr=[],[],[],[],[]
		for line in info[6:]:
			tx,ty,tz,ta,tcgr=line.split()
			x.append(tx)
			y.append(ty)
			z.append(tz)
			a.append(ta)
			cgr.append(tcgr)
			myfile.close()
		outfile=os.path.splitext(filename)[0]+'.out'
		obConversion2.ReadFile(mol, outfile)
		smiles=obConversion2.WriteString(mol).split('\t')[0]
		MASS=mol.GetExactMass()
		#Do stuff find formulas
		CFID=sqltool.insertcf(cur,FORMULA,MASS)
		SID=sqltool.insertsm(cur,CFID,smiles)
		DID,DCHK=sqltool.insertdetails(cur,CFID,SID,method,basisset,TCCS,TKo,energy)
		if DCHK=='New':
			for i in range(0,len(x)):
				sqltool.insertgeometry(cur,CFID,SID,DID,numtoa[a[i]],x[i],y[i],z[i],cgr[i])
	sqltool.close(conn)
		