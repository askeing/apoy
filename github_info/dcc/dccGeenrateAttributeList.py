__author__ = 'shako'
import os
import json
import argparse
from argparse import ArgumentDefaultsHelpFormatter

TEMPLATE_CONTENT = "content"
TEMPLATE_ATTRIBUTE = "attribute"
FILTER_LIST = ["basic", "security"]

class DccAttributeGenerator(object):

    def __init__(self):
        self.read_arguments()

    def read_arguments(self):
        self.arg_parser = argparse.ArgumentParser(description='Dynamic Case Composition Attribute File Generator',
                                                  formatter_class=ArgumentDefaultsHelpFormatter)
        self.arg_parser.add_argument('-i', '--input', action='store', dest='input_dir_path', default=None,
                                     help='Specify the directory of input files', required=True)
        self.arg_parser.add_argument('-o', '--output', action='store', dest='output_dir_path', default=None,
                                     help='Specify the directory of input files', required=True)

        self.args = self.arg_parser.parse_args()
        self.input_dir_path = self.args.input_dir_path
        self.output_dir_path = self.args.output_dir_path

    def dump_to_json(self, output_fp, input_data):
        with open(output_fp, "wb") as fh:
            json.dump(input_data, fh)

    def generate_list(self, input_fp):
        result_dict = {}
        with open(input_fp) as fh:
            input_data = json.load(fh)
            for data_key in input_data:
                for attribute in input_data[data_key]:
                    if attribute not in result_dict and attribute not in FILTER_LIST:
                        result_dict[attribute] = False
        return result_dict

    def run(self):
        input_fp = os.path.join(self.input_dir_path, TEMPLATE_CONTENT + ".json")
        result_list = self.generate_list(input_fp)
        output_fp = os.path.join(self.output_dir_path, TEMPLATE_ATTRIBUTE + ".json")
        self.dump_to_json(output_fp, result_list)



def main():
    run_obj = DccAttributeGenerator()
    run_obj.run()

if __name__ == '__main__':
    main()
