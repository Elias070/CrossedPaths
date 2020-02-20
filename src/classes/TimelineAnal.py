""" [{"timestamp": "1470016004000", "lat": 520611354, "lon": 44134579}, """

class TimelineAnal(object):
    """docstring for TimelineAnal."""

    analData = None

    def __init__(self, firstTimeline, secondTimeline):
        super(TimelineAnal, self).__init__()
        self.firstTimeline = firstTimeline
        self.secondTimeline = secondTimeline

        self.anal()

    def getAnalResults(): return analData

    def getClosest(self, num, secondTimelineDictKeys):
        secondTimelineDictKeysList = list(secondTimelineDictKeys)
        secondTimelineDictKeysToIntList = []

        # Omzetten naar list met int's ipv str's
        for dict_key in secondTimelineDictKeysList:
            secondTimelineDictKeysToIntList.append(int(dict_key))

        return min(secondTimelineDictKeysToIntList,key=lambda x:abs(x-int(num)))

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

        # Data gaat op timestamps van HOOG naar LAAG zodat er gestopt kan worden als het voorbij timeframe is
        """
        1. voor elke item in first timeline
        1a. vind closest timestamp in uit second timeline
        1b. haal geoinfo uit first timeline
        1b. haal geoinfo uit second timeline
        1b. bepaal afstand dmv co-ords
        1b. append gegevens in analData variable
        """
        count = 0
        for firstTimeline_idx, firstTimeline_item in firstTimelineData.items():
            count = count + 1
            print(str(count) + " / " + str(len(firstTimelineData.items())))
            # print()

            firstTimelineTimestamp = firstTimeline_idx
            secondTimelineTimestamp = self.getClosest(firstTimelineTimestamp, secondTimelineData.keys())

            firstTimelineLat = firstTimeline_item['lat']
            firstTimelineLon = firstTimeline_item['lon']
            secondTimelineLat = secondTimelineData[str(secondTimelineTimestamp)]['lat']
            secondTimelineLon = secondTimelineData[str(secondTimelineTimestamp)]['lon']

            # get average timestamp
            averageTimestamp = str( round( (int(firstTimelineTimestamp) + int(secondTimelineTimestamp)) / 2 ) )

            # get avg distance
            distance = 100


            analData.append([
                averageTimestamp,
                distance,
                firstTimelineLat,
                firstTimelineLon,
                secondTimelineLat,
                secondTimelineLon
            ])


        ## measure distance per TIMEFRAME
        ## get basic variables pre rendered
        ##  -> closest
        ##  -> farest
        ##  -> percentage together/not together in bar-statistic within (n) distance
