#Imports
import json

class Timeline(object):
    """docstring for Timeline."""

    # filepath = os.path.realpath(__file__)
    filepath = 'C:/xampp/htdocs/WebProjects/CrossedPaths/src/dataimport/'

    timelinedata = None # gets filled within init function

    def __init__(self, filename):
        super(Timeline, self).__init__()
        self.filename = filename

        #load the file in
        #todo: catch doen op json.load en error message laten zien voor data integriteit
        #todo: check for timezone mismatches, catch and maybe do some changes to align the timezones
        with open(self.filepath + self.filename + '.json', 'r') as f:
            self.timelinedata = json.load(f)

    def loop(self, count):
        loopCount = count + 1
        for idx, item in enumerate(self.timelinedata):
            if (idx+1) % loopCount == 0:
              break
            print(item['timestamp'])
            print(item['lat'])
            print(item['lon'])
            print(' ')
