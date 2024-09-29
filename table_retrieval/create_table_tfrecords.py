import argparse
import tensorflow as tf
from tapas.protos import interaction_pb2
import os
import json
from tqdm import tqdm
import uuid
from google import protobuf 

def read_table(table_file):
    with open(table_file) as f:
        for line in f:
            table_item = json.loads(line)
            nq_table_info = table_item_2_nq_table(table_item)
            yield nq_table_info

def table_item_2_nq_table(table_item):
    nq_table_info = {}
    col_data = table_item['columns']
    nq_table_info['columns'] = [{'text':a['text']} for a in col_data]
    nq_rows_info = []
    row_data = table_item['rows']
    for row_info in row_data:
        item_cells = row_info['cells']
        nq_row_cells = [{'text':a['text']} for a in item_cells]
        nq_rows_info.append({'cells':nq_row_cells})
    nq_table_info['rows'] = nq_rows_info
    nq_table_info['documentTitle'] = table_item['documentTitle']
    nq_table_info['documentUrl'] = ''
    nq_table_info['table_id'] = table_item['tableId']
    return nq_table_info
        
def main():
    args = get_args()
    out_dir = f'./output/{args.dataset}/tables'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_file_name = f'{args.dataset}_tables.tfrecord'
    out_full_file = os.path.join(out_dir, out_file_name)
    if os.path.isfile(out_full_file):
        print(f'{out_full_file} already exists')
        return
    rd_writer = tf.io.TFRecordWriter(out_full_file)
    table_id_set = set()
    table_file = f'/home/cc/data/{args.dataset}/tables/tables.jsonl'
    for table_item in tqdm(read_table(table_file)):
        table_id = table_item['table_id']
        if table_id in table_id_set:
            print('duplicate tables')
            continue
        table_id_set.add(table_id)
        table_data = interaction_pb2.Table()
        protobuf.json_format.ParseDict(table_item, table_data)
        rd_writer.write(table_data.SerializeToString())
    rd_writer.close()
         
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
