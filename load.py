# Process RSS feeds. 
# Luis Gomez. 2013

# Goal is to create a mysql import ready file with comma delimited items which would be events.

import feedparser
import csv
import time

from datetime import date
from os.path import exists
from urlparse import urlparse, parse_qs, parse_qsl

# Open up files 

fileToWrite = open('results.csv', 'wb')
fileToWrite.truncate()

# Datttaaaaaaaa
monthNumbers = { 'January':'1', 'February':'2', 'March':'3', 'April':'4', 'May':'5', 'June':'6', 'July':'7', 'August':'8', 'September':'9', 'October':'10', 'November':'11', 'December':'12' }

# Functions 


# Main Process
with open('librariesList.txt', 'rb') as line:
	linesToParse = csv.reader(line, delimiter=",")
	for feed in linesToParse:
		if feed[2]:
			libraryFeeds = feedparser.parse(feed[2])
			libraryFeedsCount = 0
			for libraryFeedEntry in libraryFeeds.entries:
				
				# Name - libraryFeedEntry.title.encode('utf-8')
				# Venue - feed[3].encode('utf-8')
				# Date - NA
				# Created - NA
				# Description - libraryFeedEntry.description.encode('utf-8')
				# Start Time - NA
				# End Time - NA
				# ZIP Code - feed[5].encode('utf-8')
				# Address - feed[4].encode('utf-8')
				# Phone - feed[6].encode('utf-8')
				# City - feed[0].encode('utf-8')
				# Link - libraryFeeds.feed.link.encode('utf-8')
				
				queryString = parse_qs(libraryFeedEntry.link.encode('utf-8'))
				
				if queryString.has_key('F_Day'):
					dateObject  = str(queryString['F_Day']).split('/')
					eventMonth = monthNumbers[dateObject[0].replace("['", "")]
					eventDay = dateObject[1]
					eventYear = dateObject[2].replace("']", "")
					
					eventDate = "%s-%s-%s" %(eventYear, eventMonth, eventDay)

					# created on the fly since missing
					eventStartTime = ""
					eventEndTime = ""
					eventCreated = date.today()
					eventVenue = feed[3].encode('utf-8')

				else:										
					if libraryFeedEntry.has_key('date'):
						# Wednesday, May 08, 2013
						dateObject = str(libraryFeedEntry.date).split(',')
						dateStringObject = dateObject[1].strip()
						dateStringObjectDayMonthSplit = dateStringObject.split(' ')
						eventMonth = monthNumbers[dateStringObjectDayMonthSplit[0]]
						eventDay = dateStringObjectDayMonthSplit[1]
						eventDate = "%s-%s-%s" %(dateObject[2], eventMonth, eventDay)
					else:
						eventDate = date.today()

					eventCreated = date.today()
					if libraryFeedEntry.has_key('time'):
						eventStartTime = libraryFeedEntry.time
					if libraryFeedEntry.has_key('endtime'):
						eventEndTime = libraryFeedEntry.endtime
					if libraryFeedEntry.has_key('location'):
						eventVenue = "%s - %s " %(feed[3].encode('utf-8'), libraryFeedEntry.location )

				writer = csv.writer(fileToWrite)
				writer.writerow((libraryFeedEntry.title.encode('utf-8'),  eventVenue.encode('utf-8'), eventDate, eventCreated, libraryFeedEntry.description.encode('utf-8'), eventStartTime, eventEndTime, feed[5].encode('utf-8'), feed[4].encode('utf-8'), feed[6].encode('utf-8'), feed[0].encode('utf-8'), libraryFeedEntry.link.encode('utf-8')))

				libraryFeedsCount += 1
			print "Total number of items for %s: %r" %(feed[3], libraryFeedsCount)
			time.sleep(5)
		else:
			print " - %s - doesn't have an RSS feed" %feed[3]

fileToWrite.close()

## Make this file able to run on production server vs locally
## Make sure to email file with data [total event items, feeds]