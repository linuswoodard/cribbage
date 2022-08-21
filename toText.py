import os.path


path = "overall_score.txt"

#initialize file
def file_init():
	file = open(path, 'w')

	file.write('0\n')
	file.write('0\n')

	file.close()

def file_append(r, b):
	r = str(r)
	b = str(b)
	file = open(path, 'a')
	file.write(r+'\n')
	file.write(b+'\n')
	file.close()

def get_last_score():
	if not os.path.exists(path):
		file_init()
	file = open(path, 'r')
	filelines = file.readlines()
	file.close()

	lst = []
	for item in filelines:
		l = len(item)-2
		num = item[0:1]
		num = int(num)
		lst.append(num)

	r = lst[-2]
	b = lst[-1]
	return r, b
