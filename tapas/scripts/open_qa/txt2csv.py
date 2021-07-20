import json
import csv
import os
from tqdm import tqdm

def read_table():
    table_id_lst = [8, 19, 63, 102, 186, 209, 228, 289, 601, 962]
    data_dir = '/home/cc/data/nq/interactions/dev_qas_tables/tables'
    for table_id in table_id_lst:
        table_name = 'table_%d' % table_id
        data_file = os.path.join(data_dir, table_name, 'table.json')
        with open(data_file) as f:
            table_data = json.load(f)
            yield (table_name, table_data)

def main():
    for table_name, table in tqdm(read_table()):
        out_file = os.path.join('./output', '%s.csv' % table_name)
        with open(out_file, 'w') as f_o:
            columns = table['columns']
            writer = csv.writer(f_o)
            col_names = [col_info['text'] for col_info in columns]
            writer.writerow(col_names)
            row_data = table['rows']
            for row_item in row_data:
                cells = row_item['cells']
                cell_values = [a['text'] for a in cells] 
                writer.writerow(cell_values)

if __name__ == '__main__':
    main()
