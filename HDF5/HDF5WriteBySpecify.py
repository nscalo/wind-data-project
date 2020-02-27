import numpy as np
import h5py

class HDF5Write():

    def __init__(self):
        self.f_write = None
        self.f_read = None
        pass

    def create_file(self, filepath):
        self.f_write = h5py.File(filepath, 'w')
        
        return None

    def read_file(self, filepath):
        self.f_read = h5py.File(filepath, 'r')

        return None

    def create_group(self, group_name):
        try:
            g = self.f_write.require_group(group_name)
            r = True
        except TypeError as e:
            g = self.f_write[group_name]
            r = false

        return g, r

    def create_dataset(self, group, data, dataset_name):
        d = group.create_dataset(dataset_name,data=data, compression="gzip", compression_opts=9)

        return d

    def check_end_of_dataset(self, dataset, data, start):
        size = dataset.shape[0]
        return len(data) <= (size - start)

    def write_dataset(self, group_name, dataset_name, data, start):
        group = self.f_write[group_name]
        dataset = group[dataset_name]
        if self.check_end_of_dataset(dataset, data, start):
            group[dataset_name][start:start+len(data)] = data
        else:
            raise Exception("Dataset overflow")

    def close(self):
        if self.f_read:
            self.f_read.close()
        if self.f_write:
            self.f_write.close()

    