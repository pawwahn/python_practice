## >> called on auto initialization
def description(self):
    # autocase description
    self.setPurpose(purpose="GUI_Automation_Capture")

    # steps description
    self.step1 = self.addStep(expected="Action executed with success", description="", summary="", enabled=True,
                              repeat=False, continueonException=False)


## >> called on auto preparation, adapters and libraries definitions
def prepare(self):
    # adapters and libraries definitions
    self.Window = System.GUI.Window(parent=self, agent=agent('BOT_GUI'), debug=input('DEBUG'))


## >> called on error or to cleanup the auto properly
def cleanup(self, aborted):
    pass


## >> called on auto begin
def definition(self):
    ##CAPTURE>
    if self.step1.isEnabled():
        self.step1.start()
        ### Manual Code Start ###
        Result = True
        from docx import Document
        from datetime import datetime
        import os
        self.info(os.getcwd())
        self.info('..................')
        # open the document
        doc = Document('C:\\poc.docx')
    ### Manual Code End ###
    if Result:
        self.step1.setPassed('Executing with success: ')
    else:
        self.step1.setFailed('Step has an error,unable to execute ')
    self.step1.end()




