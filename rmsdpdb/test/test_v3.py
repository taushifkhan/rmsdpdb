import random

import v3


def random_mag(): 
  return random.uniform(-90, 90)


def random_vector():
  return v3.vector(random_mag(), random_mag(), random_mag())


def random_rotation():
  return v3.rotation(random_vector(), v3.radians(random_mag()))


def random_matrix():
  return v3.combine(
      random_rotation(), v3.translation(random_vector()))


def test_orthogonality():
  x = v3.vector(random_mag(), 0, 0)
  y = v3.vector(0, random_mag(), 0)
  z = v3.vector(0, 0, random_mag())

  ry_x = v3.transform(v3.rotation(y, v3.radians(90)), x)
  assert v3.is_similar_vector(v3.norm(ry_x), -v3.norm(z))
  assert v3.is_similar_mag(v3.mag(ry_x), v3.mag(x))

  ry_z = v3.transform(v3.rotation(y, v3.radians(90)), z)
  assert v3.is_similar_vector(v3.norm(ry_z), v3.norm(x))

  cross_x_y = v3.cross(x, y)
  assert v3.is_similar_vector(v3.norm(cross_x_y), v3.norm(z))

  cross_y_x = v3.cross(y, x)
  assert v3.is_similar_vector(-v3.norm(cross_x_y), v3.norm(z))


def test_translation():
  x = random_vector()
  y = random_vector()
  x_and_y = v3.transform(v3.translation(y), x)
  assert v3.is_similar_vector(x_and_y, x+y)


def test_rotation():
  x = random_vector()
  m_x = v3.transform(random_rotation(), x)
  assert v3.is_similar_mag(v3.mag(x), v3.mag(m_x))


def test_matrix_combination():
  n = 4
  x = random_vector()
  y1 = v3.vector(x)
  matrix = v3.identity()
  for r_matrix in [random_matrix() for i in range(4)]:
    y1 = v3.transform(r_matrix, y1)
    matrix = v3.combine(r_matrix, matrix)
  y2 = v3.transform(matrix, x)
  assert v3.is_similar_vector(y1, y2)


def test_inverse():
  m = random_matrix()
  m_left_inv = v3.left_inverse(m)
  m_return = v3.combine(m_left_inv, m)
  assert v3.is_similar_matrix(v3.identity(), m_return)


def test_superposition():
  n = 30
  vecs1 = [random_vector() for i in range(n)]
  m = random_rotation()
  vecs2 = [v3.transform(m, vec1) for vec1 in vecs1]
  superposition = v3.superposition(vecs1, vecs2)
  for vec1, vec2 in zip(vecs1, vecs2):
    m_vec1 = v3.transform(superposition, vec1)
    assert v3.is_similar_vector(m_vec1, vec2)


def test_rmsd():
  n = 30
  vecs1 = [random_vector() for i in range(n)]
  m = random_rotation()
  vecs2 = [v3.transform(m, vec1) for vec1 in vecs1]
  assert v3.is_similar_mag(0, v3.rmsd(vecs1, vecs2))


