""" ###  Do dome checks
    1. moet from EN date gevuld hebben anders mag niet error ga maar dood klootzak
    2. data is georderd op timestamp DESC
    -> percentage together/not together in bar-statistic within (n) distance
"""
from classes.Timeline import Timeline
from classes.TimelineAnal import TimelineAnal

class CrossedPaths(object):
    """docstring for CrossedPaths."""

    timelineAnal        = None
    firstTimeline       = None
    firstTimelineName   = None
    secondTimeline      = None
    secondTimelineName  = None
    fromDate            = None
    toDate              = None
    firstTimeline       = None

    def __init__(self, firstTimelineName, secondTimelineName, fromDate = 0, toDate = 0):
        super(CrossedPaths, self).__init__()

        self.firstTimelineName  = firstTimelineName
        self.secondTimelineName = secondTimelineName
        self.fromDate           = fromDate
        self.toDate             = toDate

        self.firstTimeline      = Timeline(firstTimelineName)
        self.secondTimeline     = Timeline(secondTimelineName)

        self.timelineAnal       = TimelineAnal(self.firstTimeline, self.secondTimeline)
