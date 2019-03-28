import time
import csv

class Storage(object):

  def __init__(self):
    self.store = {}

  def retrieve(self, key):
    # Returns the value for key.
    return self.store[key]['data'] if key in self.store else "Invalid key."

  def save(self, key, value):
    # Returns the newly saved key and value.
    self.store[key] = {'data': value, 'time': time.time()}
    return key + " = " + value

  def dump(self):
    # Returns exported keys and exports data to csv file.
    keys = self.keys()
    with open('dump.csv', 'w') as fp:
      w = csv.DictWriter(fp, fieldnames=['key', 'value'])
      w.writeheader()
      for key in keys:
        w.writerow({'key': key, 'value': self.retrieve(key)})
    return ", ".join(keys)

  def keys(self):
    # Returns a list of all keys in the datastore.
    return [key for key in self.store]

  def times(self):
    # Returns a list of all times in the datastore.
    return [value['time'] for key, value in self.store]

  def values(self):
    # Returns a list of all values in the datastore.
    return [value['data'] for key, value in self.store]
  