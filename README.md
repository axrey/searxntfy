# Searx Notify
Searx scraper with pushover notifications

The idea came from Justin Seitz's [Automating OSINT blog](http://www.automatingosint.com/blog/2017/04/building-a-keyword-monitoring-pipeline-with-python-pastebin-and-searx/) and I have repurposed his [keywordmonitor.py](https://github.com/automatingosint/osint_public/blob/master/keyword_monitor/keywordmonitor.py) code stripping out the pastebin features and replacing the email functions with pushover notification system.


# Requirements
`sudo pip install python-pushover --user`

Follow the blog entry linked above to setup a Searx instance.

# Usage

Add a few keywords to a keywords.txt file in the same directory. If there are domains, words, or phrases you'd like to black list just add them to blacklist.txt.
Then just run ./searxmon.py on the same server that is running your Searx instance.
