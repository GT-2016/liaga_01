#coding:utf-8

global num

def readF(fn):
	f = open(fn, 'r')
	fs = open('w.txt','w+')
	num = 1
	for line in f:
		if line and line !='\n':
			line_s = line.split('.')
			
		try:
			if line_s and int(line_s[0])<10:
				line_w = str(num) + '.' + line[2:]
				fs.write(line_w)
				num+=1
				print(num)
			elif line_s and int(line_s[0])>=10:
				line_w = str(num) + '.' + line[3:]
				print(line_w)
				fs.write(line_w)
				num+=1
			else:
				line_w = str(num) + '.' + line
				fs.write(line_w)
				num+=1
		except Exception as e:
			line_w = str(num) + '.' + line
			fs.write(line_w)
			num+=1
			
	fs.close()
	f.close()
if __name__ == '__main__':
	path = r"r.txt"
	readF(path)