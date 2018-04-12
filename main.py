import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from numpy import pi
from matplotlib import animation
import scipy.linalg
import scipy as sp
import scipy.sparse
import scipy.sparse.linalg
import toml, time, sys
import util, field


size, delta_t, N, step = 0, 0, 0, 0
k_x, k_y, a_x, a_y = 0, 0, 0, 0
x0, y0 = 0, 0

x_axis, y_axis, X, Y = None, None, None, None

flag_intensity = False

wall_potential = 1e10

V_x, V_y = None, None

start_time = 0

wave_function = None

compteur = 0

LAPLACE_MATRIX = None

H1 = None
HX, HY = None, None


potential_boudnary = []

def init():

	global x_axis, y_axis, X, Y, wave_function, start_time, H1, HX, HY, V_x, V_y
	x_axis = np.linspace(-size/2, size/2, N)
	y_axis = np.linspace(-size/2, size/2, N)
	X, Y = np.meshgrid(x_axis, y_axis)

	phase = np.exp( 1j*(X*k_x + Y*k_y))
	px = np.exp( - ((x0 - X)**2)/(4*a_x**2))
	py = np.exp( - ((y0 - Y)**2)/(4*a_y**2))
	wave_function = phase*px*py
	norm = np.sqrt(util.integrate(np.abs(wave_function)**2, N, step))
	wave_function = wave_function/norm


	LAPLACE_MATRIX = sp.sparse.lil_matrix(-2*sp.sparse.identity(N*N))
	for i in range(N):
		for j in range(N-1):
			k = i*N + j
			LAPLACE_MATRIX[k,k+1] = 1
			LAPLACE_MATRIX[k+1,k] = 1

	V_x = np.zeros(N*N, dtype='c16')
	
	for j in range(N):
		for i in range(N):
			xx = i
			yy = N*j
			if field.isObstacle(x_axis[j], y_axis[i]):
				V_x[xx+yy] = wall_potential
			else:
				V_x[xx+yy] = field.getPotential(x_axis[j], y_axis[i])
	
	
	V_y = np.zeros(N*N, dtype='c16')
	
	for j in range(N):
		for i in range(N):
			xx = j*N
			yy = i
			if field.isObstacle(x_axis[i], y_axis[j]):
				V_y[xx+yy] = wall_potential
			else:
				V_y[xx+yy] = field.getPotential(x_axis[i], y_axis[j])


	

	V_x_matrix = sp.sparse.diags([V_x], [0])
	V_y_matrix = sp.sparse.diags([V_y], [0])


	LAPLACE_MATRIX = LAPLACE_MATRIX/(step ** 2)

	H1 = (1*sp.sparse.identity(N*N) - 1j*(delta_t/2)*(LAPLACE_MATRIX))
	H1 = sp.sparse.dia_matrix(H1)

	HX = (1*sp.sparse.identity(N*N) - 1j*(delta_t/2)*(LAPLACE_MATRIX - V_x_matrix))
	HX = sp.sparse.dia_matrix(HX)

	HY = (1*sp.sparse.identity(N*N) - 1j*(delta_t/2)*(LAPLACE_MATRIX - V_y_matrix))
	HY = sp.sparse.dia_matrix(HY)

	for i in range(0, N):
		for j in range(0, N):
			if field.isObstacle(x_axis[j], y_axis[i]):
				adj = util.getAdjPos(i, j, N)
				for xx, yy in adj:
					if xx >= 0 and yy >= 0 and xx < N and yy <N and not field.isObstacle(x_axis[yy], y_axis[xx]):
						potential_boudnary.append((i, j))

	start_time = time.time()

def plot_animation(t):

	global wave_function
	rgb_map = None
	
	if flag_intensity:
		cmap = plt.cm.inferno
		data = np.abs(wave_function)**2
		norm = plt.Normalize(data.min(), data.max())
		rgb_map = cmap(norm(data))
		rgb_map = rgb_map[:, :, :3]
	else:
		rgb_map = util.colorize(wave_function)

	for i, j in potential_boudnary:
		rgb_map[i][j] = 1, 1, 1

	plt.imshow(rgb_map, interpolation='none', extent=[-size/2,size/2,-size/2,size/2])



	vector_selon_x = util.x_concatenate(wave_function, N) 	


	vector_derive_y_selon_x = util.x_concatenate(util.dy_square(wave_function, N, step), N)
	U_selon_x = vector_selon_x + (1j*delta_t/2 )*(vector_derive_y_selon_x - V_x*vector_selon_x)
	U_selon_x_plus = scipy.sparse.linalg.spsolve(HX, U_selon_x)

	wave_function = util.x_deconcatenate(U_selon_x_plus, N)



	vector_selon_y = util.y_concatenate(wave_function, N) 	
	vector_derive_x_selon_y = util.y_concatenate(util.dx_square(wave_function, N, step), N)
	U_selon_y = vector_selon_y  + (1j*delta_t/2 )*(vector_derive_x_selon_y - V_y *vector_selon_y)
	U_selon_y_plus = scipy.sparse.linalg.spsolve(HY, U_selon_y)

	wave_function = util.y_deconcatenate(U_selon_y_plus, N)
	



	print_update()

def print_update():
	global compteur, wave_function

	NORM = np.sqrt(util.integrate(np.abs(wave_function)**2, N, step))

	util.clear()
	rapport = compteur/(duration*FPS)
	M = 20
	k = int(rapport*M)
	l = M - k
	to_print = '[' + k*'#' + l*'-'+ ']   {0:.3f} %'

	d_time = time.time() - start_time

	print('--- Simulation en cours ---')
	print(to_print.format(rapport*100))
	print('Temps écoulé : {0:.1f} s'.format(d_time))
	if rapport > 0:
		print('Temps restant estimé : {0:.1f} s'.format(d_time/rapport - d_time))
	print('Norme de la fonction : {0:.3f} '.format(NORM))
	compteur += 1

if len(sys.argv) >= 2:


	name_file = sys.argv[1]
	config_toml = toml.load("config.toml")

	FPS = int(config_toml["FPS"])
	duration = int(config_toml["DURATION"])
	
	size = int(config_toml["SIZE"])
	N = int(config_toml["N"])
	delta_t = float(config_toml["DELTA_T"])/FPS

	x0 = float(config_toml['x'])
	y0 = float(config_toml['y'])

	k_x = float(config_toml["Kx"])
	k_y = float(config_toml["Ky"])
	a_x = float(config_toml["Ax"])
	a_y = float(config_toml["Ay"])

	field.setPotential(config_toml["V"])
	field.setObstacle(config_toml["O"])




	if len(sys.argv) >= 3 and  "--intensity" in sys.argv[2:]:
		flag_intensity = True

	step = size/N

	frame = duration * FPS

	init()

	fig = plt.figure(figsize=(5,5))
	ani = animation.FuncAnimation(fig, plot_animation,  frames=frame, blit=False, interval=0, repeat=False)
	ani.save(name_file+'.mp4', fps=FPS)
	util.launch(name_file+'.mp4')
		

else:
	print("Veuillez entrer le nom du fichier")


