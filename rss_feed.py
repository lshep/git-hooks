import subprocess
import datetime
# import re
from os.path import basename, abspath
from xml.etree.ElementTree import fromstring
import logging


ENTRY="""
    <item>
      <title>%s</title>
      <link>https://bioconductor.org</link>
      <description><![CDATA[ %s ]]></description>
      <author>%s</author>
      <pubDate>%s</pubDate>
      <guid>%s</guid>
    </item>
"""


def rss_feed(oldrev, newrev, refname, length):
    """Post receive hook to check start Git RSS feed"""
    entry_list = []
    try:
        latest_commit = subprocess.check_output([
            "git", "log", oldrev + ".." + newrev,
            "--pretty=format:%H|%an|%ae|%s|%at"
        ])
        # Get package name
        package_path = subprocess.check_output([
            "git", "rev-parse", "--show-toplevel"]).strip()
        package_name = basename(abspath(package_path)).replace(".git", "")
    except Exception as e:
        logging.error("Exception: %s" % e)
        pass
    if latest_commit:
        # If more than one commit to unpack
        latest_commit = latest_commit.split("\n")
        # Reverse if there are multiple commits
        for commit in latest_commit[::-1]:
            commit_id, author, email, commit_msg, timestamp = commit.split("|")
            pubDate = datetime.datetime.fromtimestamp(
                        float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

            entry = ENTRY % (package_name,
                             commit_msg,
                             author + " : " + email,
                             pubDate,
                             commit_id)
            # Add entry as element in xml.etree
            entry_list.append(fromstring(entry))
    return entry_list
