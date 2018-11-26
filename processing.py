from pyspark import SparkContext


# import findspark
# findspark.init()

# Class for pyspark processing
class Processing:

    # Constructor that creates or gets a SparkContext object.
    def __init__(self):
        self.sc = SparkContext.getOrCreate()

    # takes a csvfile and a number as arguments. Finds the numberOfWords most popular words used in tweets stored in csvfile
    # and returns a list with tuples as elements. The tuples are frequencies and words.
    def wordcounter(self, csvfile, numberOfWords):
        lines = self.sc.textFile(csvfile)
        lines_nonempty = lines.filter(lambda x: len(x) > 0)
        words = lines_nonempty.flatMap(lambda x: x.split())
        wordcounts = words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).map(lambda x: (x[1], x[0])).sortByKey(
            False)
        res = wordcounts.take(numberOfWords)
        return res

    # takes a csvfile with twitter texts and a number as arguments. Finds the numberOfWords most popular combination of two
    # words in sequence (bigrams), and returns these in a list with tuples as elements. The tuples are frequencies and bigrams.
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

    # Function that taks a list as arguments and returns the most frequent element in that list
    def most_common(self, list):
        return max(set(list), key=list.count)

    #Takes a list as argument. Uses a SparkContext object to find all elements in the list that contains a string,
    # in this example, "RT" - to find all elements in the list that contains the string. All elements containing the
    # string are returned.
    def retweets(self, list):
        words = self.sc.parallelize(list)
        words_filter = words.filter(lambda x: 'RT' in x)
        filtered = words_filter.collect()
        # res = self.most_common(filtered)
        return filtered

    #Stops the running of a SparkContext object.
    def stopspark(self):
        self.sc.stop()
