# Création de fichier binaire à partir de fichier hex.


import sys
import os
import errno
from struct import *

PrintDebEnable = 1

class PrintDeb:
	def __init__ (self):
		self.enable = PrintDebEnable
	def Print(self, message):
		if self.enable == 1: 
			print( message )
		else:
			print()
			# Ne rien faire.
		return 0
#end class PrintDeb.
		



# Ouverture d'un fichier
class OpenFile:
	def __init_(self):
		self.name = []
		self.opened = 0
		self.file
	def Open(self, fichier, mode ):
		pr	= PrintDeb()
		pr.Print("lirefichier")
		try:
			self.file=file( fichier, mode )
		except:
			x=sys.exc_info()
			print "File, %s, does not exist!" % fichier
			sys.exit(2)
		return self.file
	def File(self):
		return self.file
	
#end class OpenFile.


def HexComputeCC( line, count ):
	if len(line) < (256 + 11 + 256 ) : # 256: pour la valeur de ll, 11 pour les caractères obligatoire
			# et 256 pour un tampon pour des espaces et le retour de chariot et line feed.
		if line[0] == ":" :
			# lire la grandeur des données
			size = int(line[1:3],16)
			if size < 256:
				cc = 0
				# print range(1, 8 + 2 * size, 2 )
				# il y a huit caractères formant le début de chaque ligne.
				# il faut tenir compte que chaque octet de donnée est composer de deux caracteres alphanumériques. 2 * size
				for i in range(1, 8 + (2 * size), 2 ):
					tmp = int(line[i:i+2],16)
					cc = (cc+tmp) % 256
					# print tmp, cc 
				# print hex(cc)
				# complement a1.
				a = ((~cc % 256) + 1) % 256
				# print hex(a)
				b = int(line[8+2*size+1:8+2*size+1+2],16)
				if a != b:
					print count
					print "Erreur"
					for i in range(1, 8 + (2 * size), 2 ):
						tmp = int(line[i:i+2],16)
						cc = (cc+tmp) % 256
						print hex(tmp), hex(cc) 
					# print hex(cc)
					# complement a1.
					a = (~cc % 256) + 1
					print hex(a)
					b = int(line[8+2*size+1:8+2*size+1+2],16)
					print hex(b)
					sys.exit(2)
			else:
				print "Erreur size is too big:", size
				sys.exit(2)
		else :
			print ("Erreur dans la line, :, n'est pas présent")
			return -2
	else :			
		print ("Erreur dans la line, trop long")
		print len(line)
		return -1
#end def HexComputeCC.

# Extended Linear Address Records
def FindExtLinAddrRecords( line, count, list ):
	if (line[7] == '0') & (line[8] == '4' ):
		# C'est un Extended Linear Address Records
		# Calculer l'offset.
		offset = int( line[9:13], 16 );
		list.append( offset );
	return 	
	
class FindOffsetAndEnd:
	def __init__(self):
		self.list_offset = []
		self.size = 0
		self.tail = 0
	def find(self, file):
		file.seek( 0 );
		count = 0
		for line in file :
			HexComputeCC(line, count )
			count += 1
		file.seek( 0 );
		count = 0
		for line in file :
			(line, count )
			count += 1
			FindExtLinAddrRecords( line, count, self.list_offset )
			#if count > 10:
			#	print self.list_offset
			#	return
		print self.list_offset
#end class FindOffsetAndEnd.			

class TranslateHexToBin:
	def _init_ (self):
		self.allo = 0
	def GetLine( self, line, buf ):
		count = int(line[1:3],16)
		addr  = int(line[3:7],16)
		# print "Count et Addresse", count, addr
		if (line[7] == '0') & (line[8] == '0' ):
			# on commence a la position 9 jusqu'a 9+(2*size)
			# les données commencent à 9 (index commence à 0).
			# Si il y a 16 données, octets, de deux caractères chacun.
			# 9-10 -> donnée 1
			# 11-12 -> donnée 2
			# ...
			# 
			for i in range(0, count ):
				j = (2*i) + 9
				data = int(line[j:j+2],16)
				#print j, data
				buf.append(data)
			# print buf
	def Write (self, inFile, outFile ):
		inFile.seek( 0 );
		outFile.seek( 0 );
		xcounter = 0
		for line in inFile :
			buf = []
			xcounter += 1;
			self.GetLine( line, buf )
			for tampon in buf:
			#	octet = chr(tampon)
			#	print octet, len(octet)
			#	outFile.write(octet)
				outFile.write(pack('c', chr(tampon) ))
#end class TranslateHexToBin.
				
class HexConvert:
	def __init__(self):
		self.opened = 0
		self.head = 0
		self.current = 0
		self.size = 0
		self.tail = 0
		self.out = 0
		
	def Convert(self, inFile, outFile):
		self.out = file( "out.bin", "wb+" );
		cOffset = FindOffsetAndEnd()
		cOffset.find( inFile )
		cTrans = TranslateHexToBin()
		cTrans.Write( inFile, self.out );
		self.out.close()
		inFile.close()
		return;
#end class HexConvert.

# Programme principal.	
if __name__ == "__main__":
	print ("Convertit le fichier entrant du format hex en format bin.")
	# Véfifie les arguments entrés en paramètres.
	if len(sys.argv) < 3:
		cFichierHex = OpenFile()
		cFichierHex.Open( sys.argv[1], "r" )
		cHexConvert = HexConvert()
		cHexConvert.Convert( cFichierHex.File(), "fichier.bin" );
		
	