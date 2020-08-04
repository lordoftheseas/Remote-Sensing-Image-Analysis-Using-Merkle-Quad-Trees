from PIL import Image
import imagehash
import hashlib
import image_slicer
import subprocess
class merkleQuadTree:
	def __init__(self):
		self.hash_list=[]
		self.hash_level3=[]
		self.hash_level2=[]
		self.hash_level1=[]
		self.parent_hash=[]
		self.image_pieces=[]


	#The first part of the code contains the functions required to the trees for the two images
	#This function is used for image division
	#Its accepts two arguments	
	#param 1 is the name of the image (slice.jpg)
	#2nd param is the number of pieces the images has to be divided into(64)
	#It stores the tuple into the attribute of the object of the class merkleQuadTree
	def imageDivide(self,name,no):
		self.image_pieces=image_slicer.slice(name, no)
		

	

	#This function is used to calc the hash value of the each of the divded pieces
	#This function takes in 3 param
	#1)The name of the  org file
	#2)The number of rows in the division of images
	#3)The number of columns in the divided image
	#It returns a list of all the hash values of the pieces
	def hashList(self,name,r,c):
		for i in range(1,r+1):
			for j in range(1,c+1):
				string0 = name
				if i<10:
					string1 = "_0"
				else:
					string1 = '_'
				string2 = str(i)
				if j<10:
					string3 = "_0"
				else:
					string3 = '_'
				string4 = str(j)
				string5 = ".png"
				hash_val=imagehash.phash(Image.open(string0 + string1 + string2 + string3 + string4 + string5 ))
				self.hash_list.append(hash_val)
		


	#This function takes the list of hashes as input and returns a list of hashes of the parent as the output
	#It takes only one parameter
	#Param1 is a list of child hashes
	#It retruns a list of parent hashes
	def parent_Hash(self,child):	
		hash_level2=[]
		r=len(child)
		for i in range(1,r+1):
			if i % 4 == 0:
				val=str(child[i-1]) + str(child[i-2]) + str(child[i-3]) + str(child[i-4])
				h5=hashlib.sha256(val.encode('utf-8')).hexdigest()
				hash_level2.append(h5) 
		return hash_level2

#This marks the end of the class merkleQuadTree 


#This is the starting of the main part of the project
def main():
	print("*****************************************************************************************************************")
	print("                                           Remote Sensing Image Analyzer")
	print("*****************************************************************************************************************")
	name = "slice.jpg"
	Tree1=merkleQuadTree()
	Tree1.imageDivide(name,256)
	#Initializing the name of the image in the name variable
	name = "slice"
	row = 16
	col = 16
	Tree1.hashList(name,row,col)
	#Calculating the level 3 parent hash and storing it in hash_level3
	Tree1.hash_level3 =Tree1.parent_Hash(Tree1.hash_list)
	#Calculating the level 2 parent hash and storing it in hash_level2
	Tree1.hash_level2 = Tree1.parent_Hash(Tree1.hash_level3)
	#Calculating the level 1 parent hash and storing it in hash_level1
	Tree1.hash_level1 = Tree1.parent_Hash(Tree1.hash_level2)
	#Calculating the level 0 parent hash and storing it in hash_level1
	Tree1.parent_hash = Tree1.parent_Hash(Tree1.hash_level1)
	parent1 = Tree1.parent_hash[0]
	print "Root hash for tree 1:",parent1
	print "The first tree has been built!!!!"
	#The first tree has been built by the above code
	



	#Starting to implement the second tree!!!
	name = "slice1.jpg"
	Tree2=merkleQuadTree()
	Tree2.imageDivide(name,256)
	#Initializing the name of the image in the name variable
	name = "slice1"
	row = 16
	col = 16
	Tree2.hashList(name,row,col)	
	#Calculating the level 3 parent hash and storing it in hash_level3
	Tree2.hash_level3 =Tree2.parent_Hash(Tree2.hash_list)
	#Calculating the level 2 parent hash and storing it in hash_level2
	Tree2.hash_level2 = Tree2.parent_Hash(Tree2.hash_level3)
	#Calculating the level 1 parent hash and storing it in hash_level1
	Tree2.hash_level1 = Tree2.parent_Hash(Tree2.hash_level2)
	#Calculating the level 0 parent hash and storing it in hash_level1
	Tree2.parent_hash = Tree2.parent_Hash(Tree2.hash_level1)
	parent2 = Tree2.parent_hash[0]
	print "Root hash for tree 2:",parent2
	print "The second tree has been built!!!!"
	#The second tree has been built by the above code






	#Starting the comparision phase!!!
	if( parent1 == parent2):
		print "Both images are same!!!"
	else:
		print "Both images are different"
		count=0
		#This part of the code finds the pieces of image that are different, grayscales the pieces that are different and joins it back
		for x in range (0,4,1):
			if ( Tree1.hash_level1[x] != Tree2.hash_level1[x]):
			
				i = 4 * x
				for y in range(i,i+4,1):
					if (Tree1.hash_level2[y] != Tree2.hash_level2[y]):
						p = 4 * y
						for z in range(p,p+4,1):
							if(Tree1.hash_level3[z] != Tree2.hash_level3[z]):
								m = 4 * z
								for w in range(m,m+4):
									if ( Tree1.hash_list[w] != Tree2.hash_list[w]):
										count=count+1
										b = Tree1.image_pieces[w].image
										Tree1.image_pieces[w].image = b.convert('LA')
		t = image_slicer.join(Tree1.image_pieces)
		t.save('diffRes.png') 
		print "The number of different pieces in the two image are:",count
	a=subprocess.call(['./abc.sh'])



if __name__=="__main__":
	main()
