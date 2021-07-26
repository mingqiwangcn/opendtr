import json
import os
import tensorflow as tf
from google.protobuf.json_format import MessageToJson
from tapas.protos import interaction_pb2
from tqdm import tqdm
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    parser.add_argument('--output')
    args = parser.parse_args()
    return args

def record2json(input_file, output_file):
    dataset = tf.data.TFRecordDataset(input_file)
    f_o = open(output_file, 'w')
    for record in tqdm(dataset):
        data = interaction_pb2.Interaction()
        data.ParseFromString(record.numpy())
        example_str = MessageToJson(data)
        example = json.loads(example_str)
        f_o.write(json.dumps(example) + '\n')
    f_o.close()

def main():
    args = get_args()
    if os.path.exists(args.output):
        print('%s already exists.' % args.output)
        return
    record2json(args.input, args.output)

if __name__ == '__main__':
    main()
