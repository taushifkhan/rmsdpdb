import v3


def pad_atom_type(in_atom_type):
  atom_type = in_atom_type
  if len(atom_type) == 1:
    atom_type = " %s  " % atom_type
  elif len(atom_type) == 2:
    atom_type = " %s " % atom_type
  elif len(atom_type) == 3:
    if atom_type[0].isdigit():
      atom_type = "%s " % atom_type
    else:
      atom_type = " %s" % atom_type
  return atom_type


class Atom:
  def __init__(self):
    self.is_hetatm = False
    self.pos = v3.vector()
    self.vel = v3.vector()
    self.mass = 0.0
    self.type = ""
    self.element = ""
    self.chain_id = " "
    self.res_type = ""
    self.res_num = ""
    self.res_insert = ""
    self.bfactor = 0.0
    self.occupancy = 0.0
    self.num = 0
  
  def pdb_str(self):
    if self.is_hetatm:
      field = "HETATM"
    else:
      field = "ATOM  "
    x, y, z = v3.crd(self.pos)
    return "%6s%5s %4s %3s %1s%4d%1s   %8.3f%8.3f%8.3f%6.2f%6.2f" \
            % (field, self.num, 
               pad_atom_type(self.type),
               self.res_type, self.chain_id,
               self.res_num, self.res_insert,
               x, y, z,
               self.occupancy, self.bfactor)
               
  def __str__(self):
    x, y, z = v3.crd(self.pos)
    return "%s%s-%s (% .1f % .1f % .1f)" \
            %  (self.res_type, self.res_num, 
                self.type, x, y, z)

  def transform(self, matrix):
    new_pos = v3.transform(matrix, self.pos)
    v3.set_vector(self.pos, new_pos)


def AtomFromPdbLine(line):
  """Returns an Atom object from an atom line in a pdb file."""
  atom = Atom()
  if line.startswith('HETATM'):
    atom.is_hetatm = True
  else:
    atom.is_hetatm = False
  atom.num = int(line[6:11])
  atom.type = line[12:16].strip(" ")
  element = ''
  for c in line[12:15]:
    if not c.isdigit() and c != " ":
      element += c
  if element[:2] in two_char_elements:
    atom.element = element[:2]
  else:
    atom.element = element[0]
  atom.res_type = line[17:20]
  atom.chain_id = line[21]
  atom.res_num = int(line[22:26])
  atom.res_insert = line[26]
  if atom.res_insert == " ":
    atom.res_insert = ""
  x = float(line[30:38])
  y = float(line[38:46])
  z = float(line[46:54])
  v3.set_vector(atom.pos, x, y, z)
  try:
    atom.occupancy = float(line[54:60])
  except:
    atom.occupancy = 100.0
  try:
    atom.bfactor = float(line[60:66])
  except:
    atom.bfactor = 0.0
  return atom
  
  
def cmp_atom(a1, a2):
  if a1.num < a2.num:
    return -1
  else:
    return 0


radii = { 
 'H': 1.20,
 'N': 1.55,
 'NA': 2.27,
 'CU': 1.40,
 'CL': 1.75,
 'C': 1.70,
 'O': 1.52,
 'I': 1.98,
 'P': 1.80,
 'B': 1.85,
 'BR': 1.85,
 'S': 1.80,
 'SE': 1.90,
 'F': 1.47,
 'FE': 1.80,
 'K':  2.75,
 'MN': 1.73,
 'MG': 1.73,
 'ZN': 1.39,
 'HG': 1.8,
 'XE': 1.8,
 'AU': 1.8,
 'LI': 1.8,
 '.': 1.8
}
two_char_elements = [e for e in radii.keys() if len(e) == 2]


def add_radii(atoms):
  for atom in atoms:
    atom.radius = radii[atom.element]


def get_center(atoms):
  center = v3.vector()
  for atom in atoms:
    center += atom.pos
  return center/float(len(atoms))


def get_width(atoms, center):
  max_diff = 0
  for atom in atoms:
    diff = v3.distance(atom.pos, center)
    if diff > max_diff:
      max_diff = diff
  return 2*max_diff


class Molecule:

  def __init__(self):
    self.id = ''
    self._atoms = []

  def n_atom(self):
    return len(self._atoms)

  def atoms(self):
    return self._atoms

  def atom(self, i):
    return _atoms[i]
    
  def clear(self):
    for atom in self._atoms:
      del atom
    del self._atoms[:]

  def transform(self, matrix):
    for atom in self._atoms:
      atom.transform(matrix)

  def insert_atom(self, atom):
    self._atoms.append(atom)
    
  def erase_atom(self, atom_type):
    for atom in self._atoms:
      if atom.type == atom_type:
        self._atoms.remove(atom)
        del atom
        return

  def read_pdb(self, fname):
    self.clear()
    for line in open(fname, 'r').readlines():
      if line.startswith(("ATOM", "HETATM")):
        atom = AtomFromPdbLine(line);
        if len(self._atoms) == 1:
          self.id = atom.chain_id
        self.insert_atom(atom)
      if line.startswith("ENDMDL"):
        return

  def write_pdb(self, pdb):
    f = open(pdb, 'w')
    n_atom = 0
    for atom in sorted(self._atoms, cmp=cmp_atom):
      n_atom += 1
      atom.num = n_atom
      f.write(atom.pdb_str() + '\n')
    f.close()

