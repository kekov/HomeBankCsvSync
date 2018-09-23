# Passer en parametre 2 fichiers CSV au format HomeBank
# Le programme compare les 2 fichiers puis complete le fichier n°2 ( export de la banque ) avec les infos du fichier n°1
# le résultat est stocké dans le fichiers sync.csv
# le programme ajoute le caractere * dans le champ info pour les opérations présentent dans le fichier 1 et 2
# le programme ajoute le caractere = dans le champ info pour les opérations présentent plusieurs fois ( même montant )
# Le champ info reste inchangé pour les opérations présentent dans le fichier 2 mais pas dans le fichier 1
# Enfin un fichier nonDebite.csv est géneré. Il correspond aux operations présentent dans le fichier 1 et non dans le fichier 2.

import csv 
import sys
 
csvMe=[]
csvCa=[]

uniqueMe={}
uniqueCA={}

#Dict : cle : prix de l'operation  value : la ligne CSV
rowuniqueMe={}
rowUniqueCA={}

#Tableau contenant les lignes du fichier CSV present plusieurs fois dans le fichier
rowDoubleCA=[]
rowDoubleMe=[]

#Tableau contenant les operations presentent dans ME mais pas dans CA
rowNonDebite=[]

colMontant=5
colInfo=2
colTiers=3
colCat=6
colTag=7

#-----------------------------------------------------------------------------------------------------------------------

def prixEnDouble( csv , uniqueDict , rowUniqueDict , rowDouble , fichier ):
	for row in csv:
		if row[colMontant] in uniqueDict:
			print("\nAttention le montant " + row[colMontant] + " est present plusieurs fois dans le fichier " + fichier)
			print("    > " + str(row))
			uniqueDict[ row[colMontant] ] = uniqueDict[ row[colMontant] ] + 1
			row[colTag] = "=" + row[colTag]
			rowDouble.append(row)			
		else:
			uniqueDict[ row[colMontant] ] = 1
			rowUniqueDict[ row[colMontant] ] = row
			
#-----------------------------------------------------------------------------------------------------------------------
 
def tagCa( ):
	for key,value in rowuniqueMe.items():
		 #print(key,value)
		 if key in rowUniqueCA:
			# print("Cle dans CA")
			 rowUniqueCA[key][colTag] = "*"+rowUniqueCA[key][colTag] 			 
			 rowUniqueCA[key][colInfo] = rowuniqueMe[key][colInfo] 
			 rowUniqueCA[key][colTiers] = rowuniqueMe[key][colTiers] 
			 rowUniqueCA[key][colCat] = rowuniqueMe[key][colCat] 
			# print("------>" + str(rowUniqueCA[key]) + "  --- " + str(rowUniqueCA[key][colTag] ) )
		 else:
			 #operation pas encore debit
			 rowNonDebite.append( rowuniqueMe[key] )
			 
#-----------------------------------------------------------------------------------------------------------------------
 
if len(sys.argv) == 1:
	print("Usage : python sync.py <me.csv> <CA.csv>")
else :
	me = open(sys.argv[1], "r")
	ca = open(sys.argv[2], "r")
	sync = open("sync.csv", "w")
	nonDebite = open("nonDebite.csv", "w")

	meFile = csv.reader(me,delimiter=';')
	caFile = csv.reader(ca,delimiter=';')
	syncFile = csv.writer(sync, delimiter=';')
	nonDebiteFile = csv.writer(nonDebite, delimiter=';')

	for row in meFile:
		csvMe.append(row)

	for row in caFile:
		csvCa.append(row) 
		
	#Détection des prix en double dans les fichiers
	prixEnDouble(csvMe , uniqueMe , rowuniqueMe , rowDoubleMe ,"me")
	prixEnDouble(csvCa , uniqueCA , rowUniqueCA , rowDoubleCA , "CA")

	#ajoute entete dans le fichier des operations non debitees
	rowNonDebite.append(csvCa[0])

	tagCa()

	#enleve le caractere * 
	rowUniqueCA["amount"][colTag]="tag"

	for key,value in rowUniqueCA.items():
		syncFile.writerow( value )
		
	#ajoute les lignes avec un montant present plusieurs fois
	for row in rowDoubleCA:
		syncFile.writerow( row )
		
	for row in rowNonDebite:
		nonDebiteFile.writerow( row )
		
	me.close()
	ca.close()
	sync.close()
	nonDebite.close()
