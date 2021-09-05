import tensorflow as tf
from tapas.protos import interaction_pb2
import os
import json
from tqdm import tqdm
import uuid
from google import protobuf 

def create_data(mode, out_dir, table_lst):
    out_file_name = '%s_fetaqa.tfrecord' % mode
    out_full_file = os.path.join(out_dir, out_file_name)
    rd_writer = tf.io.TFRecordWriter(out_full_file)
    
    for nq_item in tqdm(create_nq_json(mode)):
        itr_data = interaction_pb2.Interaction()
        protobuf.json_format.ParseDict(nq_item, itr_data)
        rd_writer.write(itr_data.SerializeToString())

        table_lst.append(nq_item['table'])

    rd_writer.close()

def create_nq_json(mode):
    table_source_dict = {}
    table_id_dict = {}

    for feta_item in read_fetaQA_json(mode):
        nq_item = {}
        nq_item['id'] = str(feta_item['feta_id'])
        nq_table_info = {}
        nq_item['table'] = nq_table_info
        feta_table_array = feta_item['table_array']
        col_names = feta_table_array[0]
        nq_table_info['columns'] = [{'text':a} for a in col_names]
        nq_rows_info = []
        feta_rows = feta_table_array[1:]
        nq_rows_info = []
        for row_info in feta_rows:
            nq_row_cells = [{'text':a} for a in row_info]
            nq_rows_info.append({'cells':nq_row_cells})

        nq_table_info['rows'] = nq_rows_info
        nq_table_info['documentTitle'] = feta_item['table_page_title'] + ' , ' + feta_item['table_section_title']
        nq_table_info['documentUrl'] = feta_item['page_wikipedia_url']

        document_title = nq_table_info['documentTitle']
        table_source = feta_item['table_source_json']
        if table_source not in table_source_dict:
            table_id = document_title + ' - ' + str(uuid.uuid4()) 
            table_source_dict[table_source] = {'table_id': table_id}
        else:
            print('same table source')
            table_id = table_source_dict[table_source]['table_id']
         
        nq_table_info['table_id'] = table_id
        
        nq_q_info = {}
        nq_q_info['id'] = nq_item['id'] + '_0'
        nq_q_info['originalText'] = feta_item['question']
        nq_q_info['answer'] = {'answerTexts':[feta_item['answer']]}
        nq_item['questions'] = [nq_q_info]
        
        yield nq_item 

 
def read_fetaQA_json(mode):
    data_file = '/home/cc/data/FeTaQA/data/fetaQA-v1_%s.jsonl' % mode
    with open(data_file) as f:
        for line in f:
            item = json.loads(line)
            yield item   
     

def main():
    out_dir = './output/interactions'
    table_lst = []
    create_data('train', out_dir, table_lst)
    create_data('dev', out_dir, table_lst)
    create_data('test', out_dir, table_lst)

    out_file_name = 'fetaqa_tables.tfrecord'
    out_table_dir = './output/tables'
    out_full_file = os.path.join(out_table_dir, out_file_name)
    rd_writer = tf.io.TFRecordWriter(out_full_file)

    table_id_set = set()
    for table_item in tqdm(table_lst):
        table_id = table_item['table_id']
        if table_id in table_id_set:
            print('duplicate tables')
            continue
        table_id_set.add(table_id)
        table_data = interaction_pb2.Table()
        protobuf.json_format.ParseDict(table_item, table_data)
        rd_writer.write(table_data.SerializeToString())

    rd_writer.close() 
         
    

if __name__ == '__main__':
    main()
