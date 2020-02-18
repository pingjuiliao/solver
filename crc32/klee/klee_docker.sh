#!/bin/bash
docker run -it --rm --name klee_eval_crc32  \
    -v $(pwd):/home/klee/app/ klee/klee






#--mount type=bind,source="$(pwd)",target=/home/klee/app \

