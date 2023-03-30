#!/bin/bash
# Get the unique nodes allocated for the job
NODES=$(scontrol show hostname $SLURM_JOB_NODELIST)

# Create and empty the hostfile
echo -n "" > hostfile

# Loop through the nodes and add them to the hostfile
for NODE in $NODES; do
  echo $NODE >> hostfile
done

