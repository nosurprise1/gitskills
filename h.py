import os
import posixpath
import urllib
import itchatmp, time, requests
import csv

itchatmp.auto_login()
friends= itchatmp.get_friends(update=True)
print len(friends)
print friends[0]
