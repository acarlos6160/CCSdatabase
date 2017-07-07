BA Python to SQLite

import os
os.chdir('C:\\Users\\Carlos\\Desktop\\CCSdatabase')

import sqlite3
conn = sqlite3.connect('SMILES.sqlite')
c = conn.cursor()

c.execute("INSERT INTO ChemicalFormula (CFID, Formula, Mass) VALUES (2, 2, 'C10H8', 128.17)")

"""
c.execute("INSERT INTO ChemicalFormula (%s, %s, %s)"%(CFID, Formula, Mass))\
	.format(CFID = '2', Formula = 'C10H8', Mass = '128.17'))
"""

conn.commit()
conn.close()