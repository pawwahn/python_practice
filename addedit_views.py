import copy
from ftplib import FTP, error_perm
from os.path import split

from django import forms
from operator import itemgetter

from pt.datacmp.OrganizationTypeView import OrganizationTypeView
from pt.datacmp.OrganizationType import cmpOrganizationType
from pt.ableconstants.constants import STUDENT, PARENT, STAFF, TEACHER
from pt.datacmp.AccountView import AccountView
from pt.datacmp.Organization import Organization
from pt.datacmp.PersonGroup import PersonGroup
from pt.datacmp.PersonGroupMemberView import PersonGroupMemberView
from pt.datacmp.PersonGroupUserView import PersonGroupUserView
from pt.datacmp.PersonGroupView import PersonGroupView
from pt.datacmp.PersonView import PersonView
from pt.datacmp.QueryCriteria import QueryCriteria
from pt.datacmp.QueryCriteriaView import QueryCriteriaView
from pt.datacmp.QueryFieldView import QueryFieldView
from pt.datacmp.Role import Role
from pt.datacmp.RoleView import RoleView
from pt.datacmp.Section import Section
from pt.datacmp.SectionView import SectionView
from pt.datacmp.datautilities import getTermsForAllTracks, getGroupMemberCount, getRandomPublicGroupChoice, getPrivateGroupChoice
from pt.django.main import PLView
from pt.querycmp.querycriteria import operationList, operationDict, fieldDefinitions, fieldDescriptions, fieldMcsExclusions
from pt.querycmp.querymanager import QueryManager
from pt import ptlog

class MessagesGroupsAddEditBaseView(PLView):
    def defaultDict(self):
        return {'GROUPS':set(), 'ROLES':set(), 'INDIVIDUALS':set(), 'CLASSES':set(), 'PREVIEW':set()}

    def selectGetMyOrgs(self):
        orgIDs = []
        senderOrgIDs = self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER', 'SEND_TO_CLASSES'])
        for orgID in senderOrgIDs:
            org = self.get_org(orgID)
            parentIDs = org.getParentIDs()
            # only get org where their parent orgs are not in the senderOrgIDs
            tempList = parentIDs + senderOrgIDs
            if len(set(tempList)) == len(tempList):
                orgIDs.append(orgID)
        return self.get_orgs(orgIDs)

    def getSubOrgsByRole(self, roleID, orgID):
        retval = []
        # get count of students at each subOrg
        # for each org in subOrgs:
          # if org in count, display select
          # if role exists in suborgs display select all

        org = self.get_org(orgID)
        subOrgIDs = ','.join(map(str, org['childrenIDs']))
        if subOrgIDs:
            subOrgCount = {organizationID:count for organizationID, count in org.executeQuery('SELECT organizationID, COUNT(*) FROM Account WHERE roleID=%s AND organizationID IN (%s) AND temp="FALSE" GROUP BY organizationID' % (roleID, subOrgIDs)).fetchall()}
        else:
            subOrgCount = {}

        for subOrg in org.getChildren(wholeTree=False):
            subOrgDict = {'id':subOrg['id'], 'name':subOrg['name'], 'roleInOrg':subOrgCount.has_key(subOrg['id']), 'roleInSubOrgs':False}
            grandChildrenIDs = ','.join(map(str, subOrg.getChildrenIDs(wholeTree=True)))
            if grandChildrenIDs:
                subOrgDict['roleInSubOrgs'] = bool(AccountView(where='roleID=%s AND organizationID IN (%s) AND temp="FALSE"' % (roleID, grandChildrenIDs)).getRowCount())
            if subOrgDict['roleInOrg'] or subOrgDict['roleInSubOrgs']:
                retval.append(subOrgDict)
        return retval

    def listClearList(self, type):
        if type == 'members':
            self.set_temp('memberDict', self.defaultDict())
        else:
            self.set_temp('userDict', self.defaultDict())

    def getClasses(self, orgID=None, teacherID=None):
        if orgID and teacherID:
            return [section for section in self.get_classes(classPersonID=teacherID, personID=self.get_my_id(), orgIDs=[orgID], teacherClass=True) if str(section['organizationID']) == orgID]
        else:
            return self.get_classes(classPersonID=self.get_my_id(), teacherClass=True)

    def getClassMembers(self, uniqueID, memberType):
        section = SectionView(where="uniqueID=%s" % uniqueID).fetchone()
        members = section.getMembers(memberType)
        return [{'memberID':member['id'], 'name':member.getName(lastFirst=True)} for member in members]

    def listClearPreview(self):
        memberDict = self.get_temp('memberDict')
        memberDict['PREVIEW'] = set([])
        self.set_temp('memberDict', memberDict)

    def getOperations(self, queryField=None):
        allowedOperations = []
        if queryField:
            for groupDict in [dict(groupList) for groupName, groupList in fieldDefinitions]:
                if groupDict.has_key(queryField):
                    allowedOperations = groupDict[queryField].allowedOperations
        if not allowedOperations:
            allowedOperations = operationList
        return [(opKey, operationDict[opKey]['name']) for opKey in allowedOperations]

    def getOrganizationValueOptions(self):
        orgList = [(str(org['id']), org['name']) for org in self.get_orgs(self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER', 'SEND_TO_STUDENTS_IN_MY_CLASSES', 'SEND_TO_PARENTS_IN_MY_CLASSES']), forDisplay=True)]
        return sorted(orgList, key=itemgetter(1))

    def getOrganizationValues(self, orgValue=None):
        names = []
        multiOptions = []
        for orgID, orgName in self.getOrganizationValueOptions():
            # handle school names with single quotes and ampersands in them that will mess up our javascript
            orgName = orgName.replace("'", '&#39;')
            displayName = orgName.replace('&nbsp;', '')
            displayName = displayName.replace(' & ', ' &amp; ')
            displayName = displayName.replace(' < ', ' &lt; ')
            displayName = displayName.replace(' > ', ' &gt; ')
            if orgValue:
                if orgID in orgValue:
                    selected = True
                    names.append(displayName)
                else:
                    selected = False
            else:
                selected = False
            multiOptions.append({'name':orgName, 'value':orgID, 'selected':selected, 'displayName':displayName})
        multiOptions = sorted(multiOptions, key=itemgetter('name'))
        names.sort()
        allSelected = orgValue and multiOptions and len(orgValue) == len(multiOptions)
        return self.multiselectbox(fieldName='organizationValue', divID='organizationValues', names=','.join(names), selectOptions=multiOptions, allSelected=allSelected)

    def getRoleValueOptions(self):
        return [(str(optionValue), optionName) for optionValue, optionName in self.get_advanced_search_roles()]

    def getRoleValues(self, roleValue=None):
        names = []
        multiOptions = []
        for roleID, roleName in self.getRoleValueOptions():
            if roleValue:
                if roleID in roleValue:
                    selected = True
                    names.append(roleName)
                else:
                    selected = False
            else:
                selected = False
            multiOptions.append({'name':roleName, 'value':roleID, 'selected':selected, 'displayName':roleName})
        allSelected = roleValue and multiOptions and len(roleValue) == len(multiOptions)
        return self.multiselectbox(fieldName='roleValue', divID='roleValues', names=','.join(names), selectOptions=multiOptions, allSelected=allSelected)

    def getMatchCriteria(self, groupID):
        if groupID:
            matchCriteria = PersonGroup(verify=True, id=groupID)['matchCriteria']
            if matchCriteria == '':
                return 'AND'
            return matchCriteria

    def list_str(self, type, expand=True):
        data = {'expandIndividuals':expand}
        if type == 'users':
            data['userDict'] = self.get_temp('userDict')
            data['individuals'] = self.listGetIndividuals(type)
            data['roles'] = self.listGetOrgRoles('users')
            return self.render_to_string('main/messages/groups/addedit/listuserlist.html', data)
        else:
            self.listCopyPreview()
            data['memberDict'] = self.get_temp('memberDict')
            data['groups'] = self.listGetGroups()
            data['individuals'] = self.listGetIndividuals(type)
            data['classes'] = self.listGetClasses()
            data['roles'] = self.listGetOrgRoles('members')
            return self.render_to_string('main/messages/groups/addedit/listmemberlist.html', data)

    def listGetOrgRoles(self, type):
        retval = []
        if type == 'users':
            dictString = 'userDict'
        else:
            dictString = 'memberDict'
        personDict = self.get_temp(dictString)
        if personDict:
            roles = list(personDict['ROLES'])
            roles.sort()
            retval = [{'roleID':roleID, 'orgID':orgID, 'name':roleName, 'orgName':orgName, 'suborgs':subOrgs} for roleName, orgName, roleID, orgID, subOrgs in roles]
        return retval

    def listGetClasses(self):
        retval = []
        memberDict = self.get_temp('memberDict')
        if memberDict:
            sections = list(memberDict['CLASSES'])
            sections.sort()
            retval = [{'name':sectionName, 'sectionID':sectionID, 'orgID':orgID, 'memberCount':memberCount, 'memberType':memberType, 'uniqueID':uniqueID} for period, sectionName, memberCount, sectionID, orgID, memberType, uniqueID in sections]
        return retval

    def listGetIndividuals(self, type='members'):
        personDict = self.get_temp('userDict' if type == 'users' else 'memberDict')
        retval = []
        if personDict and personDict['INDIVIDUALS']:
            recipients = list(personDict['INDIVIDUALS'])
            recipients.sort()
            retval = [{'personID':recipientID, 'name':recipientName} for recipientName, recipientID in recipients]
        return retval

    def listCopyPreview(self):
        memberDict = self.get_temp('memberDict') or self.defaultDict()
        if memberDict['PREVIEW']:
            memberDict['INDIVIDUALS'] = copy.deepcopy(memberDict['PREVIEW'])
            memberDict['PREVIEW'] = set([])
        self.set_temp('memberDict', memberDict)

    def listGetGroups(self):
        retval = []
        memberDict = self.get_temp('memberDict')
        if memberDict:
            groups = list(memberDict['GROUPS'])
            groupIDs = [groupID for orgName, groupName, groupID in groups]
            groupMemberCountDict = getGroupMemberCount(groupIDs=groupIDs,recursive=True)
            groups.sort()
            retval = [{'orgName':orgName, 'name':groupName, 'groupID':groupID, 'count':groupMemberCountDict.get(int(groupID)) or 0} for orgName, groupName, groupID in groups]
        return retval

    def _form(self, data=None, initial=None, advanced_only=False, include_advanced=True):
        if not initial:
            initial = {}
        if not initial.get('matchCriteria'):
            initial['matchCriteria'] = 'AND'
        form = forms.Form(data, initial=initial)
        if not advanced_only:
            form.fields['groupID'] = forms.IntegerField(required=False)
            form.fields['orgID'] = forms.ChoiceField(choices=[(org['id'], org['name']) for org in self.get_orgs(self.get_org_ids_by_capability(['VIEW_GROUPS', 'EDIT_PUBLIC_GROUPS', 'ADD_REMOVE_PUBLIC_GROUPS']), forDisplay=True, indentSpaces=2)])
            form.fields['query'] = forms.IntegerField(required=False)
            form.fields['groupName'] = forms.CharField(label='Group name')
            form.fields['groupName'].widget.attrs['size'] = 35
            form.fields['choice'] = forms.IntegerField(label='Group ID', min_value=1, max_value=(not self.check_permissions(['ADD_REMOVE_PUBLIC_GROUPS']) and 100) or 999999999)
            form.fields['choice'].widget.attrs['style'] = 'width:70px'
            group_types = [('PERSON', 'From a list')]
            if self.check_permissions(['SEND_UPLOADED_IDS']):
                group_types.append(('FILE', 'From a file'))
            group_types.append(('QUERY', 'Advanced search'))
            form.fields['groupType'] = forms.ChoiceField(required=False, choices=group_types)
            form.fields['groupType'].widget.attrs['onchange'] = 'javascript:groupTypeChanged()'
            for f in ('searchString', 'usersSearchString'):
                form.fields[f] = forms.CharField(required=False)
                form.fields[f].widget.attrs.update({'size': 12})
        if include_advanced:
            form.fields['organizationOperation'] = forms.ChoiceField(required=False, choices=self.getOperations(queryField='organizationID'))
            form.fields['organizationValue'] = forms.MultipleChoiceField(label=self.context['org_label'], choices=self.getOrganizationValueOptions(), required=False)
            form.fields['roleOperation'] = forms.ChoiceField(required=False, choices=self.getOperations(queryField='organizationID'))
            form.fields['roleValue'] = forms.MultipleChoiceField(label='Account', choices=self.getRoleValueOptions(), required=False)
            form.fields['matchCriteria'] = forms.ChoiceField(label='Find accounts that', widget=forms.RadioSelect, required=False, choices=(('AND', 'Match all'), ('OR', 'Match any')))
        return form


class MessagesGroupsAddEditView(MessagesGroupsAddEditBaseView):
    def _get(self, request):
        return self._render()

    def _post(self, request):
        form = self._form(request.POST)
        if self.form_is_valid(form):
            errors = []
            errorFields = []
            self.checkGroup(request, errors, errorFields)
            externalIDs = None
            if request.POST.has_key('LOAD'):
                if request.FILES.get('localFile'):
                    externalIDs = []
                    [externalIDs.extend(filter(bool, externalID.strip().split('\r'))) for externalID in request.FILES['localFile'].readlines()]
                    externalIDs = set(externalIDs) - set(['']) # remove any blank lines from the file
                else:
                    errors.append('<b>Import File:</b> Import file is required')
                    errorFields.append('id_localFile')

            if request.POST.get('groupType') == 'QUERY':
                # stick the organizationID and roleID criteria at the front of the list
                orgValue = request.POST.getlist('organizationValue')
                roleValue = request.POST.getlist('roleValue')
                if not orgValue:
                    errors.append('<b>{}:</b> Please select at least one {}'.format(self.get_org_label(), self.get_org_label()))
                if not roleValue:
                    errors.append('<b>Account:</b> Please select at least one account type')

            if errors or errorFields:
                self.listClearPreview()
                self.context['message_errors'] = errors
                self.context['message_error_fields'] = errorFields
                return self._render(form)
            return self.save(form, request, externalIDs)
        else:
            return self._render(form)

    def _render(self, form=None):
        groupID = self.get_param('groupID')
        ptlog.syslog("--------------1 groupID:{}".format(groupID))
        data = {
            'groupID': groupID,
            'canCreatePublic': self.check_permissions(['ADD_REMOVE_PUBLIC_GROUPS']),
            'canCreatePrivate': self.canCreatePrivateGroup(),
            'advancedSelection': self.check_permissions(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER']),
            'is_admin': self.is_admin(),
            'has_classes': self.has_classes(classPersonID=self.get_my_id(), personID=self.get_my_id()),
            'my_orgs': self.selectGetMyOrgs(),
        }

        self.delete_temp('invalidGroupIDs')
        just_loaded_file = self.request.GET.has_key('LOAD') or self.request.POST.has_key('LOAD')
        if groupID:
            ptlog.syslog("--------------2 groupID:{}".format(groupID))
            personGroup = PersonGroup(id=groupID)
            ptlog.syslog("++++++++++ personGroup['id']: {}".format(personGroup['id']))
            ccc = personGroup.getParentGroups()
            ptlog.syslog("++++++++++ ccc['id'] :{}".format(ccc['id']))
            if int(personGroup['id']) != int(ccc['id']):
                ptlog.syslog("---------------- ccc:{}".format(ccc))
                self.set_temp('invalidGroupIDs', [groupID] + [group['id'] for group in ccc])
                data['orgID'] = str(personGroup['organizationID'])
                data['groupName'] = personGroup['name']
                data['choice'] = personGroup['choice']
                data['groupType'] = personGroup['groupType']
                data['matchCriteria'] = personGroup['matchCriteria']

            if just_loaded_file:
                # get individuals out of the list that were just loaded
                memberDict = self.get_temp('memberDict') or self.defaultDict()
                userDict = self.get_temp('userDict') or self.defaultDict()
            else:
                groupQuery = 'SELECT Organization.name, PersonGroup.name, PersonGroup.id FROM (PersonGroupMember JOIN PersonGroup ON PersonGroupMember.memberID=PersonGroup.id) JOIN Organization ON PersonGroup.organizationID=Organization.id WHERE PersonGroupMember.personGroupID=%s AND PersonGroupMember.memberType="GROUP"' % groupID
                memberDict = {'ROLES':set([]),
                              'CLASSES':set([]),
                              'INDIVIDUALS':set([]),
                              'GROUPS':set([(orgName, groupName, str(tmpGroupID)) for orgName, groupName, tmpGroupID in self.execute_query(groupQuery).fetchall()]),
                              'PREVIEW':set([])}
                userDict = {'ROLES':set([]),
                            'INDIVIDUALS':set([(personGroupUser['user'].getName(lastFirst=True), str(personGroupUser['personID'])) for personGroupUser in PersonGroupUserView(where='personGroupID = %s',whereValues=[groupID]).generateall() if personGroupUser['user']])}

                recipientIDs = list(personGroup.getRecipientIDs(recursive=False))
                if recipientIDs:
                    memberDict['INDIVIDUALS'] = []
                    memberQuery = 'SELECT id, lastName, firstName FROM Person WHERE id IN (%s)'
                    while recipientIDs:
                        tempRecipientIDs = recipientIDs[:1000]
                        recipientIDs = recipientIDs[1000:]
                        memberDict['INDIVIDUALS'].extend([('%s, %s' % (lastName,firstName), str(personID)) for personID, lastName, firstName in self.execute_query(memberQuery % ','.join(map(str, tempRecipientIDs))).fetchall()])
                    memberDict['INDIVIDUALS'] = set(memberDict['INDIVIDUALS'])

            self.set_temp('memberDict', memberDict)
            self.set_temp('userDict', userDict)

        elif not just_loaded_file and not self.request.method == 'POST':
            self.listClearList('users')
            self.listClearList('members')

        data['memberDict'] = self.get_temp('memberDict')
        data['userDict'] = self.get_temp('userDict')
        data['member_list'] = self.list_str('members', expand=False)
        data['user_list'] = self.list_str('users', expand=False)

        if data.get('userDict'):
            data['has_users'] = len(data['userDict']['INDIVIDUALS']) != 0 or len(data['userDict']['ROLES']) != 0

        data['form'] = form or self._form(initial=data)
        if self.request.POST.get('groupType'):
            data['groupType'] = self.request.POST.get('groupType')

        return self.render_to_response('main/messages/groups/addedit/index.html', data)

    def save(self, form, request, externalIDs):
        if request.POST.has_key('LOAD'):
            organizationIDs = map(str, self.get_org_ids_by_capability(['SEND_TO_OTHER', 'SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_CLASSES']))

            if request.POST['memberType'] == 'PARENTS':
                query = 'SELECT DISTINCT Account.externalID, Parent.id, CONCAT(Parent.lastName, ", ", Parent.firstName) FROM Account, Role, Person AS Student, Relationship, Person as Parent WHERE Account.roleID=Role.id and Role.roleType = "STUDENT" AND Account.organizationID in (%s) AND Account.personID = Student.id AND Student.id = Relationship.personID2 AND Relationship.personID1 = Parent.id' % ','.join(organizationIDs)
            elif request.POST['memberType'] == 'STAFF':
                query = 'SELECT DISTINCT Account.externalID, Account.personID, CONCAT(Person.lastName, ", ", Person.firstName) FROM Account, Role, Person WHERE Account.personID = Person.id AND Account.roleID=Role.id AND Role.roleType IN ("ADMIN","STAFF","TEACHER") AND Account.organizationID in (%s)' % ','.join(organizationIDs)
            elif request.POST['memberType'] == 'OTHER':
                query = 'SELECT DISTINCT Account.externalID, Account.personID, CONCAT(Person.lastName, ", ", Person.firstName) FROM Account, Role, Person WHERE Account.personID = Person.id AND Account.roleID=Role.id AND Role.roleType = "OTHER" AND Account.organizationID in (%s)' % ','.join(organizationIDs)
            else:
                query = 'SELECT DISTINCT Account.externalID, Account.personID, CONCAT(Person.lastName, ", ", Person.firstName) FROM Account, Role, Person WHERE Account.personID = Person.id AND Account.roleID=Role.id AND Role.roleType = "STUDENT" AND Account.organizationID in (%s)' % ','.join(organizationIDs)

            # get all the students in the org and filter in python rather than in the SQL statement
            # the SQL could have thousands of externalIDs and could get really slow
            recipients = filter(lambda recipient: recipient[0] in externalIDs, self.execute_query(query).fetchall())

            unusedIDs = list(externalIDs - set([recipient[0] for recipient in recipients]))
            recipientIDs = {(name, str(personID)) for externalID, personID, name in recipients}
            self.listAddPeople(recipientIDs=recipientIDs, type='members')
            msg_success = len(recipientIDs) and ('%s %s%s added.' % (len(recipientIDs), {'PARENTS':'parent', 'STAFF': 'staff member'}.get(request.POST['memberType'], 'student'), (len(recipientIDs) > 1 and 's were') or ' was'))
# <tal:savedGroup condition="not:request/addedMembers | nothing" replace="string:The group has been saved."/>
            if unusedIDs:
                plural = len(unusedIDs) > 1
                textFormat = '<b>%s</b> %s'
                text = textFormat % ('Missing Recipients:', 'The following %s%s not found:<br/>' % ((request.POST.get('recipientType') == 'PARENTS' and 'parent') or (request.POST.get('recipientType') == 'STAFF' and 'staff member') or (request.POST.get('recipientType') == 'OTHER' and 'community member') or 'student', (plural and 's were') or ' was'))
                text += ', '.join(unusedIDs)
                if msg_success:
                    text = '{}<br>{}'.format(msg_success, text)
                self.set_msg_warning(text)
                self.log('setting warning: {}'.format(text))
            elif msg_success:
                self.set_msg_success(msg_success)
            return self._render(form)
        else:
            if int(request.POST.get('choice')) >= 100:
                public = 'TRUE'
            else:
                public = 'FALSE'

            criteria = []
            if request.POST.get('groupType') == 'QUERY':
                i = 1
                while True:
                    queryField = request.POST.get('queryField_%s' % i)
                    queryOperation = request.POST.get('queryOperation_%s' % i)
                    #PEB-3382 Query Group Settings is got fixed
                    if queryOperation in ['in', '!in']:
                        query_value_keys = [k for k in dict(request.POST).keys() if k.startswith('queryValue_')]
                        queryValues = []
                        for query_key in query_value_keys:
                            queryValues.append(request.POST.get(query_key))
                        queryValue = ','.join(queryValues)
                    else:
                        queryValue = request.POST.get('queryValue_%s' % i)

                    if queryField and queryOperation and queryValue:
                        criteria.append((queryField, queryOperation, queryValue))
                        i += 1
                    else:
                        break
                # stick the organizationID and roleID criteria at the front of the list
                orgOperation = request.POST.get('organizationOperation')
                orgValue = request.POST.getlist('organizationValue')
                criteria = [('organizationID', orgOperation, orgValue)] + criteria

                roleOperation = request.POST.get('roleOperation')
                roleValue = request.POST.getlist('roleValue')
                criteria = [('roleID', roleOperation, roleValue)] + criteria
                groupType = 'QUERY'
            else:
                groupType = 'PERSON'

            if request.POST.get('groupID'):
                personGroup = PersonGroup(verify=True,id=request.POST['groupID'])
                if groupType != personGroup['groupType']:
                    personGroup['personGroupMember'].delete()
                    personGroup.set('groupType', groupType)
                personGroup.set('organizationID', request.POST.get('orgID'))
                personGroup.set('name',request.POST.get('groupName'))
                personGroup.set('choice',request.POST.get('choice'))
                personGroup.set('public',public)
                personGroup.set('matchCriteria',request.POST['matchCriteria'])
                personGroup.store()
            else:
                personGroup = PersonGroup(new=True,
                                          ownerPersonID=self.get_my_id(),
                                          organizationID=request.POST.get('orgID'),
                                          name=request.POST.get('groupName'),
                                          choice=request.POST.get('choice'),
                                          public=public,
                                          groupType=groupType,
                                          matchCriteria=request.POST['matchCriteria'])
                personGroup.insert()

            if request.POST.get('groupType') == 'QUERY':
                personGroupMembers = personGroup['personGroupMember'].fetchall()

                # overwrite query criteria
                while criteria and personGroupMembers:
                    queryField, queryOperation, queryValue=criteria.pop(0)
                    if queryOperation in ['in', '!in'] and isinstance(queryValue, basestring):
                        queryValue = queryValue.split(',')
                    member = personGroupMembers.pop(0)
                    member.set('fieldName',queryField)
                    member.set('operation',queryOperation)
                    member.set('value',queryValue)
                    member.store()

                # delete any old query criteria that are left
                for member in personGroupMembers:
                    member.delete()

                # insert any insert query criteria that are left
                for queryField, queryOperation, queryValue in criteria:
                    QueryCriteria(new=True,
                                  personGroupID=personGroup['id'],
                                  fieldName=queryField,
                                  operation=queryOperation,
                                  value=queryValue).insert()

            else:
                # TODO add members
                memberDict = self.get_temp('memberDict')

                memberPersonIDs = set([personID for personName, personID in list(memberDict['INDIVIDUALS'])])
                memberGroupIDs = set([groupID for orgName, groupName, groupID in list(memberDict['GROUPS'])])

                for roleName, orgName, roleID, orgID, subOrgs in list(memberDict['ROLES']):
                    orgIDs = [orgID]
                    if subOrgs:
                        orgIDs.extend(Organization(verify=True, id=orgID).getChildrenIDs(wholeTree=True))
                    query = 'SELECT DISTINCT personID FROM Account WHERE roleID=%%s AND organizationID in (%s) AND temp=%%s' % ','.join(map(str, orgIDs))
                    values = (roleID, 'FALSE')
                    memberPersonIDs = memberPersonIDs | set(map(lambda personID: str(personID[0]), personGroup.executeQuery(query=query, values=values).fetchall()))

                for period, sectionName, memberCount, sectionID, orgID, memberType, uniqueID in list(memberDict['CLASSES']):
                    memberPersonIDs = memberPersonIDs | set(Section(verify=True, id=sectionID, organizationID=orgID).getMemberIDs(memberType))

                if memberPersonIDs:
                    PersonGroupMemberView(where='personGroupID=%%s AND memberType = "PERSON" AND memberID NOT IN (%s)' % ','.join(map(str, list(memberPersonIDs))), whereValues=[personGroup['id']]).delete()
                    query = 'INSERT IGNORE INTO PersonGroupMember VALUES '
                    memberPersonIDsQuery = []
                    for memberPersonID in list(memberPersonIDs):
                        memberPersonIDsQuery.append((str(personGroup['id']), int(memberPersonID), 'PERSON'))
                    query += ','.join(map(str, memberPersonIDsQuery))
                    personGroup.executeQuery(query=query)
                else:
                    PersonGroupMemberView(where='personGroupID=%s AND memberType = "PERSON"', whereValues=[personGroup['id']]).delete()

                if memberGroupIDs:
                    PersonGroupMemberView(where='personGroupID=%%s AND memberType = "GROUP" AND memberID NOT IN (%s)' % ','.join(map(str, list(memberGroupIDs))), whereValues=[personGroup['id']]).delete()
                    query = 'INSERT IGNORE INTO PersonGroupMember VALUES '
                    memberGroupIDsQuery = []
                    for memberGroupID in list(memberGroupIDs):
                        memberGroupIDsQuery.append((str(personGroup['id']), memberGroupID, 'GROUP'))
                    query += ','.join(map(str, memberGroupIDsQuery))
                    personGroup.executeQuery(query=query)
                else:
                    PersonGroupMemberView(where='personGroupID=%s AND memberType = "GROUP"',
                                          whereValues=[personGroup['id']]).delete()

            userDict = self.get_temp('userDict')
            if userDict:
                userPersonIDs = set([personID for personName, personID in list(userDict['INDIVIDUALS'])])

                for roleName, orgName, roleID, orgID, subOrgs in list(userDict['ROLES']):
                    orgIDs = [orgID]
                    if subOrgs:
                        orgIDs.extend(Organization(verify=True, id=orgID).getChildrenIDs(wholeTree=True))
                    query = 'SELECT DISTINCT personID FROM Account WHERE roleID=%%s AND organizationID in (%s) AND temp=%%s' % ','.join(map(str, orgIDs))
                    values = (roleID, 'FALSE')
                    userPersonIDs = userPersonIDs | set(map(lambda personID: str(personID[0]), personGroup.executeQuery(query=query, values=values).fetchall()))

                if userPersonIDs:
                    PersonGroupUserView(where='personGroupID=%%s AND personID NOT IN (%s)' % ','.join(map(str, list(userPersonIDs))), whereValues=[personGroup['id']]).delete()
                    query = 'INSERT IGNORE INTO PersonGroupUser VALUES '
                    userPersonIDsQuery = []
                    for userPersonID in list(userPersonIDs):
                        userPersonIDsQuery.append((str(personGroup['id']), int(userPersonID)))
                    query += ','.join(map(str, userPersonIDsQuery))
                    personGroup.executeQuery(query=query)
                else:
                    PersonGroupUserView(where='personGroupID=%s', whereValues=[personGroup['id']]).delete()

            self.listClearList('users')
            self.listClearList('members')
            self.set_msg_success('The group has been saved.')
            return self.redirect('/main/messages/groups')

    def listAddPeople(self, recipientIDs, type):
        try:
            if type == 'users':
                dictString = 'userDict'
            else:
                dictString = 'memberDict'
            dictionary = self.get_temp(dictString) or self.defaultDict()
            dictionary['INDIVIDUALS'] = dictionary['INDIVIDUALS'] | recipientIDs
        except:
            raise 'error in addPeople'
        else:
            self.set_temp(dictString, dictionary)

    def checkFtp(self, request, errors, errorFields):
        retval = True
        if not request.POST.get('host'):
            errors.append('<b>Host:</b> Host name or IP Address is required')
            errorFields.append('host')
            retval = False
        if not request.POST.get('userName'):
            errors.append('<b>User Name:</b> User Name is required')
            errorFields.append('userName')
            retval = False
        if not request.POST.get('password'):
            errors.append('<b>Password:</b> Password is required')
            errorFields.append('password')
            retval = False
        if not request.POST.get('path'):
            errors.append('<b>Path:</b> Path is required')
            errorFields.append('path')
            retval = False
        return retval

    def checkGroup(self, request, errors, errorFields):
        retval = True
        choice = self.get_param_int('choice')
        if choice >= 100 and not self.check_permissions(['ADD_REMOVE_PUBLIC_GROUPS']):
            errors.append('<b>Group ID:</b> Enter a Group ID between 1 and 99')
            errorFields.append('groupID')
            retval = False
        # check that the choice is not in use.
        if not request.POST['groupID']:
            if choice < 100:
                pgv = PersonGroupView(where='ownerPersonID=%s AND choice=%s' % (self.get_my_id(), choice))
            else:
                pgv = PersonGroupView(where='choice=%s AND organizationID=%s' % (choice, request.POST['orgID']))

            if pgv.getRowCount():
                retval = False
                errors.append('<b>Group ID:</b> The Group ID  is already in use.  Please choose a different Group ID '
                              'or use the "Private ID" and "Public ID" buttons to generate an available ID.')
                errorFields.append('choice')

        if self.get_temp('userDict') and (self.get_temp('userDict').get('INDIVIDUALS') or
                                          self.get_temp('userDict').get('ROLES')) and choice < 100:
            retval = False
            errors.append('<b>Group ID:</b> The Group ID must be public (>100) if group users have been assigned.')

        return retval

    def canCreatePrivateGroup(self):
        return PersonGroupView(where='ownerPersonID=%s AND public="FALSE"' % self.get_my_id()).getRowCount() < 99


class MessagesGroupsAddEditUtilView(MessagesGroupsAddEditBaseView):
    def _get(self, request):
        action = self.get_param('action')
        data = {}
        if action == 'loadfile':
            data['loadFileTransfer'] = self.get_param('loadFileTransfer')
        elif action == 'advancedcontent':
            groupID = self.get_param('groupID')
            data['groupID'] = groupID
            data['organizationQueryCriteria'] = self.getOrganizationQueryCriteria(groupID)
            data['accountQueryCriteria'] = self.getAccountQueryCriteria(groupID)
            if data['organizationQueryCriteria']:
                data['organizationOperation'] = data['organizationQueryCriteria']['operation']
            if data['accountQueryCriteria']:
                data['roleOperation'] = data['accountQueryCriteria']['operation']
            data['organization_values'] = self.getOrganizationValues(data['organizationQueryCriteria'] and data['organizationQueryCriteria']['value'])
            data['role_values'] = self.getRoleValues(data['accountQueryCriteria'] and data['accountQueryCriteria']['value'])
            data['matchCriteria'] = self.getMatchCriteria(groupID)
            data['criteria'] = self.getQueryCriteria(groupID)
            data['form'] = self._form(initial=data, advanced_only=True)
        elif action == 'advancedGetCriteria':
            return self.advancedGetCriteria()
        elif action == 'generatechoice':
            return self.response(self.generate_choice())
        elif action == 'selectgroupsfolder':
            data['groups'] = self.selectGetGroups(self.get_param('orgID'))
            data['childOrgs'] = self.selectGetSubOrgsByGroup(self.get_param('orgID'))
        elif action == 'selectgroupmembers':
            data['members'] = self.getGroupMembers(self.get_param('groupID'), showCount=True)
        elif action == 'selectmemberssearchresults':
            searchResults = self.selectSearch(searchString=self.get_param('searchString'))
            data['roles'] = searchResults['ROLES']
            data['groups'] = searchResults['GROUPS']
        elif action == 'selectuserssearchresults':
            searchResults = self.selectSearch(searchString=self.get_param('searchString'), type='users')
            data['roles'] = searchResults['ROLES']
            data['groups'] = searchResults['GROUPS']
        elif action == 'listindividualrecipients':
            data['individuals'] = self.listGetIndividuals()
        elif action == 'listindividualusers':
            data['individuals'] = self.listGetIndividuals('users')
        elif action == 'listClearList':
            self.listClearList(self.get_param('type'))
            return self.response()
        elif action == 'selectMembersOrgFolderContents':
            orgID = self.get_param('orgID')
            data['orgID'] = orgID
            subOrgIDs = self.get_org(self.get_param('orgID'))['allChildrenIDs']
            data['orgRoles'] = self.selectGetOrgRoles(orgID=orgID, subOrgIDs=subOrgIDs, type='members')
            data['canSendToGroups'] = self.selectCanSendToGroups(orgID=orgID, subOrgIDs=subOrgIDs)
            data['canSendToClasses'] = self.selectCanSendToClasses(orgID=orgID, subOrgIDs=subOrgIDs)
        elif action == 'selectUsersOrgFolderContents':
            orgID = self.get_param('orgID')
            data['orgID'] = orgID
            subOrgIDs = self.get_org(self.get_param('orgID'))['allChildrenIDs']
            data['orgRoles'] = self.selectGetOrgRoles(orgID=orgID, subOrgIDs=subOrgIDs, type='users')
        elif action == 'selectOrgRoleMembers':
            orgID = self.get_param('orgID')
            roleID = self.get_param('roleID')
            data['roleID'] = roleID
            data['orgRoleMembers'] = self.get_org_role_members(orgID, roleID)
            data['childOrgs'] = self.getSubOrgsByRole(roleID, orgID)
        elif action == 'selectOrgRoleUsers':
            orgID = self.get_param('orgID')
            roleID = self.get_param('roleID')
            data['roleID'] = roleID
            data['orgRoleMembers'] = self.get_org_role_members(orgID, roleID)
            data['childOrgs'] = self.getSubOrgsByRole(roleID, orgID)
        elif action == 'selectOrgTeachers':
            orgID = self.get_param('orgID')
            data['teachers'] = self.selectGetTeachers(orgID)
            data['childOrgs'] = self.selectGetSubOrgsByClasses(orgID)
        elif action == 'selectOrgTeacherClasses':
            orgID = self.get_param('orgID')
            teacherID = self.get_param('teacherID')
            data['sections'] = self.getClasses(orgID=orgID, teacherID=teacherID)
        elif action == 'selectClassFolderContent':
            uniqueID = self.get_param('uniqueID')
            data['uniqueID'] = uniqueID
            data['hasStudents'] = self.check_permissions(['SEND_TO_STUDENTS_IN_MY_CLASSES','SEND_TO_STUDENT']) and self.selectClassHasMembers(uniqueID, 'STUDENT')
            data['hasParents'] = self.check_permissions(['SEND_TO_PARENTS_IN_MY_CLASSES','SEND_TO_PARENT']) and self.selectClassHasMembers(uniqueID, 'PARENT')
        elif action == 'selectClassMembers':
            uniqueID = self.get_param('uniqueID')
            memberType = self.get_param('memberType')
            data['members'] = self.getClassMembers(uniqueID, memberType)
        elif action == 'selectClassesFolder':
            data['sections'] = self.getClasses()
        elif action == 'listOrgRoleMembers':
            orgID = self.get_param('orgID')
            roleID = self.get_param('roleID')
            subOrgs = self.get_param_int('subOrgs')
            data['orgID'] = orgID
            data['roleID'] = roleID
            data['subOrgs'] = subOrgs
            data['orgRoleMembers'] = self.get_org_role_members(orgID, roleID)
            if subOrgs:
                data['childOrgs'] = self.getSubOrgsByRole(roleID, orgID)
        elif action == 'listOrgRoleUsers':
            orgID = self.get_param('orgID')
            roleID = self.get_param('roleID')
            subOrgs = self.get_param_int('subOrgs')
            data['orgID'] = orgID
            data['roleID'] = roleID
            data['orgRoleMembers'] = self.get_org_role_members(orgID, roleID)
            data['subOrgs'] = subOrgs
            if subOrgs:
                data['childOrgs'] = self.getSubOrgsByRole(roleID, orgID)
        elif action == 'listGroupMembers':
            data['parentGroupID'] = self.get_param('parentGroupID')
            data['members'] = self.getGroupMembers(self.get_param('groupID'), showCount=True)
        elif action == 'listClassMembers':
            uniqueID = self.get_param('uniqueID')
            memberType = self.get_param('memberType')
            data['uniqueID'] = uniqueID
            data['memberType'] = memberType
            data['members'] = self.getClassMembers(uniqueID, memberType)
        elif action == 'listMemberList':
            return self.list('members', expand=False)
        elif hasattr(self, action):
            return self.add_remove(getattr(self, action))

        return self.render_to_response('main/messages/groups/addedit/{}.html'.format(action.lower()), data)

    def _post(self, request):
        action = self.get_param('action')
        if action == 'advancedLoadQuery':
            return self.advancedLoadQuery()

    def list(self, type, expand=True):
        return self.response(self.list_str(type, expand=expand))

    def add_remove(self, fnc):
        type = self.get_param('type')
        dictString = 'userDict' if type == 'users' else 'memberDict'
        personDict = self.get_temp(dictString) or self.defaultDict()
        fnc(personDict)
        self.set_temp(dictString, personDict)
        return self.list(type)

    def listRemoveAll(self, personDict):
        if personDict:
            personDict[self.get_param('key')] = set([])

    def listRemoveRole(self, personDict):
        def checkSubOrganizations(orgID, deleteOrgID):
            for subOrg in self.getSubOrgsByRole(roleID, orgID):
                if subOrg['id'] != deleteOrgID and deleteOrgID not in self.get_org(subOrg['id'])['allChildrenIDs']:
                    personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], subOrg['name'], roleID, str(subOrg['id']), True)])
                elif subOrg['id'] != deleteOrgID:
                    if subOrg['roleInOrg']:
                        personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], subOrg['name'], roleID, str(subOrg['id']), False)])
                    checkSubOrganizations(subOrg['id'], deleteOrgID)
                else:
                    for grandChild in self.getSubOrgsByRole(roleID, subOrg['id']):
                        personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], grandChild['name'], roleID, str(grandChild['id']), True)])

        roleID = self.get_param('roleID')
        orgID = self.get_param('orgID')
        org = self.get_org(orgID)
        role = Role(verify=True, id=roleID)

        # the org is in the list and doesn't include suborgs
        if personDict['ROLES'] & set([(role['name'], org['name'], roleID, orgID, False)]):
            personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], org['name'], roleID, orgID, False)])

        # the org is in the list and includes suborgs
        elif personDict['ROLES'] & set([(role['name'], org['name'], roleID, orgID, True)]):
            # else, remove it from the list and add the sub org roles to the list
            personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], org['name'], roleID, orgID, True)])
            children = set([(role['name'], subOrg['name'], roleID, str(subOrg['id']), True) for subOrg in self.getSubOrgsByRole(roleID, orgID)])
            personDict['ROLES'] = personDict['ROLES'] | children

        else:
            # the org is not in the list, one of its parents must be in the list
            for parent in org.getParents():
                if personDict['ROLES'] & set([(role['name'], parent['name'], roleID, str(parent['id']), True)]):
                    personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], parent['name'], roleID, str(parent['id']), True)])
                    if AccountView(where='roleID=%s AND organizationID=%s AND temp="FALSE"', whereValues=[roleID, parent['id']]).getRowCount():
                        personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], parent['name'], roleID, str(parent['id']), False)])
                    checkSubOrganizations(parent['id'], int(orgID))

    def listRemoveEntireRole(self, personDict):
        def checkSubOrganizations(orgID, deleteOrgID):
            for subOrg in self.getSubOrgsByRole(roleID, orgID):
                if subOrg['id'] != deleteOrgID and deleteOrgID not in self.get_org(subOrg['id'])['allChildrenIDs']:
                    personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], subOrg['name'], roleID, str(subOrg['id']), True)])
                elif subOrg['id'] != deleteOrgID:
                    if subOrg['roleInOrg']:
                        personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], subOrg['name'], roleID, str(subOrg['id']), False)])
                    checkSubOrganizations(subOrg['id'], deleteOrgID)

        roleID = self.get_param('roleID')
        orgID = self.get_param('orgID')
        org = self.get_org(orgID)
        role = Role(verify=True, id=roleID)

        # the org is in the list and doesn't include suborgs
        if personDict['ROLES'] & set([(role['name'], org['name'], roleID, orgID, False)]):
            personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], org['name'], roleID, orgID, False)])

        # the org is in the list and includes suborgs
        if personDict['ROLES'] & set([(role['name'], org['name'], roleID, orgID, True)]):
            # else, remove it from the list and add the sub org roles to the list
            personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], org['name'], roleID, orgID, True)])
        else:
            # the org is not in the list, one of its parents must be in the list
            for parent in org.getParents():
                if personDict['ROLES'] & set([(role['name'], parent['name'], roleID, str(parent['id']), True)]):
                    personDict['ROLES'] = personDict['ROLES'] - set([(role['name'], parent['name'], roleID, str(parent['id']), True)])
                    if AccountView(where='roleID=%s AND organizationID=%s AND temp="FALSE"', whereValues=[roleID, parent['id']]).getRowCount():
                        personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], parent['name'], roleID, str(parent['id']), False)])
                    checkSubOrganizations(parent['id'], int(orgID))


    def listRemoveOrgRolePerson(self, personDict):
        if personDict:
            roleID = self.get_param('roleID')
            orgID = self.get_param('orgID')
            personID = self.get_param('personID')
            # Remove this role
            self.listRemoveRole(personDict)
            # Add all people of this role except the person that was removed to the individuals list
            query = 'SELECT Account.personID, CONCAT(Person.lastName, ", ", Person.firstName) as name FROM Account, Person WHERE Person.id = Account.personID AND Account.roleID=%s AND Account.organizationID = %s AND Account.temp = "FALSE" AND Person.id !=%s ORDER BY Person.lastName, Person.firstName'
            queryValues = (roleID, orgID, personID)
            individuals = set([(name, str(personID)) for personID, name in self.execute_query(query=query, values=queryValues).fetchall()])
            personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] | individuals

    def listRemoveGroup(self, personDict):
        groupID = self.get_param('groupID')
        parentGroupID = self.get_param('parentGroupID')

        if groupID == parentGroupID:
            # remove the parent group
            personGroup = PersonGroup(verify=True, id=groupID)
            personDict['GROUPS'] = personDict['GROUPS'] - set([(personGroup['organization']['name'], personGroup['name'], groupID)])
        else:
            # remove a child group
            parentGroup = PersonGroup(verify=True, id=parentGroupID)
            childGroup =  PersonGroup(verify=True, id=groupID)

            # remove the parent group
            personDict['GROUPS'] = personDict['GROUPS'] - set([(parentGroup['organization']['name'], parentGroup['name'], parentGroupID)])

            # add the individuals in the parent group minus the indiviuals in the child group
            personIDs = parentGroup.getRecipientIDs() - childGroup.getRecipientIDs()

            if personIDs:
                recipients = [(recipient.getName(lastFirst=True), str(recipient['id'])) for recipient in PersonView(where='id in (%s)' % ','.join(list(map(str, personIDs)))).generateall()]
            else:
                recipients = []

            personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] | set(recipients)

    def listRemoveGroupMemberRecipient(self, personDict):
        memberID = self.get_param('memberID')
        parentGroupID = self.get_param('parentGroupID')
        if personDict:
            parentGroup = PersonGroup(verify=True, id=parentGroupID)

            # remove the parent group
            personDict['GROUPS'] = personDict['GROUPS'] - set([(parentGroup['organization']['name'], parentGroup['name'], parentGroupID)])

            # get all the individuals in the groups and remove the one that was clicked
            members = filter(lambda person: int(person['id']) != int(memberID), list(parentGroup.getRecipients()))
            recipients = set([(person.getName(lastFirst=True), str(person['id'])) for person in members])

            # add the remaining individuals
            personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] | recipients

    def listRemoveClassMembers(self, personDict):
        uniqueID = self.get_param('uniqueID')
        memberType = self.get_param('memberType')
        section = SectionView(where="uniqueID=%s" % uniqueID).fetchone()
        period = section['period']
        try:
            period = int(period)
        except ValueError:
            period = period.upper()
        except TypeError:
            pass
        memberCount = section.getMemberCount(memberType)
        personDict['CLASSES'] = personDict['CLASSES'] - set([(period, '%s %ss' % (section.getDisplayName(), memberType.capitalize()), memberCount, section['id'], section['organizationID'], memberType, int(uniqueID))])

    def listRemoveClassMemberRecipient(self, personDict):
        memberID = self.get_param('memberID')
        uniqueID = self.get_param('uniqueID')
        memberType = self.get_param('memberType')
        if personDict:
            section = SectionView(where="uniqueID=%s" % uniqueID).fetchone()
            period = section['period']
            try:
                period = int(period)
            except ValueError:
                period = period.upper()
            except TypeError:
                pass
            memberCount = section.getMemberCount(memberType)
            # remove the class
            personDict['CLASSES'] = personDict['CLASSES'] - set([(period, '%s %ss' % (section.getDisplayName(), memberType.capitalize()), memberCount, section['id'], section['organizationID'], memberType, int(uniqueID))])
            # get all the individuals in the groups and remove the one that was clicked
            members = section.getMembers(memberType)
            recipients = set([(person.getName(lastFirst=True), str(person['id'])) for person in members if str(person['id']) != memberID])
            # add the remaining individuals
            personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] | recipients

    def listRemovePerson(self, personDict):
        personID = self.get_param('personID')
        if personDict:
            recipientName = self.get_person(personID).getName(lastFirst=True)
            personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] - set([(recipientName, personID)])

    def listAddRole(self, personDict):
        roleID = self.get_param('roleID')
        orgID = self.get_param('orgID')
        org = self.get_org(orgID)
        role = Role(verify=True, id=roleID)
        parents = [(role['name'], org['name'], roleID, orgID, True)]
        parents.extend([(role['name'], organization['name'], roleID, str(organization['id']), True) for organization in org.getParents()])
        if not personDict['ROLES'] & set(parents):
            personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], org['name'], roleID, orgID, False)])

    def listAddEntireRole(self, personDict):
        roleID = self.get_param('roleID')
        orgID = self.get_param('orgID')
        role = Role(verify=True, id=roleID)
        org = self.get_org(orgID)

        # remove this org role and all sub orgs role from ROLES
        roles = [(role['name'], org['name'], roleID, orgID, False)]
        for subOrg in self.get_children(organizationID=org['id'], wholeTree=True):
            roles.extend([(role['name'], subOrg['name'], roleID, str(subOrg['id']), True), (role['name'], subOrg['name'], roleID, str(subOrg['id']), False)])
        personDict['ROLES'] = personDict['ROLES'] - set(roles)
        # add (roleID, orgID, subOrgFlag) to roles
        parents = [(role['name'], org['name'], roleID, orgID, True)]
        parents.extend([(role['name'], organization['name'], roleID, str(organization['id']), True) for organization in org.getParents()])
        if not personDict['ROLES'] & set(parents):
            personDict['ROLES'] = personDict['ROLES'] | set([(role['name'], org['name'], roleID, orgID, True)])

    def listAddPerson(self, personDict):
        recipientID = self.get_param('recipientID')
        memberName = self.get_person(recipientID).getName(lastFirst=True)
        personDict['INDIVIDUALS'] = personDict['INDIVIDUALS'] | set([(memberName, recipientID)])

    def listAddGroup(self, personDict):
        # remove any groups that are children, grandchildren, etc of the group that we are adding
        groupID = self.get_param('groupID')
        pg = PersonGroup(verify=True, id=groupID)
        personDict['GROUPS'] = personDict['GROUPS'] - set([(childGroup['organization']['name'], childGroup['name'], str(childGroup['id'])) for childGroup in pg.getChildGroups()])
        personDict['GROUPS'] = personDict['GROUPS'] | set([(pg['organization']['name'], pg['name'], groupID)])

    def listAddOrgGroups(self, personDict):
        orgID = self.get_param('orgID')
        invalidGroupIDs = ','.join(map(str, self.get_temp('invalidGroupIDs') or []))
        personID = self.get_my_id()
        if invalidGroupIDs:
            pgv = PersonGroupView(where='organizationID=%%s AND ownerPersonID!=%%s AND public="TRUE" and groupType IN ("PERSON", "QUERY") AND id NOT IN (%s)' % invalidGroupIDs, whereValues=[orgID, personID])
        else:
            pgv = PersonGroupView(where='organizationID=%s AND ownerPersonID!=%s AND public="TRUE" and groupType IN ("PERSON", "QUERY")', whereValues=[orgID, personID])
        personDict['GROUPS'] = personDict['GROUPS'] | set([(group['organization']['name'], group['name'], str(group['id'])) for group in  pgv.generateall()])

    def listAddClassMembers(self, personDict):
        uniqueID = self.get_param('uniqueID')
        memberType = self.get_param('memberType')
        section = SectionView(where="uniqueID=%s" % uniqueID).fetchone()
        period = section['period']
        try:
            period = int(period)
        except ValueError:
            period = period.upper()
        except TypeError:
            pass
        memberCount = section.getMemberCount(memberType)
        personDict['CLASSES'] = personDict['CLASSES'] | set([(period, '%s %ss' % (section.getDisplayName(), memberType.capitalize()), memberCount, section['id'], section['organizationID'], memberType, int(uniqueID))])

    def listAddEntireOrgGroups(self, personDict):
        orgID = self.get_param('orgID')
        invalidGroupIDs = ','.join(map(str, self.get_temp('invalidGroupIDs') or []))
        personID = self.get_my_id()
        orgIDs = ','.join(map(str, [orgID] + self.get_org(orgID)['allChildrenIDs']))
        if invalidGroupIDs:
            pgv = PersonGroupView(where='organizationID IN (%s) AND ownerPersonID!=%s AND public="TRUE" and groupType IN ("PERSON", "QUERY") AND id NOT IN (%s)' % (orgIDs, personID, invalidGroupIDs))
        else:
            pgv = PersonGroupView(where='organizationID IN (%s) AND ownerPersonID!=%s AND public="TRUE" and groupType IN ("PERSON", "QUERY")' % (orgIDs, personID))
        personDict['GROUPS'] = personDict['GROUPS'] | set([(group['organization']['name'], group['name'], str(group['id'])) for group in pgv.generateall()])

    def generate_choice(self):
        if int(self.get_param('public')):
            return getRandomPublicGroupChoice(organizationID=self.get_param('orgID'))
        else:
            return getPrivateGroupChoice(personID=self.get_my_id())

    def selectSearch(self, searchString, type='members'):
        if searchString:
            myPersonID = self.get_my_id()
            searchValue = searchString
            searchString = '{}%'.format(searchString)
            my_orgs = self.selectGetMyOrgs()
            org_id_list = []
            for org in my_orgs:
                org_id_list.append(org['id'])
                org_id_list.extend(org['allChildrenIDs'])
            orgIDs = ','.join(map(str, org_id_list))

            results = {'ROLES':{}, 'GROUPS':{}}
            accountSearchResults = self.search_accounts(searchValue, for_send=True)

            for accountSearchResult in accountSearchResults:
                roleID = accountSearchResult['roleID']
                roleName = accountSearchResult['roleName']
                for account in accountSearchResult['accounts']:
                    if not results['ROLES'].has_key(roleID):
                        results['ROLES'][roleID] = {
                            'name': roleName,
                            'roleID': roleID,
                            'orgs': {},
                        }
                    if not results['ROLES'][roleID]['orgs'].has_key(account['organizationID']):
                        results['ROLES'][roleID]['orgs'][account['organizationID']] = {
                            'name': account['orgName'],
                            'orgID': account['organizationID'],
                            'members': [],
                        }
                    results['ROLES'][roleID]['orgs'][account['organizationID']]['members'].append({
                        'personID': account['personID'],
                        'name': '{}, {}'.format(account['lastName'], account['firstName']),
                    })

            for roleID, roleResults in results['ROLES'].items():
                results['ROLES'][roleID]['orgs'] = roleResults['orgs'].values()

            results['ROLES'] = results['ROLES'].values()

            if orgIDs:
                viewPublicGroups = self.check_permissions(['VIEW_GROUPS'])
                invalidGroupIDs = ','.join(map(str, self.get_temp('invalidGroupIDs') or []))
                for group in PersonGroupView(where="name LIKE %%s AND organizationID IN (%s) AND (ownerPersonID=%%s OR public=%%s) %s" % (orgIDs, ' AND id NOT IN (%s)' % invalidGroupIDs if invalidGroupIDs else ''), whereValues=[searchString, myPersonID, 'TRUE'], order="name").generateall():
                    if viewPublicGroups or group['ownerPersonID'] == myPersonID:
                        if not results['GROUPS'].has_key(group['organizationID']):
                            results['GROUPS'][group['organizationID']] = {
                                'name':group['organization']['name'],
                                'orgID':group['organizationID'],
                            }
                        if not results['GROUPS'][group['organizationID']].has_key('groups'):
                            results['GROUPS'][group['organizationID']]['groups'] = []
                        results['GROUPS'][group['organizationID']]['groups'].append({
                            'groupID': group['id'],
                            'name': group['name'],
                            'count': group.getDisplayRecipients(),
                        })

            results['GROUPS'] = results['GROUPS'].values()
            for org in results['GROUPS']:
                for group in org['groups']:
                    group['objectID'] = self.selectGetGroupObjectID(org['orgID'], group['groupID'], search=True)
                    group['javascriptParams'] = self.selectGetGroupJavascriptParams(org['orgID'], group['groupID'], search=True)

            return results

    def getGroupMembers(self, groupID, showCount=False):
        retval = []
        group = PersonGroup(verify=True, id=groupID)
        if group['groupType'] == 'QUERY':
            recipientPersonIDs = group.getRecipientIDs()
            count = len(recipientPersonIDs)
            if count > 20000:
                retval.append({
                    'memberID': 0,
                    'memberType': 'PERSON',
                    'name': '{} members (too many to display)'.format(count),
                })
            elif count > 0:
                if showCount and count > 1:
                    retval.append({
                        'memberID': 0,
                        'memberType': 'PERSON',
                        'name': '{} members'.format(count),
                    })
                for person in PersonView(where='id IN (%s)'%(','.join(map(str,recipientPersonIDs))),fieldNames=['id','lastName','firstName'], order='lastName, firstName').generateall():
                    retval.append({
                        'memberID': person['id'],
                        'memberType': 'PERSON',
                        'name': person.getName(lastFirst=True),
                    })
        else:
            count = self.execute_query(query='SELECT COUNT(*) FROM PersonGroupMember WHERE personGroupID = %s AND memberType = "PERSON"' % groupID).fetchone()[0]
            if count > 20000:
                retval.append({
                    'memberID': 0,
                    'memberType': 'PERSON',
                    'name': '{} members (too many to display)'.format(count),
                })
            elif count > 0:
                cursor = self.execute_query(query='SELECT DISTINCT memberID, CONCAT(lastName, ", ", firstName) FROM (PersonGroupMember JOIN Person ON Person.id = PersonGroupMember.memberID) JOIN Account ON Person.id=Account.personID WHERE personGroupID = %s AND memberType = "PERSON" AND Account.temp="FALSE" ORDER BY lastName, firstName' % groupID)
                groupMember = cursor.fetchone()
                while groupMember:
                    memberID, name = groupMember
                    retval.append({
                        'memberID': memberID,
                        'memberType': 'PERSON',
                        'name': name,
                    })
                    groupMember = cursor.fetchone()
            subGroupIDs = [groupID for groupID, in self.execute_query(query='SELECT memberID FROM PersonGroupMember WHERE  personGroupID = %s AND memberType = "GROUP"' % groupID).fetchall()]
            while subGroupIDs:
                tempSubGroupIDs = subGroupIDs[:1000]
                subGroupIDs = subGroupIDs[1000:]
                for personGroup in PersonGroupView(where='id IN (%s)' % ','.join(map(str, tempSubGroupIDs))).generateall():
                    retval.append({
                        'memberID': personGroup['id'],
                        'memberType': 'GROUP',
                        'name': personGroup['name'],
                        'count': personGroup.getDisplayRecipients(),
                    })
        orgID = self.get_param('orgID')
        for member in retval:
            if member['memberType'] == 'GROUP':
                member['objectID'] = self.selectGetGroupObjectID(orgID, member['memberID'], parentID=groupID)
                member['javascriptParams'] = self.selectGetGroupJavascriptParams(orgID, member['memberID'], parentID=groupID)
        return retval

    def selectGetTeachers(self, orgID):
        personID = self.get_my_id()
        query = 'SELECT DISTINCT Section.teacherPersonID FROM SectionTermLink JOIN Section ON SectionTermLink.sectionID=Section.id AND SectionTermLink.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE SectionTermLink.organizationID=%%s AND SectionTermLink.termID IN (%s) UNION SELECT DISTINCT Section.teacherPersonID FROM StudentSchedule JOIN Section ON StudentSchedule.sectionID=Section.id AND StudentSchedule.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE StudentSchedule.organizationID=%%s AND StudentSchedule.termID IN (%s)'
        terms = getTermsForAllTracks(organizationID=orgID)
        if terms:
            termIDs = ','.join([str(term['id']) for term in terms])
        else:
            termIDs = '0'
        values = (personID, orgID, personID, orgID)
        teacherIDs = '","'.join(set([str(teacherID) for teacherID, in self.execute_query(query % (termIDs, termIDs), values).fetchall()]))
        if teacherIDs:
            return [{'teacherID':teacher['id'], 'name':teacher.getName(), 'organizationID':orgID} for teacher in PersonView(where='id IN ("%s")' % teacherIDs, order='firstName, lastName').generateall()]
        else:
            return []

    def selectGetSubOrgsByClasses(self, orgID):
        retval = []
        org = self.get_org(orgID)
        subOrgIDs = org['childrenIDs']
        subOrgCount = {}
        query = 'SELECT COUNT(*) as count FROM SectionTermLink JOIN Section ON SectionTermLink.sectionID=Section.id AND SectionTermLink.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE SectionTermLink.organizationID=%%s AND SectionTermLink.termID IN (%s) UNION SELECT COUNT(*) as count FROM StudentSchedule JOIN Section ON StudentSchedule.sectionID=Section.id AND StudentSchedule.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE StudentSchedule.organizationID=%%s AND StudentSchedule.termID IN (%s)'
        personID = self.get_my_id()

        for subOrgID in subOrgIDs:
            terms = getTermsForAllTracks(organizationID=subOrgID)
            if terms:
                termIDs = ','.join([str(term['id']) for term in terms])
            else:
                termIDs = '0'

            count = sum([count for count, in org.executeQuery(query % (termIDs, termIDs), values=(personID, subOrgID, personID, subOrgID)).fetchall()])
            if count:
                subOrgCount[subOrgID] = count

        for subOrg in org.getChildren(wholeTree=False):
            subOrgDict = {'id':subOrg['id'], 'name':subOrg['name'], 'classesInOrg':subOrgCount.has_key(subOrg['id']), 'classesInSubOrgs':False}
            grandChildrenIDs = subOrg.getChildrenIDs(wholeTree=True)
            if grandChildrenIDs:
                for grandChildID in grandChildrenIDs:
                    terms = getTermsForAllTracks(organizationID=grandChildID)
                    if terms:
                        termIDs = ','.join([str(term['id']) for term in terms])
                    else:
                        termIDs = '0'
                    if sum([count for count, in subOrg.executeQuery(query % (termIDs, termIDs), values=(personID, grandChildID, personID, grandChildID)).fetchall()]):
                        subOrgDict['classesInSubOrgs'] = True
                        break
                else:
                    subOrgDict['classesInSubOrgs'] = False

            if subOrgDict['classesInOrg'] or subOrgDict['classesInSubOrgs']:
                retval.append(subOrgDict)

        return retval

    def selectGetOrgRoles(self, orgID, subOrgIDs, type='members'):
        roleDict = {}
        retval = []
        permissions = {}
        roleIDs = []

        # TODO This needs to be modified for custom roles feature.

        for role in RoleView(where="id > 2 AND display='TRUE'", order="id DESC").generateall():
            if not permissions.has_key(role['mergedRoleType']):
                permissions[role['mergedRoleType']] = self.check_permissions(['SEND_TO_%s' % role['mergedRoleType']], int(orgID))
            roleDict[role['id']] = {
                'roleID': role['id'],
                'name': role['name'],
                'roleType': role['mergedRoleType'],
                'roleInOrg': False,
                'roleInSubOrgs': False,
            }
            roleIDs.append(str(role['id']))

        roleIDs = ','.join(roleIDs)

        where = ['Account.roleID IN (%s)' % roleIDs, 'Account.organizationID=%s' % orgID, 'Account.temp="FALSE"']
        subOrgWhere = ['Account.roleID IN (%s)' % roleIDs, 'Account.organizationID IN (%s)' % ','.join(map(str, subOrgIDs)), 'Account.temp="FALSE"']
        order = 'Account.roleID DESC'

        for roleID, in self.execute_query('SELECT DISTINCT Account.roleID FROM Account WHERE %s ORDER BY %s' % (' AND '.join(where), order)).fetchall():
            roleDict[roleID]['roleInOrg'] = True

        if subOrgIDs:
            for roleID, in self.execute_query('SELECT DISTINCT Account.roleID FROM Account WHERE %s ORDER BY %s' % (' AND '.join(subOrgWhere), order)).fetchall():
                roleDict[roleID]['roleInSubOrgs'] = True

        roleIDs = roleDict.keys()
        roleIDs.sort()
        roleIDs.reverse()
        for roleID in roleIDs:
            if permissions[roleDict[roleID]['roleType']] and (roleDict[roleID]['roleInOrg'] or roleDict[roleID]['roleInSubOrgs']):
                if type != 'users' or roleDict[roleID]['roleType'] not in [PARENT, STUDENT]:
                    retval.append(roleDict[roleID])

        return retval

    def selectCanSendToGroups(self, orgID, subOrgIDs):
        personID = self.get_my_id()
        groupsInOrg = bool(PersonGroupView(where='organizationID=%s AND ownerPersonID != %s AND public="TRUE" AND groupType IN ("PERSON", "QUERY")', whereValues=[orgID, personID]).getRowCount())
        if not groupsInOrg and subOrgIDs:
            groupsInSubOrgs = bool(PersonGroupView(where='organizationID IN (%s) AND ownerPersonID != %s AND public="TRUE" AND groupType IN ("PERSON", "QUERY")' % (','.join(map(str,subOrgIDs)), personID)).getRowCount())
        else:
            groupsInSubOrgs = False
        if self.check_permissions(['VIEW_GROUPS']) and (groupsInOrg or groupsInSubOrgs):
            return {'groupsInOrg':groupsInOrg, 'groupsInSubOrgs':groupsInSubOrgs}

    def selectCanSendToClasses(self, orgID, subOrgIDs):
        query = 'SELECT COUNT(*) as count FROM SectionTermLink JOIN Section ON SectionTermLink.sectionID=Section.id AND SectionTermLink.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE SectionTermLink.organizationID=%%s AND SectionTermLink.termID IN (%s) UNION SELECT COUNT(*) as count FROM StudentSchedule JOIN Section ON StudentSchedule.sectionID=Section.id AND StudentSchedule.organizationID=Section.organizationID AND Section.teacherPersonID!=%%s WHERE StudentSchedule.organizationID=%%s AND StudentSchedule.termID IN (%s)'

        if self.check_permissions(['SEND_TO_CLASSES']):
            personID = self.get_my_id()

            terms = getTermsForAllTracks(organizationID=orgID)
            if terms:
                termIDs = ','.join([str(term['id']) for term in terms])
            else:
                termIDs = '0'

            classesInOrg = bool(sum([count for count, in self.execute_query(query % (termIDs, termIDs), values=(personID, orgID, personID, orgID)).fetchall()]))

            if subOrgIDs:
                for subOrgID in subOrgIDs:
                    terms = getTermsForAllTracks(organizationID=subOrgID)
                    if terms:
                        termIDs = ','.join([str(term['id']) for term in terms])
                    else:
                        termIDs = '0'
                    if sum([count for count, in self.execute_query(query % (termIDs, termIDs), values=(personID, subOrgID, personID, subOrgID)).fetchall()]):
                        classesInSubOrgs = True
                        break
                else:
                    classesInSubOrgs = False
            else:
                classesInSubOrgs = False

            if classesInOrg or classesInSubOrgs:
                return {'classesInOrg':classesInOrg, 'classesInSubOrgs':classesInSubOrgs}

    def selectGetGroups(self, orgID):
        personID = self.get_my_id()
        invalidGroupIDs = ','.join(map(str, self.get_temp('invalidGroupIDs') or []))
        retval = []
        if orgID:
            where = 'ownerPersonID != %s AND organizationID = %s AND public="TRUE" AND groupType IN ("PERSON", "QUERY") {}'.format('AND id NOT IN ({})'.format(invalidGroupIDs) if invalidGroupIDs else '')
            retval = [{'name':personGroup['name'], 'groupID':personGroup['id'], 'count':personGroup.getDisplayRecipients()} for personGroup in PersonGroupView(where=where, whereValues=(personID, orgID), order='name').generateall()]
        else:
            groupIDs = []
            where = 'ownerPersonID = %s AND groupType IN ("PERSON", "QUERY") {}'.format('AND id NOT IN ({})'.format(invalidGroupIDs) if invalidGroupIDs else '')
            pgv = PersonGroupView(where=where, whereValues=[personID], order='name')
            for personGroup in pgv.generateall():
                retval.append({'name':personGroup['name'], 'groupID':personGroup['id'], 'count':personGroup.getDisplayRecipients()})
                groupIDs.append(personGroup['id'])
            if retval:
                removeGroups = map(lambda group: group[0], personGroup.executeQuery('SELECT DISTINCT memberID from PersonGroupMember where memberID in (%s) and memberType = "GROUP"' % ','.join(map(str, groupIDs))).fetchall())
                retval = filter(lambda group: group['groupID'] not in removeGroups, retval)

        for group in retval:
            group['objectID'] = self.selectGetGroupObjectID(orgID, group['groupID'])
            group['javascriptParams'] = self.selectGetGroupJavascriptParams(orgID, group['groupID'])

        return retval

    def selectGetSubOrgsByGroup(self, orgID):
        invalidGroupIDs = ','.join(map(str, self.get_temp('invalidGroupIDs') or []))

        retval = []
        if orgID:
            org = self.get_org(orgID)
            subOrgIDs = ','.join(map(str, org['childrenIDs']))
            if subOrgIDs:
                if invalidGroupIDs:
                    subOrgCount = dict([(organizationID, count) for organizationID, count in org.executeQuery('SELECT organizationID, COUNT(*) FROM PersonGroup WHERE organizationID IN (%s) AND id NOT IN (%s) GROUP BY organizationID' % (subOrgIDs, invalidGroupIDs)).fetchall()])
                else:
                    subOrgCount = dict([(organizationID, count) for organizationID, count in org.executeQuery('SELECT organizationID, COUNT(*) FROM PersonGroup WHERE organizationID IN (%s) GROUP BY organizationID' % subOrgIDs).fetchall()])

            else:
                subOrgCount = {}

            for subOrg in org.getChildren(wholeTree=False):
                subOrgDict = {'id':subOrg['id'], 'name':subOrg['name'], 'groupsInOrg':subOrgCount.has_key(subOrg['id']), 'groupsInSubOrgs':False}
                grandChildrenIDs = ','.join(map(str, subOrg.getChildrenIDs(wholeTree=True)))
                if grandChildrenIDs:
                    if invalidGroupIDs:
                        subOrgDict['groupsInSubOrgs'] = bool(PersonGroupView(where='organizationID IN (%s) AND id NOT IN (%s)' % (grandChildrenIDs, invalidGroupIDs)).getRowCount())
                    else:
                        subOrgDict['groupsInSubOrgs'] = bool(PersonGroupView(where='organizationID IN (%s)' % grandChildrenIDs).getRowCount())
                if subOrgDict['groupsInOrg'] or subOrgDict['groupsInSubOrgs']:
                    retval.append(subOrgDict)

        return retval

    def selectGetGroupObjectID(self, orgID, groupID, parentID=None, search=False):
        retval = ''
        if orgID:
            retval += 'Org%s' % orgID
        retval += 'Group%s' % groupID
        if parentID:
            retval += 'Parent%s' % parentID
        if search:
            retval += 'Search'
        return retval

    def selectGetGroupJavascriptParams(self, orgID, groupID, parentID=None, search=False):
        return '%s,%s,%s, %s' % (groupID, orgID or "''", parentID or "''", (search and 1) or "''")

    def selectClassHasMembers(self, uniqueID, memberType):
        for section in SectionView(where="uniqueID=%s" % uniqueID).fetchall():
            return section.hasMembers(memberType)
        return False

    def getOrganizationQueryCriteria(self, groupID):
        if groupID and groupID != 'None':
            return QueryCriteriaView(where='personGroupID=%s AND fieldName="organizationID"'%groupID).fetchone()

    def getAccountQueryCriteria(self, groupID):
        if groupID and groupID != 'None':
            return QueryCriteriaView(where='personGroupID=%s AND fieldName="roleID"'%groupID).fetchone()

    def getQueryCriteria(self, groupID):
        criteria_list = []
        if self.get_param('criteria'):
            criteria_list = [{'fieldName':fieldName, 'operation':op, 'value':value} for fieldName, op, value in self.get_param('criteria')]
        elif groupID and groupID != 'None':
            criteria_list = QueryCriteriaView(where='personGroupID=%s AND fieldName NOT IN ("roleID","organizationID")' % groupID, order='fieldName').fetchall()
        if not criteria_list:
            criteria_list = [{}]
        for rowIndex, criteria in enumerate(criteria_list):
            rowIndex += 1
            criteria['queryFields'] = self.getQueryFields(rowIndex=rowIndex, queryField=criteria.get('fieldName'))
            criteria['queryOperations'] = self.getQueryOperations(rowIndex=rowIndex, queryField=criteria.get('fieldName'), queryOperation=criteria.get('operation'))
            criteria['queryValues'] = self.getQueryValues(rowIndex=rowIndex, queryField=criteria.get('fieldName'), queryOperation=criteria.get('operation'), queryValue=criteria.get('value'))
            criteria['rowIndex'] = rowIndex
        return criteria_list

    def getQueryFields(self, rowIndex, queryField=None):
        retval = '<select class="queryField" id="queryField_%s" name="queryField_%s" onchange="javascript:updateOperation(this);"><option value=""></option>' % (rowIndex, rowIndex)

        market = self.get_market()
        for groupName, groupList in fieldDescriptions:
            if market != 'K12' and fieldMcsExclusions[groupName] == 'All':
                continue
            retval += '<optgroup label="%s">' % groupName
            for fieldID, fieldName in groupList:
                if fieldID not in ['organizationID', 'roleID'] and (market == 'K12' or fieldID not in fieldMcsExclusions[groupName]):
                    if queryField == fieldID:
                        retval += '<option value="%s" selected>%s</options>' % (fieldID, fieldName)
                    else:
                        retval += '<option value="%s">%s</options>' % (fieldID, fieldName)
            retval += '</optgroup>'

        # Add the user defined fields.
        myOrgID = self.get_my_org_id()
        orgIDs = self.get_org(myOrgID)['allChildrenIDs']
        orgIDs.append(myOrgID)
        accExtraFields = [qf['name'] for qf in QueryFieldView(where = 'organizationID in (%s)' % ','.join(map(str,orgIDs)), group='name').generateall()]
        if accExtraFields:
            retval += '<optgroup label="Other">'
            for fieldName in accExtraFields:
                if queryField == fieldName:
                    retval += '<option value="%s" selected>%s</options>' % (fieldName, fieldName)
                else:
                    retval += '<option value="%s">%s</options>' % (fieldName, fieldName)
            retval += '</optgroup>'

        return retval + '</select>'

    def getQueryOperations(self, rowIndex, queryField=None, queryOperation=None, allowEmpty=True, default=None):
        retval = '<select class="queryOperation-narrow" id="queryOperation_%s" name="queryOperation_%s" onchange="updateValue(this)"><option value=""></option>' % (rowIndex, rowIndex)

        for opKey, opName in self.getOperations(queryField):
            if queryOperation == opKey:
                retval += '<option value="%s" selected>%s</option>' % (opKey, opName)
            else:
                retval += '<option value="%s">%s</option>' % (opKey, opName)

        return retval + '</select>'

    def getQueryValues(self, rowIndex, queryField=None, queryOperation=None, queryValue=None, default=None, textWidth='13em'):
        def addInput(rowIndex):
            data = {
                'fieldID':'queryValue_%s' % rowIndex,
                'fieldName':'queryValue_%s' % rowIndex,
                'value':(','.join(queryValue) if isinstance(queryValue, list) else queryValue) or ''
            }
            return self.render_to_string('main/messages/groups/addedit/inputvalue.html', data)

        def addSelect(rowIndex, options):
            return self.render_to_string('main/messages/groups/addedit/selectvalue.html', {'fieldID':'queryValue_%s' % rowIndex, 'fieldName':'queryValue_%s' % rowIndex, 'selectOptions':options})

        def addMultiSelect(rowIndex, options):
            fieldName = 'queryValue_%s' % rowIndex
            divID = 'multiSelect_%s' % rowIndex
            names = ','.join([opDict['displayName'] for opDict in options if opDict['selected']])
            return self.multiselectbox(fieldName=fieldName, divID=divID, names=names,
                                       selectOptions=options, narrow=True, isQueryCriteria=True)

        def getOrganizationTypes():
            orgTypes = OrganizationTypeView(where='market="%s"' % self.get_market()).fetchall()
            orgTypes.sort(cmpOrganizationType)
            return [(x['displayName'],x['id']) for x in orgTypes]

        if queryField in ['externalID', 'lastName', 'firstName', 'middleName', 'myID', 'replyToEmailAddress', 'replyToPhonNumber']:
            return addInput(rowIndex)

        elif queryOperation == 'exists' or queryField in ['hasUsedPassword', 'accountConfigured', 'locked']:
            options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue} for opName, opValue in [('True','true'), ('False','false')]]
            return addSelect(rowIndex, options)

        elif queryField == 'gender':
            options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue} for opName, opValue in [('Male','M'), ('Female','F')]]
            return addSelect(rowIndex, options)

        elif queryField in ['organizationType', 'preferredLanguage', 'teacherPersonID', 'attTeacher', 'gradeTeacher', 'assignmentTeacher', 'courseID', 'attCourse', 'gradeCourse', 'assignmentCourse', 'period', 'attPeriod', 'gradePeriod', 'assignmentPeriod', 'attCat', 'overallGrade', 'assignmentGrade', 'attCat']:
            if queryOperation in ['=', '!=', 'in', '!in']:
                if queryField == 'organizationType':
                    options = getOrganizationTypes()

                elif queryField == 'preferredLanguage':
                    options = [(lang['name'], lang['id']) for lang in self.get_enabled_languages()]

                elif queryField in ['teacherPersonID', 'attTeacher', 'gradeTeacher', 'assignmentTeacher']:
                    orgIDs = ','.join([str(orgID) for orgID in self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER'])])
                    options = self.getTeachers(orgIDs=orgIDs)

                elif queryField in ['courseID', 'attCourse', 'gradeCourse', 'assignmentCourse']:
                    orgIDs = ','.join([str(orgID) for orgID in self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER'])])
                    options = self.getCourses(orgIDs=orgIDs)

                elif queryField in ['attCat']:
                    orgIDs = ','.join([str(orgID) for orgID in self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER'])])
                    options = self.getCategories(orgIDs=orgIDs)

                elif queryField in ['overallGrade', 'assignmentGrade']:
                    orgIDs = ','.join([str(orgID) for orgID in self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER'])])
                    options = self.getGrades(orgIDs=orgIDs, assignments=queryField == 'assignmentGrade')

                else:
                    options = []

                if options and queryOperation in ['=', '!=']:
                    options = [{'name':opName, 'value':opValue, 'selected':str(opValue)==queryValue} for opName, opValue in options]
                    return addSelect(rowIndex, options)

                elif options and queryOperation in ['in', '!in']:
                    options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue or (queryValue and str(opValue) in queryValue), 'displayName':opName.replace('&nbsp;', '')} for opName, opValue in options]
                    return addMultiSelect(rowIndex,options)

                else:
                    return addInput(rowIndex)

            else:
                return addInput(rowIndex)

        elif queryField in ['period', 'attPeriod', 'gradePeriod', 'assignmentPeriod']:
            orgIDs = ','.join([str(orgID) for orgID in self.get_org_ids_by_capability(['SEND_TO_STUDENT', 'SEND_TO_PARENT', 'SEND_TO_STAFF', 'SEND_TO_OTHER'])])
            options = self.getPeriods(orgIDs=orgIDs)

            if options and queryOperation in ['in', '!in']:
                options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue or (queryValue and opValue in queryValue), 'displayName':opName.replace('&nbsp;', '')} for opName, opValue in options]
                return addMultiSelect(rowIndex,options)
            else:
                options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue} for opName, opValue in options]
                return addSelect(rowIndex, options)


        elif queryField in ['birthDate', 'attDate', 'assignmentDueDate']:
            options = [{'name':opName, 'value':opValue, 'selected':opValue==queryValue} for opName, opValue in [('Today','today'), ('Yesterday','yesterday'), ('Enter a date ...','date')]]
            retval = addSelect(rowIndex, options)
            # return retval + '&nbsp;&nbsp;<input type="text" name="birthDate%s_month" maxlength="2" size="2">/<input type="text" name="birthDate%s_day" maxlength="2" size="2">/<input type="text" name="birthDate%s_year" maxlength="4" size="4"> <i class="fa fa-calendar" onclick="displayPopUp(\'birthDate_calendar\', %s)"></i>' % (rowIndex, rowIndex, rowIndex, rowIndex)
            return retval + '&nbsp;&nbsp;<input type="text" id="birthDate%s"  name="birthDate" maxlength="25" size="12" style="display:none"/>'%rowIndex
        else:
            return addInput(rowIndex)

    def getTeachers(self, orgIDs):
        query = 'SELECT DISTINCT Person.id, CONCAT(Person.lastName, ", ", Person.firstName), Account.externalID FROM Account JOIN Person ON Account.personID=Person.id JOIN Role ON Role.id=Account.roleID WHERE Account.organizationID IN (%s) AND Role.roleType IN ("%s","%s") ORDER BY Person.lastName, Person.firstName' % (orgIDs, STAFF, TEACHER)
        return [('%s (%s)' % (tchName, tchID), str(personID)) for personID, tchName, tchID in self.execute_query(query).fetchall()]

    def getCourses(self, orgIDs):
        # TODO This query is slower than the old one. We need to look at optimizing it.
        # TODO Is this query supposed to be the same as the getTeachers query?
        query = 'SELECT DISTINCT Person.id, CONCAT(Person.lastName, ", ", Person.firstName), Account.externalID FROM Account JOIN Person ON Account.personID=Person.id JOIN Role ON Role.id=Account.roleID WHERE Account.organizationID IN (%s) AND Role.roleType IN ("%s","%s") ORDER BY Person.lastName, Person.firstName' % (orgIDs, STAFF, TEACHER)
        return [('%s (%s)' % (tchName, tchID), str(personID)) for personID, tchName, tchID in self.execute_query(query).fetchall()]

    def getCategories(self, orgIDs):
        query = 'SELECT DISTINCT code, description FROM AttendanceCode WHERE organizationID IN (%s) ORDER BY code' % orgIDs
        return [('%s (%s)' % (description.strip(), code.strip()), code.strip()) for code, description in self.execute_query(query).fetchall() if code.strip() and description.strip()]

    def getGrades(self, orgIDs, assignments=False):
        if assignments:
            query = 'SELECT DISTINCT grade FROM AssignmentScore WHERE organizationID IN (%s)' % orgIDs
        else:
            query = 'SELECT DISTINCT overallGrade FROM Grade WHERE organizationID IN (%s)' % orgIDs

        standard = ['A+','A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F']
        grades = [grade.strip() for grade, in self.execute_query(query).fetchall() if grade and grade.strip() and grade.strip() not in standard]
        grades.sort()
        standard.extend(grades)
        return [(grade, grade) for grade in standard]

    def getPeriods(self, orgIDs):
        query = 'SELECT DISTINCT period FROM Section WHERE organizationID IN (%s) ORDER BY period' % orgIDs
        periods = [period.strip() for period, in self.execute_query(query).fetchall()]
        intPeriods = []
        strPeriods = []

        for period in periods:
            if period:
                try:
                    period = int(period)
                except ValueError:
                    strPeriods.append(period)
                else:
                    intPeriods.append(period)

        intPeriods.sort()
        strPeriods.sort()

        return [(str(period), str(period)) for period in intPeriods+strPeriods]

    def advancedGetCriteria(self):
        rowIndex = self.get_param('rowIndex')
        queryField = self.get_param('queryField')
        queryOperation = self.get_param('queryOperation')
        queryValue = self.get_param('queryValue')
        selectRecordHTML = '<input type="checkbox" name="field_selectRecord:list" value="%s"/>' % rowIndex
        queryFieldHTML = self.getQueryFields(rowIndex=rowIndex, queryField=queryField)
        queryOperationHTML = self.getQueryOperations(rowIndex=rowIndex, queryField=queryField, queryOperation=queryOperation)
        queryValueHTML = self.getQueryValues(rowIndex=rowIndex, queryField=queryField, queryOperation=queryOperation, queryValue=queryValue)
        return self.response('''<?xml version="1.0" encoding="UTF-8"?>
          <criteria>
            <rowIndex>%s</rowIndex>
            <selectRecord><![CDATA[%s]]></selectRecord>
            <queryField><![CDATA[%s]]></queryField>
            <queryOperation><![CDATA[%s]]></queryOperation>
            <queryValue><![CDATA[%s]]></queryValue>
          </criteria>''' % (rowIndex, selectRecordHTML, queryFieldHTML, queryOperationHTML, queryValueHTML), content_type='text/xml')

    def advancedLoadQuery(self):
        q = self.get_param('q')
        queryParams = q.split('|')
        match = queryParams.pop(0)
        selectionCriteria = []
        personID = self.get_my_id()
        orgIDs = []
        orgOperation=None
        roleIDs = []
        roleOperation = None

        while len(queryParams) >= 3:
            fieldName, operation, value = queryParams[:3]
            queryParams = queryParams[3:]
            if fieldName == 'organizationID':
                orgOperation = operation
                orgIDs = value.split(',')
            elif fieldName == 'roleID':
                roleOperation = operation
                roleIDs = value.split(',')
            else:
                selectionCriteria.append((fieldName, operation, value))

        queryManager = QueryManager(personID=personID, match=match, queryCriteriaList=selectionCriteria, organizationIDs=orgIDs, organizationOperation=orgOperation, roleIDs=roleIDs, roleOperation=roleOperation)

        recipientPersonIDs = queryManager.execute()
        retval = ''
        addedRecipients = ''
        if recipientPersonIDs:
            try:
                recipients = [(person.getName(lastFirst=True), str(person['id'])) for person in PersonView(where='id IN (%s)'%(','.join(map(str,recipientPersonIDs))),fieldNames=['id','lastName','firstName']).generateall()]
                recipients.sort()
                retval = '<br>'.join([recipientName for recipientName, recipientID in recipients])
                dictionary = self.get_temp('memberDict') or self.defaultDict()
                dictionary['PREVIEW'] = set(recipients)
                self.set_temp('memberDict', dictionary)

            except:
                raise
                addedRecipients = 'error'
            else:
                addedRecipients = str(len(recipients))

        return self.json_response({'result':retval, 'addedRecipients':addedRecipients})


