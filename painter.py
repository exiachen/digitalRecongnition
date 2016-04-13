
from Tkinter import *
from numpy import *
import time, os, sys
import subprocess
from PIL import Image
from sklearn import neighbors
import timer

rows = 32
cols = 32

knn = neighbors.KNeighborsClassifier()

class myCanvas(object):
	def __init__(self, root):
		self.color = 'black'
		self.root = root
		self.canvas = Canvas(root, width=200, height=200, bg='white')
		self.canvas.pack()
		self.timer = timer.Timer(0, self.SaveFile, [])
		self.timer.start()
		self.canvas.bind('<Button-1>', self.Press)
		self.canvas.bind('<B1-Motion>', self.Draw)

	def Press(self, event):
		self.x = event.x
		self.y = event.y
		self.timer.modTimer(2)

	def Draw(self, event):
		self.canvas.create_line(self.x, self.y, event.x, event.y,
								fill = self.color, width = 16)
		self.x = event.x
		self.y = event.y


	def SaveFile(self, args = []):
		rootdir = sys.path[0] + '/image/'
		filename = time.strftime('%m%d%H%M%S', time.localtime(time.time())) + '.png'

		espFileName = rootdir + "tmp.esp"
		pngFileName = rootdir + filename

		self.canvas.postscript(file = espFileName)

		process = subprocess.Popen("gswin32c -dBATCH -dNOPAUSE -dEPSCrop -sDEVICE=png256 -sOutputFile=%s %s" % (pngFileName, espFileName), shell=True)
		process.wait()

		os.remove(espFileName)
		self.canvas.delete(ALL)

		vector = image2Vector(pngFileName)
		print knn.predict(vector[0])



def image2Vector(imageFileName):
	im = Image.open(imageFileName)
	smallImage = im.resize((rows, cols))
	imageSize = smallImage.size

	vector = zeros((1, rows * cols))

	for i in range(imageSize[0]):
		for j in range(imageSize[1]):
			if smallImage.getpixel((j, i)) == 215:
				vector[0, j + i * rows] = 0
			else:
				vector[0, j + i * rows] = 1

	return vector

def file2Vector(filename):
	vector = zeros((1, rows * cols))
	f = open(filename)

	for line in range(rows):
		msg = f.readline()
		for col in range(cols):
			vector[0, col + line * rows] = int(msg[col])

	return vector

def setUpTrainingData():
	print "---Getting training set---"
	dataSetDir = sys.path[0] + '/'
	trainingFileList = os.listdir(dataSetDir + 'trainingDigits') # load the training set
	numSamples = len(trainingFileList)

	train_x = zeros((numSamples, 1024))
	train_y = []
	for i in xrange(numSamples):
		filename = trainingFileList[i]

		# get train_x
		train_x[i, :] = file2Vector(dataSetDir + 'trainingDigits/%s' % filename)

		# get label from file name such as "1_18.txt"
		label = int(filename.split('_')[0]) # return 1
		train_y.append(label)

	return train_x, train_y

def setUpClassifier():
	train_x, train_y = setUpTrainingData()

	#training
	print 'traing...'
	knn.fit(train_x, train_y)


def main():

	setUpClassifier()

	root = Tk()
	root.geometry('200x200')
	canvas1 = myCanvas(root)

	root.mainloop()

if __name__ == '__main__':
	main()
