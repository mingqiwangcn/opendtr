import json
import tensorflow as tf
from google.protobuf.json_format import MessageToJson
from tapas.protos import interaction_pb2
from tqdm import tqdm

def read_tables():
    dataset = tf.data.TFRecordDataset("/home/cc/data/nq/tables/tables.tfrecord")
    f_o = open('/home/cc/data/nq/tables/output/tables.json', 'w')
    for record in tqdm(dataset):
        table = interaction_pb2.Table()
        table.ParseFromString(record.numpy())
        example_str = MessageToJson(table)
        example = json.loads(example_str)
        f_o.write(json.dumps(example) + '\n')
    f_o.close()

def main():
    read_tables()

if __name__ == '__main__':
    main()
