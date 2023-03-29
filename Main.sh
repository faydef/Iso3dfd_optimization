#!/bin/bash

# Définir la variable qui indique si l'option --parallel a été passée
parallel=false

# Récupérer les arguments
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --i) i="$2"; shift ;;
    --n1) n1="$2"; shift ;;
    --n2) n2="$2"; shift ;;
    --n3) n3="$2"; shift ;;
    --nt) nt="$2"; shift ;;
    --m) m="$2"; shift ;;
    --n) n="$2"; shift ;;
    --rho) rho="$2"; shift ;;
    --alpha) alpha="$2"; shift ;;
    --q) q="$2"; shift ;;
    --parallel) parallel=true ;;
    *) echo "Option invalide: $1" >&2; exit 1 ;;
  esac
  shift
done

# Afficher "lili" si l'option --parallel a été passée
if [ "$parallel" = true ]; then
    echo "executing /usr/bin/mpirun --hostfile hostfile --rank-by node --map-by ppr:1:node:PE=16 python3 parallel_ant_main.py $i $n $n1 $n2 $n3 $rho $alpha $q 30 "
    sbatch main.sh $i $n $n1 $n2 $n3 $rho $alpha $q 30 
else 
    echo "executing python3 main.py $@"
    srun -N 1 -n 32 --exclusive -p cpu_tp python3 main.py "$@"
fi


