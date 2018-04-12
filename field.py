import numpy as np
from numpy import sin, cos, exp, pi, tan, log, sinh, cosh, tanh, sinc, sqrt, cbrt, angle, real, imag, abs, arcsin, arccos, arctan, arcsinh, arccosh, arctanh
from numpy import pi, e


potential_expr = None
obstacle_expr = None

def setPotential(expr):
	global potential_expr
	potential_expr = expr
	test_pot_expr()

def setObstacle(expr):
	global obstacle_expr
	obstacle_expr = expr
	test_obs_expr() 


def test_pot_expr():
	global potential_expr
	x = 0
	y = 0
	try:
		a = eval(potential_expr)
	except:
		print(potential_expr)
		print('Erreur de calcul du potentiel : mis à 0 par défaut')
		potential_expr = '0'
		input('Appuyez sur une touche poour continuer')

def test_obs_expr():
	global obstacle_expr
	x = 0
	y = 0
	try:
		a = eval(obstacle_expr)
	except e:
		
		print('Erreur lors de la definition de l\'obsatcle : Mis à False par défaut')
		obstacle_expr = 'False'
		input('Appuyez sur une touche poour continuer')


def isObstacle(x, y):
	a = False
	try:
		a = eval(obstacle_expr)
	except:
		pass
	return a

def getPotential(x, y):
	a = 0 + 0j
	try:
		a = eval(potential_expr)
	except:
		pass
	return a

