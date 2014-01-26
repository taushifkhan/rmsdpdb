import unittest
import random

import rmsdpdb.v3 as v3


def test_orthogonality():
  x = v3.vector(v3.random_mag(), 0, 0)
  y = v3.vector(0, v3.random_mag(), 0)
  z = v3.vector(0, 0, v3.random_mag())
  ry_x = v3.transform(v3.rotation(y, v3.radians(90)), x)
  assert v3.is_similar_vector(v3.norm(ry_x), -v3.norm(z))
  assert v3.is_similar_mag(v3.mag(ry_x), v3.mag(x))
  ry_z = v3.transform(v3.rotation(y, v3.radians(90)), z)
  assert v3.is_similar_vector(v3.norm(ry_z), v3.norm(x))
  cross_x_y = v3.cross(x, y)
  assert v3.is_similar_vector(v3.norm(cross_x_y), v3.norm(z))
  cross_y_x = v3.cross(y, x)
  assert v3.is_similar_vector(v3.norm(cross_x_y), -v3.norm(z))


def test_translation():
  x = v3.vector(v3.random_mag(), 0, 0)
  y = v3.vector(0, v3.random_mag(), 0)
  x_and_y = v3.transform(v3.translation(y), x)
  assert v3.is_similar_vector(x_and_y, x+y)


def test_rotation():
  x = v3.random_vector()
  y = v3.transform(v3.random_rotation(), x)
  assert v3.is_similar_mag(v3.mag(x), v3.mag(y))


def test_matrix_combination():
  n = 4
  x = v3.random_vector()
  y1 = v3.vector(x)
  matrix = v3.identity()
  for i in range(4):
    r_matrix = v3.random_matrix()
    y1 = v3.transform(r_matrix, y1)
    matrix = v3.combine(r_matrix, matrix)
  y2 = v3.transform(matrix, x)
  assert v3.is_similar_vector(y1, y2)


def test_inverse():
  m = v3.random_matrix()
  m_left_inv = v3.left_inverse(m)
  assert v3.is_similar_matrix(v3.identity(), v3.combine(m_left_inv, m))


def test_superposition():
  n = 4
  crds1 = [v3.random_vector() for i in range(n)]
  random_m = v3.random_rotation()
  crds2 = [v3.transform(random_m, c) for c in crds1]
  m = v3.superposition(crds1, crds2)
  for crd1, crd2 in zip(crds1, crds2):
    assert v3.is_similar_vector(v3.transform(m, crd1), crd2)


def test_rmsd():
  n = 4
  crds1 = [v3.random_vector() for i in range(n)]
  random_m = v3.random_rotation()
  crds2 = [v3.transform(random_m, c) for c in crds1]
  rmsd = v3.rmsd(crds1, crds2)
  assert v3.is_similar_mag(0, rmsd)


def test_rmsd_and_superposition():
  n = 4
  crds1 = [v3.random_vector() for i in range(n)]
  crds2 = [v3.random_vector() for i in range(n)]
  rmsd = v3.rmsd(crds1, crds2)
  m = v3.superposition(crds1, crds2)
  crds1 = [v3.transform(m, c) for c in crds1]
  superposition_rmsd = v3.sum_rmsd(crds1, crds2)
  assert v3.is_similar_mag(rmsd, superposition_rmsd)
