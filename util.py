import numpy as np
from numpy import pi
from colorsys import hls_to_rgb
import field
import os

def colorize(z):
    r = np.abs(z)
    arg = np.angle(z) 

    h = (arg + pi)  / (2 * pi) + 0.5
    l = 1.0 - 1.0/(1.0 + 2*r**1.2)
    s = 0.8

    c = np.vectorize(hls_to_rgb) (h,l,s) # --> tuple
    c = np.array(c)  # -->  array of (3,n,m) shape, but need (n,m,3)
    c = c.swapaxes(0,2) 
    c = c.swapaxes(0,1) 
    return c

def x_concatenate(MM, N):
	result = []
	for j in range(N):
		for i in range(N):
			result.append(MM[i][j])	

	return np.array(result, dtype='c16')

def x_deconcatenate(vector, N):
	result = np.zeros((N, N), dtype='c16')
	for j in range(N):
		for i in range(N):
			result[i][j] = vector[N*j + i]

	return result

def y_concatenate(MM, N):
	result = []
	for i in range(N):
		for j in range(N):
			result.append(MM[i][j])	
	return np.array(result, dtype='c16')

def y_deconcatenate(vector, N):
	result = np.zeros((N, N), dtype='c16')
	for i in range(N):
		for j in range(N):
			result[i][j] = vector[N*i + j]

	return result

def dx_square(MM, N, step):
	result = np.zeros((N, N), dtype='c16')
	for j in range(N):
		result[0][j] = MM[1][j] - 2*MM[0][j]

		for i in range(1, N-1):
			result[i][j] = MM[i+1][j] + MM[i-1][j] - 2*MM[i][j]

		result[N-1][j] = MM[N-2][j] - 2*MM[N-1][j]

	return result / (step**2)

def dy_square(MM, N, step):
	result = np.zeros((N, N), dtype='c16')
	for j in range(N):

		result[j][0] = MM[j][1] - 2*MM[j][0]

		for i in range(1, N-1):
			result[j][i] = MM[j][i+1] + MM[j][i-1] - 2*MM[j][i]

		result[j][N-1] = MM[j][N-2] - 2*MM[j][N-1]
		
	return result / (step**2)

def apply_obstacle(MM, N, meshX, meshY):
	for i in range(N):
		for j in range(N):
			if field.isObstacle(meshX[i][j], meshY[i][j]):
				MM[i][j] = 0 + 0j
	return MM


def getAdjPos(x, y, N):
	res = []
	
	res.append((x-1,y))
	res.append((x+1,y))
	res.append((x, y - 1))
	res.append((x,y+1))
	res.append((x - 1,y+1))
	res.append((x - 1,y-1))
	res.append((x + 1,y+1))
	res.append((x+1, y+1))
	return res
	

def clear():
	os.system('cls')

def launch(filename):
	os.system(filename)

def integrate(MM, N, step):
	a = 0
	air = step*step/2
	for i in range(N-1):
		for j in range(N-1):
			AA, AB, BA, BB = MM[i][j], MM[i][j+1], MM[i+1][j], MM[i+1][j+1]
			a += air*(AA+AB+BA)/3
			a += air*(BB+AB+BA)/3
	return a
