

# rmsdpdb

Calculates the CA rmsd between two PDB structures, and generates the
optimal superposition between them

Installation:

    pip install rmsdpdb

`rmsdpdb` depends on `numpy` that should be installed by pip

Usage: 

    rmsdpdb -o transform_pdb1 pdb1 pdb2 [segments1] [segments2]

- transform_pdb1: PDB with the optimal superposition of pdb1 to pdb2,
                if not selected, optimal rotation will not
                be calculated

- segments1: string that encodes the residues to be matched from pdb1,
           if none given, all residues are considered

- segments2: string encoding residues from pdb2, if not given,
           assumed to be same as segments1

The format of the segments string: 

  - e.g. "A:5-A:10 B:3-B:19" gives two discrete segments on
    chain A and on chain B, there are no spaces between the '-' characters
  - the ":" character is optional if there are no chain identifiers
  - insertions at the end of the residue tag "A:335E"

The RMSD calculation leverages the SVD decomposition available in the 
`numpy` package.

Copyright (c) 2010, 2007 Bosco Ho
