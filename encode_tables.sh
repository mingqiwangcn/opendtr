if [ "$#" -ne 3 ]; then
  echo "Usage: ./encode_tables.sh <dataset> <model dir> <checkpoint_step>"
  exit
fi

dataset=$1
model_dir=$2
step=$3
data_dir=~/data/${dataset}
max_seq_length=512
retrieval_model_name=tapas_dual_encoder_proj_256_medium
for mode in dev test tables; do
  echo "encoding ${mode}"
  python3 tapas/experiments/table_retriever_experiment.py \
     --do_predict \
     --model_dir="${model_dir}" \
     --prediction_output_dir="${model_dir}/${dataset}_${mode}_${step}" \
     --input_file_predict="${data_dir}/tf_examples/${mode}.tfrecord" \
     --bert_config_file="${retrieval_model_name}/bert_config.json" \
     --init_from_single_encoder=false \
     --down_projection_dim=256 \
     --eval_batch_size=32 \
     --max_seq_length="${max_seq_length}" \
     --evaluated_checkpoint_step ${step} \
     #--evaluated_checkpoint_metric=precision_at_1 \
done

