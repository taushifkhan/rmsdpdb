import copy
import string
import molecule


class Residue:

  def __init__(self, in_type, in_chain_id, in_num, in_insert=''):
    self.type = in_type
    self.chain_id = in_chain_id
    self.num = in_num
    self.insert = in_insert
    self._atom_dict = {}
 
  def __str__(self):
    atom_name_list = [a.type for a in self.atoms()]
    atom_name = " ".join(atom_name_list)
    return "%s-%s { %s }" % (self.type, self.num, atom_name)

  def copy(self):
    return copy.deepcopy(self)
  
  def n_atom(self):
    return len(self._atom_dict)
    
  def atom(self, atom_type):
    return self._atom_dict[atom_type]
    
  def has_atom(self, atom_type):
    return atom_type in self._atom_dict.keys()
    
  def atoms(self):
    return self._atom_dict.values()
  
  def atom_name(self, atom_type):
    return self.type + self.num + ":" + atom_type

  def insert_atom(self, atom):
    self._atom_dict[atom.type] = atom
    atom.chain_id = self.chain_id
    atom.res_num = self.num
    atom.res_type = self.type
  
  def erase_atom(self, atom_type):
    del self._atom_dict[atom_type]
    
  def set_num(self, i, insert=""):
    self.num = i
    self.insert = insert
    for atom in self.atoms():
      atom.res_num = self.num
      atom.res_insert = insert
     
  def inc_num(self):
    self.set_num(self.num+1, self.insert)

  def dec_num(self):
    self.set_num(self.num-1, self.insert)
    
  def dec_insert(self):
    l = self.insert;
    if l == "A" or l == "a":
      self.insert = ''
    else:
      i = string.ascii_letters.find(l)
      self.insert = string.ascii_letters[i-1]

  def transform(self, matrix):
     for atom in self.atoms():
       atom.transform(matrix)

  
class Polymer(molecule.Molecule):

  def __init__(self, fname=""):
    molecule.Molecule.__init__(self)
    self._residues = []
    if fname:
      self.read_pdb(fname)

  def copy(self):
    return copy.deepcopy(self)

  def residue(self, i):
    return self._residues[i]
    
  def residues(self):
    return self._residues

  def insert_atom(self, i, atom):
    self._atoms.append(atom)
    self.residue(i).insert_atom(atom)
    
  def erase_atom(self, i, atom_type):
    atom = self.residue(i).atom(atom_type)
    self._atoms.remove(atom)
    self.residue(i).erase_atom(atom_type)
    del atom
    
  def clear(self):
    del self._residues[:]
    molecule.Molecule.clear(self)
    
  def n_residue(self):
    return len(self._residues)
    
  def insert_residue(self, i, res):
    is_insertion = False
    if i < self.n_residue()-1:
      save_res_num = self.residue(i).num
      if self.residue(i+1).num == save_res_num:
        is_insertion = True

    if self.n_residue() == 0:
      res.set_num(res.num, res.insert)
    elif i < self.n_residue():
      res.set_num(self.residue(i).num, self.residue(i).insert)
    else:
      res.set_num(self.residue(i-1).num, "")
      res.inc_num()

    self._residues.insert(i, res)
    for atom in res.atoms():
      self.insert_atom(i, atom)

    for j in range(i+1, self.n_residue()):
      self.residue(j).inc_num()

    if is_insertion:
      while self.residue(i+1).insert:
        for j in range(i+1, self.n_residue()):
          if self.residue(j).res_num == save_res_num:
            self.residue(k).dec_insert()
    
  def append_residue(self, res):
    self._residues.append(res)
    for atom in res.atoms():
      self.insert_atom(self.n_residue()-1, atom)

  def erase_residue(self, i):  
    save_res_num = self.residue(i).num

    for atom in self.residue(i).atoms():
      self._atoms.remove(atom)
      del atom
    self._residues.pop(i)  
    
    if i < self.n_residue():
      if self.residue(i).num == save_res_num:
        # erasing residue in an insertion
        for j in range(i, self.n_residue()):
          if self.residue(j).num == erase_res_num_int:
            self.residue(j).dec_insert()
      else:
        for j in range(i, self.n_residue()):
          self.residue(j).dec_num()
    
  def extract_polymer(self, i, j):
    extract = Polymer()
    for res in self.residues()[i:j]:
      extract.append_residue(res.copy())
    return extract
 
  def insert_polymer(self, i, insert):
    for res in reversed(insert.residues()):
      self.insert_residue(i, res.copy())
    
  def __str__(self):
    res_name_list = [str(res) for res in self._residues]
    return "\n".join(res_name_list)
 
  def read_pdb(self, fname):
    self.clear()
    res_num = -1
    res_insert = " "
    for line in open(fname, 'r').readlines():
      if line.startswith("ATOM") or line.startswith("HETATM"):
        atom = molecule.AtomFromPdbLine(line);
        if (res_num != atom.res_num) or (res_insert != atom.res_insert):
          residue = Residue(atom.res_type, atom.chain_id,
                            atom.res_num, atom.res_insert)
          self.append_residue(residue)
          res_num = atom.res_num
          res_insert = atom.res_insert
        self.insert_atom(-1, atom)
      if line.startswith("ENDMDL"):
        return

  def write_pdb(self, pdb):
    f = open(pdb, 'w')
    n_atom = 0
    for res in self.residues():
      res_atoms = res.atoms()
      res_atoms.sort(molecule.cmp_atom)
      for atom in res_atoms:
        f.write(atom.pdb_str() + '\n')
    f.close()
