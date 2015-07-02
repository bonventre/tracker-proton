#!/bin/bash
rootcint -f Dict.cc -c Hit.h LinkDef.h
g++ -shared -fPIC -o Dict.so `root-config --ldflags` -I$ROOTSYS/include Dict.cc
