import json
import csv
from tqdm import tqdm

def read_table():
    data_file = '/home/cc/data/nq/tables/tables.json'
    with open(data_file) as f:
        for line in f:
            table = json.loads(line)
            yield table

def main():
    idx = 0
    for table in tqdm(read_table()):
        idx += 1
        out_file = '/home/cc/data/nq/tables/output/table_%d.csv' % idx
        with open(out_file, 'w', newline='') as f_o:
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
