from datetime import date
import numpy as np
from HDF5WriteBySpecify import HDF5Write
from Logger import Logger

class Datasets(object):
    def __init__(self):
        super(Datasets, self).__init__()
        self.speed_datasets = dict()
        self.direction_datasets = dict()

    def set_speed_dataset(self, current_dataset, current_pointer):
        self.speed_datasets.clear()
        self.speed_datasets["dataset"] = {"current": current_dataset, "start": current_pointer}

    def set_direction_dataset(self, current_dataset, current_pointer):
        self.direction_datasets.clear()
        self.direction_datasets["dataset"] = {"current": current_dataset, "start": current_pointer}

class HDF5Schedule():

    SIZE = {"speed": 6000, "direction": 3000}
    CREATE_DATASET = "Dataset created"
    CREATE_GROUP = "Group created"
    WRITE_DATASET = "Dataset written"
    
    def __init__(self):
        self.logger = Logger()

    def get_dataset_name(self):
        return date.today().strftime("%Y-%d-%m %H:%M:%S")

    def create_dataset(self, name, hdf5write : HDF5Write):
        group, ret = hdf5write.create_group(name)
        d = self.get_dataset_name()
        if ret:
            self.logger.log(name, "debug", ": ".join([d, HDF5Schedule.CREATE_GROUP]))
        data = np.zeros(HDF5Schedule.SIZE[name])
        dataset_name = d
        self.logger.log(name, "info", ": ".join([d, HDF5Schedule.CREATE_DATASET]))
        return hdf5write.create_dataset(group, data, dataset_name)

    def write_dataset(self, hdf5write : HDF5Write, group_name, dataset_name, data, start):
        try:
            hdf5write.write_dataset(group_name, dataset_name, data, start)
        except Exception as e:
            group = hdf5write.f_write[group_name]
            d = self.get_dataset_name()
            init_data = np.zeros(HDF5Schedule.SIZE[group_name])
            hdf5write.create_dataset(group, init_data, d)
            hdf5write.write_dataset(group_name, d, data, 0)
            self.logger.log(group_name, "info", ": ".join([d, HDF5Schedule.WRITE_DATASET]))
