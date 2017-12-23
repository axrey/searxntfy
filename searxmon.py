#!/usr/bin/python
import os, time, requests
from pushover import init, Client

pushover_token 		 = ""
pushover_key 		 = ""
searx_url            = "http://localhost:8888/?"
max_sleep_time       = 300


if os.path.isfile("keywords.txt"):
	keywords = filter(None, open("keywords.txt", "r").read().splitlines())
else:
	print("Failed to read in keywords.txt")
    raise SystemExit()


if not os.path.exists("detections"):
    os.mkdir("detections")


def send_alert(alert_kw):
    init(pushover_token)
    alert_body = "OSINT ALERT:\r\n"
    # walk through the searx results
    if alert_kw.has_key("searx"):
        for keyword in alert_kw['searx']:
            alert_body += "\r\nDetection: %s\r\n" % keyword
            for keyword_hit in alert_kw['searx'][keyword]:
                alert_body += "%s\r\n" % keyword_hit
    Client(pushover_key).send_message(title="OSINT Alert: Searx", message=alert_body)
    print "[!] Alert sent!"
    return


# Check if the URL is new.
def check_urls(keyword,urls):
    new_urls = []
    if os.path.exists("detections/%s.txt" % keyword):
        with open("detections/%s.txt" % keyword,"r") as fd:
            stored_urls = fd.read().splitlines()
        for url in urls:
            if url not in stored_urls:
                print "[*] New URL for %s discovered: %s" % (keyword,url)
                new_urls.append(url)
    else:
        new_urls = urls
    # now store the new urls back in the file
    with open("detections/%s.txt" % keyword,"ab") as fd:
        for url in new_urls:
            fd.write("%s\r\n" % url)
    return new_urls


def check_searx(keyword):
    hits = []
    # build parameter dictionary
    params               = {}
    params['q']          = keyword
    params['categories'] = 'general'
    params['time_range'] = 'day' #day,week,month or year will work
    params['format']     = 'json'
    print "[*] Querying Searx for: %s" % keyword
    # send the request off to searx
    try:
        response = requests.get(searx_url,params=params)
        results  = response.json()
    except:
        return hits
    # if we have results we want to check them against our stored URLs
    if len(results['results']):
        urls = []
        for result in results['results']:
            if result['url'] not in urls:
                urls.append(result['url'])
        hits = check_urls(keyword,urls)
    return hits


def check_keywords(keywords):
    alert_kw          = {}
    time_start = time.time()
    for keyword in keywords:
        result = check_searx(keyword)
        if len(result):
            if not alert_kw.has_key("searx"):
                alert_kw['searx'] = {}
            alert_kw['searx'][keyword] = result
    time_end   = time.time()
    total_time = time_end - time_start

    # if we complete the above inside of the max_sleep_time setting
    # we sleep. This is for Pastebin rate limiting
    if total_time < max_sleep_time:
        sleep_time = max_sleep_time - total_time
        print "[*] Sleeping for %d s" % sleep_time
        time.sleep(sleep_time)
    return alert_kw

check_keywords(keywords)

while True:
    alert_kw = check_keywords(keywords)
    if len(alert_kw.keys()):
        send_alert(alert_kw)
