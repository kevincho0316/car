
def visualize_data(data):
	out=[]
	out.append(data[0])
	if data[1]==0:
		out.append('brake')
	elif data[1]==1:
		out.append('-')
	elif data[1]==2:
		out.append('gas')

	if data[2]==0:
		out.append('R')
	elif data[2]==1:
		out.append('P')
	elif data[2]==2:
		out.append('D')
	out.append(data[3])
	return out

print(visualize_data([100,1,1,'']))