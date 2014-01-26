import unittest
import random

import v3


def random_vector():
  return v3.vector(
      random.uniform(-100, 100),
      random.uniform(-100, 100),
      random.uniform(-100, 100))


def random_rotation():
  axis = random_vector()
  angle = random.uniform(-v3.radians(90), v3.radians(90))
  return v3.rotation(axis, angle)


def random_matrix():
  r = random_rotation()
  m = v3.translation(random_vector())
  return v3.combine(r, m)


def test_orthogonal_rotation():
  x = v3.vector(2, 0, 0)
  y = v3.vector(0, 3, 0)
  z = v3.vector(0, 0, 6)

  ry_x = v3.transform(v3.rotation(y, v3.radians(90)), x)
  assert v3.is_similar_vector(v3.norm(ry_x), -v3.norm(z))
  assert v3.is_similar_mag(v3.mag(ry_x), v3.mag(x))

  ry_z = v3.transform(v3.rotation(y, v3.radians(90)), z)
  assert v3.is_similar_vector(v3.norm(ry_z), v3.norm(x))


def test_translation():
  x = v3.vector(2, 0, 0)
  y = v3.vector(0, 3, 0)
  assert v3.is_similar_vector(v3.transform(v3.translation(y), x), x+y)


def test_rotation():
  x = v3.vector(2, 0, 0)
  assert v3.is_similar_mag(v3.mag(x), v3.mag(v3.transform(random_rotation(), x)))


def test_matrix_combination():
  n = 4
  x = random_vector()
  y1 = v3.vector(x)
  matrix = v3.identity()
  for i in range(4):
    r_matrix = random_matrix()
    y1 = v3.transform(r_matrix, y1)
    matrix = v3.combine(r_matrix, matrix)
  y2 = v3.transform(matrix, x)
  assert v3.is_similar_vector(y1, y2)


def test_inverse():
  m = random_matrix()
  m_left_inv = v3.left_inverse(m)
  assert v3.is_similar_matrix(v3.identity(), v3.combine(m_left_inv, m))


