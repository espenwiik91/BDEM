from pyspark import SparkContext


# import findspark
# findspark.init()


class Processing:

    def __init__(self):
        self.sc = SparkContext.getOrCreate()

    # takes a csvfile and a number as arguments. Finds the N most popular words used in tweets stored in csvfile
    def wordcounter(self, csvfile, numberOfWords):
        lines = self.sc.textFile(csvfile)
        lines_nonempty = lines.filter(lambda x: len(x) > 0)
        words = lines_nonempty.flatMap(lambda x: x.split())
        wordcounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).map(lambda x: (x[1], x[0])).sortByKey(
            False)
        res = wordcounts.take(numberOfWords)
        return res

    # takes a csvfile and a numeber as arguments. Finds the N most popular bigrams ues in tweets stored in csvfile
    def bigram(self, csvfile, numberOfWords):
        sentences = self.sc.textFile(csvfile) \
            .glom() \
            .map(lambda x: " ".join(x)) \
            .flatMap(lambda x: x.split("."))
        bigrams = sentences.map(lambda x: x.split()) \
            .flatMap(lambda x: [((x[i], x[i + 1]), 1) for i in range(0, len(x) - 1)])

        freq_bigrams = bigrams.reduceByKey(lambda x, y: x + y) \
            .map(lambda x: (x[1], x[0])) \
            .sortByKey(False)

        res = (freq_bigrams.take(numberOfWords))
        return res

    def most_common(self, list):
        return max(set(list), key=list.count)

    def retweets(self, list):
        words = self.sc.parallelize(list)
        words_filter = words.filter(lambda x: 'RT' in x)
        filtered = words_filter.collect()
        # res = self.most_common(filtered)
        return filtered

    def stopspark(self):
        self.sc.stop()
