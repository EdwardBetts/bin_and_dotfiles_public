#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <algorithm>
#include <fstream>
#include "TFile.h"
#include "TKey.h"
#include "TTree.h"

using namespace std;

////////////////////////////////////////////////////////////////////////
//prototypes
int check_existence(char *filename, int verbose);
int check_structure(char *filename,char *key_name,char *key_class,int verbose);
int check_Nevents(char *filename,char *key_name,char *key_class,int Nevents,int verbose);

////////////////////////////////////////////////////////////////////////
//main function
int main (int argc, char *argv[])
{
  //------------------------------------------------------
  //reading and checking input arguments
  if(argc<2)
    {
      printf("not enough arguments\n");
      printf("You gave %d argumenst.\n",argc-1);
      printf("At least 1 argument is needed:\n");
      printf("char *filename, char *key_name=\"cbmsim\", char *key_class=\"TTree\", int Nevents=1000, int pattern=7=existence/structure/Nevents, int verbose=1\n");
      printf("pattern=7=existence+structure+Nevents\n");
      printf("pattern=5=existence+Nevents\n");
      printf("pattern=2=structure\n");
      printf("...\n");
      exit(-1);
    }

  char filename[256];
  char key_name[256];
  strcpy(key_name,"cbmsim");
  char key_class[256];
  strcpy(key_class,"TTree");
  int Nevents=1000;
  int pattern=7;
  int verbose=1;

  if(argc>1)
    strcpy(filename,argv[1]);
  if(argc>2)
    strcpy(key_name,argv[2]);
  if(argc>3)
    strcpy(key_class,argv[3]);
  if(argc>4)
    Nevents=atoi(argv[4]);
  if(argc>5)
    pattern=atoi(argv[5]);
  if(argc>6)
    verbose=atoi(argv[6]);

  printf("===========================\n");
  printf("filename=%s\n",filename);
  printf("key_name=%s\n",key_name);
  printf("key_class=%s\n",key_class);
  printf("Nevents=%d\n",Nevents);
  printf("pattern=%d\n",pattern);
  printf("verbose=%d\n",verbose);
  printf("===========================\n");

  //------------------------------------------------------
  int ret=0;
  if(pattern & 0x4)
    if(check_existence(filename,verbose))
      ret=ret+4;
  if(pattern & 0x2)
    if(check_structure(filename,key_name,key_class,verbose))
      ret=ret+2;
  if(pattern & 0x1)
    if(check_Nevents(filename,key_name,key_class,Nevents,verbose))
      ret=ret+1;
  printf("===========================\n");
  printf("ret=%d\n",ret);
  if(ret & 0x4)
    printf("existence: OK\n");
  else
    printf("existence: FAILED\n");
  if(ret & 0x2)
    printf("structure: OK\n");
  else
    printf("structure: FAILED\n");
  if(ret & 0x1)
    printf("Nevents: OK\n");
  else
    printf("Nevents: FAILED\n");
  printf("===========================\n");
  //------------------------------------------------------
  if(ret==pattern)
    return(1);
  else
    return(0);
}

////////////////////////////////////////////////////////////////////////
//check_existence
int check_existence(char *filename, int verbose)
{
  fstream fin;
  fin.open(filename,ios::in);
  if( fin.is_open() )
    {
      if(verbose)
        cout<<"file "<<filename<<" exists"<<endl;
      return(1);
    }
  else
    {
      if(verbose)
        cerr<<"error: file "<<filename<<" does not exist"<<endl;
      return(0);
    }
  fin.close();
}

////////////////////////////////////////////////////////////////////////
//check_structure
int check_structure(char *filename,char *key_name,char *key_class,int verbose)
{
  int ok=0;
  TFile f(filename,"READ");
  if(f.IsZombie())
    {
      if(verbose)
        cout<<"ERROR: File "<<filename<<" not found"<<endl;
      return(0);
    }
  TIter next(f.GetListOfKeys());
  TKey *key;
  while ((key=(TKey*)next()))
    {
      if(strcmp(key->GetName(),key_name) == 0 && strcmp(key->GetClassName(),key_class) == 0)
        ok=1;
    }
  f.Close();
  if(ok==1)
    {
      return(1);
    }
  else
    {
      if(verbose)
        cout<<"ERROR: Key "<<key_name<<" pointing to object of class "<<key_class<<" not found."<<endl;
      return(0);
    }
}

////////////////////////////////////////////////////////////////////////
//check_Nevents
int check_Nevents(char *filename,char *key_name,char *key_class,int Nevents,int verbose)
{
  //get the nb of events
  int N=-1;
  TFile InputFile(filename,"READ");
  if(InputFile.IsZombie())
    {
      if(verbose)
        cout<<"ERROR: File "<<filename<<" not found"<<endl;
      return(0);
    }
  TTree *InputTree = (TTree*)InputFile.Get(key_name);
  if(!InputTree)
    {
      cout<<"ERROR: File "<<filename<<" is corrupt"<<endl;
      return(0);
    }
  N=InputTree->GetEntries();
  InputFile.Close();

  if(verbose)
    printf("N=%d\n",N);

  //compare N with Nevents
  if(N!=Nevents)
    return(0);
  else
    return(1);
}

////////////////////////////////////////////////////////////////////////
