import tensorflow as tf
from tapas.protos import interaction_pb2
import os
import json
from tqdm import tqdm
import argparse
import uuid
from google import protobuf 

def read_tables(table_file):
    table_dict = {}
    with open(table_file) as f:
        for line in tqdm(f):
            item = json.loads(line)
            table_id = item['tableId']
            table_dict[table_id] = item
    return table_dict 

def main():
    args = get_args()
    output_dir = '/home/cc/data/%s/syt_%s_interactions' % (args.dataset, args.sql_expr)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, 'syt_%s.tfrecord' % args.mode)
    if os.path.exists(output_file):
        print('output file (%s) already exists.' % output_file)
        return
    
    table_file = os.path.join('/home/cc/data', args.dataset, 'tables/tables.jsonl')
    table_dict = read_tables(table_file)

    fusion_dir = '/home/cc/code/open_table_discovery/table2question/dataset/'
    fusion_file = os.path.join(fusion_dir, args.dataset, args.sql_expr, 
                               args.expr, 'fusion_retrieved_%s.jsonl' % args.mode) 
    
    rd_writer = tf.io.TFRecordWriter(output_file)
    for nq_item in tqdm(create_nq_json(fusion_file, table_dict)):
        itr_data = interaction_pb2.Interaction()
        protobuf.json_format.ParseDict(nq_item, itr_data)
        rd_writer.write(itr_data.SerializeToString())

    rd_writer.close()

def create_nq_json(fusion_file, table_dict):
    with open(fusion_file) as f:
        for line in f:
            fusion_item = json.loads(line)
            nq_item = {}
            nq_item['id'] = str(fusion_item['id'])
            gold_table_id_lst = fusion_item['table_id_lst']
            assert(len(gold_table_id_lst) == 1)
            gold_table_id = gold_table_id_lst[0]
            nq_item['table'] = table_dict[gold_table_id] 
            
            nq_q_info = {}
            nq_q_info['id'] = nq_item['id'] + '_0'
            nq_q_info['originalText'] = fusion_item['question']
            nq_q_info['answer'] = {'answerTexts':fusion_item['answers']}
            nq_item['questions'] = [nq_q_info]
        
            yield nq_item 
 

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--expr', type=str, required=True)
    parser.add_argument('--sql_expr', type=str, required=True)
    parser.add_argument('--mode', type=str, required=True)
    args = parser.parse_args()
    return args
     
if __name__ == '__main__':
    main()
