# ideas: takes input: a complete trace, or a distribution, or a boxplot.
from abc import ABC, abstractmethod
import collections
from enum import Enum
import random
import statistics
import string
from numpy import random as np_random
from common.ListsHelper import save_list_to_file
from simulator.power_models.CalibrationDataDescription import DataDistributionDescription
from simulator.power_models.Enums import ModelNameEnum, SpecificCalibMode

from simulator.simulator_common import *
import numpy as np 


class ParentPowerStateModel(ABC):
    # Power state model is non-ordered set of double-value entries: state, power description
    # Assuming power state model entry is for one device.
    # Assuming each state is unique.(Name idle in different ways if u have many sub-states)

    def __init__(self, model_Name):
        self.name = model_Name # todo in parent
        self.StateDictionary = {}
    @abstractmethod
    def calibrate(self, stateName, trace_power_array, allow_update: bool=False):
        pass
    
    def add_or_update_state(self, stateName,  data_description: DataDistributionDescription):
        self.StateDictionary[stateName] = data_description

    def add_new_state(self, stateName,  data_description: DataDistributionDescription):
        if self.StateDictionary.get(stateName, "NA") != "NA":
            raise TypeError("state " + stateName +
                            " is already defined in the model")
        self.StateDictionary[stateName] = data_description

    def _add_power_state(self,stateName, data_description, allow_update):
        if allow_update:
            print("allow_update state calibration:"+allow_update)
            self.add_or_update_state(stateName, data_description)
        else:
            self.add_new_state(stateName, data_description)

def constructModel(modelNameEnum: ModelNameEnum, calibMode: SpecificCalibMode,predictionBucketSize) -> ParentPowerStateModel:
    model:ParentPowerStateModel = None
    if modelNameEnum == ModelNameEnum.STATIC and calibMode == SpecificCalibMode._MEDIAN:
       model = StaticPowerStateModel(calibMode._MEDIAN)
    
    elif   modelNameEnum == ModelNameEnum.STATIC and calibMode == SpecificCalibMode._MEAN:
       model = StaticPowerStateModel(calibMode._MEAN)
    
    elif  modelNameEnum == ModelNameEnum.UNIFORM_AVG_STDEV:
        model = VarAware_PSM_uniformAvg_Stdev(predictionBucketSize = predictionBucketSize)
    
    elif   modelNameEnum == ModelNameEnum.UNIFORM_Q1_Q3:
        model = VarAware_PSM_uniform_q1_q3(predictionBucketSize = predictionBucketSize)
    
    elif   modelNameEnum == ModelNameEnum.EMPIRICAL_DIST:
        model=VarAware_PSM_empirical_dist(predictionBucketSize = predictionBucketSize)
    
    else:
        print (modelNameEnum.name+" "+calibMode.name)
        raise NotImplementedError()
    return model

class StaticPowerStateModel(ParentPowerStateModel): 

    def __init__(self, calibMode:SpecificCalibMode):
        model_name = 'static' + (calibMode.name).lower()
        super().__init__(model_name)
        self.calibMode = calibMode
      
    def calibrate(self, stateName, trace_power_array, allow_update: bool=False):
        # print("calibrating static model " + self.name)
        pow: float = 0
        if  self.calibMode == SpecificCalibMode._MEDIAN:
            pow = statistics.median(trace_power_array)
        elif self.calibMode == SpecificCalibMode._MEAN:
            pow = statistics.mean(trace_power_array)
        elif self.calibMode == SpecificCalibMode._MIN:
            pow = min(trace_power_array)
        elif self.calibMode == SpecificCalibMode._MAX:
            pow = max(trace_power_array)
        else:
            raise NotImplementedError()
      
        pow = apply_power_measurement_resolution(pow)
        data_description = DataDistributionDescription(staticValue=pow)
        self._add_power_state( stateName, data_description, allow_update)

    def get_power_prediction(self, stateName) -> float:
        state_data_desc:DataDistributionDescription = self.StateDictionary.get(stateName, "-1")
        if state_data_desc == -1:
            raise TypeError("State " + stateName +
                            " is not defined in the model.")
        return state_data_desc.staticValue

class VarAware_PSM(ParentPowerStateModel,ABC): # abstract class coz we want to force child to implement 2 methods.
    def __init__(self, model_Name, predictionBucketSize):
        super().__init__(model_Name)
        self.predictionBucketSize = predictionBucketSize
        self.bucket = [] # each model state needs a bucket. todo remove state dictionary
        pass

    #abstract methods
    @abstractmethod
    def _predictInBucket(self, state_data_desc: DataDistributionDescription):
       pass
    
    @abstractmethod
    def calibrate(self, stateName:str, trace_power_array, allow_update:bool):
        pass

    # predictions
    def get_power_prediction(self, stateName) -> float:
        state_data_desc = self.StateDictionary.get(stateName, "-1")
        if state_data_desc == -1:
            raise TypeError("State " + stateName + " is not defined in the model.")
        if len(self.bucket) == 0:
            self.bucket=self._predictInBucket(state_data_desc) #abstract method, implemented by each child.

        last_index = len(self.bucket) -1
        prediction = self.bucket.pop(last_index)
        return apply_power_measurement_resolution(prediction)
    
    def _predictUniformlyInBucket(self, _from, _to):
       # https://www.w3schools.com/python/ref_random_uniform.asp
       return list(np_random.uniform( _from, _to, size = self.predictionBucketSize)) 
    pass

#################################################

class VarAware_PSM_uniform_q1_q3(VarAware_PSM):
    def __init__(self, predictionBucketSize): 
        super().__init__(model_Name='var-unif-q1-q3', predictionBucketSize=predictionBucketSize)

    # function calibrate only from the state, q1 and q3.
    def calibrate(self, stateName:string, trace_power_array, allow_update:bool=False):
        trace_power_q1 = apply_power_measurement_resolution(np.percentile(trace_power_array, [25]))
        trace_power_q3 = apply_power_measurement_resolution(np.percentile(trace_power_array, [75]))
        data_description = DataDistributionDescription(q1=trace_power_q1, q3=trace_power_q3)
        self._add_power_state(stateName,data_description, allow_update)
    
    def _predictInBucket(self, state_data_desc: DataDistributionDescription):
        return  self._predictUniformlyInBucket(state_data_desc.q1, state_data_desc.q3)
      
###################################################

class VarAware_PSM_empirical_dist(VarAware_PSM):
    def __init__(self, predictionBucketSize):
        super().__init__(model_Name= 'var-empirical-dist', predictionBucketSize=predictionBucketSize)

    def calibrate(self, stateName:string, trace_power_array, allow_update:bool=False):
        trace_power_freq_counter = collections.Counter(trace_power_array)
        data_description = DataDistributionDescription(power_measurements_frequencies_dictionary=trace_power_freq_counter)
        self._add_power_state(stateName,data_description, allow_update)
        pass
    
    def _predictInBucket(self, state_data_desc: DataDistributionDescription):
        return random.choices(population=state_data_desc.power_measurements,
                              weights=state_data_desc.power_measurements_frequencies,
                              k=self.predictionBucketSize)
    
##################################################

class VarAware_PSM_uniformAvg_Stdev(VarAware_PSM):
    def __init__(self, predictionBucketSize): 
        super().__init__(model_Name='var-unif-avg-stdev', predictionBucketSize=predictionBucketSize)

    def calibrate(self, stateName:string, trace_power_array, allow_update:bool=False):
        trace_power_avg = apply_power_measurement_resolution(statistics.mean(trace_power_array))
        trace_power_stdev = apply_power_measurement_resolution(statistics.stdev(trace_power_array))
        data_description = DataDistributionDescription(avg=trace_power_avg,stdev=trace_power_stdev)
        self._add_power_state(stateName,data_description, allow_update)

    def _predictInBucket(self, state_data_desc: DataDistributionDescription):
        min = state_data_desc.avg - state_data_desc.stdev 
        max = state_data_desc.avg + state_data_desc.stdev 
        return self._predictUniformlyInBucket(min, max)
 