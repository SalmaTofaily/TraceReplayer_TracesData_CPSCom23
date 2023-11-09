
class DataDistributionDescription(): 
    def __init__(self, minimum: float = None, q1: float = None, median: float = None, q3: float = None,
                  maximum: float = None, power_measurements_frequencies_dictionary: dict = None,
                  avg: float = None, stdev:float = None, staticValue: float = None
                  ):
        self.staticValue = staticValue
        self.minimum = minimum
        self.q1 = q1
        self.median = median
        self.q3 = q3
        self.maximum = maximum
        self.avg = avg
        self.stdev = stdev
        # self.mean
        # self.stdev

        # 2 lists items correspond to each others.
        self.power_measurements = []
        self.power_measurements_frequencies = []

        # I neeed probability not frequency
        self.power_measurements_frequencies_dictionary = power_measurements_frequencies_dictionary
        if power_measurements_frequencies_dictionary != None:
            self.power_measurements = list(
                power_measurements_frequencies_dictionary.keys())
            self.power_measurements_frequencies = list(
                power_measurements_frequencies_dictionary.values())
            
    def toString(self):
        return "dataDistributionDesc: staticValue=" + str(self.staticValue)+ \
    ",min="+str(self.minimum)+",max="+str(self.maximum)+\
    ",q1="+str(self.q1)+",q2="+str(self.median)+",q3="+str(self.q3)+"avg="+str(self.avg)+\
        ",stdev="+str(self.stdev)+",len(power_measurements)="+str(len(self.power_measurements)) #   self.power_measurements = [] self.power_measurements_frequencies = []
     
    def update_power_measurements_frequencies_dictionary(self,power_measurements_frequencies_dictionary):
        if power_measurements_frequencies_dictionary != None:
            self.power_measurements = list(
                power_measurements_frequencies_dictionary.keys())
            self.power_measurements_frequencies = list(
                power_measurements_frequencies_dictionary.values())
        else:
            raise TypeError("power_measurements_frequencies_dictionary is empty")
