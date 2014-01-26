

# match.py


Calculates the CA rmsd between two PDB structures, and generates the
optimal superposition between them

Requires: numpy and python 2.4 or higher


Usage: python match.py [-nrs] pdb1 pdb2 segments1 [segments2]


-n Calculates direct RMSD without any rotations

-r Calculates RMSD without saving rotated structure

-s Show aligned structures with pymol

segments1: a string that encodes the residues to be matched from
pdb1. if segments2 is not given, it is assumed that the residues
listed in segments1 will be used for pdb2

segments2: string encoding residues from pdb2

format of the string: e.g, "[('A:5', 'A:10'), ('B:3', 'B:19')]". For
convenience, the ":" character is optional, and quotes are not
needed if there are chain identifiers. Put insertions at the end of
the residue tag "A:335E"

Copyright (c) 2010, 2007 Bosco Ho
