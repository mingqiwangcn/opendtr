import tensorflow as tf
from tapas.protos import interaction_pb2
import os
import json
from tqdm import tqdm
import argparse
import uuid
from google import protobuf
import random

def read_tables(table_file):
    table_dict = {}
    with open(table_file) as f:
        for line in tqdm(f):
            item = json.loads(line)
            table_id = item['tableId']
            table_dict[table_id] = item
    return table_dict

def load_annotated_query(table_file):
    q_dict = {}
    with open(table_file) as f:
        for line in f:
            query = json.loads(line)
            q_dict[query['id']] = query
    return q_dict

def get_out_dir(args):
    if args.syt:
        out_dir = f'/home/cc/data/{args.dataset}/syt_{args.sql_expr}_interactions'
    else:
        out_dir = f'/home/cc/data/{args.dataset}/interactions'
    return out_dir

def get_out_filename(args):
    if args.syt:
        return f'syt_{args.mode}.tfrecord'
    else:
        return f'{args.mode}.tfrecord'

def get_input_file(args):
    if args.syt:
        input_dir = '/home/cc/code/project/open_table_discovery/table2question/dataset/'
        input_file = os.path.join(input_dir, args.dataset, args.sql_expr, 
                                 f'syt_{args.expr}', 
                                 f'fusion_retrieved_{args.mode}_tagged.jsonl') 
    else:
        input_dir = '/home/cc/data'
        input_file = os.path.join(input_dir, args.dataset, 'query', args.mode, 
                                args.expr, f'fusion_retrieved_tagged.jsonl')
    return input_file

def main():
    args = get_args()
    output_dir = get_out_dir(args)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    out_filename = get_out_filename(args)
    output_file = os.path.join(output_dir, out_filename)
    if os.path.isfile(output_file):
        print('output file (%s) already exists.' % output_file)
        return
    
    annotated_query_file = os.path.join('/home/cc/data', args.dataset, 
                                        f'query/{args.dataset}_questions_annotated.jsonl')
    q_dict = load_annotated_query(annotated_query_file)
    table_file = os.path.join('/home/cc/data', args.dataset, 'tables/tables.jsonl')
    table_dict = read_tables(table_file)
    input_file = get_input_file(args)
    rd_writer = tf.io.TFRecordWriter(output_file)
    is_train = (args.mode == 'train')
    for nq_item in tqdm(create_nq_json(is_train, input_file, table_dict, q_dict)):
        itr_data = interaction_pb2.Interaction()
        protobuf.json_format.ParseDict(nq_item, itr_data)
        rd_writer.write(itr_data.SerializeToString())
    rd_writer.close()

def sample_answer_tables(query_item, q_dict):
    answer_tables = query_item['table_id_lst']
    src_table = q_dict[query_item['id']]['meta']['table_id']
    assert src_table in answer_tables
    other_tables = [a for a in answer_tables if a != src_table]
    other_sample_tables = []
    if len(other_tables) > 0:
        M = min(2, len(other_tables))
        other_sample_tables = random.sample(other_tables, M)
    
    ret_tables = [src_table] + other_sample_tables
    return ret_tables

def create_nq_json(is_train, input_file, table_dict, q_dict):
    with open(input_file) as f:
        for line in f:
            query_item = json.loads(line)
            nq_item = {}
            nq_item['id'] = str(query_item['id'])
            answer_table_lst = None
            if is_train:
                answer_table_lst = sample_answer_tables(query_item,  q_dict)
            else:
                answer_table_lst = query_item['table_id_lst']
            for gold_table_id in answer_table_lst:
                nq_item['table'] = table_dict[gold_table_id] 
                nq_q_info = {}
                nq_q_info['id'] = nq_item['id'] + '_0' # use same item and question id if multiple tables are correct.
                nq_q_info['originalText'] = query_item['question']
                nq_q_info['answer'] = {'answerTexts':query_item['answers']}
                nq_item['questions'] = [nq_q_info]
                yield nq_item 
 
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, required=True)
    parser.add_argument('--syt', type=int, required=True)
    parser.add_argument('--expr', type=str, required=True)
    parser.add_argument('--sql_expr', type=str, required=True)
    parser.add_argument('--mode', type=str, required=True)
    args = parser.parse_args()
    return args
     
if __name__ == '__main__':
    main()
