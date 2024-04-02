import sys
import math

def get_plane(x1, y1, z1, x2, y2, z2, x3, y3, z3):
	normale = [(y2-y1)*(z3-z1) - (z2-z1)*(y3-y1), (z2-z1)*(x3-x1) - (x2-x1)*(z3-z1), (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)]
	A = normale[0]
	B = normale[1]
	C = normale[2]
	D = -x1*normale[0] - y1*normale[1] - z1*normale[2]
	return A, B, C, D

def fourth_triangle_vertex(x1, y1, z1, x2, y2, z2, x3, y3, z3):
	h_x = (x1 + x3) / 2.0
	h_y = (y1 + y3) / 2.0
	h_z = (z1 + z3) / 2.0
	e_x = x2 + (h_x - x2) * 2.0
	e_y = y2 + (h_y - y2) * 2.0
	e_z = z2 + (h_z - z2) * 2.0
	return e_x, e_y, e_z

def count_delta(matrix):
	return matrix[0][0] * (matrix[1][1]*matrix[2][2] - matrix[1][2]*matrix[2][1]) - matrix[0][1] * (matrix[1][0]*matrix[2][2] - matrix[1][2]*matrix[2][0]) + matrix[0][2] * (matrix[1][0]*matrix[2][1] - matrix[1][1]*matrix[2][0])

def crummer(matrix, free):
	delta = count_delta(matrix)
	if delta == 0.0:
		raise ValueError
	nm = [[matrix[0][0], matrix[0][1], matrix[0][2]], [matrix[1][0], matrix[1][1], matrix[1][2]], [matrix[2][0], matrix[2][1], matrix[2][2]]]
	nm[0][0] = free[0]
	nm[1][0] = free[1]
	nm[2][0] = free[2]
	delta1 = count_delta(nm)
	nm = [[matrix[0][0], matrix[0][1], matrix[0][2]], [matrix[1][0], matrix[1][1], matrix[1][2]], [matrix[2][0], matrix[2][1], matrix[2][2]]]
	nm[0][1] = free[0]
	nm[1][1] = free[1]
	nm[2][1] = free[2]
	delta2 = count_delta(nm)
	nm = [[matrix[0][0], matrix[0][1], matrix[0][2]], [matrix[1][0], matrix[1][1], matrix[1][2]], [matrix[2][0], matrix[2][1], matrix[2][2]]]
	nm[0][2] = free[0]
	nm[1][2] = free[1]
	nm[2][2] = free[2]
	delta3 = count_delta(nm)
	return delta1 / delta, delta2 / delta, delta3 / delta

class Mirror:
	def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3):
		self.x1 = x1
		self.x2 = x2
		self.x3 = x3
		self.y1 = y1
		self.y2 = y2
		self.y3 = y3
		self.z1 = z1
		self.z2 = z2
		self.z3 = z3


class Brink:
	def __init__(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
		self.x1 = x1
		self.x2 = x2
		self.x3 = x3
		self.y1 = y1
		self.y2 = y2
		self.y3 = y3
		self.z1 = z1
		self.z2 = z2
		self.z3 = z3
		self.x4 = x4
		self.y4 = y4
		self.z4 = z4

class Ray:
	def normalize_vector(self):
		while max(abs(self.dir_x), abs(self.dir_y), abs(self.dir_z)) < 1.0:
			self.dir_x *= 2.0
			self.dir_y *= 2.0
			self.dir_z *= 2.0
		otrX = self.dir_x < 0.0
		otrY = self.dir_y < 0.0
		otrZ = self.dir_z < 0.0
		self.dir_x = abs(self.dir_x)
		self.dir_y = abs(self.dir_y)
		self.dir_z = abs(self.dir_z)
		coef = max(self.dir_x, self.dir_y, self.dir_z)
		self.dir_x /= coef
		self.dir_y /= coef
		self.dir_z /= coef
		if otrX:
			self.dir_x *= -1.0
		if otrY:
			self.dir_y *= -1.0
		if otrZ:
			self.dir_z *= -1.0

	def __init__(self, x, y, z, dir_x, dir_y, dir_z, e):
		self.x = x
		self.y = y
		self.z = z
		self.dir_x = dir_x
		self.dir_y = dir_y
		self.dir_z = dir_z
		self.energy = e

	def cross_plane(self, A, B, C, D):
		if abs(A * self.x + B * self.y + C * self.z + D) < 1e-9:
			return self.x, self.y, self.z
		x1 = self.x
		y1 = self.y
		z1 = self.z
		m1 = self.dir_x
		p1 = self.dir_y
		l1 = self.dir_z
		if p1 != 0.0:
			matrix = [[p1, -m1, 0.0], [0.0, l1, -p1], [A, B, C]]
			free = [p1*x1 - m1*y1, l1*y1 - p1*z1, -D]
			try:
				r1, r2, r3 = map(float, crummer(matrix, free))
				return r1, r2, r3
			except ValueError:
				raise ValueError
		elif m1 != 0.0:
			matrix = [[p1, -m1, 0.0], [l1, 0.0, -m1], [A, B, C]]
			free = [p1*x1 - m1*y1, l1*x1 - m1*z1, -D]
			try:
				r1, r2, r3 = map(float, crummer(matrix, free))
				return r1, r2, r3
			except ValueError:
				raise ValueError
		else:
			matrix = [[0.0, l1, -p1], [l1, 0.0, -m1], [A, B, C]]
			free = [l1*y1 - p1*z1, l1*x1 - m1*z1, -D]
			try:
				r1, r2, r3 = map(float, crummer(matrix, free))
				return r1, r2, r3
			except ValueError:
				raise ValueError
	
	def reflect_mirror(self, mirror, op = False):
		A, B, C, D = map(float, get_plane(mirror.x1, mirror.y1, mirror.z1, mirror.x2, mirror.y2, mirror.z2, mirror.x3, mirror.y3, mirror.z3))
		try:
			p_x, p_y, p_z = map(float, self.cross_plane(A, B, C, D))
		except ValueError:
			raise ValueError


		if self.dir_x != 0.0:
			k = (p_x - self.x) / self.dir_x
		elif self.dir_y != 0.0:
			k = (p_y - self.y) / self.dir_y
		else:
			k = (p_z - self.z) / self.dir_z
		if k <= 0.0:
			raise ValueError

		mir_x = p_x + self.dir_x
		mir_y = p_y + self.dir_y
		mir_z = p_z + self.dir_z

		ort_ray = Ray(mir_x, mir_y, mir_z, A, B, C, 0)
		ort_x, ort_y, ort_z = map(float, ort_ray.cross_plane(A, B, C, D))

		mir_x = mir_x + (ort_x - mir_x) * 2
		mir_y = mir_y + (ort_y - mir_y) * 2
		mir_z = mir_z + (ort_z - mir_z) * 2

		return k, p_x, p_y, p_z, mir_x - p_x, mir_y - p_y, mir_z - p_z


sys.stdin = open("input.txt", "r")
sys.stdout = open("output.txt", "w")

x_a, y_a, z_a = map(float, input().split())
x_b, y_b, z_b = map(float, input().split())
x_c, y_c, z_c = map(float, input().split())
x_d, y_d, z_d = map(float, input().split())

brinks = []
x_e, y_e, z_e = map(float, fourth_triangle_vertex(x_a, y_a, z_a, x_b, y_b, z_b, x_c, y_c, z_c))
brinks.append(Brink(x_a, y_a, z_a, x_b, y_b, z_b, x_c, y_c, z_c, x_e, y_e, z_e))
x_f, y_f, z_f = map(float, fourth_triangle_vertex(x_e, y_e, z_e, x_c, y_c, z_c, x_d, y_d, z_d))
brinks.append(Brink(x_e, y_e, z_e, x_c, y_c, z_c, x_d, y_d, z_d, x_f, y_f, z_f))
x_g, y_g, z_g = map(float, fourth_triangle_vertex(x_b, y_b, z_b, x_c, y_c, z_c, x_d, y_d, z_d))
brinks.append(Brink(x_b, y_b, z_b, x_c, y_c, z_c, x_d, y_d, z_d, x_g, y_g, z_g))
x_h, y_h, z_h = map(float, fourth_triangle_vertex(x_f, y_f, z_f, x_d, y_d, z_d, x_g, y_g, z_g))
brinks.append(Brink(x_f, y_f, z_f, x_d, y_d, z_d, x_g, y_g, z_g, x_h, y_h, z_h))

brinks.append(Brink(x_a, y_a, z_a, x_e, y_e, z_e, x_f, y_f, z_f, x_h, y_h, z_h))
brinks.append(Brink(x_a, y_a, z_a, x_b, y_b, z_b, x_g, y_g, z_g, x_h, y_h, z_h))

dir_x, dir_y, dir_z = map(float, input().split())
ent_x, ent_y, ent_z = map(float, input().split())
e = int(input())
cur_ray = Ray(ent_x, ent_y, ent_z, dir_x, dir_y, dir_z, e)

mirrors = []

n = int(input())
for i in range(n):
	x_p, y_p, z_p = map(float, input().split())
	x_q, y_q, z_q = map(float, input().split())
	x_r, y_r, z_r = map(float, input().split())
	mirrors.append(Mirror(x_p, y_p, z_p, x_q, y_q, z_q, x_r, y_r, z_r))

lastRefl = -1

min_x = 10000000.0
max_x = -10000000.0
min_y = 10000000.0
max_y = -10000000.0
min_z = 10000000.0
max_z = -10000000.0

for i in range(len(brinks)):
	min_x = min(min_x, min(brinks[i].x1, brinks[i].x2, brinks[i].x3, brinks[i].x4))
	max_x = max(max_x, max(brinks[i].x1, brinks[i].x2, brinks[i].x3, brinks[i].x4))
	min_y = min(min_y, min(brinks[i].y1, brinks[i].y2, brinks[i].y3, brinks[i].y4))
	max_y = max(max_y, max(brinks[i].y1, brinks[i].y2, brinks[i].y3, brinks[i].y4))
	min_z = min(min_z, min(brinks[i].z1, brinks[i].z2, brinks[i].z3, brinks[i].z4))
	max_z = max(max_z, max(brinks[i].z1, brinks[i].z2, brinks[i].z3, brinks[i].z4))

reflected = 0

while 1:
	cur_ray.normalize_vector()
	reflects = False
	vec_len = 10000000.0
	idx = 0

	for i in range(len(mirrors)):
		if lastRefl == i:
			continue
		try:
			vl, p_x, p_y, p_z, dir_x, dir_y, dir_z = map(float, cur_ray.reflect_mirror(mirrors[i]))
			reflects = True
			if vl < vec_len:
				vec_len = vl
				idx = i
		except ValueError:
			continue


	if reflects:
		vl, p_x, p_y, p_z, dir_x, dir_y, dir_z = map(float, cur_ray.reflect_mirror(mirrors[idx], False))
		p_x = round(p_x, 8)
		p_y = round(p_y, 8)
		p_z = round(p_z, 8)
		if (p_x >= min_x and p_x <= max_x and p_y >= min_y and p_y <= max_y and p_z >= min_z and p_z <= max_z):
			reflected += 1
			cur_ray.energy -= 1
			cur_ray.x = p_x
			cur_ray.y = p_y
			cur_ray.z = p_z
			cur_ray.dir_x = dir_x
			cur_ray.dir_y = dir_y
			cur_ray.dir_z = dir_z
			cur_ray.x = round(cur_ray.x, 8)
			cur_ray.y = round(cur_ray.y, 8)
			cur_ray.z = round(cur_ray.z, 8)
			cur_ray.dir_x = round(cur_ray.dir_x, 8)
			cur_ray.dir_y = round(cur_ray.dir_y, 8)
			cur_ray.dir_z = round(cur_ray.dir_z, 8)
			lastRefl = idx
			if cur_ray.energy == 0:
				print(0)
				print(cur_ray.x, cur_ray.y, cur_ray.z)
				exit(0)
			continue


	for i in range(len(brinks)):
		A, B, C, D = map(float, get_plane(brinks[i].x1, brinks[i].y1, brinks[i].z1, brinks[i].x2, brinks[i].y2, brinks[i].z2, brinks[i].x3, brinks[i].y3, brinks[i].z3))
		try:
			p_x, p_y, p_z = map(float, cur_ray.cross_plane(A, B, C, D))
			if cur_ray.dir_x != 0.0:
				k = (p_x - cur_ray.x) / cur_ray.dir_x
			elif cur_ray.dir_y != 0.0:
				k = (p_y - cur_ray.y) / cur_ray.dir_y
			else:
				k = (p_z - cur_ray.z) / cur_ray.dir_z
			if k < 0.0:
				continue
			if k == 0.0 and reflected == 0:
				continue
			p_x = round(p_x, 8)
			p_y = round(p_y, 8)
			p_z = round(p_z, 8)
			if not(p_x >= min_x and p_x <= max_x and p_y >= min_y and p_y <= max_y and p_z >= min_z and p_z <= max_z):
				continue
			print(1)
			print(cur_ray.energy)
			print(p_x, p_y, p_z)
			print(cur_ray.dir_x, cur_ray.dir_y, cur_ray.dir_z)
			break
		except:
			continue
	exit(0)