if [ "$#" -ne 4 ]; then
  echo "Usage: ./fusion2inters.sh <dataset> <expr> <sql_expr> <mode>"
  exit
fi

dataset=$1
expr=$2
sql_expr=$3
mode=$4

python ./fusion_to_interactions.py \
    --dataset ${dataset} \
    --expr ${expr} \
    --sql_expr ${sql_expr} \
    --mode ${mode}

