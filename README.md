# Searx Notify
Searx scraper with pushover notifications

The idea came from Justin Seitz's [Automating OSINT blog](http://www.automatingosint.com/blog/2017/04/building-a-keyword-monitoring-pipeline-with-python-pastebin-and-searx/) and I have repurposed his [keywordmonitor.py](https://github.com/automatingosint/osint_public/blob/master/keyword_monitor/keywordmonitor.py) code stripping out the pastebin features and replacing the email functions with pushover notification system.


# Requirements
`sudo pip install python-pushover --user`

Follow the blog entry linked above to setup a Searx instance.
