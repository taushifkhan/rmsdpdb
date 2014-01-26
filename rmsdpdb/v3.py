import random
import numpy as np


def is_similar_mag(a, b, small=1E-5):
  return abs(abs(a)-abs(b)) <= small


def vector(*args):
  n_arg = len(args)
  if n_arg == 0:
    return np.zeros(3, dtype=np.float)
  if n_arg == 1:
    data = args[0]
    if len(data) == 3:
      return np.array(data, copy=True)
    raise TypeError('vector() with 1 argument must have 3 elements')
  if n_arg == 3:
    return np.array(args, dtype=np.float, copy=True)
  else:
    raise TypeError('vector() takes 0, 1 or 3 arguments')


def set_vector(*args):
  "Changes values of a vector in place"
  vector = args[0]
  if len(args) == 2:
    vector[:] = args[1]
  elif len(args) == 4:
    vector[:] = args[1:4]


def crd(vector):
  "Returns values of vector as a sequence of floats"
  return vector


def is_similar_matrix(m1, m2):
  iter1 = np.ndenumerate(m1)
  iter2 = np.ndenumerate(m2)
  for (i1, val1), (i2, val2) in zip(iter1, iter2):
    if not is_similar_mag(val1, val2):
      return False
  return True


is_similar_vector = is_similar_matrix


def mag(vector):
  return np.sqrt(np.dot(vector, vector))


def scale(vector, s):
  return  s*vector


def norm(vector):
  return scale(vector, 1.0/mag(vector))


def distance(p1, p2):
  return mag(p1 - p2)


radians = np.radians

degrees = np.degrees

cross = np.cross

dot = np.dot


def identity():
  m = np.zeros((4, 3))
  m[:3,:3] = np.eye(3)
  return m


def transform(matrix, vector):
  return np.dot(matrix[:3,:3], vector) + matrix[3,:]  


def left_inverse(matrix):
  inverse = identity()
  r = matrix[:3,:3].transpose()
  inverse[:3,:3] = r
  inverse[3,:] = -np.dot(r, matrix[3,:])
  return inverse


# from http://stackoverflow.com/a/6802723
# uses the right hand screw rule for theta
def rotation(axis, theta):
  m = identity()
  a = np.cos(theta/2)
  b, c, d = norm(axis) * np.sin(theta/2)
  m[0] = [a*a+b*b-c*c-d*d, 2*(b*c-a*d),     2*(b*d+a*c)    ]
  m[1] = [2*(b*c+a*d),     a*a+c*c-b*b-d*d, 2*(c*d-a*b)    ]
  m[2] = [2*(b*d-a*c),     2*(c*d+a*b),     a*a+d*d-b*b-c*c]
  return m


def translation(displacement):
  m = identity()
  m[3,:] = displacement
  return m


def combine(m1, m2):
  m3 = identity()
  m3[:3,:3] = np.dot(m1[:3,:3], m2[:3,:3])
  m3[3,:] = np.dot(m1[:3,:3], m2[3,:]) + m1[3,:]
  return m3


def rotation_at_center(axis, theta, center):
  t = translation(-center)
  r = rotation(axis, theta)
  t_inv = translation(center)
  return combine(t_inv, combine(r, t))


def rmsd(in_crds1, in_crds2):
  """Returns RMSD between 2 sets of [nx3] np array"""

  crds1 = np.array(in_crds1)
  crds2 = np.array(in_crds2)
  assert(crds1.shape[1] == 3)
  assert(crds1.shape == crds2.shape)

  n_vec = np.shape(crds1)[0]
  correlation_matrix = np.dot(np.transpose(crds1), crds2)
  v, s, w = np.linalg.svd(correlation_matrix)
  is_reflection = (np.linalg.det(v) * np.linalg.det(w)) < 0.0
  if is_reflection:
    s[-1] = - s[-1]
  E0 = sum(sum(crds1 * crds1)) + \
       sum(sum(crds2 * crds2))
  rmsd_sq = (E0 - 2.0*sum(s)) / float(n_vec)
  rmsd_sq = max([rmsd_sq, 0.0])
  return np.sqrt(rmsd_sq)


def superposition(in_ref_crds, in_target_crds):
  """
  Returns best transform m between two sets of [nx3] arrays.
  
  Direction: transform(m, ref_crd) => target_crd.
  """

  ref_crds = np.array(in_ref_crds)
  target_crds = np.array(in_target_crds)
  assert(ref_crds.shape[1] == 3)
  assert(ref_crds.shape == target_crds.shape)

  correlation_matrix = np.dot(np.transpose(ref_crds), target_crds)
  v, s, w = np.linalg.svd(correlation_matrix)
  is_reflection = (np.linalg.det(v) * np.linalg.det(w)) < 0.0
  if is_reflection:
    v[-1,:] = -v[-1,:]

  rot33 = np.dot(v, w)
  m = identity()
  m[:3,:3] = rot33.transpose()

  return m


def sum_rmsd(crds1, crds2):
  sum_squared = 0.0
  for crd1, crd2 in zip(crds1, crds2):
    sum_squared += distance(crd1, crd2)**2
  return np.sqrt(sum_squared/float(len(crds1)))
  

def random_mag(): 
  return random.uniform(-90, 90)


def random_vector():
  return vector(random_mag(), random_mag(), random_mag())


def random_rotation():
  return rotation(random_vector(), radians(random_mag()))


def random_matrix():
  return combine(random_rotation(), translation(random_vector()))

