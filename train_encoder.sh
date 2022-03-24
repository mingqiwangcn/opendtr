if [ "$#" -ne 1 ]; then
  echo "Usage: ./train_encoder.sh <dataset>"
  exit
fi

dataset=$1
data_dir=~/data/${dataset}
retrieval_model_name=tapas_dual_encoder_proj_256_medium
max_seq_length=512
model_dir=./models/fetaqa
python tapas/experiments/table_retriever_experiment.py \
   --do_train \
   --keep_checkpoint_max=40 \
   --model_dir="${model_dir}" \
   --input_file_train="${data_dir}/tf_examples/train.tfrecord" \
   --bert_config_file="${retrieval_model_name}/bert_config.json" \
   --init_checkpoint="${retrieval_model_name}/model.ckpt" \
   --init_from_single_encoder=false \
   --down_projection_dim=256 \
   --num_train_examples=5120000 \
   --learning_rate=1.25e-5 \
   --train_batch_size=32 \
   --warmup_ratio=0.01 \
   --max_seq_length="${max_seq_length}"
