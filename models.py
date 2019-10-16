import datetime
import logging
from scipy import stats


class FileModel(object):
    """Class for FileModel and properties processing"""
    def __init__(self, **kwargs):
        self.uuid = kwargs.get('uuid')
        self.name = (kwargs.get('name') + "_" +
                     (str(datetime.datetime.now()))).replace(' ', '')

        self.data_list = kwargs.get("data_list", None)
        self.key_list = kwargs.get("key_list", None)
        self.value_list = kwargs.get("value_list", None)
        self.key_set = set(self.key_list)

    @staticmethod
    def mean_per_key(key_set, data_list):
        result = dict()
        for key in key_set:
            counter = 0
            summ = 0
            for element in data_list:
                if element.get(key):
                    counter += 1
                    summ += int(element.get(key))
            mean = summ / counter
            iter_result = {key: mean}
            result.update(iter_result)
        return result

    @staticmethod
    def mode_per_key(key_set, data_list):
        result = dict()
        for key in key_set:
            value_to_key = []
            for element in data_list:
                if element.get(key):
                    value_to_key.append(int(element.get(key)))
            logging.warning(f' value_to_key - {value_to_key}')
            mode_key = int(str(stats.mode(value_to_key)[0]).replace('[',
                                                         '').replace(']', ''))
            result.update({key: mode_key})
        return result

    def process(self):
        means = self.mean_per_key(self.key_set, self.data_list)
        logging.warning(f'\n{means}\n')
        modes = self.mode_per_key(self.key_set, self.data_list)
        logging.warning(f'\n{modes}\n')
        result = {'mean': means, 'mode': modes}
        return result

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)
