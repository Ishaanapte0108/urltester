import os
import json
import pandas as pd
import timeit
import numpy as np
from logger import logger


class testurl:
    def __init__(self, inputFilePath, respFilePath) -> None:
        self.respFilePath = respFilePath
        try:
            with open(inputFilePath, 'r') as f:
                # read provided urls and save them in a dataframe
                fileContent = json.load(f)
                self.df = pd.DataFrame(list(fileContent.items()), columns=[
                                       'Website_Name', 'URL'])
        except Exception as e:
            logger.critical(e)
            return

    def calculate(self, url, num):
        # code snippets necessary for timeit module
        TEST_CODE = f"requests.get('{url}')"
        SETUP_CODE = "import requests"
        # returs a list containing time it took for resp from website, number of of list items equal to number of runs
        val = timeit.repeat(
            stmt=TEST_CODE, setup=SETUP_CODE, repeat=num, number=1)
        # save it to 2D numpy array
        self.arr = np.vstack((self.arr, val))

    def test(self, num):
        # initialize a 2D array with suitable dimensions
        self.arr = np.zeros((len(self.df.index), num))
        # use apply method on dataframe to calculate time for each url resp
        self.df['URL'].apply(self.calculate, args=[num])
        # remove garbage values from 2D array and create new 2D array
        self.arr = self.arr[len(self.df.index):, :]
        # create columns for response times (equal to number of times we want to test)
        l = list(map(lambda x: f"rt_{x}", range(0, num)))
        # create new small dataframe
        df2 = pd.DataFrame(self.arr, columns=l)
        # concatenate it to the old dataframe
        self.df = pd.concat([self.df, df2], axis=1)
        # calculate mean of response times
        self.df['avg_time'] = self.df.iloc[:, 2:].mean(axis=1)
        print(self.df)

    def export(self):
        # export data to new file
        try:
            with open(self.respFilePath, 'w') as f:
                self.df = self.df.drop(['URL'], axis=1)
                jsonContent = self.df.to_dict('records')
                json.dump(jsonContent, f, indent=2)
                logger.info('Records tranfered Successfully')
        except Exception as e:
            logger.critical(e)


t = testurl(r"urls.json", r"response.json")
# argument to test should be integer greater than 1
t.test(3)
t.export()
