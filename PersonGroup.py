# encoding: utf-8
from pt import ptlog
from pt.ableconstants.constants import REACH_ACTIVE_ROLES
from pt.dataobjects.constants import *
from pt.dataobjects.DatabaseDict import DatabaseDict, WavAudio, NotFetched, getDefaultClassData
from pt.datacmp.PersonGroupMemberView import PersonGroupMemberView
from pt.datacmp.PersonGroupUserView import PersonGroupUserView
from pt.datacmp.PermissionChecker import getInstance
from pt.datacmp.QueryCriteriaView import QueryCriteriaView
from pt.dataobjects.dataobjecterr import DatabaseErr, DuplicateEntryErr
from pt.querycmp.querymanager import QueryManager
from pt.datacmp.PersonGroupMember import PersonGroupMember

permissionChecker = getInstance()


class InvalidGroupChoice(DatabaseErr):
    """0497 An invalid choice was given for the Person Group.
       The group choice must be an integer."""


class InvalidPublicGroupChoice(DatabaseErr):
    """0498 An invalid choice was given for the Person Group.
       A public group must have a choice number greater than 99."""


class InvalidPrivateGroupChoice(DatabaseErr):
    """0498 An invalid choice was given for the Person Group.
       A private group must have a choice number less than 100."""


class PersonGroup(DatabaseDict, WavAudio):
    table = 'PersonGroup'
    tableOptions = {'ENGINE': 'InnoDB'}
    fields = [{'Field': "id",
               'Type': IDTYPE,
               'Extra': "AUTO_INCREMENT"},

              {'Field': "ownerPersonID",
               'Type': IDTYPE,
               'Link': "Person"},

              {'Field': "organizationID",
               'Type': IDTYPE,
               'Link': "Organization"},

              {'Field': "name",
               'Type': "VARCHAR(128)"},

              {'Field': "choice",
               'Type': UNSIGNEDBIGINTTYPE},

              {'Field': "public",
               'Type': BOOLEANTYPE,
               'Default': "FALSE"},

              {'Field': 'groupType',
               'Type': "ENUM('PERSON','ADDRESS','QUERY')",
               'Default': 'PERSON'},

              {'Field': 'matchCriteria',
               'Type': "ENUM('AND','OR')",
               'Default': 'AND'},

              {'Field': "createdBy",
               'Type': "ENUM('MESSAGERECEIVER','WEBINTERFACE')",
               'Default': "WEBINTERFACE"},

              {'Field': "deleteRecord",  # used to mark record to be deleted
               'Type': BOOLEANTYPE,
               'Default': "FALSE"},

              {'Field': "recordedName",  # saved as PCM
               'Type': 'MEDIUMBLOB',
               'Null': "YES"},
              {
                  'Field': "reachStatus",
                  'Type': BOOLEANTYPE,
                  'Default': "TRUE"
              }
              ]

    primaryKey = ['id']
    uniqueKeys = []
    indexes = [['ownerPersonID'], ['choice'], ['organizationID', 'public', 'groupType'], ['id', 'groupType']]

    subObjects = ['organization']
    views = ['personGroupMember', 'personGroupUser']

    defaultRecords = []
    defaultClassData = getDefaultClassData(table, fields, primaryKey)

    def __init__(self, verify=None, new=None, noRedirect=None, checkMaster=False, readOnly=None, **fieldDictArgs):
        DatabaseDict.__init__(self, verify=verify, new=new, noRedirect=noRedirect, checkMaster=checkMaster,
                              readOnly=readOnly, **fieldDictArgs)

    def _setupSubObjects(self, key):
        if key == 'organization':
            self.data['organization'] = self._getSubObject('Organization', id=self['organizationID'])

    def _setupViews(self):
        if self.data['personGroupMember'] is NotFetched:
            if self['groupType'] == 'QUERY':
                self.data['personGroupMember'] = QueryCriteriaView(where='personGroupID = %s' % self['id'])
            else:
                self.data['personGroupMember'] = PersonGroupMemberView(where='personGroupID = %s' % self['id'])
        if self.data['personGroupUser'] is NotFetched:
            self.data['personGroupUser'] = PersonGroupUserView(where='personGroupID = %s' % self['id'])

    def delete(self, verify=None):
        # delete any dependent objects
        for view in ['personGroupMember', 'personGroupUser']:
            self[view].delete()
        # delete this group as a member of some other group
        PersonGroupMemberView(where='memberID=%s and memberType="GROUP"', whereValues=[self['id']]).delete()
        # call parent's delete method
        DatabaseDict.delete(self, verify=verify)

    def insert(self, verify=None):
        if not self.data['choice'] or self.data['choice'] is NotFetched:
            # if you have public but no choice, generate a choice
            from pt.datacmp.datautilities import getPersonGroupChoice
            self.data['choice'] = getPersonGroupChoice(personID=self.data['ownerPersonID'],
                                                       organizationID=self.data['organizationID'],
                                                       public=(self.data['public'] == 'TRUE'))
        else:
            try:
                if int(self.data['choice']) >= 100 and self.data['public'] != 'TRUE':
                    raise InvalidPrivateGroupChoice
                elif int(self.data['choice']) < 100 and self.data['public'] == 'TRUE':
                    raise InvalidPublicGroupChoice
            except ValueError:
                raise InvalidGroupChoice

        # make sure that this group doesn't exist already
        from pt.datacmp.PersonGroupView import PersonGroupView
        if self.data['public'] == 'TRUE':
            pgv = PersonGroupView(where='choice=%s AND organizationID=%s AND public="TRUE"' % (
                self.data['choice'], self.data['organizationID']))
        else:
            pgv = PersonGroupView(where='choice=%s AND ownerPersonID=%s AND public="FALSE"' % (
                self.data['choice'], self.data['ownerPersonID']))

        if pgv.getRowCount():
            raise DuplicateEntryErr

        DatabaseDict.insert(self, verify=verify)

    def _getAllowedOrgs(self, groupData):
        if not groupData['ownerPersonID']:
            # there is no owner
            allowed_orgs = [groupData['organizationID']]
        else:
            allowed_orgs = []
            for org_id, role_id in self.executeQuery(
                            'SELECT organizationID, roleID '
                            'FROM Account '
                            'WHERE personID=%s' % groupData['ownerPersonID']).fetchall():
                if org_id not in allowed_orgs \
                        and permissionChecker.checkPermissions(organizationID=org_id,
                                                               roleIDs=[role_id],
                                                               capabilityGroups=['SEND_MESSAGES']):
                    allowed_orgs.append(org_id)
        return allowed_orgs

    def _getSubGroupData(self, parentGroupIDs):
        ptlog.syslog("--------- parentGroupIDs:{}".format(parentGroupIDs))
        sub_groups = {}
        Aaa = self.executeQuery(
                        'SELECT DISTINCT PersonGroup.id, PersonGroup.groupType, PersonGroup.ownerPersonID, '
                        'PersonGroup.organizationID,PersonGroupMember.personGroupID '
                        'FROM PersonGroupMember '
                        'JOIN PersonGroup '
                        'ON PersonGroup.id=PersonGroupMember.memberID '
                        'WHERE personGroupID IN (%s) '
                        'AND memberType="GROUP"' % ','.join(map(str, parentGroupIDs))).fetchall()
        ptlog.syslog("---------------- Aaa:{}".format(Aaa))
        for sub_group_id, sub_group_type, sub_group_owner_id, sub_group_org_id, member_group_id in Aaa:
            ptlog.syslog("==== sub_group_id :{}, sub_group_type :{}, sub_group_owner_id :{}, sub_group_org_id :{}".format(sub_group_id, sub_group_type, sub_group_owner_id, sub_group_org_id))
            if member_group_id == sub_group_id:
                ptlog.syslog("--------------- came here as condition matched --------------")
                continue
            else:
                sub_groups.setdefault(sub_group_id,
                                  {'ownerPersonID': sub_group_owner_id,
                                   'organizationID': sub_group_org_id,
                                   'groupType': sub_group_type,
                                   'members': set()})
        if sub_groups:
            sub_groups.update(self._getSubGroupData(sub_groups.keys()))
        ptlog.syslog("------------------------------>> updated sub_groups:{}".format(sub_groups))
        return sub_groups

    def _getGroupData(self, recursive=True):
        groupData = {self['id']: {'ownerPersonID': self['ownerPersonID'], 'organizationID': self['organizationID'],
                                  'groupType': self['groupType'], 'members': set()}}
        ptlog.syslog("--------------------------- _getGroupData's  groupData :{}".format(groupData))
        if recursive:
            groupData.update(self._getSubGroupData([self['id']]))
        query_group_ids = []
        non_query_group_ids = []
        for group_id, group_dict in groupData.items():
            if group_dict['groupType'] == 'QUERY':
                query_group_ids.append(group_id)
            else:
                non_query_group_ids.append(group_id)
        return groupData, non_query_group_ids, query_group_ids

    def _filterAccounts(self, groupData, filterWhere=None):
        """_filterAccounts - recipientIDs, filterWhere=None"""
        recipient_ids = set()
        for group_id, group_dict in groupData.items():
            if group_dict['groupType'] == 'PERSON' and group_dict['members']:
                allowed_org_ids = self._getAllowedOrgs(group_dict)
                # allowedOrgIDs is the list of organization the group creator has sender rights at
                where = ['Account.personID IN (%s)' % ','.join(map(str, group_dict['members']))]
                if allowed_org_ids:
                    tables = '(Account JOIN Organization ON Account.organizationID=Organization.id) ' \
                             'JOIN Organization AS ParentOrg ' \
                             'ON Organization.lft BETWEEN ParentOrg.lft AND ParentOrg.rgt'
                    where.append('ParentOrg.id IN (%s)' % ','.join(map(str, allowed_org_ids)))
                else:
                    tables = 'Account'

                temp_recipients = set()
                allowed_recipients = set()
                # find accounts that exist temp or not
                for personID, temp in self.executeQuery(
                                'SELECT personID, temp '
                                'FROM %s '
                                'WHERE %s' % (tables, ' AND '.join(where))).fetchall():
                    if temp == 'TRUE':
                        temp_recipients.add(personID)
                    else:
                        allowed_recipients.add(personID)
                # invalid accounts are people without any account within the allowed orgs of the creator of the group
                # preservice temp accounts within the group, but don't include them as recipients
                invalid_members = group_dict['members'] - (allowed_recipients | temp_recipients)
                group_dict['members'] = allowed_recipients

                # remove any invalid recipients - people with no accounts within the allowed orgs
                if invalid_members:
                    self.executeQuery(
                        'DELETE FROM PersonGroupMember '
                        'WHERE memberID IN (%s) '
                        'AND personGroupID = %s '
                        'AND memberType="PERSON"' % (','.join(map(str, invalid_members)), group_id))

                if filterWhere and group_dict['members']:
                    # filter out any existing recipients - usually used in passcode letters to filter people
                    # that shouldn't receive a letter again.
                    where = ['Account.personID IN (%s)' % ','.join(map(str, group_dict['members']))]
                    if filterWhere:
                        if type(filterWhere) is list:
                            where.extend(filterWhere)
                        else:
                            where.append(filterWhere)
                    filtered_members = set([personID for personID, in self.executeQuery(
                        'SELECT personID '
                        'FROM Account '
                        'JOIN Person '
                        'ON Account.personID=Person.id '
                        'WHERE %s' % ' AND '.join(where)).fetchall()])
                    group_dict['members'] = filtered_members

            recipient_ids |= group_dict['members']

        return recipient_ids

    def _hasGroupMember(self, groupData, groupIDs, filterWhere=None):
        # try and find the first 10 members of the groups and see if one of them has a valid account,
        # short circuit early if we find one valid account
        for group_id, member_id in self.executeQuery(
                        'SELECT personGroupID, memberID '
                        'FROM PersonGroupMember '
                        'WHERE personGroupID IN (%s) '
                        'AND memberType!="GROUP" LIMIT 10' % ','.join(map(str, groupIDs))).fetchall():
            group_dict = groupData[group_id]
            allowed_org_ids = self._getAllowedOrgs(group_dict)
            # allowedOrgIDs is the list of organization the group creator has sender rights at
            where = ['Account.personID = %s' % member_id, 'Account.temp="FALSE"']
            if filterWhere:
                if type(filterWhere) is list:
                    where.extend(filterWhere)
                else:
                    where.append(filterWhere)
            if allowed_org_ids:
                tables = '(Account JOIN Organization ' \
                         'ON Account.organizationID=Organization.id) ' \
                         'JOIN Organization AS ParentOrg ' \
                         'ON Organization.lft BETWEEN ParentOrg.lft AND ParentOrg.rgt'
                where.append('ParentOrg.id IN (%s)' % ','.join(map(str, allowed_org_ids)))
            else:
                tables = 'Account'

            if self.executeQuery('SELECT personID FROM %s WHERE %s' % (tables, ' AND '.join(where))).fetchone():
                return True
        else:
            # if we couldn't short circuit early, run the full filter, cleaning up invalid members
            # to determine if there truly are no members of this group
            return bool(self._getGroupMembers(groupData, groupIDs, filterWhere))

    def _getGroupMembers(self, groupData, groupIDs, filterWhere=None):
        for group_id, member_id in self.executeQuery(
                        'SELECT personGroupID, memberID '
                        'FROM PersonGroupMember '
                        'WHERE personGroupID IN (%s) '
                        'AND memberType!="GROUP"' % ','.join([str(group_id) for group_id in groupIDs])).fetchall():
            groupData[group_id]['members'].add(member_id)
        return self._filterAccounts(groupData, filterWhere=filterWhere)

    def getDisplayRecipients(self, recursive=True, filterWhere=None):
        if self['groupType'] == 'QUERY':
            return 'query'
        else:
            group_data, non_query_group_i_ds, query_group_ids = self._getGroupData(recursive=recursive)
            recipient_ids = self._getGroupMembers(group_data,
                                                  non_query_group_i_ds,
                                                  filterWhere)  # gets my group members, remove invalid members
            num_recipients = len(recipient_ids)

            if query_group_ids:
                if num_recipients:
                    return '%s+' % num_recipients
                else:
                    return 'query'
            else:
                return str(num_recipients)

    def getRecipientIDs(self, recursive=True, filterWhere=None, senderPersonID=None):
        if not senderPersonID:
            senderPersonID = self['ownerPersonID']
        if self['groupType'] == 'QUERY':
            return self._getQueryRecipientIDs(senderPersonID=senderPersonID)
        else:
            group_data, non_query_group_ids, query_group_ids = self._getGroupData(recursive=recursive)
            recipient_ids = self._getGroupMembers(group_data,
                                                  non_query_group_ids,
                                                  filterWhere)  # gets my group members, remove invalid members
            for query_group_id in query_group_ids:
                recipient_ids |= PersonGroup(verify=True, id=query_group_id) \
                    ._getQueryRecipientIDs(senderPersonID=senderPersonID)
            return recipient_ids

    def hasRecipients(self, recursive=True, filterWhere=None, senderPersonID=None):
        if not senderPersonID:
            senderPersonID = self['ownerPersonID']
        if self['groupType'] == 'QUERY':
            return bool(self._getQueryRecipientIDs(senderPersonID=senderPersonID))
        else:
            group_data, non_query_group_ids, query_group_ids = self._getGroupData(recursive=recursive)
            if self._hasGroupMember(group_data, non_query_group_ids, filterWhere):
                return True
            for query_group_id in query_group_ids:
                if PersonGroup(id=query_group_id)._getQueryRecipientIDs(senderPersonID=senderPersonID):
                    return True
            return False

    def _getQueryRecipientIDs(self, senderPersonID):
        criteria_list = []
        org_ids = []
        org_operation = None
        role_ids = []
        role_operation = None
        for query_criteria in self['personGroupMember'].generateall():
            if query_criteria['fieldName'] == 'organizationID':
                org_operation = query_criteria['operation']
                org_ids = query_criteria['value']
            elif query_criteria['fieldName'] == 'roleID':
                role_operation = query_criteria['operation']
                role_ids = query_criteria['value']
            else:
                criteria_list.append((query_criteria['fieldName'],
                                      query_criteria['operation'],
                                      query_criteria['value']))

        if type(org_ids) is not list:
            org_ids = [org_ids]
        if type(role_ids) is not list:
            role_ids = [role_ids]

        if self['ownerPersonID']:
            # if there is an owner, permission for the queries are based on the owner's permissions
            person_id = self['ownerPersonID']
        else:
            # use the sender's permissions if there is no owner
            person_id = senderPersonID

        return QueryManager(personID=person_id,
                            match=self['matchCriteria'],
                            queryCriteriaList=criteria_list,
                            organizationIDs=org_ids,
                            organizationOperation=org_operation,
                            roleIDs=role_ids,
                            roleOperation=role_operation).execute()

    def getNumRecipients(self, recursive=True):
        return len(self.getRecipientIDs(recursive=recursive))

    def getRecipients(self, recursive=True, filterWhere=None, senderPersonID=None):
        if self['groupType'] in ['PERSON', 'QUERY']:
            from pt.datacmp.PersonView import PersonView
            person_ids = ','.join(map(str, self.getRecipientIDs(recursive=recursive,
                                                                filterWhere=filterWhere,
                                                                senderPersonID=senderPersonID)))
            if person_ids:
                return PersonView(where='id IN (%s)' % person_ids).fetchall()
            return []
        elif self['groupType'] == 'ADDRESS':
            from pt.datacmp.DeliveryAddress import DeliveryAddress
            # TODO this appears to use a list of person ids to look up a bunch of delivery addresses.
            #      i don't think this is returning what the caller expects.
            return map(lambda addressID: DeliveryAddress(id=addressID), self.getRecipientIDs())

    def getChildGroups(self):
        retval = set([])
        for child_group_member in PersonGroupMemberView(where='personGroupID=%s and memberType="GROUP"',
                                                        whereValues=self['id']).fetchall():
            retval.add(child_group_member['member'])
            retval |= set(child_group_member['member'].getChildGroups())
        return list(retval)

    def getChildGroupIDs(self):
        return [group['id'] for group in self.getChildGroups()]

    def getParentGroups(self):
        ptlog.syslog("----------------- getParentGroups()")
        ptlog.syslog("------------ self['id']:{}".format(self['id']))
        ptlog.syslog("------------ type of self['id']:{}".format(type(self['id'])))
        retval = set([])
        #bbb = PersonGroupMemberView(where='memberID=%s and memberType="GROUP"', whereValues=int(self['id'])).fetchall()
        bbb = PersonGroupMemberView(where='personGroupID=%s and memberType="GROUP"', whereValues=int(self['id'])).fetchall()
        #bbb = self.executeQuery('SELECT  FROM PersonGroupMember WHERE memberID=%s and memberType="GROUP"' % self['id']).fetchall()
        #bbb =

        ptlog.syslog("====================== bbb :{}".format(bbb))
        if bbb:
            for parent_group_member in bbb:
                retval.add(parent_group_member['group'])
                retval |= set(parent_group_member['group'].getParentGroups())
            ptlog.syslog("====================== retval:{}".format(list(retval)))
            return list(retval)

    def groupQueryRecipientIDs(self, senderPersonID, orgId):
        """
            To get Query type group recipients for Reach api
        """
        criteria_list = []
        org_ids = []
        org_operation = None
        role_ids = []
        role_operation = None

        for query_criteria in self['personGroupMember'].generateall():
            if query_criteria['fieldName'] == 'organizationID':
                org_operation = query_criteria['operation']
                org_ids = query_criteria['value']
            elif query_criteria['fieldName'] == 'roleID':
                role_operation = query_criteria['operation']
                role_ids = query_criteria['value']
            else:
                criteria_list.append((query_criteria['fieldName'],
                                      query_criteria['operation'],
                                      query_criteria['value']))

        if type(org_ids) is not list:
            org_ids = [org_ids]
        if type(role_ids) is not list:
            role_ids = [role_ids]

        if str(orgId) in org_ids:
            org_ids = [orgId]
        else:
            return []

        role_ids = set(role_ids).intersection(set(map(str, REACH_ACTIVE_ROLES)))

        if self['ownerPersonID']:
            # if there is an owner, permission for the queries are based on the owner's permissions
            person_id = self['ownerPersonID']
        else:
            # use the sender's permissions if there is no owner
            person_id = senderPersonID

        return QueryManager(personID=person_id,
                            match=self['matchCriteria'],
                            queryCriteriaList=criteria_list,
                            organizationIDs=org_ids,
                            organizationOperation=org_operation,
                            roleIDs=role_ids,
                            roleOperation=role_operation).execute()

    def getRecipientPersonIDs(self, recursive=True, filterWhere=None, senderPersonID=None, orgId=None):
        if self['groupType'] == 'QUERY':
            return self.groupQueryRecipientIDs(senderPersonID=senderPersonID, orgId=orgId)
        elif self['groupType'] == 'PERSON':
            group_data, non_query_group_ids, query_group_ids = self._getGroupData(recursive=recursive)
            recipient_ids = self._getGroupMembers(group_data,
                                                  non_query_group_ids,
                                                  filterWhere)
            for each in query_group_ids:
                group = PersonGroup(verify=True, id=int(each))
                recips = group.groupQueryRecipientIDs(senderPersonID=senderPersonID, orgId=orgId)
                if recips:
                    recipient_ids = list(recipient_ids)
                    recipient_ids.extend(group.groupQueryRecipientIDs(senderPersonID=senderPersonID, orgId=orgId))
            return recipient_ids
        elif self['groupType'] == 'GROUP':
            childGroupsIds = self.getChildGroupIDs()
            recipients = []
            for eachgrp in childGroupsIds:
                childPersonGroup = PersonGroup(verify=True, id=int(eachgrp))
                getrecipientIds = childPersonGroup.getRecipientPersonIDs()
                recipients.extend(getrecipientIds)
            return recipients

