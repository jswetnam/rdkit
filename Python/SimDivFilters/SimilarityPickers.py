# $Id: SimilarityPickers.py 5042 2006-03-02 19:36:20Z glandrum $
#
# Copyright (C) 2003 Rational Discovery LLC
#  All Rights Reserved
#
import RDConfig
import DataStructs
from DataStructs.TopNContainer import TopNContainer
import bisect

class TopNOverallPicker(object):
  """  A class for picking the top N overall best matches across a library

  Connect to a database:
  >>> import os.path
  >>> from Dbase.DbConnection import DbConnect
  >>> if RDConfig.usePgSQL:
  ...   dbName = "::RDTests"
  ... else:
  ...   dbName = os.path.join(RDConfig.RDCodeDir,'SimDivFilters','test_data','data.gdb')
  >>> conn = DbConnect(dbName,'simple_mols1_fp')
  >>> [x.upper() for x in conn.GetColumnNames()]
  ['ID', 'AUTOFRAGMENTFP']

  Create a supplier to give us fingerprints from the database:
  >>> import Chem
  >>> from Chem.Fingerprints.DbFpSupplier import RandomAccessDbFpSupplier as FpSupplier
  >>> suppl = FpSupplier(conn.GetData())
  >>> len(suppl)
  12
  
  Start by finding the top matches for a single probe.  This ether should pull
  other ethers from the db:
  >>> mol = Chem.MolFromSmiles('COC')
  >>> probeFp = Chem.DaylightFingerprint(mol)
  >>> picker = TopNOverallPicker(numToPick=2,probeFps=[probeFp],dataSet=suppl)
  >>> len(picker)
  2
  >>> fp,score = picker[0]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-1'
  >>> score
  1.0

  The results come back in order:
  >>> fp,score = picker[1]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-2'

  Now find the top matches for 2 probes.  We'll get one ether and one acid:
  >>> fps = []
  >>> fps.append(Chem.DaylightFingerprint(Chem.MolFromSmiles('COC')))
  >>> fps.append(Chem.DaylightFingerprint(Chem.MolFromSmiles('CC(=O)O')))
  >>> picker = TopNOverallPicker(numToPick=3,probeFps=fps,dataSet=suppl)
  >>> len(picker)
  3
  >>> fp,score = picker[0]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'acid-1'
  >>> fp,score = picker[1]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-1'
  >>> score
  1.0
  >>> fp,score = picker[2]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'acid-2'
  
  
  """
  def __init__(self,numToPick=10,probeFps=None,dataSet=None,
               simMetric=DataStructs.TanimotoSimilarity):
    """

      dataSet should be a sequence of BitVectors

    """
    self.numToPick = numToPick
    self.probes = probeFps
    self.data = dataSet
    self.simMetric = simMetric
    self._picks = None

  def MakePicks(self,force=0):
    if self._picks is not None and not force:
      return
    picks = TopNContainer(self.numToPick)
    for fp in self.data:
      origFp = fp
      bestScore = -1.0
      for probeFp in self.probes:
        score = DataStructs.FingerprintSimilarity(origFp,probeFp,
                                                  self.simMetric)
        bestScore = max(score,bestScore)
      picks.Insert(bestScore,fp)
    self._picks = []
    for score,pt in picks:
      self._picks.append((pt,score))
    self._picks.reverse()  
  def __len__(self):
    if self._picks is None:
      self.MakePicks()
    return len(self._picks)
  def __getitem__(self,which):
    if self._picks is None:
      self.MakePicks()
    return self._picks[which]
          


class SpreadPicker(object):
  """  A class for picking the best matches across a library

  Connect to a database:
  >>> import os.path
  >>> from Dbase.DbConnection import DbConnect
  >>> if RDConfig.usePgSQL:
  ...   dbName = "::RDTests"
  ... else:
  ...   dbName = os.path.join(RDConfig.RDCodeDir,'SimDivFilters','test_data','data.gdb')
  >>> conn = DbConnect(dbName,'simple_mols1_fp')
  >>> [x.upper() for x in conn.GetColumnNames()]
  ['ID', 'AUTOFRAGMENTFP']

  Create a supplier to give us fingerprints from the database:
  >>> import Chem
  >>> from Chem.Fingerprints.DbFpSupplier import RandomAccessDbFpSupplier as FpSupplier
  >>> suppl = FpSupplier(conn.GetData())
  >>> len(suppl)
  12
  
  Start by finding the top matches for a single probe.  This ether should pull
  other ethers from the db:
  >>> mol = Chem.MolFromSmiles('COC')
  >>> probeFp = Chem.DaylightFingerprint(mol)
  >>> picker = SpreadPicker(numToPick=2,probeFps=[probeFp],dataSet=suppl)
  >>> len(picker)
  2
  >>> fp,score = picker[0]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-1'
  >>> score
  1.0

  The results come back in order:
  >>> fp,score = picker[1]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-2'

  Now find the top matches for 2 probes.  We'll get one ether and one acid:
  >>> fps = []
  >>> fps.append(Chem.DaylightFingerprint(Chem.MolFromSmiles('COC')))
  >>> fps.append(Chem.DaylightFingerprint(Chem.MolFromSmiles('CC(=O)O')))
  >>> picker = SpreadPicker(numToPick=3,probeFps=fps,dataSet=suppl)
  >>> len(picker)
  3
  >>> fp,score = picker[0]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-1'
  >>> score
  1.0
  >>> fp,score = picker[1]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'acid-1'
  >>> score
  1.0
  >>> fp,score = picker[2]
  >>> id = fp._fieldsFromDb[0]
  >>> id
  'ether-2'

  
  
  """
  def __init__(self,numToPick=10,probeFps=None,dataSet=None,
               simMetric=DataStructs.TanimotoSimilarity,
               expectPickles=True,onlyNames=False):
    """

      dataSet should be a sequence of BitVectors or, if expectPickles
      is False, a set of strings that can be converted to bit vectors

    """
    self.numToPick = numToPick
    self.probes = probeFps
    self.data = dataSet
    self.simMetric = simMetric
    self.expectPickles = expectPickles
    self.onlyNames=onlyNames
    
    self._picks = None

  def MakePicks(self,force=0,silent=True):
    if self._picks is not None and not force:
      return

    # start by getting the NxM score matrix
    #  (N=num probes, M=num fps)
    nProbes = len(self.probes)
    scores = [None]*nProbes
    for i in range(nProbes):
      scores[i] = []
    j = 0
    fps = []
    for origFp in self.data:
      for i in range(nProbes):
        score = DataStructs.FingerprintSimilarity(self.probes[i],origFp,
                                                  self.simMetric)
        bisect.insort(scores[i],(score,j))
        if len(scores[i])>=self.numToPick:
          del scores[self.numToPick:]
      if self.onlyNames and hasattr(origFp,'_fieldsFromDb'):
        fps.append(origFp._fieldsFromDb[0])
      else:
        fps.append(origFp)
      j+=1
      if not silent and not j%1000:
        print 'scored %d fps'%j

    # sort the rows of that matrix:
    #for i in range(nProbes):
    #  scores[i].sort()

    # now go probe by probe and select the current top entry until we are finished:
    nPicked = 0
    self._picks = []
    taken = [0]*len(fps)
    while nPicked < self.numToPick:
      rowIdx = nPicked%len(scores)
      row = scores[rowIdx]
      score,idx = row.pop()
      # make sure we haven't taken this one already (from another row):
      while taken[idx] and len(row):
        score,idx = row.pop()
      if not taken[idx]:
        fp = fps[idx]
        self._picks.append((fp,score))
        taken[idx]=1
        nPicked += 1

  def __len__(self):
    if self._picks is None:
      self.MakePicks()
    return len(self._picks)
  def __getitem__(self,which):
    if self._picks is None:
      self.MakePicks()
    return self._picks[which]



  
#------------------------------------
#
#  doctest boilerplate
#
def _test():
  import doctest,sys
  return doctest.testmod(sys.modules["__main__"])

if __name__ == '__main__':
  import sys
  failed,tried = _test()
  sys.exit(failed)
