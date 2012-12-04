SELECT mol_amw('c1ccccc1'::mol) mol_amw;
SELECT mol_logp('c1ccccc1'::mol) mol_logp;
SELECT mol_hba('c1ccccc1'::mol) mol_hba;
SELECT mol_hbd('c1ccccc1'::mol) mol_hbd;
SELECT mol_hba('c1ccncc1'::mol) mol_hba;
SELECT mol_hbd('c1ccncc1'::mol) mol_hbd;
SELECT mol_hbd('c1ccncc1O'::mol) mol_hbd;
SELECT mol_hba('c1ccncc1O'::mol) mol_hba;
SELECT mol_logp('c1ccncc1O'::mol) mol_logp;
SELECT mol_numrotatablebonds('CCC'::mol) mol_numrotatablebonds;
SELECT mol_numrotatablebonds('CCCC'::mol) mol_numrotatablebonds;
SELECT mol_numrotatablebonds('c1ccccc1c1ccc(CCC)cc1'::mol) mol_numrotatablebonds;
SELECT mol_numheavyatoms('CCC'::mol) val;
SELECT mol_numatoms('CCC'::mol) val;
SELECT mol_numheteroatoms('CCC'::mol) val;
SELECT mol_numheteroatoms('CCO'::mol) val;
SELECT mol_tpsa('CCC'::mol) val;
SELECT mol_tpsa('CCO'::mol) val;
SELECT mol_numrings('CCC'::mol) val;
SELECT mol_numrings('C1CC1'::mol) val;
SELECT mol_murckoscaffold('c1ccccc1CCC'::mol) val;
SELECT mol_murckoscaffold('CSC(C)=O'::mol) is NULL;
