import os
import pprint
import json
from threading import Thread
from rule_analysis.rule_analysis import run_analysis
from dcc.dccCaseFilter import DccCaseLibGenerator
from dcc.dccCompiler import DccCompiler


class TaskWorker(Thread):
    def __init__(self, project_repo_summary, taskid):
        Thread.__init__(self)
        self.taskid = taskid
        self.project_repo_summary = project_repo_summary

    def run(self):
        case_json_dir = os.path.join(os.getcwd(), "results")
        print('TaskID: {}'.format(self.taskid))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.project_repo_summary)
        attribute_list = run_analysis(self.project_repo_summary)

        attr_json_fp = os.path.join(case_json_dir,
                                    str(self.taskid) + "_summary.json")
        dump_target = self.project_repo_summary.copy()
        dump_target["enabled_attributes"] = attribute_list.copy()
        self.dump_to_file(
            dump_target, attr_json_fp)

        case_csv_fp = os.path.join(os.getcwd(),
                                   "dcc",
                                   "tmp",
                                   str(self.taskid) + ".csv")
        obj_case_filter = DccCaseLibGenerator(attribute_list, case_csv_fp)
        obj_case_filter.run()
        case_json_fp = os.path.join(case_json_dir, str(self.taskid) + ".json")
        obj_dcc_compiler = DccCompiler(case_csv_fp, case_json_fp)
        obj_dcc_compiler.run()

    @staticmethod
    def dump_to_file(data, output_path):
        dirname = os.path.dirname(output_path)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        with open(output_path, 'wb') as write_fh:
            json.dump(data, write_fh)
