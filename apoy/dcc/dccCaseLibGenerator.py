__author__ = 'shako'
import os
import json
import argparse
from argparse import ArgumentDefaultsHelpFormatter

"""
Generate cases.json from caseCategory.csv
"""

class DccCaseLibGenerator(object):

    case_lib_content = {}

    def __init__(self):
        self.read_arguments()

    def read_arguments(self):
        self.arg_parser = argparse.ArgumentParser(description='Dynamic Case Composition Compiler',
                                                  formatter_class=ArgumentDefaultsHelpFormatter)
        self.arg_parser.add_argument('-i', '--input', action='store', dest='input_dir_path', default=None,
                                     help='Specify the directory of input case data files.', required=True)
        self.arg_parser.add_argument('-o', '--output', action='store', dest='output_file_path', default=None,
                                     help='Specify the output file.', required=True)
        self.args = self.arg_parser.parse_args()
        self.input_dir_path = self.args.input_dir_path
        self.output_file_path = self.args.output_file_path

    def generate(self, input_data_fp):
        return_result = []
        with open(input_data_fp) as input_data_fh:
            for input_data_read_line in input_data_fh.readlines():
                tmp_content = {'content': "", 'attribute': []}
                tmp_content['content'] = input_data_read_line
                case_data_list = filter(None, input_data_read_line.strip().lower().split(","))
                for index in range(1, len(case_data_list)):
                    attribute = case_data_list[index].split(":")[0].strip().lower()
                    if attribute not in tmp_content['attribute']:
                        tmp_content['attribute'].append(attribute)
                return_result.append(tmp_content)
        return return_result

    def run_generate(self):
        for input_data_fn in os.listdir(self.input_dir_path):
            input_data_fp = os.path.join(self.input_dir_path, input_data_fn)
            feature_name = input_data_fn.split(".")[0]
            self.case_lib_content[feature_name] = self.generate(input_data_fp)

    def output_to_json(self):
        with open(self.output_file_path, "wb") as write_fh:
            json.dump(self.case_lib_content, write_fh)

    def run(self):
        self.run_generate()
        self.output_to_json()

def main():
    run_obj = DccCaseLibGenerator()
    run_obj.run()

if __name__ == '__main__':
    main()
