#BA Python to SQLite/Users/carlosacosta/Desktop/Chemsoft/sqltool.py
import sqlite3

class utilities:
	def connect(self, sqlite_file):
		conn = sqlite3.connect(sqlite_file)
		c = conn.cursor()
		return conn,c

	def close(self, conn):
		conn.commit()
		conn.close()

	def insertcf(self, cursor, formula, mass):
		cursor.execute("SELECT CFID FROM ChemicalFormula WHERE Formula= ?",(formula,))
		data=cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO ChemicalFormula (Formula,Mass) VALUES (?,?)",(formula, mass))
			cursor.execute("SELECT max(CFID) from ChemicalFormula")
			data=cursor.fetchone()
			print "%s added to table in for %s"%(formula,data[0])
		else:
			print "%s exists at row %s"%(formula,data[0])
		return data[0]

	def insertsm(self, cursor, cid, smiles):
		cursor.execute("SELECT SID FROM SMILESname WHERE SMILES= ?",(smiles,))
		data=cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO SMILESname (CFID,SMILES) VALUES (?,?)",(cid, smiles))
			cursor.execute("SELECT max(SID) FROM SMILESname")
			data=cursor.fetchone()
		return data[0]

	def insertdetails(self, cursor, cid, sid, method, basisset, tccs, tko, energy):
		cursor.execute("SELECT DID FROM Details WHERE Energy= ?",(energy,))
		data=cursor.fetchone()
		if data is None:
			cursor.execute("INSERT INTO Details (CFID,SID,Method, BasisSet, TCCS,TKo,Energy ) VALUES (?,?,?,?,?,?,?)",(cid, sid, method, basisset, tccs, tko, energy))
			cursor.execute("SELECT max(DID) FROM Details")
			data=cursor.fetchone()
			DIDnew='New'
		else:
			DIDnew='Old'
		return data[0],DIDnew
		
	def insertgeometry(self, cursor, cid, sid, did, label, x,y,z,charge):
		cursor.execute("INSERT INTO Geometry (CFID,SID, DID,Label,X,Y,Z,Charge) VALUES (?,?,?,?,?,?,?,?)",(cid, sid, did, label, x,y,z,charge))
