import json
from txt2graph import process_table 
import os
from tqdm import tqdm

def main():
    output_dir = '/home/cc/data/nq/interactions/dev_qas_tables/tables'
    question_data_file = os.path.join('/home/cc/data/nq/interactions/dev_qas_tables', 'dev_qas.json')
    q_info_lst = []
    with open('/home/cc/data/nq/interactions/dev.json') as f:
        row = 0
        for line in tqdm(f):
            row += 1
            item = json.loads(line)
            item_id = item['id']
            table_code = ('table_%d' % row)
            table_dir = os.path.join(output_dir, table_code)
            os.mkdir(table_dir)    
            table_data = item['table']
            graph_lst = process_table(table_data)

            out_table_file = os.path.join(table_dir, 'table.json')
            with open(out_table_file, 'w') as f_o:
                f_o.write(json.dumps(table_data))
            
            out_file_src = os.path.join(table_dir, 'test_unseen.source')
            out_file_tar = os.path.join(table_dir, 'test_unseen.target')

            f_o_src = open(out_file_src, 'w')
            f_o_tar = open(out_file_tar, 'w')
            for graph in graph_lst:
                f_o_src.write(graph + '\n')
                f_o_tar.write('a\n')
            
            f_o_src.close()
            f_o_tar.close()
             
            out_q_file = os.path.join(table_dir, 'questions.json')
            f_o_q = open(out_q_file, 'w')
            q_data = item['questions']
            f_o_q.write(json.dumps(q_data))
            f_o_q.close()
            
            for q_item in q_data:
                q_text = q_item['originalText']
                q_info = {
                    'text':q_text,
                    'table':table_code
                }
                q_info_lst.append(q_info)
                
        
    with open(question_data_file, 'w') as f_o_q_all:
        f_o_q_all.write(json.dumps(q_info_lst))

if __name__ == '__main__':
    main()
