#!/bin/bash
if [ $(pwd) == "/home/klee" ] ; then
    clang -I ${HOME}/klee_src/include -emit-llvm -g -c app/crc32_symbol.c
else
    echo "Please run this scripts in the klee/klee docker !"
fi

