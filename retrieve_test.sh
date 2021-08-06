step=0
model_dir=./models/tapas_nq_hn_retriever_large
python tapas/scripts/eval_table_retriever.py \
 --prediction_files_local=${model_dir}/test/predict_results_${step}.tsv \
 --prediction_files_global=${model_dir}/tables/predict_results_${step}.tsv \
 --retrieval_results_file_path="${model_dir}/test_knn.jsonl"

