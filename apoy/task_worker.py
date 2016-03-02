import pprint
from threading import Thread
from rule_analysis.rule_analysis import run_analysis


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
        pp.pprint(run_analysis(self.project_repo_summary))
