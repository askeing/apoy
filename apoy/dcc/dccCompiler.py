__author__ = 'shako'
import os
import json
import argparse
import itertools
from argparse import ArgumentDefaultsHelpFormatter

TEMPLATE_ACTION = "action"
TEMPLATE_EXPECTED = "expected"
TEMPLATE_CONTENT = "content"
TEMPLATE_SEQUENCE = "sequence"
KEYWORD_CASE_VARIABLE = "<case_variable>"
KEYWORD_STEP_VARIABLE = "<step_variable>"


class DccCompiler(object):
    refernce_data = {}
    compiled_data = {}
    reference_dir_path = ""
    input_file_path = ""
    output_file_path = ""

    def __init__(self, input_fp, output_fp, reference_dp="dcc/references"):
        self.output_file_path = output_fp
        self.input_file_path = input_fp
        self.reference_dir_path = reference_dp

    def read_arguments(self):
        self.arg_parser = argparse.ArgumentParser(description='Dynamic Case Composition Compiler',
                                                  formatter_class=ArgumentDefaultsHelpFormatter)
        self.arg_parser.add_argument('-r', '--reference', action='store', dest='reference_dir_path', default=None,
                                     help='Specify the directory of reference files.', required=True)
        self.arg_parser.add_argument('-i', '--input', action='store', dest='input_dir_path', default=None,
                                     help='Specify the directory of input case data files.', required=True)
        self.arg_parser.add_argument('-o', '--output', action='store', dest='output_file_path', default=None,
                                     help='Specify the output file.', required=True)
        self.args = self.arg_parser.parse_args()
        self.reference_dir_path = self.args.reference_dir_path
        self.input_dir_path = self.args.input_dir_path
        self.output_file_path = self.args.output_file_path

    def import_reference_files(self):
        for reference_fn in os.listdir(self.reference_dir_path):
            reference_type = reference_fn.split(".")[0]
            reference_fp = os.path.join(self.reference_dir_path, reference_fn)
            with open(reference_fp) as reference_fh:
                self.refernce_data[reference_type] = json.load(reference_fh)

    def compile(self, input_data_fp):
        result_list = []
        with open(input_data_fp) as input_data_fh:
            for input_data_read_line in input_data_fh.readlines():
                case_step_list = []
                case_data_list = filter(None, input_data_read_line.strip().lower().split(","))
                seq_template_index = int(case_data_list[0])
                step_seq_list = self.refernce_data[TEMPLATE_SEQUENCE][seq_template_index]
                for step_seq_index in range(len(step_seq_list)):
                    step_key_name = step_seq_list[step_seq_index]
                    step_list = []
                    case_variable_index = step_seq_index + 1
                    case_variables_list = filter(None, case_data_list[case_variable_index].strip().lower().split("|"))
                    for case_variable in case_variables_list:
                        tmp_list = case_variable.strip().lower().split(":")
                        case_type = tmp_list[0]
                        case_variable_value_list = tmp_list[1].strip().lower().split("+")
                        case_content = self.refernce_data[TEMPLATE_CONTENT][step_key_name][case_type]['content']
                        expected_content = self.refernce_data[TEMPLATE_CONTENT][step_key_name][case_type]['expected']
                        step_variables = self.refernce_data[TEMPLATE_CONTENT][step_key_name][case_type]['value']
                        for case_variable_value in case_variable_value_list:
                            if KEYWORD_CASE_VARIABLE in case_content:
                                case_content = case_content.replace(KEYWORD_CASE_VARIABLE, case_variable_value, 1)
                            else:
                                expected_content = expected_content.replace(KEYWORD_CASE_VARIABLE, case_variable_value, 1)
                        case_replaced_content = case_content
                        for step_variable in step_variables:
                            if KEYWORD_STEP_VARIABLE in case_content:
                                case_replaced_content = case_content.replace(KEYWORD_STEP_VARIABLE, step_variable, 1)
                            step_list.append({'step': case_replaced_content, 'expected': expected_content})
                    case_step_list.append(step_list)
                result_list.extend([t for t in itertools.product(*case_step_list)])
        return result_list

    def run_compile(self):
        feature_name = self.input_file_path.split(".")[0]
        self.compiled_data[feature_name] = self.compile(self.input_file_path)

    def output_compiled_data(self):
        dir_name = os.path.dirname(self.output_file_path)
        if os.path.exists(dir_name) is False:
            os.mkdir(dir_name)
        with open(self.output_file_path, "wb") as write_fh:
            json.dump(self.compiled_data, write_fh)

    def run(self):
        self.import_reference_files()
        self.run_compile()
        self.output_compiled_data()

def main():
    run_obj = DccCompiler()
    run_obj.run()

if __name__ == '__main__':
    main()
