import os
import time
from datetime import date

import pandas as pd
from pytrends.request import TrendReq


def get_google_top10(year, geo):
    """Let us see what was trending in searches yearly.
    Make sure you use VPN, because Google keep blocking unusual activity.

    Args:
        year (Int): search in that year
        geo (String): search in that geolocation

    Returns:
        pandas.DataFrame: get the weekly top 10 Google Search trend in that year.
    """
    # get the top10 list
    top10_charts = pytrend.top_charts(year, geo=geo)
    # get weekly interest over time for each keyword
    dataset = []
    for keyword in top10_charts["title"].tolist():
        try:
            if year == date.today().year:  # to avoid timeframe error
                pytrend.build_payload(
                    kw_list=[keyword],
                    cat=0,
                    timeframe="{0}-01-01 {0}-12-{1}".format(
                        str(date.today().year), str(date.today().day)
                    ),
                    geo=geo,
                )
                data = pytrend.interest_over_time()
                time.sleep(6)
            else:
                pytrend.build_payload(
                    kw_list=[keyword],
                    cat=0,
                    timeframe="{0}-01-01 {0}-12-30".format(str(year)),
                    geo=geo,
                )
                data = pytrend.interest_over_time()
                time.sleep(6)
            data = data.drop(labels=["isPartial"], axis="columns")
            dataset.append(data)
        except Exception as e:
            print(e)
    result = pd.concat(dataset, axis=1).T
    # output
    return result


def get_topic_title(year, geo):
    # get the top10 list
    top10_charts = pytrend.top_charts(year, geo=geo)
    dataset = []
    for keyword in top10_charts["title"].tolist():
        try:
            # get the related topic from the keyword
            pytrend.build_payload(kw_list=[keyword])
            related_topic = pytrend.related_topics()
            time.sleep(6)
            # convert to df and reformat the df
            df = related_topic[keyword]["top"][["value", "topic_title"]]
            df.insert(0, "Source", list([keyword] * df.shape[0]), True)
            df = df.rename({"value": "Weight", "topic_title": "Target"}, axis="columns")
            df = df[["Source", "Target", "Weight"]]
            # append to dataset
            dataset.append(df)
        except Exception as e:
            print(e)
    result = pd.concat(dataset, axis=0)
    # output
    return result


def get_topic_type(year, geo):
    # get the top10 list
    top10_charts = pytrend.top_charts(year, geo=geo)
    dataset = []
    for keyword in top10_charts["title"].tolist():
        try:
            # get the related topic from the keyword
            pytrend.build_payload(kw_list=[keyword])
            related_topic = pytrend.related_topics()
            time.sleep(6)
            # convert to df and reformat the df
            df = related_topic[keyword]["top"][["value", "topic_type"]]
            df.insert(0, "Source", list([keyword] * df.shape[0]), True)
            df = df.rename({"value": "Weight", "topic_type": "Target"}, axis="columns")
            df = df[["Source", "Target", "Weight"]]
            # append to dataset
            dataset.append(df)
        except Exception as e:
            print(e)
    result = pd.concat(dataset, axis=0)
    # output
    return result


def iter_google_top10(
    func="all", year_start=2012, year_end=date.today().year, geo="ID"
):
    """to implement the function and
    save the output to csv file

    Args:
        func (String): what function you want to iterate:
                        (get_google_top10, get_topic_title, get_topic_type, all)
        year_start (Int): pytrends year start
        year_end (Int): pytrends year end
        geo (String): pytrends geolocation
    """
    if func == "get_google_top10":
        try:
            # iterate yearly (2012-this year)
            for year in list(range(year_start, year_end + 1)):
                print("Please wait, scraping Top 10 Charts " + str(year) + "...")
                get_google_top10(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\google_top10/googletop10_{0}_{1}.csv".format(
                        geo, str(year)
                    )
                )
            print("Scraping done!")
        except Exception as e:
            print(e)
    elif func == "get_topic_title":
        try:
            # iterate yearly (2012-this year)
            for year in list(range(year_start, year_end + 1)):
                print("Please wait, scraping Topic Title " + str(year) + "...")
                get_topic_title(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\related_topics\\topic_title/topictitle_{0}_{1}.csv".format(
                        geo, str(year)
                    ),
                    index=False,
                )
            print("Scraping done!")
        except Exception as e:
            print(e)
    elif func == "get_topic_type":
        try:
            # iterate yearly (2012-this year)
            for year in list(range(year_start, year_end + 1)):
                print("Please wait, scraping Topic Type " + str(year) + "...")
                get_topic_type(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\related_topics\\topic_type/topictype_{0}_{1}.csv".format(
                        geo, str(year)
                    ),
                    index=False,
                )
            print("Scraping done!")
        except Exception as e:
            print(e)
    elif func == "all":
        try:
            # iterate yearly (2012-this year)
            for year in list(range(year_start, year_end + 1)):
                print("Please wait, scraping " + str(year) + "...")
                get_google_top10(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\google_top10/googletop10_{0}_{1}.csv".format(
                        geo, str(year)
                    )
                )
                get_topic_title(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\related_topics\\topic_title/topictitle_{0}_{1}.csv".format(
                        geo, str(year)
                    ),
                    index=False,
                )
                get_topic_type(year, geo).to_csv(
                    os.getcwd()
                    + "\\data\\related_topics\\topic_type/topictype_{0}_{1}.csv".format(
                        geo, str(year)
                    ),
                    index=False,
                )
            print("Scraping done!")
        except Exception as e:
            print(e)
    else:
        print("Please insert the func parameter")


"""
Implement the functions
"""
pytrend = TrendReq()
iter_google_top10()
