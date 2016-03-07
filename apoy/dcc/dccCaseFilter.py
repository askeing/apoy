__author__ = 'shako'
import os
import json

DEFAULT_ATTRIBUTES = ["basic", "security"]
SENSITIVE_LEVEL = 0
class DccCaseLibGenerator(object):

    case_lib_content = {}

    def __init__(self, input_attribute_list, output_csv_fp, input_case_lib_fp="dcc/output/cases.json"):
        self.case_lib_fp = input_case_lib_fp
        self.csv_fp = output_csv_fp
        self.attribute_list = input_attribute_list

    def import_case_lib(self):
        with open(self.case_lib_fp) as read_fh:
            self.case_lib_content = json.load(read_fh)

    def filter(self):
        return_result = []
        for attribute in self.attribute_list:
            if attribute in self.case_lib_content:
                for case_content in self.case_lib_content[attribute]:
                    if attribute in case_content['attribute']:
                        case_content['attribute'].remove(attribute)
                    for default_attribute in DEFAULT_ATTRIBUTES:
                        if default_attribute in case_content['attribute']:
                            case_content['attribute'].remove(default_attribute)
                    if len(case_content['attribute']) <= SENSITIVE_LEVEL:
                        return_result.append(case_content['content'])
        return return_result

    def output_to_csv(self, input_contents):
        dir_name = os.path.dirname(self.csv_fp)
        if os.path.exists(dir_name) is False:
            os.mkdir(dir_name)
        with open(self.csv_fp, "wb") as write_fh:
            write_fh.writelines(input_contents)

    def run(self):
        self.import_case_lib()
        self.output_to_csv(self.filter())

def main():
    run_obj = DccCaseLibGenerator()
    run_obj.run()

if __name__ == '__main__':
    main()
