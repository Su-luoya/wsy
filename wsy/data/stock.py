# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-20 10:17:13
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-23 18:21:05
import os
import sys
import warnings
from pprint import pprint

import baostock as bs
import numpy as np
import pandas as pd
import pretty_errors
from tqdm import tqdm, trange

sys.path.append(os.path.dirname(__file__) + os.sep + "../")
try:
    from ..log.log import checkfile, hide, makedir, show, wprint
    from ..speed.multiprocess import multiprocess
except Exception:
    from log.log import checkfile, hide, makedir, show, wprint
    from speed.multiprocess import multiprocess

warnings.filterwarnings("ignore")


class BarStock(object):
    """barstock basic functions"""

    def __init__(self):
        self.login()

    def login(self):
        """Log in"""
        hide()
        bs.login()
        show()

    def logout(self):
        """Log out"""
        hide()
        bs.logout()
        show()

    def get_data(self, rs):
        """Get data
        Args:
            rs : barstock resultset object
        Returns:
            Data Result (DataFrame): data returned from barstock
        """
        data_list = []
        if rs.error_code != "0":
            wprint(rs.error_msg)
            # raise ValueError(rs.error_msg)
        while rs.next():
            data_list.append(rs.get_row_data())
        return pd.DataFrame(data_list, columns=rs.fields)

    def date_check(self, stocks_info_dict, name):
        """Check if the start_date entered by the user is before the IPO"""
        if stocks_info_dict[name]["ipoDate"] > self.start_date:
            wprint(
                f"{name}'s ipo date is {stocks_info_dict[name]['ipoDate']}, which is after {self.start_date}."
            )

    @property
    def index_dict(self):
        """Stocks Data Index"""
        common_index = "date,code,open,high,low,close,volume,amount,turn,pctChg"
        return {
            "d": f"{common_index},preclose,tradestatus,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST",
            "w": common_index,
            "m": common_index,
        }


class ConstituentStocks(BarStock):
    """Stock Industry, sz50, hs300, zz500
    Returns:
        Stock Class (DataFrame)
    """

    def __init__(self):
        self.mk_dir()
        self.login()
        self.path = ".\\StockData Cache\\"

    def mk_dir(self):
        makedir(self.path, "constituent")

    def save_data(self, df, path):
        """save data"""
        df = df.set_index("code_name")
        df.index.name = "name"
        df.to_csv(f"{self.path}{path}")
        return df

    def stock_industry(self):
        """
        Return a DataFrame containing all stock industry data
        """
        df = self.get_data(bs.query_stock_industry())
        return self.save_data(df, "\\constituent\\stock_industry.csv")

    def sz50(self):
        """sz50"""
        df = self.get_data(bs.query_sz50_stocks())
        return self.save_data(df, "\\constituent\\sz50.csv")

    def hs300(self):
        """hs300"""
        df = self.get_data(bs.query_hs300_stocks())
        return self.save_data(df, "\\constituent\\hs300.csv")

    def zz500(self):
        """zz500"""
        df = self.get_data(bs.query_zz500_stocks())
        return self.save_data(df, "\\constituent\\zz500.csv")


class StockData(ConstituentStocks):
    """A-share historical K-line data
    Args:
        names (list): Stock Name. Defaults to ['贵州茅台', '隆基绿能'].
        start_date (str): Start Date. Defaults to '2019-12-01'.
        end_date (str): End Date. Defaults to '2020-12-31'.
        frequency (str): Trading Frequency → choose from ['d','w','m']. Defaults to 'd'.
        path (str): Data cache path (False → no cache). Defaults to './StockData Cache/'
    """

    def __init__(
        self,
        names=["贵州茅台", "隆基绿能"],
        start_date="2019-12-01",
        end_date="2020-12-31",
        frequency="d",
        path=".\\StockData Cache\\",
    ):  # sourcery skip: default-mutable-arg
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.path = path
        if not self.path:
            self.path = ".\\StockData Cache\\"
        makedir(self.path, "")
        self.stocks_info_file = f"{self.path}\\stock data\\stocks_info.csv"
        self.stocks_data_file = f"{self.path}\\stock data\\stocks_data.csv"
        super().__init__()

    def stocks_info_save(self, df_info):
        """Save stocks info dict into a ".csv" file"""
        makedir(self.path, "stock data")
        df_info.to_csv(self.stocks_info_file)

    def stocks_info_read(self):
        """Read stocks info cache
        Returns:
            Dict: stocks info dict
        """
        return (
            pd.read_csv(self.stocks_info_file, index_col="name").T.to_dict()
            if checkfile(self.stocks_info_file)
            else {}
        )

    def stocks_info_task(self, name):
        """Stock Info Task
        Args:
            name (str): stock Name
        """
        return self.get_data(bs.query_stock_basic(code_name=name))

    def stocks_info(self):
        """
        Return a dict containing stock names, codes and ipoDate
        {
            '贵州茅台': {'code': 'sh.600519', 'ipoDate': '2001-08-27'},
            '隆基绿能': {'code': 'sh.601012', 'ipoDate': '2012-04-11'},
            ...
        }
        """
        wprint("Loading stocks information...")
        # try loading cache
        stocks_info_dict = self.stocks_info_read()
        if stocks_info_dict:
            return stocks_info_dict
        # multiprocessing
        result = multiprocess(
            thread_function=self.stocks_info_task, task_list=self.names, max_workers=10
        )
        # concat and preprocess
        df_info = pd.concat(list(result))[["code_name", "code", "ipoDate"]]
        df_info.columns = ["name", "code", "ipoDate"]
        df_info = df_info.set_index(["name"])
        stocks_info_dict = df_info.T.to_dict()
        # save info data
        self.stocks_info_save(df_info)
        return stocks_info_dict

    def stocks_data_read(self):
        """Read stocks info and data cache
        Returns:
            DataFrame / None
        """
        return (
            pd.read_csv(self.stocks_data_file, index_col="date")
            if checkfile(self.stocks_data_file)
            else None
        )

    def stocks_data(self):
        """Return a DataFrame containing all the stocks data
        date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,psTTM,pcfNcfTTM,pbMRQ,isST
        """
        # Check cache data
        stocks_info_dict, stocks_data = self.stocks_info(), self.stocks_data_read()
        if stocks_data is not None:
            return stocks_data
        # Main
        wprint("Loading stocks data...")
        df_list = []
        for name in tqdm(self.names):
            self.date_check(stocks_info_dict, name)
            rs = bs.query_history_k_data_plus(
                code=stocks_info_dict[name]["code"],
                fields=self.index_dict[self.frequency],
                start_date=self.start_date,
                end_date=self.end_date,
                frequency=self.frequency,
                adjustflag="3",
            )
            df = self.get_data(rs)
            df.insert(loc=1, column="name", value=name)
            df_list.append(df)
        df = pd.concat(df_list).apply(pd.to_numeric, errors="ignore")
        df.index = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df.drop("date", axis="columns", inplace=True)
        # save stock data
        df.to_csv(self.stocks_data_file)
        return df


# To do ...
class QuickData(StockData, ConstituentStocks):
    """Faster but not stable sometimes.
    Used when there are more than 30 stocks.
    Args:
        names (list): Stock Name. Defaults to ['贵州茅台', '隆基绿能'].
        start_date (str): Start Date. Defaults to '2019-12-01'.
        end_date (str): End Date. Defaults to '2020-12-31'.
        frequency (str): Trading Frequency → choose from ['d','w','m']. Defaults to 'd'.
        sleep_time (float): In case of unstable connection.
    """

    def init(
        self,
        names=["贵州茅台", "隆基绿能"],
        start_date="2019-12-01",
        end_date="2020-12-31",
        frequency="d",
        sleep_time=0.2,
    ):
        # sourcery skip: default-mutable-arg
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.frequency = frequency
        self.sleep_time = sleep_time
        self.path = ".\\StockData Cache\\"
        makedir(self.path, "")
        makedir(self.path, "stock data")
        self.stocks_info_file = f"{self.path}\\stock data\\stocks_info.csv"
        self.stocks_data_file = f"{self.path}\\stock data\\stocks_data.csv"
        self.task_info = []
        self.df_list = []
        self.stocks_info_dict = {}

    def stock_info_task(self, name):
        """Stock Info Task
        Args:
            name (str): stock Name
        """
        return self.get_data(bs.query_stock_basic(code_name=name))

    def stocks_info_work(self):
        """Stock Info Work Function
        Returns:
            Dict: Stock Data
        """
        result = multiprocess(self.stock_info_task, self.names, max_workers=10)
        self.task_info = list(result)
        wprint("ヾ(≧▽≦*)o")
        df_info = pd.concat(self.task_info)[["code_name", "code", "ipoDate"]]
        df_info.columns = ["name", "code", "ipoDate"]
        df_info = df_info.set_index(["name"])
        df_info.to_csv(self.stocks_info_file)
        self.stocks_info_dict = df_info.T.to_dict()

    def stock_data_task(self, name):
        """Stock Data Task
        Args:
            name (str): stock Name
        """
        # sleep(self.sleep_time)
        self.login()
        self.date_check(self.stocks_info_dict, name)
        rs = bs.query_history_k_data_plus(
            code=self.stocks_info_dict[name]["code"],
            fields=self.index_dict[self.frequency],
            start_date=self.start_date,
            end_date=self.end_date,
            frequency=self.frequency,
            adjustflag="3",
        )
        self.logout()
        wprint(rs.error_msg)
        df = self.get_data(rs)
        df.insert(loc=1, column="name", value=name)
        return df

    def stocks_data_work(self):
        """Stock Data Work Function
        Returns:
            DataFrame: Stock Data
        """
        df_list = multiprocess(self.stock_data_task, self.names, max_workers=10)
        df = pd.concat(list(df_list)).apply(pd.to_numeric, errors="ignore")
        df.index = pd.to_datetime(df["date"], format="%Y-%m-%d")
        df.drop("date", axis="columns", inplace=True)
        df.to_csv(self.stocks_data_file)
        return df

    def main(self):
        """Main Function → multiprocessing
        Returns:
            DataFrame: Stock Data
        """
        self.stocks_info_work()
        return self.stocks_data_work()


if __name__ == "__main__":
    # cs = ConstituentStocks()
    # names = list(cs.hs300()['code_name'])
    # wprint(names)
    # ####################################################
    sd = StockData(  # names=names,
        start_date="2010-12-01", end_date="2022-12-31", frequency="d", path=False
    )
    # sd.names = list(sd.sz50().index)
    wprint(sd.stocks_data())
    # ####################################################
    # qd = QuickData()
    # qd.init(#names=list(qd.sz50()['name']),
    #         start_date='2010-12-01', end_date='2022-12-31',
    #         frequency='d')
    # pprint(qd.stocks_info_work())
    # pprint(qd.stocks_info_dict)
    # pprint(qd.stocks_data_work())
