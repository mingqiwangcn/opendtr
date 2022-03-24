if [ "$#" -ne 2 ]; then
  echo "Usage: ./retrieve_dev.sh <dataset> <checkpoint step> <mode>"
  exit
fi

dataset=$1
step=$2
mode=$3
model_dir=./models/${dataset}
python tapas/scripts/eval_table_retriever.py \
 --prediction_files_local="${model_dir}/${mode}_${step}/predict_results_${step}.tsv" \
 --prediction_files_global="${model_dir}/tables/predict_results_${step}.tsv" \
 --retrieval_results_file_path="${model_dir}/${mode}_${step}/${mode}_knn.jsonl"

