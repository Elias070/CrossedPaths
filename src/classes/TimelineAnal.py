import numpy
import geopy.distance
import csv

class TimelineAnal(object):
    """docstring for TimelineAnal."""

    analData                = None
    closestTogether         = 0
    farthestFromEachother   = 2147483647

    def __init__(self, firstTimeline, secondTimeline):
        super(TimelineAnal, self).__init__()
        self.firstTimeline = firstTimeline
        self.secondTimeline = secondTimeline
        self.anal()

    # GETTERS & SETTERS
    def getAnalResults():           return analData
    def getClosestTogether():       return closestTogether
    def getFarthestFromEachother(): return farthestFromEachother
    def getAnalResults():           return analData

    def anal(self):
        firstTimelineLowestTimestamp = self.firstTimeline.timelinedata[len(self.firstTimeline.timelinedata)-1]['timestamp'];
        firstTimelineHighestTimestamp = self.firstTimeline.timelinedata[0]['timestamp'];
        secondTimelineLowestTimestamp = self.secondTimeline.timelinedata[len(self.secondTimeline.timelinedata)-1]['timestamp'];
        secondTimelineHighestTimestamp = self.secondTimeline.timelinedata[0]['timestamp'];


        # minTimestamp = firstTimelineLowestTimestamp if secondTimelineLowestTimestamp < firstTimelineLowestTimestamp else secondTimelineLowestTimestamp
        # maxTimestamp = firstTimelineHighestTimestamp if secondTimelineHighestTimestamp > firstTimelineHighestTimestamp else secondTimelineHighestTimestamp

        minTimestamp = firstTimelineLowestTimestamp
        maxTimestamp = firstTimelineHighestTimestamp

        if minTimestamp < secondTimelineLowestTimestamp:
            minTimestamp = secondTimelineLowestTimestamp

        if maxTimestamp > secondTimelineHighestTimestamp:
            maxTimestamp = secondTimelineHighestTimestamp

        # list to dict met timestamp als key
        firstTimelineData = {}
        for firstTimeline_idx, firstTimeline_item in enumerate(self.firstTimeline.timelinedata):
            if int(firstTimeline_item['timestamp']) < int(minTimestamp):
                continue; # Stay within min boundaries

            if int(firstTimeline_item['timestamp']) > int(maxTimestamp):
                continue; # Stay within max boundaries

            firstTimelineData[firstTimeline_item['timestamp']] = firstTimeline_item

        # list to dict met timestamp als key
        secondTimelineData = {}
        for secondTimeline_idx, secondTimeline_item in enumerate(self.secondTimeline.timelinedata):
            if int(secondTimeline_item['timestamp']) < int(minTimestamp):
                continue # Stay within min boundaries

            if int(secondTimeline_item['timestamp']) > int(maxTimestamp):
                continue # Stay within max boundaries

            secondTimelineData[secondTimeline_item['timestamp']] = secondTimeline_item



        # CLUSTER PER HOUR
        # for firstTimeline_idx, firstTimeline_item in firstTimelineData.items():


        count = 0
        analData = [['AVG_TIMESTAMP', 'DISTANCE', 'LAT_1','LON_1','LAT_2','LON_2']]
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
            averageTimestamp = str(round((int(firstTimelineTimestamp) + int(secondTimelineTimestamp)) / 2))

            # get avg distance
            coords_1 = (firstTimelineLat,firstTimelineLon)
            coords_2 = (secondTimelineLat,secondTimelineLon)
            distance = geopy.distance.distance(coords_1, coords_2).km

            # Add data to analization
            analData.append([
                averageTimestamp,
                distance,
                firstTimelineLat,
                firstTimelineLon,
                secondTimelineLat,
                secondTimelineLon
            ])

            print(analData)

            ### DEFINE VARIABLES
            if distance < self.closestTogether:
                self.closestTogether = distance

            if distance > self.farthestFromEachother:
                self.farthestFromEachother = distance

            # Stop after 100 write file en close file
            if count == 100:
                with open('dataexport/export.csv', 'w', newline='') as myfile:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                    wr.writerows(analData)
                break

def getClosestSecondTimelineTimestamp(self, firstTimelineTimestamp, secondTimelineTimestamps):
    idx = numpy.searchsorted(secondTimelineTimestamps, firstTimelineTimestamp, side="left")
    if idx > 0 and (idx == len(secondTimelineTimestamps) or math.fabs(firstTimelineTimestamp - secondTimelineTimestamps[idx-1]) < math.fabs(firstTimelineTimestamp - secondTimelineTimestamps[idx])):
        return secondTimelineTimestamps[idx-1]
    else:
        return secondTimelineTimestamps[idx]
