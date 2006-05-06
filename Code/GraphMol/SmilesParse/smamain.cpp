// $Id: smamain.cpp 4974 2006-02-18 00:49:21Z glandrum $
//
//  Copyright (C) 2001-2006 Randal Henne, Greg Landrum and Rational Discovery LLC
//
//   @@ All Rights Reserved  @@
//
#include <iostream>
#include "SmilesParse.h"
#include "SmilesWrite.h"
#include <RDGeneral/RDLog.h>

using namespace RDKit;
using namespace std;
typedef ROMol Mol;
int
main(int argc, char *argv[])
{
  RDLog::InitLogs();
  int i=0;
  Mol *mol;
	
  if(argc < 2){
    return 1;
  } else {

    string sma;
    bool debugParse = false;
    int startP=1;
    if(argc>2){
      string arg(argv[1]);
      if(arg=="-d"){
	debugParse = true;
	startP = 2;
      }
    }

    while(startP<argc){
      sma = argv[startP++];
      std::cout << "In SMARTS: " << sma << std::endl;
      mol = SmartsToMol(sma,debugParse);
      if(!mol){
	BOOST_LOG(rdErrorLog) << "FAILED PARSE: " << sma << std::endl;
      }
    }
  }	
  
  return 1;
}
