import os
import pprint
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
        # TODO: not implemented
        print('TaskID: {}'.format(self.taskid))
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.project_repo_summary)
        attribute_list = run_analysis(self.project_repo_summary)
        pp.pprint(attribute_list)

        case_csv_fp = os.path.join(os.getcwd(), "apoy", "dcc", "tmp", str(self.taskid) + ".csv")
        obj_case_filter = DccCaseLibGenerator(attribute_list, case_csv_fp)
        obj_case_filter.run()
        case_json_fp = os.path.join(os.getcwd(), "apoy", "results", str(self.taskid) + ".json")
        obj_dcc_compiler = DccCompiler(case_csv_fp, case_json_fp)
        obj_dcc_compiler.run()


