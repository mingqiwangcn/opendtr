if [ "$#" -ne 1 ]; then
  echo "Usage: ./create_retrieval_data.sh <dataset>"
  exit
fi
dataset=$1
data_dir=~/data/${dataset}
max_seq_length=512
retrieval_model_name="tapas_dual_encoder_proj_256_medium"
python tapas/retrieval/create_retrieval_data_main.py \
  --input_interactions_dir="${data_dir}/interactions" \
  --input_tables_dir=${data_dir}/tables \
  --output_dir="${data_dir}/tf_examples" \
  --vocab_file="${retrieval_model_name}/vocab.txt" \
  --max_seq_length="${max_seq_length}" \
  --max_column_id="${max_seq_length}" \
  --max_row_id="${max_seq_length}" \
  --use_document_title
