""" [{"timestamp": "1470016004000", "lat": 520611354, "lon": 44134579}, """
import numpy
import geopy.distance
import csv

class TimelineAnal(object):
    """docstring for TimelineAnal."""

    analData = None

    def __init__(self, firstTimeline, secondTimeline):
        super(TimelineAnal, self).__init__()
        self.firstTimeline = firstTimeline
        self.secondTimeline = secondTimeline

        self.anal()

    def getAnalResults(): return analData

    def getClosestSecondTimelineTimestamp(self, value, array):
        idx = numpy.searchsorted(array, value, side="left")
        if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
            return array[idx-1]
        else:
            return array[idx]

    def anal(self):
        firstTimelineLowestTimestamp = self.firstTimeline.timelinedata[len(self.firstTimeline.timelinedata)-1]['timestamp'];
        firstTimelineHighestTimestamp = self.firstTimeline.timelinedata[0]['timestamp'];
        secondTimelineLowestTimestamp = self.secondTimeline.timelinedata[len(self.secondTimeline.timelinedata)-1]['timestamp'];
        secondTimelineHighestTimestamp = self.secondTimeline.timelinedata[0]['timestamp'];

        minTimestamp = firstTimelineLowestTimestamp if secondTimelineLowestTimestamp < firstTimelineLowestTimestamp else secondTimelineLowestTimestamp
        maxTimestamp = firstTimelineHighestTimestamp if secondTimelineHighestTimestamp > firstTimelineHighestTimestamp else secondTimelineHighestTimestamp

        analData = [['AVG_TIMESTAMP', 'DISTANCE', 'LAT_1','LON_1','LAT_2','LON_2']]
        collection = []

        # list to dict met timestamp als key
        firstTimelineData = {}
        for firstTimeline_idx, firstTimeline_item in enumerate(self.firstTimeline.timelinedata):
            if int(firstTimeline_item['timestamp']) < int(minTimestamp) or int(firstTimeline_item['timestamp']) > int(maxTimestamp):
                continue; # Stay within min and max boundaries
            firstTimelineData[firstTimeline_item['timestamp']] = firstTimeline_item

        # list to dict met timestamp als key
        secondTimelineData = {}
        for secondTimeline_idx, secondTimeline_item in enumerate(self.secondTimeline.timelinedata):
            if int(secondTimeline_item['timestamp']) > int(maxTimestamp) or int(secondTimeline_item['timestamp']) > int(maxTimestamp):
                continue # Stay within min and max boundaries
            secondTimelineData[secondTimeline_item['timestamp']] = secondTimeline_item

        count = 0
        for firstTimeline_idx, firstTimeline_item in firstTimelineData.items():
            count = count + 1
            print(str(count) + " / " + str(len(firstTimelineData.items())))

            firstTimelineTimestamp = firstTimeline_idx
            secondTimelineTimestamp = self.getClosestSecondTimelineTimestamp(firstTimelineTimestamp, list(secondTimelineData.keys()))

            firstTimelineLat = float(str(firstTimeline_item['lat'])[:-7] + '.' + str(firstTimeline_item['lat'])[-7:])
            firstTimelineLon = float(str(firstTimeline_item['lon'])[:-7] + '.' + str(firstTimeline_item['lon'])[-7:])
            secondTimelineLat = float(str(secondTimelineData[str(secondTimelineTimestamp)]['lat'])[:-7] + '.' + str(secondTimelineData[str(secondTimelineTimestamp)]['lat'])[-7:])
            secondTimelineLon = float(str(secondTimelineData[str(secondTimelineTimestamp)]['lon'])[:-7] + '.' + str(secondTimelineData[str(secondTimelineTimestamp)]['lon'])[-7:])

            # get average timestamp
            averageTimestamp = str( round( (int(firstTimelineTimestamp) + int(secondTimelineTimestamp)) / 2 ) )

            # get avg distance (in meters)

            # print(str(44134584))
            # print(str(44134584)[:-6] + '.' + str(44134584)[-6:])

            coords_1 = (firstTimelineLat,firstTimelineLon)
            coords_2 = (secondTimelineLat,secondTimelineLon)

            distance = geopy.distance.distance(coords_1, coords_2).km

            analData.append([
                averageTimestamp,
                distance,
                firstTimelineLat,
                firstTimelineLon,
                secondTimelineLat,
                secondTimelineLon
            ])

            print(analData)
            if count == 100:
                with open('dataexport/export.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerows(analData)
                break


        ## measure distance per TIMEFRAME
        ## get basic variables pre rendered
        ##  -> closest
        ##  -> farest
        ##  -> percentage together/not together in bar-statistic within (n) distance
