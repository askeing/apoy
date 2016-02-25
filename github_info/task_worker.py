import pprint
from threading import Thread


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
