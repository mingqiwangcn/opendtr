if [ "$#" -ne 4 ]; then
  echo "Usage: ./retrieve_dev.sh <dataset> <sql_expr> <checkpoint step> <mode>"
  exit
fi

dataset=$1
sql_expr=$2
step=$3
mode=$4
model_dir=./models/${dataset}_syt_${sql_expr}
python tapas/scripts/eval_table_retriever.py \
 --prediction_files_local="${model_dir}/${mode}_${step}/predict_results_${step}.tsv" \
 --prediction_files_global="${model_dir}/tables_${step}/predict_results_${step}.tsv" \
 --retrieval_results_file_path="${model_dir}/${mode}_${step}/${mode}_knn.jsonl"

