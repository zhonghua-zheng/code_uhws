#!/bin/bash
for i in {002..033}
do
  echo "qsub $i.sub"
  qsub $i.sub
done