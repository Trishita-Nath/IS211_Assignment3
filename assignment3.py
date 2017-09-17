
import argparse
import urllib2
import csv
from StringIO import StringIO
import re
from collections import defaultdict
from datetime import datetime


#url to use with argparse  http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
def read_url(weburl):
    response = urllib2.urlopen(weburl)
    return response.read()

##Method for calculating image hits and most common browser
def parse_csv(csvdata):
    count_img = 0
    count_rows = 0
    count_safari = 0
    count_firefox = 0
    count_chrome = 0
    count_IE = 0
    reader = csv.reader(StringIO(csvdata))
    imgRegex = re.compile(r'.jpg$|.gif$|.png$',re.IGNORECASE)
    chromeRegex = re.compile(r'Chrome',re.IGNORECASE)
    safariRegex = re.compile(r'safari',re.IGNORECASE)
    firefoxRegex = re.compile(r'firefox',re.IGNORECASE)
    IERegex = re.compile(r'internet explorer',re.IGNORECASE)

    for row in reader:
        count_rows += 1
        searchObj = imgRegex.search(row[0])
        if searchObj:
            count_img += 1
        if chromeRegex.search(row[2]):
            count_chrome += 1
        elif safariRegex.search(row[2]):
            count_safari += 1 
        elif firefoxRegex.search(row[2]):
            count_firefox += 1
        elif IERegex.search(row[2]):
            count_IE += 1         

    if(count_chrome > count_safari and count_chrome > count_firefox and count_chrome > count_IE):
        browser = "Chrome"
    elif(count_safari > count_chrome and count_safari > count_firefox and count_safari > count_IE):
        browser = "Safari"
    elif(count_firefox > count_safari and count_firefox > count_chrome and count_firefox > count_IE):
        browser = "Firefox"
    else:
        browser = "Internet Explorer"    

    print " \n Images requests account for {}%  of all requests".format(100.0 * count_img/count_rows )
    print "\n Most common browser of the day is "+browser


##Method for calculating hourly hits
def aggregate_hits_by_hour(csvdata):
    reader = csv.reader(StringIO(csvdata))
    result_dict = defaultdict(int)
    for row in reader:
        dt = datetime.strptime(row[1] ,'%Y-%m-%d %H:%M:%S')
        result_dict[dt.hour] += 1
    for i in range(24):
        if i not in result_dict:
            result_dict[i] = 0
    print('\n============================================Hit By Hours===================================')
    for hour,value in sorted(result_dict.items(), key = lambda a : - a[1]):
        print ('Hour {h} has {v} hits'.format(h = hour, v = value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assignment 3 to download a weblog and play with it.')
    parser.add_argument('--url', action="store", dest="weburl")
    args = parser.parse_args()
    csvdata = read_url(args.weburl)
    parse_csv(csvdata)
    aggregate_hits_by_hour(csvdata)