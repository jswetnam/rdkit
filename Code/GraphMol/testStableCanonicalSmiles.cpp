// Test an issue with generating stable canonical SMILES
// from molecules with two neighboring double bonds
#include <set>

#include <RDGeneral/utils.h>
#include <RDGeneral/Invariant.h>
#include <RDGeneral/RDLog.h>
//#include <boost/log/functions.hpp>
#include <GraphMol/RDKitBase.h>
#include <GraphMol/Canon.h>
#include <GraphMol/SmilesParse/SmilesParse.h>
#include <GraphMol/SmilesParse/SmilesWrite.h>
#include <GraphMol/FileParsers/FileParsers.h>

#include <iostream>

using namespace RDKit;
using std::string;
using std::set;

void testStableCanonicalSmilesFromCHEMBL451537(){
  string rdbase = getenv("RDBASE");
  set<string> canon_smi;
  for (int i=0; i < 1000; ++i) {
    RWMol* mol = MolFileToMol(rdbase + "Code/GraphMol/test_data/CHEMBL451537.mol");
    string smi = MolToSmiles(*mol,
        true,  // Do isomeric SMILES
        true,  // Canonical SMILES
        false);
    BOOST_LOG(rdInfoLog) << smi << "\n";

    canon_smi.insert(smi);  // All bonds explicit
    TEST_ASSERT(canon_smi.size()==1);
  }
};


int main(){
  RDLog::InitLogs();
  testStableCanonicalSmilesFromCHEMBL451537();
  return 0;
}


