if [ "$#" -ne 2 ]; then
  echo "Usage: ./eval_checkpoints.sh <dataset> <sql_expr>"
  exit
fi

dataset=$1
sql_expr=$2
model_dir=models/${dataset}_syt_${sql_expr}
data_dir=~/code/data/${dataset}
retrieval_model_name=tapas_dual_encoder_proj_256_medium
max_seq_length=512

python3 tapas/experiments/table_retriever_experiment.py \
   --do_predict \
   --model_dir="${model_dir}" \
   --input_file_eval="${data_dir}/syt_${sql_expr}_tf_examples/syt_dev.tfrecord" \
   --bert_config_file="${retrieval_model_name}/bert_config.json" \
   --init_from_single_encoder=false \
   --down_projection_dim=256 \
   --eval_batch_size=32 \
   --num_train_examples=51200000 \
   --max_seq_length="${max_seq_length}"

