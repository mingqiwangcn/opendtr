nq_data_dir=~/data/nq
max_seq_length=512
retrieval_model_name="./models/tapas_nq_hn_retriever_large"
python3 tapas/retrieval/create_retrieval_data_main.py \
  --input_interactions_dir="${nq_data_dir}/interactions" \
  --input_tables_dir=${nq_data_dir}/tables \
  --output_dir="${nq_data_dir}/tf_examples" \
  --vocab_file="${retrieval_model_name}/vocab.txt" \
  --max_seq_length="${max_seq_length}" \
  --max_column_id="${max_seq_length}" \
  --max_row_id="${max_seq_length}" \
  --use_document_title
