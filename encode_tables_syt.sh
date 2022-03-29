if [ "$#" -ne 2 ]; then
  echo "Usage: ./encode_tables_syt.sh <dataset> <checkpoint_step>"
  exit
fi

dataset=$1
step=$2
data_dir=~/data/${dataset}
max_seq_length=512
model_dir=models/${dataset}_syt
retrieval_model_name=tapas_dual_encoder_proj_256_medium
for mode in test tables; do
  echo "encoding ${mode}"
  python3 tapas/experiments/table_retriever_experiment.py \
     --do_predict \
     --model_dir="${model_dir}" \
     --prediction_output_dir="${model_dir}/${mode}_${step}" \
     --input_file_predict="${data_dir}/syt_tf_examples/${mode}.tfrecord" \
     --bert_config_file="${retrieval_model_name}/bert_config.json" \
     --init_from_single_encoder=false \
     --down_projection_dim=256 \
     --eval_batch_size=32 \
     --max_seq_length="${max_seq_length}" \
     --evaluated_checkpoint_step ${step} \
     #--evaluated_checkpoint_metric=precision_at_1 \
done

