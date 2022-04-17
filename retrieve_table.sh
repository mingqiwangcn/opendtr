if [ "$#" -ne 4 ]; then
  echo "Usage: ./retrieve_dev.sh <dataset> <model dir> <step> <mode>"
  exit
fi

dataset=$1
model_dir=$2
step=$3
mode=$4
python tapas/scripts/eval_table_retriever.py \
 --prediction_files_local="${model_dir}/${dataset}_${mode}_${step}/predict_results_${step}.tsv" \
 --prediction_files_global="${model_dir}/${dataset}_tables_${step}/predict_results_${step}.tsv" \
 --retrieval_results_file_path="${model_dir}/${dataset}_${mode}_${step}/${mode}_knn.jsonl"

