import json
from tqdm import tqdm
import random

def read_table():
    data_file = '/home/cc/data/nq/tables/tables.json'
    with open(data_file) as f:
        for line in f:
            table = json.loads(line)
            yield table

def main():
    out_file = './output/graph.source'
    out_file_target = './output/graph.target'
    f_o = open(out_file, 'w')
    f_o_tar = open(out_file_target, 'w')
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
                f_o.write(graph + '\n')
                f_o_tar.write('a\n') 
    f_o.close()
    f_o_tar.close() 

def gen_graph(row_info):
    graph_lst = []
    N = len(row_info)
    e_s = row_info[0]['value']
    graph = ''
    for idx in range(1, N):
        rel = row_info[idx]['name']
        e_o = row_info[idx]['value']
        graph += '<H> %s <R> %s <T> %s ' % (e_s, rel, e_o)
    graph_lst.append(graph)
    return graph_lst

if __name__ == '__main__':
    main()


