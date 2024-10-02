if [ "$#" -ne 5 ]; then
  echo "Usage: ./create_inters.sh <dataset> <syt> <expr> <sql_expr> <mode>"
  exit
fi
dataset=$1
syt=$2
expr=$3
sql_expr=$4
mode=$5
python ./create_interactions.py \
    --dataset ${dataset} \
    --syt ${syt} \
    --expr ${expr} \
    --sql_expr ${sql_expr} \
    --mode ${mode}
