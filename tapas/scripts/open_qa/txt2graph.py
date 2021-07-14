import json
from tqdm import tqdm
import random

MAX_GRAPH_SIZE = 100

def read_table():
    data_file = '/home/cc/data/nq/tables/tables.json'
    with open(data_file) as f:
        for line in f:
            table = json.loads(line)
            yield table

def main():
    out_file = './output/test_unseen.source'
    out_file_target = './output/test_unseen.target'
    f_o = open(out_file, 'w')
    f_o_tar = open(out_file_target, 'w')

    max_char_len = 0
    max_row = 0
    count = 0
    
    for table in tqdm(read_table()):
        columns = table['columns']
        col_name_lst = [col_info['text'] for col_info in columns]
        row_data = table['rows']
        for row_item in row_data:
            cell_lst = row_item['cells']
            row_info = []
            for col_idx, cell in enumerate(cell_lst):
                col_name = col_name_lst[col_idx] 
                cell_text = cell['text']
                cell_info = {
                    'name':col_name,
                    'value':cell_text
                }
                row_info.append(cell_info)
            graph_lst = gen_graph(row_info)
            for graph in graph_lst:
                count += 1
                if len(graph) > max_char_len:
                    max_char_len = len(graph)
                    max_row = count
                     
                f_o.write(graph + '\n')
                f_o_tar.write('a\n')
    f_o.close()
    f_o_tar.close()
    
    print('max_char_len=%d, max_row=%d' % (max_char_len, max_row)) 

def gen_graph(row_info):
    N = len(row_info)
    tuple_dict = {}
    tuple_info_lst = []
    for idx_1 in range(0, N):
        e_s = row_info[idx_1]['value'].strip()
        if e_s == '':
            continue
        for idx_2 in range(idx_1+1, N):
            rel = row_info[idx_2]['name'].strip()
            if rel == '':
                continue
            e_o = row_info[idx_2]['value'].strip()
            if e_o == '':
                continue
            tuple_text = '<H> %s <R> %s <T> %s ' % (e_s, rel, e_o)
            tuple_code = tuple_text.lower()
            if tuple_code not in tuple_dict:
                tuple_dict[tuple_code] = 1
                
                token_lst = tuple_text.split()
                tuple_info = {
                    'text':tuple_text,
                    'token_len':len(token_lst)
                }
                tuple_info_lst.append(tuple_info)

    graph_lst = tuple2graph(tuple_info_lst) 
    return graph_lst

def tuple2graph(tuple_info_lst):
    graph_lst = []
    buffer_tuples = []
    buffer_token_len = 0
    for tuple_info in tuple_info_lst:
        token_lst = tuple_info.split()
        if buffer_token_len + len(token_lst) > Max_Token_Len:
            
        else:
            buffer_tuples.append(tuple_info)

    return graph_lst

if __name__ == '__main__':
    main()


