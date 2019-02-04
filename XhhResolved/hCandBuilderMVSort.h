#ifndef XhhResolved_hCandBuilderMVSort_H
#define XhhResolved_hCandBuilderMVSort_H

#include <XhhResolved/hCandBuilderBase.h>

class hCandBuilderMVSort : public hCandBuilderBase
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
 public:
  
  // this is a standard constructor
  hCandBuilderMVSort ();
  ~hCandBuilderMVSort ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode buildHCands ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(hCandBuilderMVSort, 1);

 private:
  TRandom3* m_randGen;
};

#endif
