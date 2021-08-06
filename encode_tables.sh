nq_data_dir=~/data/nq
max_seq_length=512
model_dir="./models/tapas_nq_hn_retriever_large"
for mode in dev tables test; do
  python3 tapas/experiments/table_retriever_experiment.py \
     --do_predict \
     --model_dir="${model_dir}" \
     --prediction_output_dir="${model_dir}/${mode}" \
     --input_file_predict="${nq_data_dir}/tf_examples/${mode}.tfrecord" \
     --bert_config_file="./models/tapas_nq_hn_retriever_large/bert_config.json" \
     --init_from_single_encoder=false \
     --down_projection_dim=256 \
     --eval_batch_size=32 \
     --max_seq_length="${max_seq_length}" \
     --evaluated_checkpoint_step 00000
     #--evaluated_checkpoint_metric=precision_at_1 \
done

