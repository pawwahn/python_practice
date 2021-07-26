# >> called on auto initialization
def description(self):
    # autocase description
    self.setPurpose(purpose="GUI_Automation_Capture")

    # steps description
    self.step1 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step2 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step3 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step4 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step5 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step6 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)
    self.step7 = self.addStep(expected="Action executed with success", description="",
                              summary="", enabled=True, repeat=False, continueonException=False)


# >> called on auto preparation, adapters and libraries definitions


def prepare(self):
    # adapters and libraries definitions
    self.Window = System.GUI.Window(parent=self, agent=agent('BOT_GUI'), debug=input('DEBUG'))
    # self.Database = Database.SQL.MsSQL(parent=self, host='SQLDEV01', user='botdevdb01', password='Welcome123', port=1433, name=None, debug=False, shared=False, agent=agent('BOT_GUI'), agentSupport=True, logEventSent=True, logEventReceived=True, verbose=True)

    DB_HOST_CONF = shared(project='Common', name='DB_HOST_CONF', subname='')
    self.info(DB_HOST_CONF)

    DB_USER_CONF = shared(project='Common', name='DB_USER_CONF_username', subname='')
    self.info(DB_USER_CONF)

    DB_USER_CONF_PWD = shared(project='Common', name='DB_USER_CONF_password', subname='')
    DVCP = DB_USER_CONF_PWD
    self.info(DVCP)

    DB_PORT_CONF = shared(project='Common', name='DB_PORT_CONF', subname='')
    self.info(DB_PORT_CONF)

    DB_NAME_CONF = shared(project='Common', name='DB_NAME_CONF', subname='')
    self.info(DB_NAME_CONF)

    automaton_user = shared(project='Common', name='AUTOMATON_DB_USER_CONF_username', subname='')
    automaton_pwd = shared(project='Common', name='AUTOMATON_DB_USER_CONF_password', subname='')
    self.executor_user = shared(project='Common', name='AUTO_EXEC_USER_CONF_username', subname='')
    self.executor_pwd = shared(project='Common', name='AUTO_EXEC_USER_CONF_password', subname='')

    self.Database_automaton = Database.SQL.MySQL(parent=self, host='127.0.0.1', user=automaton_user,
                                                 password=automaton_pwd, port=3306, name=None, verbose=True,
                                                 debug=False, shared=False, agent=agent('BOT_GUI'), agentSupport=False,
                                                 logEventSent=True, logEventReceived=True)

    self.Database = Database.SQL.MsSQL(parent=self, host=str(DB_HOST_CONF), user=str(DB_USER_CONF),
                                       password=str(DB_USER_CONF_PWD), port=str(DB_PORT_CONF), name=None, debug=False,
                                       shared=False, agent=agent('BOT_GUI'), agentSupport=True, logEventSent=True,
                                       logEventReceived=True, verbose=True)

    self.Database.connect(dbName=str(DB_NAME_CONF), timeout=1)
    obj = self.Database.isConnected(timeout=1)
    self.DataCommunication = DataCommunication.LOCALHOST.XLSX(parent=self, agent=agent('BOT_GUI'), name=None,
                                                              debug=False, shared=False, agentSupport=True,
                                                              verbose=True, username=None, password=None, headers=None,
                                                              cookies=None)
    self.System = System.CLI.Windows(parent=self, agent=agent('BOT_GUI'), name=None, node='127.0.0.1', user=None,
                                     password=None, debug=False, shared=False, logEventSent=True, logEventReceived=True,
                                     nodes=None)
    # self.cmd = System.CLI.Windows(parent=self, agent=agent('BOT_GUI'), name=None, node='127.0.0.1', user=input('userWindows1'), password=input('passwordWindows2'), debug=False, shared=False, logEventSent=True, logEventReceived=True, nodes=input('nodesWindows3'))
    self.Database_automaton.connect(dbName="automaton", timeout=5)

    self.Data_QA = {}
    self.member_no = ''


# >> called on error or to cleanup the auto properly
def cleanup(self, aborted):
    self.Database_automaton.disconnect()
    # only for qa
    try:
        if self.member_no:
            for_qa.store_data(parent=self, agent=agent('BOT_GUI'), memberno=self.member_no, **self.Data_QA)
    except:
        pass


# >> called on auto begin


def definition(self):
    # CAPTURE>
    self.StepFailed = stepFailed.raise_exception
    import os
    import traceback
    if self.step1.isEnabled():
        self.step1.start()
        ### Manual Code Start ###---region=None,  similar=0.70, onAll=False, timeout=10.0---

        Result = True
        # process_id =1
        # process_name = 'one-off-payment'
        # task_name = 'bot_sale'
        # item_id = 2
        # updated_by = "automaton_sale_bot"

        import os
        script_path = os.path.abspath(__file__)
        process = get_process_item.details(parent=self, script_path=script_path)
        if process['status']:
            self.info(process['data'])
            data = process['data']
            process_id = data['process_ID']
            process_name = data['name']
            task_name = data['itemName']
            item_id = data['itemID']
            updated_by = data['itemName'].strip().replace(' ', '_') + "_task_bot"
            automatonTaskID = data['automatonTaskid']
        else:
            raise Exception("unable to fetch data for this script from items table.")

        LAUNCH_SIPP_PWD_CONF = shared(project='Common', name='LAUNCH_SIPP_USERNAME2_CONF_password', subname='')
        SIPP_EXE_LOC_CONF = shared(project='Common', name='SIPP_EXE_LOC_CONF', subname='')
        LAUNCH_SIPP_USERNAME_CONF = str(
            shared(project='Common', name='LAUNCH_SIPP_USERNAME2_CONF_username', subname=''))
        SIPP_ENV_CONF = str(shared(project='Common', name='SIPP_ENV_CONF', subname=''))
        shared_path = str(shared(project='Common', name='SHARED_PATH_CONF', subname=''))
        launch_sipp = r"start runas /user:group.net\{} {}".format(LAUNCH_SIPP_USERNAME_CONF, SIPP_EXE_LOC_CONF)

        sender_mail = str(shared(project='Common', name='SENDER_MAIL_CONF', subname=''))
        receiver_mail = str(shared(project='Common', name='RECEIVER_EMAIL_CONF', subname=''))
        technical_receiver_mail = str(shared(project='Common', name='TECHNICAL_RECEIVER_MAIL_CONF', subname=''))
        User_ID1 = str(shared(project='Common', name='TOM_USER1_CONF_username', subname=''))
        User_ID1_PWD = str(shared(project='Common', name='TOM_USER1_CONF_password', subname=''))
        User_ID2 = str(shared(project='Common', name='TOM_USER2_CONF_username', subname=''))
        User_ID2_PWD = str(shared(project='Common', name='TOM_USER2_CONF_password', subname=''))

        TOM_START = 'start iexplore'
        TOM_LINK_CONF = shared(project='Common', name='TOM_PATH_CONF', subname='')
        TOM_LINK_CONF = TOM_START + ' ' + TOM_LINK_CONF

        Member_sipp = "taskkill /IM {}.exe /F".format(SIPP_ENV_CONF)
        sipp_cmd = "runas /user:group.net\{} cmd.exe".format(LAUNCH_SIPP_USERNAME_CONF)

        processdata = sql_check.check_process_status(parent=self, data_pointer=self.Database_automaton,
                                                     processid=process_id)
        tasksdata = sql.sql_read_data(parent=self, data_pointer=self.Database_automaton, tablename='process_tasks',
                                      status='new', itemid=item_id)
        self.info(tasksdata)
        task = tasksdata.get('data').get('Data_Value')
        self.info(task)
        if task:
            task = task[0]
            task['processID'] = process_id
            taskid = task.get('taskID')
            memberno = task.get('memberNo')
            jobID = task.get('jobID')

            exception = []
            # uncomment this obj line below
            obj = sql_u.sql_update_data(parent=self, data_pointer=self.Database_automaton, tablename='process_tasks',
                                        taskid=taskid, memberno=memberno, updatedby=updated_by, status='inprogress',
                                        automatonTaskID=automatonTaskID)
            obj2 = sql_u.sql_update_data(parent=self, data_pointer=self.Database_automaton, tablename='process_jobs',
                                         jobid=jobID, memberno=memberno, updatedby=updated_by, status='inprogress')
            # self.info(obj)
            args1 = (
            self.Database_automaton, agent('BOT_GUI'), process_id, process_name, task_name, taskid, jobID, memberno,
            sender_mail, technical_receiver_mail, task)
            # self,step,data_pointer,agent,processid,process_name,item_name,taskid,jobID,memberno,sender_mail,receiver_mail,message
            inprogress_path = shared_path + "\\Inprogress"
            exception_path = shared_path + "\\Exception"

            # mail subject
            subject = f"Exception in Process name({process_name}) Task name({task_name}) Member number({memberno}) Jobid({jobID}) TaskID({taskid})"

            xlsx_file = os.path.join(inprogress_path, str(memberno), str(memberno) + str('.xlsx'))

            # check if someone deleted excel from inprogress folder
            obj = check_if_excel_exists.validate(parent=self, data_pointer=self.Database_automaton, filepath=xlsx_file,
                                                 taskid=taskid, process_name=process_name, task_name=task_name,
                                                 member_no=memberno, sender_mail=sender_mail,
                                                 receiver_mail=receiver_mail, subject=subject, task=task)

            # read from excel
            obj = read_lv_excel2.get_excel_data(self=self, agent=agent('BOT_GUI'), filepath=xlsx_file)
            Excel_Data = obj.get('data')
            self.info(Excel_Data)

            self.member_no = memberno
            self.Data_QA['excel_data'] = Excel_Data

        else:
            Result = False
        ### Manual Code End ###
        if Result:
            self.step1.setPassed('Executing with success: ')
        else:
            self.step1.setFailed('Step has an error,unable to execute ')
        self.step1.end()

    # CAPTURE>
    if self.step2.isEnabled():
        self.step2.start()
        ### Manual Code Start ###
        Result = True
        exception = []
        try:
            # killing sipp before opening
            obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                     LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)

            self.wait(10)
            self.Window.typeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r')
            self.wait(5)
            Result = self.Window.typeText(text='cmd', WindowTitle=None, className=None, controlID=None,
                                          timeout=input('TIMEOUT_GUI'))
            self.wait(5)
            self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            self.wait(5)
            Result = self.Window.typeText(text=launch_sipp, WindowTitle=None, className=None, controlID=None,
                                          timeout=input('TIMEOUT_GUI'))

            # obj = self.System.doCommand(cmd=launch_sipp, timeout=15)

            self.wait(10)
            self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            self.wait(5)
            Result = self.Window.typeText(text=LAUNCH_SIPP_PWD_CONF, WindowTitle=None, className=None, controlID=None,
                                          timeout=input('TIMEOUT_GUI'))
            self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            self.wait(20)
            Result = self.Window.typeText(text=memberno, WindowTitle=None, className=None, controlID=None,
                                          timeout=input('TIMEOUT_GUI'))
            self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            # self.wait(6)
            self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            # Remove enter code
            # self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
            self.wait(10)

            res = self.Window.doFindImage(image=input('IMG_20'), region=None, similar=0.70, timeout=10.0)
            if res:
                pass
            else:
                raise Exception('SIPP did not launch successfully.....')

            self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                     button='left', pressed='True', coords=(0, 0), accessname='Ne&xt Tab >>12',
                                     double=False, timeout=10.0)
            self.wait(10)
            # obj = read_lv_excel.get_excel_data(parent=self, filepath=r"C:\Users\SVC-vdibot-sys02\Desktop\InputDetails.xlsx")
            encashment = Excel_Data['Encashment']
            payment_amount = float(Excel_Data['Payment_amount'])
            adhoc_fee = Excel_Data['Adhoc_fee']

            taxcode_excel = Excel_Data['Tax_code']
            self.info('Tax code from excel------')
            self.info(taxcode_excel)
            self.info(obj)
            x = self.Database.query(
                query=f"SELECT COALESCE((SELECT SUM(V.AMOUNT) AS total FROM V_GetAmtPaidSinceAnniversary V JOIN ARRANGEMENTS A ON A.Arrangement_ID = V.arrangement_ID WHERE A.ID = {memberno} GROUP BY a.id), '0') AS Total",
                queryName=None)
            total = x.get('row_data')
            total_inception = total[0].get('Total')
            if total_inception == ' ':
                total_inception = 0
            total_inception = float(total_inception)
            total_inception = round(total_inception, 2)
            self.info('Total inception value------')
            self.info(total_inception)
            self.info(type(total_inception))
            self.Data_QA["total_inception"] = total_inception

            x = self.Database.query(query=f"select Tax_Code,Basis from Members where ID={memberno}", queryName=None)
            query = x.get('row_data')
            tax_code = query[0].get('Tax_Code')
            Basis = query[0].get('Basis')
            self.info('Tax code from DB------')
            self.info(tax_code)
            self.info(type(tax_code))
            self.info('Basis from DB------')
            self.info(Basis)
            self.Data_QA["tax_code"] = tax_code
            self.Data_QA["Basis"] = Basis

            # Tax-code

            if (tax_code in [None, 'NULL', ' ', '']):
                self.info("Tax code not present in SIPP")
                self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                         button='left', pressed='True', coords=(0, 0), accessname='Ne&xt Tab >>12',
                                         double=False, timeout=10.0)
                self.wait(2)
                self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                         button='left', pressed='True', coords=(0, 0), accessname='Edit28',
                                         double=False, timeout=10.0)
                self.wait(2)
                # self.Window.clickElement(title=u'SIPP Member Details',classname="ThunderRT6FormDC",controlID="",button='left', pressed='True', coords=(0,0),accessname='77', double=False,timeout=10.0)
                self.wait(2)
                self.Window.doTypeTextwindow(text=taxcode_excel, keysModifiers=[], image=None, similar=0.70,
                                             timeout=10.0)
                self.wait(1)
                self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                         button='left', pressed='True', coords=(0, 0), accessname='&Update11',
                                         double=False, timeout=10.0)
                self.wait(1)
                self.Window.clickElement(title=u'Update Member', classname="#32770", controlID="", button='left',
                                         pressed='True', coords=(0, 0), accessname='&Yes', double=False, timeout=10.0)
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                          timeout=10.0)
                self.wait(2)
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                          timeout=10.0)
                self.wait(2)
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                          timeout=10.0)
                self.wait(2)
                # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
                # self.wait(2)
                proceed_302 = True
            elif (tax_code != taxcode_excel):
                proceed_302 = True
            else:
                self.info("Tax code is present")
                if (tax_code == taxcode_excel):
                    if (Basis == '1'):
                        self.info("success and proceed to 3.02 and basis value is 1")
                        # Result = True
                        proceed_302 = True
                    elif (Basis == '0'):
                        if (total_inception == 0):
                            self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC",
                                                     controlID="", button='left', pressed='True', coords=(0, 0),
                                                     accessname='0 - Standard', double=False, timeout=10.0)
                            self.wait(2)
                            Result = self.Window.doTypeTextwindow(text='1', keysModifiers=[], image=None, similar=0.70,
                                                                  timeout=10.0)
                            self.wait(2)
                            self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC",
                                                     controlID="", button='left', pressed='True', coords=(0, 0),
                                                     accessname='&Update11', double=False, timeout=10.0)
                            self.wait(1)
                            self.Window.clickElement(title=u'Update Member', classname="#32770", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='&Yes',
                                                     double=False, timeout=10.0)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(2)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(2)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(2)
                            proceed_302 = True
                        else:
                            proceed_302 = True
                            Result = True
                            self.info("success and proceed to 3.02")
                else:
                    self.info("Tax_code in SIPP does not match with excel")
                    proceed_302 = True
        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)
        ### Manual Code End ###
        if Result:
            self.step2.setPassed('Executing with success: ')
        else:
            obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                     LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
            self.StepFailed(self, 'step2 Check Tax code(3.01)', *args1, message=message)
            self.step2.setFailed('Step has an error,unable to execute ')
        self.step2.end()

    # CAPTURE>
    if self.step3.isEnabled():
        self.step3.start()
        ### Manual Code Start ###
        Reference_Number = Excel_Data['Encashment']
        Result = True
        proceed_bot_sale = True
        try:
            client_exception = False
            if proceed_302:
                n = 10
                self.info(Excel_Data['Encashment'])
                # Checking encashment rule
                if Excel_Data['Encashment'].lower() == 'cash':
                    self.info("Encashment rule is CASH so avoilding BRD 3.02(TOM Encashment)")
                    proceed_bot_sale = False
                    obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                    workflow_change.updatestatus(parent=self, data=task, status="completed")

                else:
                    for j in range(n):
                        self.info("###################################################################")
                        self.info(j)
                        self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                                  timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeTextwindow(text=input('TEXT_2'), keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                  timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeTextwindow(text=input('Cmd_Kill'), keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                  timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                                  timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeTextwindow(text=input('TEXT_2'), keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                  timeout=10.0)
                        # working till here----->
                        self.wait(3)
                        self.Window.doTypeTextwindow(text=input('Kill_IE'), keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                  timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeTextwindow(text=TOM_LINK_CONF, keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                  timeout=10.0)
                        self.wait(10)
                        # self.wait(3)
                        # self.Window.doTypeTextwindow( text=input('TEXT_7'),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                        self.Window.doTypeTextwindow(text=User_ID1, keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.wait(3)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                  timeout=10.0)
                        self.wait(3)
                        # self.Window.doTypeTextwindow( text=input('TEXT_9'),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                        self.Window.doTypeTextwindow(text=User_ID1_PWD, keysModifiers=[], image=None, similar=0.70,
                                                     timeout=10.0)
                        self.wait(3)
                        self.Window.doClickImage(image=input('Validate_IMG'), region=None, similar=0.70, onAll=False,
                                                 timeout=10.0)
                        self.wait(input('WAIT_5_seconds'))
                        self.wait(3)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F5, other=None,
                                                  timeout=10.0)
                        self.wait(input('WAIT_5_seconds'))
                        # handling error
                        self.wait(10)
                        try:
                            self.info("************************************************")
                            Result = self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70,
                                                              onAll=False, timeout=10.0)
                            self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None, other='a',
                                                      timeout=10.0)
                            self.Window.doTypeShorcut(key=None, modifier=System.GUI.KEY_CTRL,
                                                      special=System.GUI.KEY_INSERT, other=None, timeout=10.0)
                            self.wait(2)
                            Tom_Data = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT,
                                                                  timeout=input('TIMEOUT_GUI'))
                            self.info(Tom_Data)
                            Tom_Data = Tom_Data.decode()
                            Log_ON = "LOGON"
                            if Log_ON in Tom_Data:
                                self.info("Reached on Tom Window")
                                self.wait(3)
                                self.info("working")
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB,
                                                          other=None, timeout=10.0)
                                self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                          special=System.GUI.KEY_END, other=None, timeout=10.0)
                                self.wait(1)
                                Result = self.Window.doTypeTextwindow(text=input('TEXT_15'), keysModifiers=[],
                                                                      image=None, similar=0.70, timeout=10.0)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB,
                                                          other=None, timeout=10.0)
                                self.wait(1)
                                Result = self.Window.doTypeTextwindow(text=Reference_Number, keysModifiers=[],
                                                                      image=None, similar=0.70, timeout=10.0)
                                self.wait(3)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                          other=None, timeout=10.0)
                                self.wait(3)
                                self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70,
                                                         onAll=False, timeout=10.0)
                                self.wait(1)
                                self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None,
                                                          other='a', timeout=10.0)
                                self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=System.GUI.KEY_INSERT,
                                                          special=None, other='c', timeout=10.0)
                                # Include Code here for Pasting
                                self.wait(2)
                                Tom_Data = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT,
                                                                      timeout=input('TIMEOUT_GUI'))
                                comma = ','

                                import re
                                self.info("Tom_Data ----------------------------------------------------->")
                                self.info(Tom_Data)
                                string_for_matching = b"\xc2\xa3([^\s]+)(  ULA39| No Exit Charge Applies  ULA39)"
                                # | Backdated two policy years - contact Actuarial for exit charges  ULA39| Remaining Encashment Allowance WS-EC-VALUE-OUT-100000 Max Exit Charge WS-ZEN-XC-AMT-OUT  ULA39| An Exit Charge of WS-EC-VALUE-OUT-1 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-10 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-100 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-1000 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-10000 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-100000 applies if policy terminates during first year.  ULA39| An Exit Charge of WS-EC-VALUE-OUT-1000000 applies if policy terminates during first year.  ULA39
                                x = re.findall(string_for_matching, Tom_Data)
                                if not x:
                                    # TOM logout
                                    self.wait(5)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                              special=System.GUI.KEY_END, other=None, timeout=10.0)
                                    self.wait(5)
                                    Result11 = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None,
                                                                            similar=0.70, timeout=10.0)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)

                                    # Closing all windows
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None,
                                                              other='r', timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T',
                                                                 keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    obj = KillSIPP.kill_sipp(parent=self,
                                                             LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF,
                                                             SIPP_ENV_CONF=SIPP_ENV_CONF)
                                    workflow_change.updatestatus(parent=self, data=task, status="exception")
                                    client_exception = True
                                    exception = [
                                        "Could not find Total Value from TOM Screen;Some other message than 'No Exit Charge Applies' came"]
                                    mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                                    sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail,
                                                      reciever=receiver_mail, subject=subject,
                                                      message=mail_body['data'], files=[])
                                    raise Exception(
                                        "Could not find Total Value from TOM Screen;Some other message than 'No Exit Charge Applies' came")
                                value = x[0][0]
                                self.info(value)
                                Tom_Final_Value = value.decode("utf-8")
                                if comma in Tom_Final_Value:
                                    Tom_Final_Value = Tom_Final_Value.replace(',', '')
                                    self.info("This is Tom Final Value------------>")
                                    Tom_Final_Value_Float = float(Tom_Final_Value)
                                    self.info(type(Tom_Final_Value_Float))
                                    self.info(Tom_Final_Value_Float)
                                else:
                                    self.info("Comma Not found!")

                                Policy_number = Excel_Data['Policy_number']

                                x = self.Database.query(
                                    query="SELECT sum(b.transaction_amount) FROM BANK_TRANSACTIONS B LEFT JOIN INVESTMENTS I on I.Investment_ID=B.Investment_ID WHERE B.Transaction_Code=1832 AND I.ID =" + str(
                                        memberno) + " AND (Statement_Date IS NULL OR Settlement_Date IS NULL) group by b.Transaction_Code",
                                    queryName=None)
                                self.info(x)
                                self.info("This is Pending_Amount--------->")
                                final = x["row_data"]
                                self.info("My final is {}".format(final))
                                if (isinstance(final, list) == True and len(final) == 0) or final in ['', " ", None,
                                                                                                      'NULL', 'None']:
                                    Pending_Amount = 0
                                else:
                                    Pending_Amount = (final[0].get(""))
                                Pending_Amount = float(Pending_Amount)
                                self.info(type(Pending_Amount))
                                self.info(Pending_Amount)

                                self.Data_QA["Pending_Amount"] = Pending_Amount

                                self.info("one_off_payment Amount is -------------------------------------------->")
                                self.info(Excel_Data['Payment_amount'])
                                self.info("Ad_Hoc Amount is -------------------------------------------->")
                                if Excel_Data['Adhoc_fee'] in ['', " ", None, 'NULL', 'None']:
                                    Excel_Data['Adhoc_fee'] = 0
                                self.info(Excel_Data["Adhoc_fee"])
                                Total_Amount = float(Excel_Data['Payment_amount']) + float(
                                    Excel_Data['Adhoc_fee']) + Pending_Amount
                                self.info("Total_Amount is  --------------------->")
                                self.info(Total_Amount)
                                self.info("This is Tom Final Value------------>")
                                self.info(Tom_Final_Value_Float)
                                # Next part will come here
                                if Total_Amount < Tom_Final_Value_Float:
                                    self.info("Proceed to ---->TOM Pending actions - ULA 30")
                                else:
                                    self.info("Insufficient funds")

                                    # TOM logout
                                    self.wait(5)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                              special=System.GUI.KEY_END, other=None, timeout=10.0)
                                    self.wait(5)
                                    Result11 = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None,
                                                                            similar=0.70, timeout=10.0)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)

                                    # Closing all windows
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None,
                                                              other='r', timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T',
                                                                 keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    obj = KillSIPP.kill_sipp(parent=self,
                                                             LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF,
                                                             SIPP_ENV_CONF=SIPP_ENV_CONF)
                                    workflow_change.updatestatus(parent=self, data=task, status="exception")
                                    client_exception = True
                                    exception = ["Insufficient Funds"]
                                    mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                                    sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail,
                                                      reciever=receiver_mail, subject=subject,
                                                      message=mail_body['data'], files=[])
                                    # raise Exception
                                    raise Exception("Insufficient Funds")

                                break
                            else:
                                self.info("Reached Wrong window :((((")
                                self.wait(3)
                                if j == n - 1:
                                    raise ValueError
                        except ValueError:
                            # Closing all windows
                            self.wait(3)
                            self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                                      timeout=10.0)
                            self.wait(3)
                            self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                         timeout=10.0)
                            self.wait(3)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(3)
                            self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[],
                                                         image=None, similar=0.70, timeout=10.0)
                            self.wait(3)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(3)
                            obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                                     LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF,
                                                     SIPP_ENV_CONF=SIPP_ENV_CONF)
                            workflow_change.updatestatus(parent=self, data=task, status="exception")
                            client_exception = True
                            exception = ["3.02 - We have tried 10 times! TOM Application is not Reachable"]
                            mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                            # self.info(mail_body['data']
                            sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail, reciever=receiver_mail,
                                              subject=subject, message=mail_body['data'], files=[])
                            raise Exception("3.02 - We have tried 10 times! TOM Application is not Reachable")

        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)

        ### Manual Code End ###step3 TOM Encashment(3.02)
        if Result:
            self.step3.setPassed('Executing with success: ')
        else:
            if not client_exception:
                obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                self.StepFailed(self, 'TOM Encashment ULA39', *args1, message=message)
            self.step3.setFailed('Step has an error,unable to execute ')
        self.step3.end()

    # CAPTURE>
    if self.step4.isEnabled():
        self.step4.start()
        ### Manual Code Start ###
        Result = True
        # 3.03
        try:
            client_exception = False
            if proceed_bot_sale:
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None, timeout=10.0)
                self.wait(2)
                self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END,
                                          other=None, timeout=10.0)
                self.wait(input('WAIT_5_seconds'))
                Result = self.Window.doTypeTextwindow(text=input('ULA_TEXT'), keysModifiers=[], image=None,
                                                      similar=0.70, timeout=10.0)
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None, timeout=10.0)
                self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END,
                                          other=None, timeout=10.0)
                self.wait(input('WAIT_5_seconds'))
                Result = self.Window.doTypeTextwindow(text=Reference_Number, keysModifiers=[], image=None, similar=0.70,
                                                      timeout=10.0)
                self.wait(2)
                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                          timeout=10.0)
                self.wait(3)
                self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False, timeout=10.0)
                self.wait(3)
                self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None, other='a', timeout=10.0)
                self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None, other='c', timeout=10.0)
                self.wait(10)

                tom_pd_data = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT,
                                                         timeout=input('TIMEOUT_GUI'))
                tom_pd_data = tom_pd_data.decode()
                self.info(tom_pd_data)
                self.wait(2)
                match = "No Pending Action Details for this Benefit"
                match_SURR = "SURR"
                match_SWIT = "SWIT"
                match_DETH = "DETH"

                if match in tom_pd_data:
                    self.info("YES, No pending actions.You can proceed to next step (3.04 -TOM Sale)")
                elif (match_SURR in tom_pd_data) or (match_SWIT in tom_pd_data) or (match_DETH in tom_pd_data):

                    # TOM logout
                    self.wait(5)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END,
                                              other=None, timeout=10.0)
                    self.wait(5)
                    Result11 = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None, similar=0.70,
                                                            timeout=10.0)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)

                    # Closing all windows
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70, timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[], image=None,
                                                 similar=0.70, timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                    workflow_change.updatestatus(parent=self, data=task, status="exception")
                    client_exception = True
                    exception = ["Pending actions in TOM"]
                    mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                    # self.info(mail_body['data']
                    sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail, reciever=receiver_mail,
                                      subject=subject, message=mail_body['data'], files=[])
                    # Now raising Exception
                    raise Exception("Pending actions in TOM")



                else:
                    self.info("Un-Supported Transaction Type detected")

                    # #TOM logout
                    # self.wait(5)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None)
                    # self.wait(3)
                    # self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END, other=None)
                    # self.wait(5)
                    # Result11 = self.Window.doTypeTextwindow( text= 'BYE' ,WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)

                    # #Closing all windows
                    # self.wait(3)
                    # self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r')
                    # self.wait(3)
                    # self.Window.doTypeTextwindow( text='cmd',WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                    # self.wait(3)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
                    # self.wait(3)
                    # self.Window.doTypeTextwindow( text='taskkill /F /IM iexplore.exe /T',WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                    # self.wait(3)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
                    # self.wait(3)
                    # self.Window.doTypeTextwindow(text=input('Cmd_Kill'),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI'))
                    # self.wait(2)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)

                    # #Now raising Exception
                    # raise Exception("Un-Supported Transaction Type detected")
        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)
        ### Manual Code End ###step4:TOM Pending actions ULA 30(3.03)
        if Result:
            self.step4.setPassed('Executing with success: ')
        else:
            if not client_exception:
                obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                self.StepFailed(self, 'TOM Pending actions ULA30', *args1, message=message)
            self.step4.setFailed('Step has an error,unable to execute ')
        self.step4.end()

    # CAPTURE>
    if self.step5.isEnabled():
        self.step5.start()
        ### Manual Code Start ###
        Result = True
        # 3.04
        try:
            client_exception = False
            if proceed_bot_sale:
                # self.Window.doClickImage( img=input('IMG_1'), description='Clicking on IE Icon', similar=input('SIMILAR_GUI') )

                # self.wait(input('WAIT_2'))

                # self.Window.doClickImage( img=input('IMG_3'), description='Clicking on Trinity_Liverpool - Web Framework', similar=input('SIMILAR_GUI') )

                def TomSale_func():
                    # Waiting
                    self.wait(5)
                    # Giving F1->To come at home page
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None,
                                              timeout=10.0)
                    # Waiting
                    self.wait(3)
                    # Typing ULA96
                    Result = self.Window.doTypeTextwindow(text='ULA96', keysModifiers=[], image=None, similar=0.70,
                                                          timeout=10.0)
                    # Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)

                    # import datetime
                    Sale_date = Excel_Data['Sale_date']
                    Sale_date = Sale_date.replace('/', '')
                    self.info(Sale_date)
                    if Excel_Data['Adhoc_fee'] in ['', " ", None, 'NULL', 'None']:
                        Excel_Data['Adhoc_fee'] = 0
                    Amount_to_encash = round((float(Excel_Data['Payment_amount']) + float(Excel_Data['Adhoc_fee'])), 2)
                    Investment_Reference = Excel_Data['Encashment']
                    Splits = []
                    Fund_code = []
                    count1 = 0
                    count2 = 0
                    for key in Excel_Data:
                        if ('Split' in key) and ('Split-n' not in key):
                            count1 += 1
                    self.info("My count1 is {}".format(count1))
                    for i in range(count1):
                        if Excel_Data['Split-' + str(i + 1)] not in ['None', None, 'Null', '', " "]:
                            count2 += 1
                    self.info("My count2 is {}".format(count2))
                    for i in range(count2):
                        for key in Excel_Data:
                            if key == ('Split-' + str(i + 1)):
                                Splits.append(float(Excel_Data[key]))
                            elif key == ('Fund_code-' + str(i + 1)):
                                Fund_code.append(int(Excel_Data[key]))
                    self.info(Splits)
                    self.info(Fund_code)

                    Fund_amt = []
                    if count2 != 1:
                        for i in range(count2):
                            if i != (count2 - 1):
                                Fund_amount = round(((Splits[i] / 100) * (Amount_to_encash)), 2)
                                Fund_amt.append(Fund_amount)
                            else:
                                s = sum(Fund_amt)
                                Remaining_amt = round((Amount_to_encash - s), 2)
                                Fund_amt.append(Remaining_amt)
                    else:
                        # Fund_amount=round(((Excel_Data.Split[0]/100)*(Amount_to_encash)),2)
                        Fund_amount = Amount_to_encash
                        Fund_amt.append(Fund_amount)

                    for i in range(count2):
                        self.info(Splits[i])
                        self.info(type(Splits[i]))
                        self.info(Fund_code[i])
                        self.info(type(Fund_code[i]))
                        self.info(Fund_amt[i])
                        self.info(type(Fund_amt[i]))

                    self.info("One off payment amount is:")
                    self.info(Excel_Data['Payment_amount'])
                    self.info("Ad hoc fee is:")
                    self.info(Excel_Data['Adhoc_fee'])
                    # self.info(Total_Amount)
                    self.info("Investment reference is:")
                    self.info(Excel_Data['Encashment'])
                    self.info(type(Excel_Data['Encashment']))
                    self.info("Sale date is :")
                    self.info(Excel_Data['Sale_date'])
                    self.info("My required Sale date is:")
                    self.info(Sale_date)

                    Result1 = self.Window.doTypeTextwindow(text=Investment_Reference, keysModifiers=[], image=None,
                                                           similar=0.70, timeout=10.0)
                    # Giving Enter
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(5)
                    ##CAPTURE>Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(2)
                    ##CAPTURE>Typing Investment Reference
                    for i in range(len(Investment_Reference)):
                        if i == 0:
                            Result2 = self.Window.pasteText(text=str(Investment_Reference[i]),
                                                            timeout=input('TIMEOUT_GUI'))
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                        else:
                            Result2 = self.Window.pasteText(text=str(Investment_Reference[i]),
                                                            timeout=input('TIMEOUT_GUI'))
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(2)
                    ##CAPTURE>Typing Benefit Reference Value
                    Benefit_Reference_Value = '01'
                    Result3 = self.Window.doTypeTextwindow(text=Benefit_Reference_Value, keysModifiers=[], image=None,
                                                           similar=0.70, timeout=10.0)
                    ##CAPTURE>Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    ##CAPTURE>Typing Effective Date->my_req_sale_date
                    Result4 = self.Window.doTypeTextwindow(text=str(Sale_date), keysModifiers=[], image=None,
                                                           similar=0.70, timeout=10.0)
                    self.wait(2)
                    ##CAPTURE>Typing Transaction Type input('TEXT_13')
                    Result5 = self.Window.pasteText(text=str('SURP'), timeout=input('TIMEOUT_GUI'))
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    ##CAPTURE>Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    ##CAPTURE>Typing Unit Type input('TEXT_14')

                    Result6 = self.Window.pasteText(text=str('S'), timeout=input('TIMEOUT_GUI'))
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    ##CAPTURE>Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    ##CAPTURE>Typing Add/Subtract input('TEXT_16')
                    Result7 = self.Window.pasteText(text=str('S'), timeout=input('TIMEOUT_GUI'))
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    ##CAPTURE>Giving Tab
                    for i in range(3):
                        self.wait(1)
                        self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                  timeout=10.0)
                    Minus = '-'
                    self.wait(1)
                    for i in range(count2):
                        if i != ((count2) - 1):
                            self.wait(1)
                            Result8 = self.Window.pasteText(text=str(Fund_code[i]), timeout=input('TIMEOUT_GUI'))
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                            Result9 = self.Window.doTypeTextwindow(text=Minus, keysModifiers=[], image=None,
                                                                   similar=0.70, timeout=10.0)
                            Result10 = self.Window.doTypeTextwindow(text=str(Fund_amt[i]), keysModifiers=[], image=None,
                                                                    similar=0.70, timeout=10.0)
                            # Result2 = self.Window.doTypeTextwindow( text=input('{0:.1f}'.format(Fund_amt[i])),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                            for j in range(2):
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB,
                                                          other=None, timeout=10.0)
                        else:
                            self.wait(1)
                            Result8 = self.Window.pasteText(text=str(Fund_code[i]), timeout=input('TIMEOUT_GUI'))
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                            Result9 = self.Window.doTypeTextwindow(text=Minus, keysModifiers=[], image=None,
                                                                   similar=0.70, timeout=10.0)
                            Result10 = self.Window.doTypeTextwindow(text=str(Fund_amt[i]), keysModifiers=[], image=None,
                                                                    similar=0.70, timeout=10.0)
                    self.wait(10)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(25)
                    # Clicking on the ULADE96
                    self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                             timeout=10.0)
                    # self.wait(1)
                    # Selecting Everything
                    self.wait(2)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None, other='a',
                                              timeout=10.0)
                    # Copying Entire data
                    self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=System.GUI.KEY_INSERT,
                                              other=None, timeout=10.0)

                TomSale_func()
                self.wait(3)
                # Pasting data and checking for the required output
                test_str = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT,
                                                      timeout=input('TIMEOUT_GUI'))
                self.info(test_str)
                string_obt = test_str.decode()
                # import re
                pattern = "The Gross Value has been calculated"
                if pattern in string_obt:
                    self.info(
                        "The required pattern -> N.B. - The Gross Value has been calculated is Found. Therefore you can proceed.")
                    self.wait(1)
                    self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                             timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(5)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END,
                                              other=None, timeout=10.0)
                    self.wait(5)
                    Result11 = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None, similar=0.70,
                                                            timeout=10.0)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                else:
                    self.info(
                        "The required pattern -> N.B. - The Gross Value has been calculated is Not Found. Therefore can't proceed")
                    self.wait(1)
                    self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                             timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None, special=System.GUI.KEY_END,
                                              other=None, timeout=10.0)
                    self.wait(5)
                    Result11 = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None, similar=0.70,
                                                            timeout=10.0)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70, timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[], image=None,
                                                 similar=0.70, timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    # SIPP Closing/KILL
                    obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                    workflow_change.updatestatus(parent=self, data=task, status="exception")
                    client_exception = True
                    exception = [
                        "The required pattern -> N.B. - The Gross Value has been calculated is Not Found. Therefore can't proceed"]
                    mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                    # self.info(mail_body['data']
                    sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail, reciever=receiver_mail,
                                      subject=subject, message=mail_body['data'], files=[])
                    raise Exception(
                        "The required pattern -> N.B. - The Gross Value has been calculated is Not Found. Therefore can't proceed")
        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)
        ### Manual Code End ###
        if Result:
            self.step5.setPassed('Executing with success: ')
        else:
            if not client_exception:
                obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                self.StepFailed(self, 'TOM Sale ULA96', *args1, message=message)

            self.step5.setFailed('Step has an error,unable to execute ')
        self.step5.end()

    # CAPTURE>
    if self.step6.isEnabled():
        self.step6.start()
        ### Manual Code Start ###
        Result = True
        # 3.05
        try:
            client_exception = False
            if proceed_bot_sale:
                # *****IMPORTANT*****The username of the processor can change in production
                Username_of_processor = User_ID1  # input('TEXT_7')

                def Login_func():
                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                              timeout=10.0)
                    # Waiting
                    self.wait(5)
                    ##CAPTURE>Typing cmd
                    Result = self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                          timeout=10.0)
                    ##CAPTURE>Giving Enter
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    # Waiting
                    self.wait(5)
                    self.Window.doTypeTextwindow(text='taskkill /IM cmd.exe /F', keysModifiers=[], image=None,
                                                 similar=0.70, timeout=10.0)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70, timeout=10.0)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    # Clsoing all IE Windows
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[], image=None,
                                                 similar=0.70, timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    # Typing command for opening a link in IE
                    Result = self.Window.doTypeTextwindow(text=TOM_LINK_CONF, keysModifiers=[], image=None,
                                                          similar=0.70, timeout=10.0)
                    ##CAPTURE>Giving Enter
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    # Waiting
                    self.wait(10)
                    ##CAPTURE>Typing Username
                    Result = self.Window.doTypeTextwindow(text=User_ID2, keysModifiers=[], image=None, similar=0.70,
                                                          timeout=10.0)
                    ##CAPTURE>Giving Tab
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                              timeout=10.0)
                    ##CAPTURE>Typing Password ->input('TEXT_9')
                    # Result=self.Window.doTypeTextwindow( text=input('TEXT_9'),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                    Result = self.Window.doTypeTextwindow(text=User_ID2_PWD, keysModifiers=[], image=None, similar=0.70,
                                                          timeout=10.0)
                    # Waiting
                    self.wait(3)
                    ##CAPTURE>Clicking on Validation
                    self.Window.doClickImage(image=input('Validate_IMG'), region=None, similar=0.70, onAll=False,
                                             timeout=10.0)
                    # Waiting
                    self.wait(2)
                    ##CAPTURE>Refreshing page
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F5, other=None,
                                              timeout=10.0)
                    # Waiting
                    self.wait(6)
                    # self.wait(20)

                def Copy_func():
                    self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=None, other='a',
                                              timeout=10.0)
                    self.wait(1)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=System.GUI.KEY_INSERT,
                                              other=None, timeout=10.0)
                    self.wait(2)
                    test_str = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT,
                                                          timeout=input('TIMEOUT_GUI'))
                    self.wait(1)
                    self.info(test_str)
                    self.info("My string is:")
                    Copy_func.test_str = test_str.decode()
                    self.info(Copy_func.test_str)
                    self.info(type(Copy_func.test_str))

                def Data_processing_func():
                    import re
                    Copy_func()
                    Copied_string = Copy_func.test_str
                    lst1 = []
                    lst2 = []
                    lst3 = []
                    lst4 = []
                    dict = {}
                    Data_processing_func.Not_Null_ID = []
                    n = len(Copied_string)
                    self.info("The length of copied string is:{}".format(n))
                    x = re.split(Username_of_processor, Copied_string, 1)
                    lst1 = x[1]
                    y = re.split("REVIEW", lst1, 1)
                    lst2 = y[0]
                    self.info("The Required String is {} {} and it's length is {} ".format(lst2, '\n', len(lst2)))

                    count = int((len(lst2)) / 65)
                    self.info("Count of rows is:", count)
                    for j in range(count):
                        for i in range(len(lst2)):
                            if i == (len(lst2) - 3):
                                break
                            else:
                                if (lst2[i] + lst2[i + 1] + lst2[i + 2] + lst2[i + 3]) == ' 0' + str(int(j) + 1) + ' ':
                                    self.info("Index is {}".format(i))
                                    lst3.append(int(i))
                                elif (lst2[i] + lst2[i + 1] + lst2[i + 2] + lst2[i + 3]) == ' ' + str(int(j) + 1) + ' ':
                                    self.info("Index is {}".format(i))
                                    lst3.append(int(i))
                    self.info(lst3)

                    for i in range(0, len(lst3), 2):
                        key = lst2[(int(lst3[i]) + 1):(int(lst3[i]) + 3)]
                        val = lst2[(int(lst3[i]) + 4):(int(lst3[i + 1] + 1))]
                        dict[key] = val
                    self.info(dict)
                    Investment_ref = str(Excel_Data['Encashment'])
                    self.info('My investment reference is {}'.format(Investment_ref))
                    input_values = dict
                    for i in range(count):
                        if i < 9:
                            val = input_values['0' + str(i + 1)]
                            if Investment_ref in val:
                                self.info('Found at {} row'.format(i + 1))
                                if " V " in val:
                                    self.info("Status of movement is found at ID {}".format('0' + str(i + 1)))
                                    Data_processing_func.Not_Null_ID.append(('0' + str(i + 1)))
                                else:
                                    Data_processing_func.First_Null_ID = ('0' + str(i + 1))
                                    self.info("My First Null ID is {}".format(Data_processing_func.First_Null_ID))
                                    break
                        else:
                            val = input_values[str(i + 1)]
                            if Investment_ref in val:
                                self.info('Found at row {}'.format(i + 1))
                                if " V " in val:
                                    self.info("Status of movement is found at ID {}".format(str(i + 1)))
                                    Data_processing_func.Not_Null_ID.append(str(i + 1))
                                else:
                                    Data_processing_func.First_Null_ID = str(i + 1)
                                    self.info("My First Null ID is {}".format(Data_processing_func.First_Null_ID))
                                    break

                n = 10
                try:
                    for i in range(n):
                        Login_func()
                        self.wait(10)
                        self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                                 timeout=10.0)
                        self.wait(2)
                        Copy_func()
                        self.wait(2)

                        pattern2 = "LOGON"
                        if pattern2 in Copy_func.test_str:
                            self.info("Logon message Found")
                            ##CAPTURE>Giving Tab
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                            # Giving Shift+End
                            self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                      special=System.GUI.KEY_END, other=None, timeout=10.0)
                            ##CAPTURE>Typing in Next Transaction
                            Result = self.Window.doTypeTextwindow(text='REVIEW', keysModifiers=[], image=None,
                                                                  similar=0.70, timeout=10.0)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                            ##CAPTURE>Typing in Reference Input Field
                            Result = self.Window.doTypeTextwindow(text='ULA/', keysModifiers=[], image=None,
                                                                  similar=0.70, timeout=10.0)
                            ##CAPTURE>Typing Username of the processor->input('TEXT_20')
                            Result = self.Window.doTypeTextwindow(text=str(Username_of_processor), keysModifiers=[],
                                                                  image=None, similar=0.70, timeout=10.0)
                            ##CAPTURE>Giving Enter
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            # Waiting
                            self.wait(2)
                            # Clicking on REVIEW
                            self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                                     timeout=10.0)
                            Copy_func()
                            self.wait(2)
                            Data_processing_func()
                            First_Null_ID_Replica = Data_processing_func.First_Null_ID
                            self.info("My replica of First Null ID is {}.".format(First_Null_ID_Replica))
                            # Waiting
                            self.wait(2)
                            # Giving tab
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_TAB, other=None,
                                                      timeout=10.0)
                            self.wait(3)
                            Result = self.Window.doTypeTextwindow(text=str(Data_processing_func.First_Null_ID),
                                                                  keysModifiers=[], image=None, similar=0.70,
                                                                  timeout=10.0)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(3)
                            Result = self.Window.doTypeTextwindow(text='V', keysModifiers=[], image=None, similar=0.70,
                                                                  timeout=10.0)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                                      timeout=10.0)
                            self.wait(2)
                            self.Window.doClickImage(image=input('Blue_IMG'), region=None, similar=0.70, onAll=False,
                                                     timeout=10.0)
                            Copy_func()
                            self.wait(2)
                            pattern3 = 'REVIEW'
                            if pattern3 in Copy_func.test_str:
                                self.wait(2)
                                Data_processing_func()
                                self.wait(2)
                                if First_Null_ID_Replica in Data_processing_func.Not_Null_ID:
                                    self.info("We can proceed...")
                                    self.wait(2)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                              special=System.GUI.KEY_END, other=None, timeout=10.0)
                                    self.wait(5)
                                    Result = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None,
                                                                          similar=0.70, timeout=10.0)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(2)
                                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
                                    # self.wait(3)
                                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None,
                                                              other='r', timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(1)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T',
                                                                 keysModifiers=[], image=None, similar=0.70,
                                                                 timeout=10.0)
                                    self.wait(1)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                                    self.wait(3)
                                    self.Window.doTypeTextwindow(text=input('Cmd_Kill'), keysModifiers=[], image=None,
                                                                 similar=0.70, timeout=10.0)
                                    self.wait(1)
                                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                              other=None, timeout=10.0)
                            else:
                                self.info("Something wrong happened during checking the status...")
                                self.wait(2)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_F1,
                                                          other=None, timeout=10.0)
                                self.wait(3)
                                self.Window.doTypeShorcut(key=System.GUI.KEY_SHIFT, modifier=None,
                                                          special=System.GUI.KEY_END, other=None, timeout=10.0)
                                self.wait(5)
                                Result = self.Window.doTypeTextwindow(text='BYE', keysModifiers=[], image=None,
                                                                      similar=0.70, timeout=10.0)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                          other=None, timeout=10.0)
                                self.wait(2)
                                self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None,
                                                          other='r', timeout=10.0)
                                self.wait(3)
                                self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70,
                                                             timeout=10.0)
                                self.wait(1)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                          other=None, timeout=10.0)
                                self.wait(3)
                                self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[],
                                                             image=None, similar=0.70, timeout=10.0)
                                self.wait(1)
                                self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER,
                                                          other=None, timeout=10.0)
                                self.wait(3)
                                # SIPP Closing/KILL
                                obj = KillSIPP.kill_sipp(parent=self,
                                                         LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF,
                                                         SIPP_ENV_CONF=SIPP_ENV_CONF)
                                workflow_change.updatestatus(parent=self, data=task, status="exception")
                                client_exception = True
                                exception = ["Did not land on 'review' page"]
                                mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                                # self.info(mail_body['data']
                                sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail,
                                                  reciever=receiver_mail, subject=subject, message=mail_body['data'],
                                                  files=[])
                                raise Exception("Did not land on 'review' page")

                            break
                        else:
                            if i == (n - 1):
                                raise ValueError
                except ValueError:
                    self.info("Maximum attempts for login exceeded!!!")
                    self.info("Login to TOM Failed. Therefore skipping TOM validation.")
                    self.wait(3)
                    self.Window.doTypeShorcut(key=System.GUI.KEY_WIN, modifier=None, special=None, other='r',
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='cmd', keysModifiers=[], image=None, similar=0.70, timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeTextwindow(text='taskkill /F /IM iexplore.exe /T', keysModifiers=[], image=None,
                                                 similar=0.70, timeout=10.0)
                    self.wait(3)
                    self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None,
                                              timeout=10.0)
                    self.wait(3)
                    # SIPP Closing/KILL
                    obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                             LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                    workflow_change.updatestatus(parent=self, data=task, status="exception")
                    client_exception = True
                    exception = ["3.05 - Login to TOM failed after trying for 10 times!!!"]
                    mail_body = exceptions_email_body.sub_unit_name(exception, parent=self)
                    # self.info(mail_body['data']
                    sendEmails.emails(self, agent=agent('BOT_GUI'), sender=sender_mail, reciever=receiver_mail,
                                      subject=subject, message=mail_body['data'], files=[])
                    raise Exception("3.05 - Login to TOM failed after trying for 10 times!!!")
        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)

        ### Manual Code End ###
        if Result:
            self.step6.setPassed('Executing with success: ')
        else:
            if not client_exception:
                obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                self.StepFailed(self, 'TOM Validation', *args1, message=message)
            self.step6.setFailed('Step has an error,unable to execute ')
        self.step6.end()

    # CAPTURE>
    if self.step7.isEnabled():
        self.step7.start()
        ### Manual Code Start ###
        Result = True
        # 3.06
        # proceed_bot_sale = True
        try:
            if proceed_bot_sale:
                y = self.Database.query(
                    query="select count(*) as TIBcount from TIBs t  join Investments i on t.Investment_ID=i.Investment_ID and i.ID=" + str(
                        memberno) + " and Internal_Policy_Type<>'FG TIP' and sold = 0", queryName=None)
                query = y.get('row_data')
                self.info(query)

                count = 0
                for i in query:
                    if isinstance(i, dict):
                        count = (i.get('TIBcount'))
                count = int(count)
                self.info(count)
                self.Data_QA["TIBcount"] = count
                if (count >= 1):
                    # Result=self.Window.doTypeTextwindow( text=input('TEXT_1'),WindowTitle=None,className=None,controlID=None,timeout=input('TIMEOUT_GUI') )
                    # self.wait(2)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
                    # self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)

                    self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                             button='left', pressed='True', coords=(0, 0), accessname='Ne&xt Tab >>',
                                             double=False, timeout=10.0)
                    self.wait(2)

                    self.Window.clickElement(title=u'SIPP Member Details', classname="ThunderRT6FormDC", controlID="",
                                             button='left', pressed='True', coords=(0, 0), accessname='31',
                                             double=False, timeout=10.0)
                    self.wait(2)

                    for j in range(count):
                        Result = self.Window.doTypeTextwindow(text=input('TEXT_18'), keysModifiers=[], image=None,
                                                              similar=0.70, timeout=10.0)
                        self.wait(5)

                        self.Window.doDoubleClickImage(image=input('IMG_18'), region=None, similar=0.70, onAll=False,
                                                       timeout=10.0)
                        self.wait(5)

                        res = self.Window.setFocus(title=u'Update TIB', class_name="ThunderRT6FormDC", controlID="",
                                                   timeout=10.0)
                        self.info(res)
                        if res['data'] != 'SUCCESS':
                            self.Window.doDoubleClickImage(image=input('IMG_18'), region=None, similar=0.70,
                                                           onAll=False, timeout=10.0)
                        self.wait(10)
                        policy_number = self.Window.getTextElement(title=u'Update TIB', classname='ThunderRT6FormDC',
                                                                   controlID=None, accessname='8', timeout=10.0)
                        # self.Window.clickElement(title=u'Update TIB',classname="ThunderRT6FormDC",controlID="",button='left', pressed='True', coords=(0,0),accessname='8', double=False,timeout=10.0)
                        # self.wait(2)
                        # self.Window.doTypeShorcut(key=System.GUI.KEY_CTRL, modifier=None, special=System.GUI.KEY_INSERT, other='c', timeout=10.0)
                        # self.wait(2)
                        # policy_number = self.Window.pasteClipboard(format_name=System.GUI.CF_UNICODETEXT, timeout=input('TIMEOUT_GUI'))
                        # policy_number = policy_number.decode()
                        self.info(policy_number)

                        encashment = Excel_Data['Encashment']
                        payment_amount = Excel_Data['Payment_amount']
                        if Excel_Data['Adhoc_fee'] in ['None', 'NULL', None, '', ' ']:
                            adhoc_fee = 0
                        else:
                            adhoc_fee = Excel_Data['Adhoc_fee']

                        if (policy_number == encashment):
                            # self.Window.doClickImage( image=input('IMG_19'), description='', similar=input('SIMILAR_GUI') )
                            self.Window.clickElement(title=u'Update TIB', classname="ThunderRT6FormDC", controlID="",
                                                     button='left', pressed='True', coords=(0, 0),
                                                     accessname='TabStripWndClass', double=False, timeout=10.0)
                            self.wait(2)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_RIGHT, other=None,
                                                      timeout=10.0)
                            self.wait(1)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_RIGHT, other=None,
                                                      timeout=10.0)
                            self.wait(1)
                            self.Window.doTypeShorcut(key=None, modifier=None, special=System.GUI.KEY_RIGHT, other=None,
                                                      timeout=10.0)
                            self.wait(1)

                            self.Window.clickElement(title=u'Update TIB', classname="ThunderRT6FormDC", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='Add',
                                                     double=False, timeout=10.0)
                            self.wait(2)

                            self.info(encashment)
                            self.info(payment_amount)
                            self.info(adhoc_fee)
                            total_consideration = adhoc_fee + payment_amount
                            total_consideration = str(total_consideration)
                            self.info(total_consideration)

                            self.Window.clickElement(title=u'Encashment Details', classname="ThunderRT6FormDC",
                                                     controlID="", button='left', pressed='True', coords=(0, 0),
                                                     accessname='1', double=False, timeout=10.0)
                            self.wait(2)
                            Result = self.Window.doTypeTextwindow(text=total_consideration, keysModifiers=[],
                                                                  image=None, similar=0.70, timeout=10.0)
                            self.wait(2)

                            self.Window.clickElement(title=u'Encashment Details', classname="ThunderRT6FormDC",
                                                     controlID="", button='left', pressed='True', coords=(0, 0),
                                                     accessname='&Add', double=False, timeout=10.0)
                            self.wait(2)

                            self.Window.clickElement(title=u'SIPP Administration', classname="#32770", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='&Yes',
                                                     double=False, timeout=10.0)
                            self.wait(2)

                            self.Window.clickElement(title=u'SIPP Administration', classname="#32770", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='&No',
                                                     double=False, timeout=10.0)
                            self.wait(2)

                            self.Window.clickElement(title=u'Update TIB', classname="ThunderRT6FormDC", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='&Cancel',
                                                     double=False, timeout=10.0)
                            self.wait(2)

                            break

                        else:
                            self.Window.clickElement(title=u'Update TIB', classname="ThunderRT6FormDC", controlID="",
                                                     button='left', pressed='True', coords=(0, 0), accessname='&Cancel',
                                                     double=False, timeout=10.0)
                            self.wait(2)



                else:
                    self.info("TIB not found")
                obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                         LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
                # obj = sql_u.sql_update_data(parent=self,data_pointer = self.Database_automaton, tablename='process_tasks',taskid = taskid,memberno=memberno,updatedby=updated_by,status='completed')
                workflow_change.updatestatus(parent=self, data=task, status="completed")

        except Exception as e:
            Result = False
            message = e
            message = traceback.format_exc()
            self.info(message)
            print(message)
        ### Manual Code End ###
        if Result:
            self.step7.setPassed('Executing with success: ')
        else:
            obj = KillSIPP.kill_sipp(parent=self, LAUNCH_SIPP_USERNAME_CONF=LAUNCH_SIPP_USERNAME_CONF,
                                     LAUNCH_SIPP_PWD_CONF=LAUNCH_SIPP_PWD_CONF, SIPP_ENV_CONF=SIPP_ENV_CONF)
            self.StepFailed(self, 'step 7 Add encashment onto SIPP(3.06)', *args1, message=message)
            self.step7.setFailed('Step has an error,unable to execute ')

        self.step7.end()












































