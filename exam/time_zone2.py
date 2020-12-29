# coding: utf-8
#******************************************************************************* handlers2.py
"""
New handlers for Community Stream. Supports paging.
"""
#*******************************************************************************

#=============================================================================== Imports

import datetime
import pytz

from dateutil import rrule
from operator import itemgetter
from pt import ptlog

from pt.ableconstants.constants import API_DATE_TIME_FORMAT, API_DATE_TIME_FORMAT_TZ
from pt.datacmp.Alert import Alert
from pt.datacmp.AlertView import AlertView
from pt.datacmp.CafeteriaMenuDay import CafeteriaMenuDay
from pt.datacmp.Calendar import CalendarEventView
from pt.datacmp.CommunityMedia import CommunityMediaView
from pt.datacmp.FeedEntry import FeedEntryView
from pt.datacmp.Flyer import FlyerView
from pt.datacmp.MarketplaceItem import MarketplaceItemView
from pt.datacmp.PermissionChecker import permissionChecker
from pt.datacmp.Person import get_person_initials, get_person_name
from pt.datacmp.utils import inbox
from pt.datacmp.utils.caches import getSettingFromSharedCache
from pt.datacmp.utils.calendars import getPlaintextEventDescription
from pt.datacmp.utils.directories import getActiveDirectories
from pt.datacmp.utils.errors import BadRequestErr
from pt.datacmp.utils.misc import get_date_time_display_string, FEATURE_ASSIGNMENT_GRADED_ALERTS, FEATURE_NATIVE_INBOX_ATTACHMENTS, FEATURE_REPLACE_TWITTER_LINKS
from pt.dataobjects.SharedDatabaseConnection import SharedDatabaseConnection
from pt.django.webservices.utils import PLHandler
from pt.pttimezone.pttimezone import getPytzSystemTimezone, timezoneMap
from pt.pttimezone.pttimezone import changeTZ
from pt.pttimezone.timezones import timezones


#=============================================================================== Static

sdc = SharedDatabaseConnection()

DEFAULT_LIMIT = 10
SYSTEM_TZ = getPytzSystemTimezone()

#=============================================================================== Classes

#------------------------------------------------------------------------------- CommunityStreamHandler2
class CommunityStreamHandler2(PLHandler):

    allowed_methods = ('GET', 'POST',)

    #--------------------------------------------------------------------------- read
    def read(self, request):
        """See POST"""

        return self.create(request)

    #--------------------------------------------------------------------------- create
    def create(self, request):
        """
        Get a page of the community stream. If the user is logged in, private messages and academic
        alerts are included in the results. All public information is opt-in. School status is always
        returned.

        Parameters
            orgIDs (type=list, optional): If present, return all stream items at these orgs. Else, use the following ids (feedIDs, mediaSourceIDs, etc)
            feedIDs (type=list): The feeds to include.
            mediaSourceIDs (type=list): The media sources to include.
            calendarIDs (type=list): The calendars to include.
            messageOrgIDs (type=list): The organizations to retrieve anonymous messages from. All private messages are included if user is logged in.
            flyerOrgIDs (type=list): The organizations to retrieve flyers from.
            marketplaceOrgIDs (type=list): The organizations to retrieve marketplace items from.
            cafeteriaMenuIDs (type=list): The cafeteria menus to include.
            cachedIDs (type=dict, optional): Dictionary mapping each item group to a list of cached ids for that group.

            limit (type=int, default=10): The maximum number of items to return in this request.
            maxTime (type=date, optional): The time of the last item returned, in UTC. All items returned in this request will have a time equal to or earlier than this date.
            tiebreakerIDs (type=dict, optional): Dictionary with groups/ids returned on previous pages. Items in the dict are not returned. This is important for calendars, messages, and alerts to prevent returning the same item on consecutive pages.

            includeSourceDetails (type=bool): Whether to include details for sources and organizations.

        Returns
            {
                "status": [
                    {
                        "directoryID": 117,
                        "name": "Lockdown",
                        "orgIDs": [
                            2000001899
                        ],
                        "displayOrgThumbnail": "https://storage.googleapis.com/pt99-1/images/organizations/b1b420a73c20b8c48b8d826284e70545b76906cf/999.jpg-thumbnail.jpg",
                        "displayOrgID": 2000001899,
                        "displayOrgName": "SPL9 Test",
                        "time": "2018-12-04 19:29:42 +0000",
                        "description": "Corgis"
                    }]
                "items": [
                    {
                        "orgThumbnailUrl": "",
                        "organizationName": "Delhi school of education",
                        "sender": "Teacher1, V",
                        "personID": 2001536905,
                        "organizationID": 2000002982,
                        "senderID": 2008121811,
                        "private": true,
                        "plaintext": "This",
                        "orgID": 2000002982,
                        "time": "2020-09-25 14:53:12 +0000",
                        "sentDate": "Sep 25, 2020 10:53 AM ADT",
                        "messageID": 2010201164,
                        "date": "2020-09-25 10:53:12",
                        "group": "messages",
                        "message": "<html><head></body>Test</body></html>",
                        "preview": "This",
                        "new": 1,
                        "id": 2010201164,
                        "subject": "You got a message from DSE-group1"
                    },
            "invalidItems": {
                "media": [<invalid media table id value>],
                "alerts": [<invalid alerts table id value>],
                "messages": [<invalid messages table id value>],
                "feedEntries": [<invalid feedEntries table id value>],
                "calendarEvents": [<invalid calendarEvents table id value>]
            },
            "limit": 10,
            "nextMaxTime": "2020-09-24 13:19:37 +0000"
        }
        """

        ret = {}
        user = self.getUser()

        limit = self.getInt('limit', DEFAULT_LIMIT)
        maxTime = getUtcDatetimeOrNow(self.get('maxTime'))
        systemMaxTime = maxTime.astimezone(SYSTEM_TZ)
        ptlog.syslog('maxtime: {}'.format(maxTime))
        maxCalendarTime = getUtcDatetimeOrNow(self.get('maxTime'), nowDelta = datetime.timedelta(days=1))
        #maxMenuTime = getUtcDatetimeOrNow(self.get('maxTime'), nowDelta = datetime.timedelta(days=2))

        cachedIDs = self.getJson('cachedIDs', {})
        previousIDs = self.getJson('tiebreakerIDs', {})
        includeSourceDetails = self.getBool('includeSourceDetails', False)

        items = []
        invalidIDs = { 'feedEntries': [], 'media': [], 'calendarEvents': [], 'messages': [], 'alerts': [] }

        loginOrg = self.getLoginOrg()
        loginOrgTZ = loginOrg.getTimezone().get_pytz()
        allOrgIDs = loginOrg['allChildrenIDs'] + [loginOrg['id']]

        defaultOrgIDs = self.getJson('orgIDs', [])
        if defaultOrgIDs:
            org_ids_str = ','.join(map(str, defaultOrgIDs))
            feedIDs = [itemID for itemID, in self.execute_query('SELECT id FROM Feed WHERE organizationID IN ({})'.format(org_ids_str)).fetchall()]
            mediaSourceIDs = [itemID for itemID, in self.execute_query('SELECT id FROM CommunityMediaSource WHERE organizationID IN ({})'.format(org_ids_str)).fetchall()]
            calendarIDs = [itemID for itemID, in self.execute_query('SELECT id FROM Calendar WHERE organizationID IN ({})'.format(org_ids_str)).fetchall()]
            cafeteriaMenuIDs = [itemID for itemID, in self.execute_query('SELECT id FROM CafeteriaMenu WHERE organizationID IN ({})'.format(org_ids_str)).fetchall()]
            messageAnonymousOrgIDs = defaultOrgIDs
            flyerOrgIDs = defaultOrgIDs
            marketplaceOrgIDs = defaultOrgIDs
        else:
            feedIDs = self.getJson('feedIDs', [])
            mediaSourceIDs = self.getJson('mediaSourceIDs', [])
            calendarIDs = self.getJson('calendarIDs', [])
            messageAnonymousOrgIDs = self.getJson('messageOrgIDs', [])
            flyerOrgIDs = self.getJson('flyerOrgIDs', [])
            marketplaceOrgIDs = self.getJson('marketplaceOrgIDs', [])
            cafeteriaMenuIDs = self.getJson('cafeteriaMenuIDs', [])

        if not self.get_param_bool('suppressOrgStatus'):
            ret['status'] = self.getOrganizationStatuses(allOrgIDs, loginOrg['id'])

        if feedIDs or mediaSourceIDs:
            maxAge = getSettingFromSharedCache('FEEDENTRYMAXAGE', loginOrg['id'])
            ret['maxAge'] = maxAge

        if feedIDs:
            candidates, invalid = self.getCandidateFeedEntries(
                    feedIDs = feedIDs,
                    maxTime = maxTime,
                    limit = limit,
                    cachedIDs = cachedIDs.get('feedEntries', []),
                    maxAge = maxAge,
                    tiebreaker = previousIDs.get('feedEntries', []))
            items.extend(candidates)
            invalidIDs['feedEntries'].extend(invalid)

        if mediaSourceIDs:
            candidates, invalid = self.getCandidateMediaEntries(
                    sourceIDs = mediaSourceIDs,
                    maxTime = maxTime,
                    limit = limit,
                    cachedIDs = cachedIDs.get('media', []),
                    maxAge = maxAge,
                    tiebreaker = previousIDs.get('media', []))
            items.extend(candidates)
            invalidIDs['media'].extend(invalid)

        if calendarIDs:
            candidates, invalid = self.getCandidateCalendarEvents(
                    calendarIDs = calendarIDs,
                    maxTime = maxCalendarTime,
                    limit = limit,
                    cachedIDs = cachedIDs.get('calendarEvents', []),
                    tiebreaker = previousIDs.get('calendarEvents', []))
            items.extend(candidates)
            invalidIDs['calendarEvents'].extend(invalid)

        if cafeteriaMenuIDs:
            # Menu items appear one day early at 2 PM (org time)
            streamHour = 14  # 2 PM
            maxMenuTime = (maxTime + datetime.timedelta(days=1)).astimezone(loginOrgTZ)
            # But if maxMenuTime is before 2 PM, move back one day
            if maxMenuTime.hour < streamHour:
                maxMenuTime = maxMenuTime + datetime.timedelta(days=-1)
            candidates = self.getCandidateCafeteriaMenuDays(
                    cafeteriaMenuIDs=cafeteriaMenuIDs,
                    maxTime=maxMenuTime,
                    limit=limit,
                    orgTZ=loginOrgTZ,
                    streamHour=streamHour,
                    cachedIDs=cachedIDs.get('cafeteriaMenuDays', []),
                    tiebreaker=previousIDs.get('cafeteriaMenuDays', []))
            items.extend(candidates)

        if user or messageAnonymousOrgIDs:
            candidates, invalid = self.getCandidateMessages(
                    orgIDs = messageAnonymousOrgIDs,
                    user = user,
                    maxTime = systemMaxTime,
                    limit = limit,
                    cachedIDs = cachedIDs.get('messages', []),
                    tiebreaker = previousIDs.get('messages', []))
            items.extend(candidates)
            invalidIDs['messages'].extend(invalid)

        if user and not self.getBool('suppressAlerts'):
            candidates, invalid = self.getCandidateAlerts(
                    user = user,
                    limit = limit,
                    maxTime = maxTime,
                    cachedIDs = cachedIDs.get('alerts', []),
                    tiebreaker = previousIDs.get('alerts', []))
            items.extend(candidates)
            invalidIDs['alerts'].extend(invalid)

        if flyerOrgIDs:
            candidates = self.getCandidateFlyers(
                    orgIDs = flyerOrgIDs,
                    maxTime = maxTime,
                    limit = limit,
                    tiebreaker = previousIDs.get('flyers', []))
            items.extend(candidates)

        if marketplaceOrgIDs:
            candidates = self.getCandidateMarketplaceItems(
                    orgIDs = marketplaceOrgIDs,
                    maxTime = maxTime,
                    limit = limit,
                    tiebreaker = previousIDs.get('marketplace', []))
            items.extend(candidates)

        sortedItems = sorted(items, key = itemgetter('time'), reverse=True)
        items = sortedItems[:limit]
        if len(items) > 0:
            ret['nextMaxTime'] = items[-1]['time'].strftime(API_DATE_TIME_FORMAT_TZ)
        else:
            ret['nextMaxTime'] = maxTime.strftime(API_DATE_TIME_FORMAT_TZ)
        ret['invalidItems'] = invalidIDs
        ret['limit'] = limit

        timeKeys = [
            'time', 'startTime', 'endTime', 'lastUpdated',
            'dtstart', 'until', 'created', 'startDateTime',
            'endDateTime', 'dateTime', 'lastModified',
            'creationDateTime',
        ]
        items, sources = self.addItemDetails(items, includeSourceDetails = includeSourceDetails, remoteAddr = self.request.META.get('REMOTE_ADDR'))
        for item in items:
            for key in timeKeys:
                if key in item:
                    if isinstance(item[key], datetime.datetime):
                        item[key] = item[key].strftime(API_DATE_TIME_FORMAT_TZ)
                    else:
                        item[key] = '*** Ran across a %s. %s ***' % (type(item[key]), item[key])
        ret['items'] = items
        if includeSourceDetails:
            ret['sources'] = sources

        return ret

    #--------------------------------------------------------------------------- getOrgTimezone
    def getOrgTimezone(self, orgID):

        query = 'SELECT timezoneName FROM Organization WHERE id = %s' % orgID
        timezoneName, = sdc.executeQuery(query).fetchone()
        return timezoneMap[timezoneName].get_pytz()

    #--------------------------------------------------------------------------- getFeedOrgTimezone
    def getFeedOrgTimezone(self, feedID):

        query = 'SELECT Organization.timezoneName FROM Feed JOIN Organization ON Feed.organizationID = Organization.id WHERE Feed.id = %s' % feedID
        timezoneName, = sdc.executeQuery(query).fetchone()
        return timezoneMap[timezoneName].get_pytz()

    #--------------------------------------------------------------------------- getMediaSourceOrgTimezone
    def getMediaSourceOrgTimezone(self, sourceID):

        query = 'SELECT Organization.timezoneName FROM CommunityMediaSource JOIN Organization ON CommunityMediaSource.organizationID = Organization.id WHERE CommunityMediaSource.id = %s' % sourceID
        timezoneName, = sdc.executeQuery(query).fetchone()
        return timezoneMap[timezoneName].get_pytz()

    #--------------------------------------------------------------------------- addItemDetails
    def addItemDetails(self, items, includeSourceDetails=False, remoteAddr=None):

        detailedItems = []
        feedTimezones = {}
        sourceTimezones = {}

        sources = {'organizations': {}, 'feeds': {}, 'calendars': {}, 'mediaSources': {}, 'cafeteriaMenus': {}}

        for group in ('messages', 'alerts', 'calendarEvents', 'feedEntries', 'media', 'flyers', 'marketplace', 'cafeteriaMenuDays'):
            groupItems = filter(lambda x: x['group'] == group, items)

            if group == 'messages':
                native_inbox_attachments = self.get_param_bool('nativeInboxAttachments') or self.appSupports(FEATURE_NATIVE_INBOX_ATTACHMENTS)
                delivery_method = self.get_param('deliveryMethod')
                if delivery_method and delivery_method not in ('INTERNET_WWW', 'MOBILE', 'HTML_RAW'):
                    raise BadRequestErr('deliveryMethod must be one of INTERNET_WWW, MOBILE, HTML_RAW')
                for messageDict in groupItems:
                    message = inbox.getInboxMessage(personID=messageDict.get('personID'), messageID=messageDict['id'], remote_addr=remoteAddr, nativeInboxAttachments=native_inbox_attachments, delivery_method=delivery_method)
                    messageDict.update(message)
                    orgID = messageDict['organizationID']
                    if includeSourceDetails and orgID not in sources['organizations']:
                        sources['organizations'][orgID] = permissionChecker.getOrganization(orgID).getApiDict()
                    detailedItems.append(messageDict)
            elif group == 'alerts':
                for alertDict in groupItems:
                    api_dicts = []
                    if alertDict.get('alertIDs'):
                        alertDict['alerts'] = []
                        for alert in AlertView(where='id IN ({})'.format(','.join(map(str, alertDict.get('alertIDs')))), fieldNames='ALL').fetchall():
                            api_dict = alert.getApiDict(login_org_id=self.getLoginOrgID())
                            alertDict.update(api_dict)
                            api_dicts.append(api_dict)
                            # alertDict['alerts'].append(api_dict)
                    else:
                        alert = Alert(verify=True, id=alertDict['id'])
                        api_dict = alert.getApiDict(login_org_id=self.getLoginOrgID())
                        alertDict.update(api_dict)

                    alert_text = ''
                    students_str = alertDict['personID'] != alertDict['studentPersonID'] and "student's " or ''
                    if alertDict['alertType'] == 'AssignmentGraded':
                        preamble = 's are' if len(api_dicts) > 1 else ' is'
                        alert_text = 'The following assignment{} now graded:\n{}'.format(preamble, '\n'.join(['{}: {}'.format(api_dict.get('description') or api_dict.get('type') or 'assignment', api_dict.get('score') or 'score') for api_dict in api_dicts]))
                    elif alertDict['alertType'] == 'LowAssignmentScore':
                        alert_text = 'Your {}grade for assignment "{}" is {}.'.format(students_str, api_dict.get('description') or api_dict.get('type') or 'assignment', api_dict.get('score') or 'score')
                    elif alertDict['alertType'] in ('ClassGradeUpdate', 'ClassGradeDropped'):
                        if api_dict.get('gradeDisplay'):
                            alert_text = 'Your {}grade is now {}.'.format(students_str, api_dict['gradeDisplay'])
                    elif alertDict['alertType'] == 'MissingAssignment':
                        alert_text = 'The assignment "{}" was due {} but has not yet been received by the teacher.'.format(api_dict.get('description') or api_dict.get('type') or 'assignment', get_date_time_display_string(datetime.datetime.strptime(api_dict['dueDate'], API_DATE_TIME_FORMAT)))
                    elif alertDict['alertType'] == 'CafeteriaBalance':
                        alert_text = 'Your {}cafeteria balance is now ${}'.format(students_str, api_dict['balance'])
                    if alert_text:
                        alertDict['alertDescription'] = alert_text

                    orgID = alertDict['organizationID']
                    for key in ('creationDateTime',):
                        if key in alertDict:
                            alertDict[key] = getDatetime(alertDict[key], SYSTEM_TZ)
                    if includeSourceDetails and orgID not in sources['organizations']:
                        sources['organizations'][orgID] = permissionChecker.getOrganization(orgID).getApiDict()
                    if includeSourceDetails:
                        org = sources['organizations'][orgID]
                        alertDict['orgName'] = org['name']
                        alertDict['orgThumbnailUrl'] = org.get('picThumbnailUrl', '')
                    detailedItems.append(alertDict)
            elif group == 'calendarEvents':
                loginOrg = self.getLoginOrg()
                loginOrgTZ = loginOrg.getTimezone()
                calendarEventIDs = [str(x['calendarEventID']) for x in groupItems]
                if calendarEventIDs:
                    events = {}
                    for event in CalendarEventView(where='id IN ({})'.format(','.join(calendarEventIDs)), fieldNames='ALL').generateall():
                        events[event['id']] = event
                    for eventDict in groupItems:
                        event = events[eventDict['calendarEventID']]
                        eventDict['summary'] = event['summary']
                        # PEB-5102 : Activity Stream reflects wrong times for calendar events and affects the correct times on the calendar itself
                        if eventDict.get('startDateTime'):
                            eventDict['startDateTime'] = changeTZ(eventDict['startDateTime'],timezone=timezones['UTC'], newTimezone=loginOrgTZ)
                            startTime = eventDict['startDateTime'].strftime('%Y-%m-%d %H:%M:%S')
                            eventDict['startDateTime'] = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')

                            eventDict['endDateTime'] = changeTZ(eventDict['endDateTime'],timezone=timezones['UTC'], newTimezone=loginOrgTZ)
                            endDateTime = eventDict['endDateTime'].strftime('%Y-%m-%d %H:%M:%S')
                            eventDict['endDateTime'] = datetime.datetime.strptime(endDateTime, '%Y-%m-%d %H:%M:%S')

                        eventDict['description'] = getPlaintextEventDescription(event['description'], eventUrl=eventDict.get('eventUrl'))
                        if includeSourceDetails and event['calendarID'] not in sources['calendars']:
                            calendar = event['calendar']
                            sources['calendars'][event['calendarID']] = calendar.getApiDict()
                            if calendar['organizationID'] not in sources['organizations']:
                                sources['organizations'][calendar['organizationID']] = permissionChecker.getOrganization(calendar['organizationID']).getApiDict()
                        if includeSourceDetails:
                            calendar = sources['calendars'][event['calendarID']]
                            org = sources['organizations'][calendar['organizationID']]
                            eventDict['orgName'] = org['name']
                            eventDict['calendarName'] = calendar['name']
                            eventDict['orgThumbnailUrl'] = org.get('picThumbnailUrl', '')
                        detailedItems.append(eventDict)
            elif group == 'feedEntries':
                feedCache = {}
                feedEntryIDs = [str(x['id']) for x in groupItems]
                if feedEntryIDs:
                    feedEntries = {}
                    for feedEntry in FeedEntryView(where='id IN ({})'.format(','.join(feedEntryIDs)), fieldNames='ALL').generateall():
                        feedEntries[feedEntry['id']] = feedEntry
                    for feedDict in groupItems:
                        entry = feedEntries[feedDict['id']]
                        feedID = entry['feedID']
                        if feedID not in feedCache:
                            feedCache[feedID] = entry['feed']
                        else:
                            entry.data['feed'] = feedCache[feedID]
                        feedDict.update(entry.getApiDict(stream=True, replaceTwitterLinks=self.appSupports(FEATURE_REPLACE_TWITTER_LINKS)))
                        if feedID not in feedTimezones:
                            feedTimezones[feedID] = self.getFeedOrgTimezone(feedID)
                        for key in ('dateTime', 'lastModified'):
                            feedDict[key] = getDatetime(feedDict[key], feedTimezones[feedID]).astimezone(pytz.utc)
                        if includeSourceDetails and feedID not in sources['feeds']:
                            feed = entry['feed']
                            sources['feeds'][feedID] = feed.getApiDict()
                            if feed['organizationID'] not in sources['organizations']:
                                sources['organizations'][feed['organizationID']] = permissionChecker.getOrganization(feed['organizationID']).getApiDict()
                        if includeSourceDetails:
                            feed = sources['feeds'][feedID]
                            orgID = feed['organizationID']
                            org = sources['organizations'][orgID]
                            feedDict['feedType'] = feed['type']
                            feedDict['orgThumbnailUrl'] = org.get('picThumbnailUrl', '')
                        detailedItems.append(feedDict)
            elif group == 'media':
                mediaIDs = [str(x['id']) for x in groupItems]
                if mediaIDs:
                    medias = {}
                    for media in CommunityMediaView(where='id IN ({})'.format(','.join(mediaIDs)), fieldNames='ALL').generateall():
                        medias[media['id']] = media
                    for mediaDict in groupItems:
                        entry = medias[mediaDict['id']]
                        mediaDict.update(entry.getApiDict())
                        sourceID = entry['communityMediaSourceID']
                        if sourceID not in sourceTimezones:
                            sourceTimezones[sourceID] = self.getMediaSourceOrgTimezone(sourceID)
                        for key in ('lastUpdated', 'created'):
                            mediaDict[key] = getDatetime(mediaDict[key], sourceTimezones[sourceID]).astimezone(pytz.utc)
                        if includeSourceDetails and sourceID not in sources['mediaSources']:
                            source = entry['communityMediaSource']
                            sources['mediaSources'][sourceID] = source.getApiDict()
                            if source['organizationID'] not in sources['organizations']:
                                sources['organizations'][source['organizationID']] = permissionChecker.getOrganization(source['organizationID']).getApiDict()
                        if includeSourceDetails:
                            source = sources['mediaSources'][sourceID]
                            org = sources['organizations'][source['organizationID']]
                            mediaDict['orgName'] = org['name']
                            mediaDict['orgThumbnailUrl'] = org.get('picThumbnailUrl', '')
                            mediaDict['sourceType'] = source['type']
                        detailedItems.append(mediaDict)
            elif group == 'flyers':
                flyerIDs = [str(x['id']) for x in groupItems]
                if flyerIDs:
                    flyers = {}
                    for flyer in FlyerView(where='id IN ({})'.format(','.join(flyerIDs)), fieldNames='ALL').generateall():
                        flyers[flyer['id']] = flyer
                    for flyerDict in groupItems:
                        flyer = flyers[flyerDict['id']]
                        flyerDict.update(flyer.getApiDict(login_org=self.getLoginOrg(), org_ids=flyerDict['organizationIDs']))
                        detailedItems.append(flyerDict)
            elif group == 'marketplace':
                itemIDs = [str(x['id']) for x in groupItems]
                if itemIDs:
                    marketplaceItems = {}
                    for item in MarketplaceItemView(where='id IN ({})'.format(','.join(itemIDs)), fieldNames='ALL').generateall():
                        marketplaceItems[item['id']] = item
                    for itemDict in groupItems:
                        item = marketplaceItems[itemDict['id']]
                        itemDict.update(item.getApiDict())
                        detailedItems.append(itemDict)
            elif group == 'cafeteriaMenuDays':
                if groupItems:
                    days = {}
                    menus = {}
                    for info in groupItems:
                        try:
                            day = CafeteriaMenuDay(menuID=info['menuID'], date=info['date'], verify=True)
                        except:
                            pass
                        else:
                            info.update(day.getApiDict())
                            detailedItems.append(info)
                            if includeSourceDetails and not sources['cafeteriaMenus'].get(day['menuID']):
                                sources['cafeteriaMenus'][day['menuID']] = day['menu'].getApiDict()

        return sorted(detailedItems, key = itemgetter('time'), reverse = True), sources

    #--------------------------------------------------------------------------- getOrganizationStatuses
    def getOrganizationStatuses(self, orgIDs, loginOrgID):

        ret = []
        groups = {}

        activeDirectories = getActiveDirectories(loginOrgID)
        if not activeDirectories:
            return []

        def activeDirectoryForOrg(orgID):
            for d in activeDirectories:
                if d.hasOrg(orgID):
                    return d
            return None

        def activeDirectoryForOrgs(orgIDs):
            for d in activeDirectories:
                hasAll = True
                for orgID in orgIDs:
                    if not d.hasOrg(orgID):
                        hasAll = False
                        break
                if hasAll:
                    return d

        query = '''
        SELECT Organization.id, OrganizationStatus.name, OrganizationStatus.description, OrganizationStatus.startDateTime
        FROM Organization LEFT JOIN OrganizationStatus ON Organization.organizationStatusID = OrganizationStatus.id
        WHERE Organization.id IN (%s)
          AND OrganizationStatus.name IS NOT NULL
        ''' % (','.join(map(str, orgIDs)))
        for orgID, statusName, statusDescription, start in sdc.executeQuery(query).fetchall():
            utcStart = mxToUtcDatetime(start)
            groupKey = '%s - %s - %s' % (statusName, statusDescription, utcStart.strftime(API_DATE_TIME_FORMAT))
            if groupKey not in groups:
                groups[groupKey] = {
                    'name': statusName,
                    'description': statusDescription,
                    'time': utcStart.strftime(API_DATE_TIME_FORMAT_TZ),
                    'orgIDs': [],
                }
            if activeDirectoryForOrg(orgID):
                groups[groupKey]['orgIDs'].append(orgID)

        ret = []
        for status in groups.values():
            if len(status['orgIDs']) == 0:
                # No org with this status is in an active directory
                continue

            displayOrgID = status['orgIDs'][0] if len(status['orgIDs']) == 1 else loginOrgID
            displayOrg = permissionChecker.getOrganization(displayOrgID)

            status['displayOrgID'] = displayOrgID
            status['displayOrgName'] = displayOrg['name']
            status['displayOrgThumbnail'] = displayOrg.getPictureUrl(thumbnail = True)
            d = activeDirectoryForOrgs(status['orgIDs'])
            status['directoryID'] = (d or activeDirectories[0]).get('id')
            ret.append(status)

        return ret

    #--------------------------------------------------------------------------- getCandidateFeedEntries
    def getCandidateFeedEntries(self, feedIDs, maxTime, limit, cachedIDs=[], maxAge=365, tiebreaker=[]):

        ret = []

        query = """
        SELECT id, dateTime FROM FeedEntry
        WHERE feedID IN (%(feedIDs)s)
          AND dateTime BETWEEN DATE_SUB(CURDATE(), INTERVAL %(maxAge)d DAY) AND "%(maxTime)s" AND hidden = "FALSE"
          %(tiebreakerWhere)s
        ORDER BY dateTime DESC, id DESC
        LIMIT %(limit)d
        """ % {
            'feedIDs': ','.join(map(str, feedIDs)),
            'maxAge': maxAge,
            'maxTime': maxTime,
            'tiebreakerWhere': ('AND id NOT IN (%s)' % ','.join(map(str, tiebreaker))) if tiebreaker else '',
            'limit': limit + 1,
        }

        for id, dateTime in sdc.executeQuery(query).fetchall():
            ret.append({
                'group': 'feedEntries',
                'id': id,
                'time': mxToUtcDatetime(dateTime),
            })

        invalid = []
        if cachedIDs:
            query = '''
            SELECT id FROM FeedEntry WHERE id IN (%s) AND hidden = "FALSE"
            ''' % (','.join(map(str, cachedIDs)))
            for row in sdc.executeQuery(query).fetchall():
                cachedIDs.remove(row[0])
            invalid.extend(cachedIDs)

        return ret, invalid

    #--------------------------------------------------------------------------- getCandidateMediaEntries
    def getCandidateMediaEntries(self, sourceIDs, maxTime, limit, cachedIDs=[], maxAge=365, tiebreaker=[]):

        ret = []

        query = """
        SELECT CommunityMedia.id, CommunityMedia.created
        FROM CommunityMedia
          JOIN CommunityMediaSource ON CommunityMedia.communityMediaSourceID = CommunityMediaSource.id
        WHERE CommunityMediaSource.id IN (%(sourceIDs)s)
          AND CommunityMediaSource.type NOT IN ("FACEBOOK", "FLICKR")
          AND CommunityMedia.created BETWEEN DATE_SUB(CURDATE(), INTERVAL %(maxAge)d DAY) AND "%(maxTime)s"
          %(tiebreakerWhere)s
        ORDER BY CommunityMedia.created DESC, CommunityMedia.id DESC
        LIMIT %(limit)d
        """ % {
            'sourceIDs': ','.join(map(str, sourceIDs)),
            'maxAge': maxAge,
            'maxTime': maxTime,
            'tiebreakerWhere': ('AND CommunityMedia.id NOT IN (%s)' % ','.join(map(str, tiebreaker))) if tiebreaker else '',
            'limit': limit + 1,
        }

        for id, created in sdc.executeQuery(query).fetchall():
            ret.append({
                'group': 'media',
                'id': id,
                'time': mxToUtcDatetime(created),
            })

        invalid = []
        # TODO: invalid?

        return ret, invalid

    #--------------------------------------------------------------------------- getCandidateCafeteriaMenuDays
    def getCandidateCafeteriaMenuDays(self, cafeteriaMenuIDs, maxTime, limit, orgTZ, streamHour=14, cachedIDs=[], tiebreaker=[]):
        ret = []

        # Exclude existing items
        tiebreakerWhere = []
        for item in tiebreaker:
            tiebreakerWhere.append('(CafeteriaMenu.id = {} AND CafeteriaMenuDay.date = "{}")'.format(item['menuID'], item['date']))
        if tiebreakerWhere:
            tiebreakerWhere = 'AND NOT {}'.format('AND NOT '.join(tiebreakerWhere))
        else:
            tiebreakerWhere = ''

        query = """
        SELECT CafeteriaMenuDay.menuID, CafeteriaMenuDay.date, CafeteriaMenu.name
        FROM CafeteriaMenuDay
          JOIN CafeteriaMenu ON CafeteriaMenuDay.menuID = CafeteriaMenu.id
        WHERE CafeteriaMenu.id IN ({menuIDs})
          AND CafeteriaMenuDay.date BETWEEN DATE_SUB(CURDATE(), INTERVAL 365 DAY) AND "{maxTime}"
          AND CafeteriaMenuDay.hasItems = 1
          {tiebreaker}
        ORDER BY CafeteriaMenuDay.date DESC, CafeteriaMenu.name ASC
        LIMIT {limit}
        """.format(
            menuIDs=','.join(map(str, cafeteriaMenuIDs)),
            maxTime=maxTime.strftime("%Y-%m-%d"),
            tiebreaker=tiebreakerWhere,
            limit=limit + 1,
        )
        for menuID, date, name in sdc.executeQuery(query).fetchall():
            d = mxToUtcDatetime(date) # Midnight UTC
            # Menu items appear at 2 PM in local org time the day before
            local = orgTZ.localize(datetime.datetime(d.year, d.month, d.day, hour=streamHour))
            stream_time = local.astimezone(pytz.utc) + datetime.timedelta(days=-1)
            ret.append({
                'group': 'cafeteriaMenuDays',
                'menuID': menuID,
                'date': d,
                'time': stream_time,
                'name': name,
            })
        return ret

    #--------------------------------------------------------------------------- getCandidateMessages
    def getCandidateMessages(self, maxTime, limit, orgIDs=[], user=None, cachedIDs=[], tiebreaker=[]):

        ret = []
        invalid = []
        excludeIDs = set(tiebreaker)
        minTime = 'DATE_SUB(CURDATE(), INTERVAL 365 DAY)' # Limit inbox to one year

        if user:
            personID = user['id']

            queryParts = []
            for recipientTable, batchTable in [('MessageRecipient', 'Batch',), ('MessageRecipientArchive', 'BatchArchive',)]:
                queryParts.append("""
                SELECT %(recipientTable)s.messageID, %(recipientTable)s.batchID, %(batchTable)s.deliverStartDateTime, %(batchTable)s.organizationID
                FROM %(recipientTable)s JOIN %(batchTable)s ON %(recipientTable)s.batchID = %(batchTable)s.id
                WHERE %(recipientTable)s.recipientPersonID = %(personID)s
                  AND %(batchTable)s.deliverStartDateTime BETWEEN %(minTime)s AND %(maxTime)s
                  AND %(batchTable)s.deleted = "FALSE"
                  AND %(recipientTable)s.view = "TRUE"
                  %(excludeIDsWhere)s
                ORDER BY %(batchTable)s.deliverStartDateTime DESC, %(recipientTable)s.messageID DESC
                LIMIT %(limit)d
                """ % {
                    'recipientTable': recipientTable,
                    'batchTable': batchTable,
                    'personID': personID,
                    'minTime': minTime,
                    'maxTime': ('"%s"' % maxTime) if maxTime else 'CURDATE()',
                    'excludeIDsWhere': ('AND %s.messageID NOT IN (%s)' % (recipientTable, ','.join(map(str, excludeIDs)),)) if excludeIDs else '',
                    'limit': limit + 1,
                })
            query = unionQuery(queryParts)

            for messageID, batchID, batchStartMx, orgID in sdc.executeQuery(query).fetchall():
                excludeIDs.add(messageID)
                ret.append({
                    'time': mxToUtcDatetime(batchStartMx, tz = SYSTEM_TZ),
                    'group': 'messages',
                    'id': messageID,
                    'private': True,
                    'personID': personID,
                })

            # Retrieve all deleted message IDs for this recipient
            query = 'SELECT messageID FROM MessageRecipient WHERE recipientPersonID = %(personID)s AND view = "FALSE" UNION SELECT messageID FROM MessageRecipientArchive WHERE recipientPersonID = %(personID)s AND view = "FALSE"' % { 'personID': personID }
            excludeIDs |= set([messageID for messageID, in sdc.executeQuery(query).fetchall()])

        if orgIDs:
            queryParts = []
            for messageTable, batchTable in [('Message', 'Batch',), ('MessageArchive', 'BatchArchive',)]:
                queryParts.append("""
                SELECT %(messageTable)s.id AS messageID, %(messageTable)s.batchID, %(batchTable)s.deliverStartDateTime, %(batchTable)s.organizationID
                FROM %(messageTable)s JOIN %(batchTable)s ON %(messageTable)s.batchID = %(batchTable)s.id
                WHERE %(batchTable)s.organizationID IN (%(orgIDs)s)
                  AND %(batchTable)s.postedCommunityApp = "TRUE"
                  AND %(batchTable)s.deliverStartDateTime BETWEEN %(minTime)s AND %(maxTime)s
                  AND %(batchTable)s.deleted = "FALSE"
                  %(excludeIDsWhere)s
                ORDER BY %(batchTable)s.deliverStartDateTime DESC, %(messageTable)s.id DESC
                LIMIT %(limit)d
                """ % {
                    'messageTable': messageTable,
                    'batchTable': batchTable,
                    'orgIDs': ','.join(map(str, orgIDs)),
                    'minTime': minTime,
                    'maxTime': '"%s"' % maxTime if maxTime else 'CURDATE()',
                    'excludeIDsWhere': ('AND %s.id NOT IN (%s)' % (messageTable, ','.join(map(str, excludeIDs)),)) if excludeIDs else '',
                    'limit': limit + 1,
                })
            query = unionQuery(queryParts)

            # Only return one message per batch, to prevent duplicates as this was a send to all app message and it's
            # possible to have multiple messages created with a batch that includes other message types.
            b_set = set()
            for messageID, batchID, batchStartMx, orgID in sdc.executeQuery(query).fetchall():
                if batchID not in b_set:
                    b_set.add(batchID)
                    ret.append({
                        'time': mxToUtcDatetime(batchStartMx, tz = SYSTEM_TZ),
                        'group': 'messages',
                        'id': messageID,
                        'private': False,
                    })

        if cachedIDs:
            queryParts = []
            for messageTable, batchTable in (('Message', 'Batch',), ('MessageArchive', 'BatchArchive',),):
                queryParts.append("""
                SELECT %(messageTable)s.id
                FROM %(messageTable)s
                  JOIN %(batchTable)s ON %(messageTable)s.batchID = %(batchTable)s.id
                WHERE %(messageTable)s.id IN (%(messageIDs)s)
                  AND %(batchTable)s.deleted = "FALSE"
                """ % {
                    'messageTable': messageTable,
                    'batchTable': batchTable,
                    'messageIDs': ','.join(map(str, cachedIDs)),
                })
            query = unionQuery(queryParts)
            for id, in sdc.executeQuery(query).fetchall():
                cachedIDs.remove(id)
            invalid.extend(cachedIDs)

        return ret, invalid

    #--------------------------------------------------------------------------- getCandidateAlerts
    def getCandidateAlerts(self, user, limit, maxTime=None, cachedIDs=[], tiebreaker=[]):

        from pt.datacmp.utils import alerts

        ret = []
        personID = user['id']
        alertTriggers = alerts.getEnabledAlertTypes(personID)

        if not self.appSupports(FEATURE_ASSIGNMENT_GRADED_ALERTS) and 'AssignmentGraded' in alertTriggers:
            alertTriggers.remove('AssignmentGraded')

        query = """
        SELECT id, personID, alertType, studentPersonID, organizationID, sectionID, assignmentID, termID, viewed, creationDateTime
        FROM Alert
        WHERE personID = %(personID)s
          AND alertType IN ("%(alertTypes)s")
          AND valid = "TRUE"
          AND deleted = "FALSE"
          AND creationDateTime <= %(maxTime)s
          ORDER BY creationDateTime DESC, id DESC
        """ % {
            'personID': personID,
            'alertTypes': '","'.join(alertTriggers),
            'maxTime': ('"%s"' % maxTime) if maxTime else 'CURDATE()',
        }

        student_dict = {}
        student_ids = set()
        alert_graded_dict = {}
        query_results = sdc.executeQuery(query).fetchall()

        if query_results:
            for id, personID, alertType, studentPersonID, organizationID, sectionID, assignmentID, termID, viewed, creationDateTime in query_results:
                student_ids.add(studentPersonID)
                if alertType == 'AssignmentGraded':
                    key = (studentPersonID, organizationID, sectionID, creationDateTime)
                    if key not in alert_graded_dict:
                        alert_graded_dict[key] = []
                    alert_graded_dict[key].append((id, personID, alertType, studentPersonID, organizationID, sectionID, assignmentID, termID, viewed, creationDateTime))

            for student_id, first_name, last_name, picture_url in sdc.executeQuery('SELECT id, firstName, lastName, pictureURL FROM Person WHERE id IN ({})'.format(','.join(map(str, student_ids)))).fetchall():
                student_dict[student_id] = (first_name, last_name, picture_url)

            tiebreaker = set(tiebreaker)
            for id, personID, alertType, studentPersonID, organizationID, sectionID, assignmentID, termID, viewed, creationDateTime in query_results:
                if len(ret) > limit:
                    break
                first_name, last_name, picture_url = student_dict.get(studentPersonID, ('', '', ''))
                item_dict = {
                    'group': 'alerts',
                    'id': id,
                    'personID': personID,
                    'alertType': alertType,
                    'studentPersonID': studentPersonID,
                    'studentInitials': get_person_initials(first_name, last_name),
                    'studentName': get_person_name(first_name, last_name),
                    'studentPicUrlThumb': picture_url,
                    'organizationID': organizationID,
                    'sectionID': sectionID,
                    'assignmentID': assignmentID,
                    'termID': termID,
                    'viewed': viewed == 'TRUE',
                    'time': mxToUtcDatetime(creationDateTime, tz=SYSTEM_TZ),
                    'valid': True,
                }
                if alertType == 'AssignmentGraded':
                    item_dict['alertIDs'] = []
                    for id, personID, alertType, studentPersonID, organizationID, sectionID, assignmentID, termID, viewed, creationDateTime in alert_graded_dict[(studentPersonID, organizationID, sectionID, creationDateTime)]:
                        item_dict['alertIDs'].append(id)
                    item_dict['id'] = ','.join(map(str, item_dict['alertIDs']))
                    if tiebreaker & set(item_dict['alertIDs']):
                        continue
                    tiebreaker |= set(item_dict['alertIDs'])
                else:
                    if id in tiebreaker:
                        continue
                ret.append(item_dict)

        invalid = []
        # TODO: invalid?

        return ret, invalid

    #--------------------------------------------------------------------------- getCandidateCalendarEvents
    def getCandidateCalendarEvents(self, calendarIDs, maxTime, limit, lastRequestTime=None, cachedIDs=[], tiebreaker=[]):

        from pt.datacmp.utils.calendars import getEvents, calendarTimeZoneCache

        items = []
        minTime = pytz.utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(days=30)

        # The cache pulls timezone from root org, so it doesn't matter which calendar we use
        calTZ = calendarTimeZoneCache[calendarIDs[0]]

        endDatetime = maxTime
        while len(items) < limit + 1:
            startDatetime = endDatetime - datetime.timedelta(days=30)
            if startDatetime < minTime: # Don't go further than minTime
                startDatetime = minTime

            found = 0

            events = getEvents(startDatetime, endDatetime,
                               newCalendarIDs = calendarIDs, modifiedCalendarIDs = calendarIDs,
                               modifiedSinceDateTime = lastRequestTime, modifiedEndDateTime = endDatetime if lastRequestTime else None,
                               translate = False)

            for instanceID, instance in events['events'].items():
                found += 1
                if not tiebreaker or instance['eventInstanceID'] not in tiebreaker:
                    for key in ['endDateTime', 'startDateTime', 'dtstart', 'until']:
                        if key in instance:
                            instance[key] = getDatetime(instance[key], calTZ).astimezone(pytz.utc)
                    instance['group'] = 'calendarEvents'
                    instance['time'] = instance['startDateTime'] - datetime.timedelta(days=1)
                    if instance['allDay']:
                        # Check all-day events against local time.
                        localStart = instance['startDateTime'].astimezone(calTZ)
                        if localStart <= endDatetime:
                            items.append(instance)
                    else:
                        items.append(instance)

            #instanceQuery = getEventInstanceQuery(calendarIDs = calendarIDs, startDateTime = startDatetime, endDateTime = endDatetime)
            #for eventInstanceID, calendarID, eventID, summary, desc, loc, utcStartMx, utcEndMx, allDay, lastUpdatedMx, exceptionID, documentID, documentUrl, documentTitle, personID, personFirstName, personLastName, trackID, trackName in sdc.executeQuery(instanceQuery).fetchall():
            #    utcStartDatetime = mxToUtcDatetime(utcStartMx)
            #    instanceID = '%s-%s' % (utcStartDatetime.astimezone(calTZ).strftime('%Y%m%d%H%M%S'), eventID)
            #    eventData = {
            #        'instanceID': instanceID,
            #        'calendarID': calendarID,
            #        'id': eventID,
            #        'summary': summary,
            #        'desc': desc,
            #        'location': loc,
            #        'startTime': utcStartDatetime,
            #        'endTime': mxToUtcDatetime(utcEndMx),
            #        'allDay': allDay == 'TRUE',
            #        'lastUpdated': mxToUtcDatetime(lastUpdatedMx),
            #        'exceptionID': exceptionID,
            #        'time': utcStartDatetime - datetime.timedelta(days=1), # place the event 1 day before start time
            #        'group': 'calendarEvents',
            #    }
            #    addDocumentDict(eventData, documentID, documentUrl, documentTitle)
            #    addPersonDict(eventData, personID, personFirstName, personLastName)
            #    addTrackDict(eventData, trackID, trackName)
            #    found += 1
            #    if not tiebreaker or instanceID not in tiebreaker:
            #        items.append(eventData)
            #exceptionDates = getEventInstanceExceptionDates(calendarIDs, startDatetime, endDatetime, calTZ)
            #recurrenceQuery = getEventRecurrenceQuery(calendarIDs = calendarIDs, startDateTime = startDatetime)
            #for calendarID, eventID, summary, desc, loc, frequency, interval, utcUntilMx, count, byDay, byMonthDay, byYearDay, byWeekNo, byMonth, bySetPos, wkst, rruleStr, utcEventStartMx, utcEventEndMx, allDay, lastUpdatedMx, documentID, documentUrl, documentTitle, personID, personFirstName, personLastName, trackID, trackName in sdc.executeQuery(recurrenceQuery).fetchall():
            #    utcEventStartDatetime = mxToUtcDatetime(utcEventStartMx)
            #    utcEventEndDatetime = mxToUtcDatetime(utcEventEndMx)
            #    eventBase = {
            #        'group': 'calendarEvents',
            #        'calendarID': calendarID,
            #        'eventID': eventID,
            #        'lastUpdated': mxToUtcDatetime(lastUpdatedMx),
            #        'summary': summary,
            #        'description': desc,
            #        'location': loc,
            #        'allDay': allDay == 'TRUE',
            #        'frequency': frequency,
            #        'interval': interval,
            #        'dtstart': utcEventStartDatetime,
            #        'rrule': rruleStr,
            #    }
            #    rule = getEventRecurrenceRule(frequency = frequency, interval = interval, eventStartDateTime = utcEventStartDatetime, calTZ = pytz.utc,
            #                                  untilUTCDateTime = utcUntilMx, count = count,
            #                                  byDay = byDay, byMonthDay = byMonthDay, byYearDay = byYearDay, byWeekNo = byWeekNo, byMonth = byMonth, bySetPos = bySetPos,
            #                                  wkst = wkst,
            #                                  eventBase = eventBase,
            #                                  format = False)
            #    rSet = rrule.rruleset()
            #    rSet.rrule(rule)
            #    eventExceptions = []
            #    if eventID in exceptionDates:
            #        for date in exceptionDates[eventID]:
            #            rSet.exdate(date)
            #            eventExceptions.append(date.replace(tzinfo=None))
            #    eventDuration = utcEventEndDatetime - utcEventStartDatetime
            #    for utcInstanceStartDatetime in rSet.between(startDatetime, endDatetime):
            #        if utcInstanceStartDatetime.replace(tzinfo=None) in eventExceptions:
            #            continue
            #        utcInstanceEndDatetime = utcInstanceStartDatetime + eventDuration
            #        instanceID = '%s-%s' % (utcInstanceStartDatetime.astimezone(calTZ).strftime('%Y%m%d%H%M%S'), eventBase['eventID'])
            #        eventData = {
            #            'instanceID': instanceID,
            #            'startTime': utcInstanceStartDatetime,
            #            'endTime': utcInstanceEndDatetime,
            #            'time': utcInstanceStartDatetime - datetime.timedelta(days=1),
            #        }
            #        eventData.update(eventBase)
            #        addDocumentDict(eventData, documentID, documentUrl, documentTitle)
            #        addPersonDict(eventData, personID, personFirstName, personLastName)
            #        addTrackDict(eventData, trackID, trackName)
            #        found += 1
            #        if not tiebreaker or instanceID not in tiebreaker:
            #            items.append(eventData)

            endDatetime = startDatetime
            if found == 0:
                # No more events. Stop loop
                break

        invalid = []
        # TODO: invalid?

        return items, invalid

    #--------------------------------------------------------------------------- getCandidateFlyers
    def getCandidateFlyers(self, orgIDs, maxTime, limit, tiebreaker=[]):

        ret = []

        query = """
        SELECT id, dateTime, organizationID
        FROM Flyer
          JOIN OrganizationFlyerLink ON Flyer.id = OrganizationFlyerLink.flyerID
        WHERE organizationID IN (%(orgIDs)s)
          AND dateTime <= %(maxTime)s
          %(tiebreakerWhere)s
        ORDER BY dateTime DESC, id DESC
        LIMIT %(limit)d
        """ % {
            'orgIDs': ','.join(map(str, orgIDs)),
            'maxTime': ('"%s"' % maxTime) if maxTime else 'CURDATE()',
            'tiebreakerWhere': ('AND id NOT IN (%s)' % ','.join(map(str, tiebreaker))) if tiebreaker else '',
            'limit': limit + 1,
        }
        flyers = {}
        for id, dateTime, organizationID in sdc.executeQuery(query).fetchall():
            if id in flyers:
                flyers[id]['organizationIDs'].append(organizationID)
            else:
                flyers[id] = {'group': 'flyers',
                              'id': id,
                              'organizationIDs': [organizationID],
                              'time': mxToUtcDatetime(dateTime)}
                ret.append(flyers[id])

        return ret

    #--------------------------------------------------------------------------- getCandidateMarketplaceItems
    def getCandidateMarketplaceItems(self, orgIDs, maxTime, limit, tiebreaker=[]):

        ret = []

        query = """
        SELECT id, updatedDateTime
        FROM MarketplaceItem
        WHERE organizationID IN (%(orgIDs)s)
          AND updatedDateTime <= %(maxTime)s
          %(tiebreakerWhere)s
        ORDER BY updatedDateTime DESC, id DESC
        LIMIT %(limit)d
        """ % {
            'orgIDs': ','.join(map(str, orgIDs)),
            'maxTime': ('"%s"' % maxTime) if maxTime else 'CURDATE()',
            'tiebreakerWhere': ('AND id NOT IN (%s)' % ','.join(map(str, tiebreaker))) if tiebreaker else '',
            'limit': limit + 1,
        }
        for id, updatedDateTime in sdc.executeQuery(query).fetchall():
            ret.append({
                'group': 'marketplace',
                'id': id,
                'time': mxToUtcDatetime(updatedDateTime)
            })

        return ret

#=============================================================================== Functions

#------------------------------------------------------------------------------- unionQuery
def unionQuery(parts):
    return ' UNION '.join(['(%s)' % s for s in parts])


#------------------------------------------------------------------------------- getDatetime
def getDatetime(s, tz=None):
    if tz is None:
        tz = pytz.utc
    return tz.localize(datetime.datetime.strptime(s, API_DATE_TIME_FORMAT))


#------------------------------------------------------------------------------- getUtcDatetimeOrNow
def getUtcDatetimeOrNow(s=None, nowDelta=None):
    """
    Parse a string into a UTC `datetime` object. If the string is falsey, return UTC now.
    """

    if s:
        return pytz.utc.localize(datetime.datetime.strptime(s, API_DATE_TIME_FORMAT))
    else:
        n = pytz.utc.localize(datetime.datetime.utcnow())
        if nowDelta:
            n += nowDelta
        return n


#------------------------------------------------------------------------------- mxToUtcDatetime
def mxToUtcDatetime(m, tz=None):
    """
    Return an equivalent, UTC-localized `datetime` object from the provided `mx.DateTime` object.
    """

    if tz is None:
        tz = pytz.utc
    return tz.localize(datetime.datetime.utcfromtimestamp(m.gmticks())).astimezone(pytz.utc)


#*******************************************************************************
