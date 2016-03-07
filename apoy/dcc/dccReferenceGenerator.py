__author__ = 'shako'
import os
import json
import argparse
from argparse import ArgumentDefaultsHelpFormatter

TEMPLATE_ACTION = "action"
TEMPLATE_EXPECTED = "expected"
TEMPLATE_CONTENT = "content"
TEMPLATE_SEQUENCE = "sequence"

class DccReferenceGenerator(object):
    refernce_data = {}
    compiled_data = {}

    def __init__(self):
        self.read_arguments()

    def load_csv_to_list(self, input_file_path):
        result_list = []
        with open(input_file_path) as f:
            for line in f.readlines():
                result_list.append(line.strip())
        return result_list

    def read_arguments(self):
        self.arg_parser = argparse.ArgumentParser(description='Dynamic Case Composition Reference Files Generator',
                                                  formatter_class=ArgumentDefaultsHelpFormatter)
        self.arg_parser.add_argument('-a', '--action', action='store_true', dest='action_gen_bol', default=False,
                                     help='Generate Action Reference File.', required=False)
        self.arg_parser.add_argument('-c', '--content', action='store_true', dest='content_gen_bol', default=False,
                                     help='Generate Content Reference File.', required=False)
        self.arg_parser.add_argument('-e', '--expected', action='store_true', dest='expected_gen_bol', default=False,
                                     help='Generate Expected Reference File', required=False)
        self.arg_parser.add_argument('-s', '--sequence', action='store_true', dest='sequence_gen_bol', default=False,
                                     help='Generate Sequence Reference File', required=False)
        self.arg_parser.add_argument('-i', '--input', action='store', dest='input_dir_path', default=None,
                                     help='Specify the directory of input files', required=True)
        self.arg_parser.add_argument('-o', '--output', action='store', dest='output_dir_path', default=None,
                                     help='Specify the directory of input files', required=True)

        self.args = self.arg_parser.parse_args()
        self.action_gen_bol = self.args.action_gen_bol
        self.content_gen_bol = self.args.content_gen_bol
        self.expected_gen_bol = self.args.expected_gen_bol
        self.sequence_gen_bol = self.args.sequence_gen_bol
        self.input_dir_path = self.args.input_dir_path
        self.output_dir_path = self.args.output_dir_path

    def dump_to_json(self, input_type, input_data):
        output_fn = input_type + ".json"
        output_fp = os.path.join(self.output_dir_path, output_fn)
        with open(output_fp, "wb") as fh:
            json.dump(input_data, fh)

    def generate_content(self, input_fp):
        result_dict = {}
        with open(input_fp) as f:
            for line in f.readlines():
                value_array = line.split(",")
                key_name = value_array[0].strip().lower()
                type = value_array[1].strip().lower()
                action = value_array[2].strip().lower()
                step_variable_list = value_array[3].strip().lower().split("|")
                expected = value_array[4].strip().lower()
                weight = float(value_array[5].strip().lower())
                if key_name not in result_dict:
                    result_dict[key_name] = {}
                for sub_type in type.strip().lower().split("|"):
                    sub_type = sub_type.strip()
                    if len(sub_type) > 0:
                        result_dict[key_name][sub_type] = {"content": action,
                                                           "value": step_variable_list,
                                                           "expected": expected,
                                                           "weight": weight}
        return result_dict

    def generate_reference_file(self, input_fp):
        input_type = os.path.basename(input_fp).split(".")[0].strip().lower()
        if input_type in [TEMPLATE_ACTION, TEMPLATE_EXPECTED, TEMPLATE_SEQUENCE]:
            self.dump_to_json(input_type, filter(None, self.load_csv_to_list(input_fp)))
        if input_type == TEMPLATE_CONTENT:
            self.dump_to_json(input_type, self.generate_content(input_fp))

    def run(self):
        if self.action_gen_bol is False and self.content_gen_bol is False and self.sequence_gen_bol is False and self.expected_gen_bol is False:
            for input_fn in os.listdir(self.input_dir_path):
                input_fp = os.path.join(self.input_dir_path, input_fn)
                self.generate_reference_file(input_fp)


def main():
    run_obj = DccReferenceGenerator()
    run_obj.run()

if __name__ == '__main__':
    main()
