properties = {
    "outputs-parameters": {
        "parameter": {
            "color": "",
            "@color": {},
            "type": "float",
            "@type": {},
            "name": "TIMEOUT",
            "@name": {},
            "value": "1.0",
            "@value": {},
            "description": "",
            "@description": {}
        },
        "@parameter": {}
    },
    "@outputs-parameters": {},
    "inputs-parameters": {
        "parameter": [
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "BROWSER_USE_FIREFOX",
                "@name": {},
                "value": "False",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "BROWSER_USE_CHROME",
                "@name": {},
                "value": "False",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "BROWSER_USE_OPERA",
                "@name": {},
                "value": "False",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "BROWSER_USE_IE",
                "@name": {},
                "value": "True",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "str",
                "@type": {},
                "name": "BROWSER_TEXT_1",
                "@name": {},
                "value": "https://www.google.com",
                "@value": {},
                "description": "opening chrome",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "float",
                "@type": {},
                "name": "TIMEOUT",
                "@name": {},
                "value": "1",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "VERBOSE",
                "@name": {},
                "value": "True",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "bool",
                "@type": {},
                "name": "DEBUG",
                "@name": {},
                "value": "False",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "float",
                "@type": {},
                "name": "TIMEOUT_GUI",
                "@name": {},
                "value": "15",
                "@value": {},
                "description": "",
                "@description": {}
            },
            {
                "color": "",
                "@color": {},
                "type": "float",
                "@type": {},
                "name": "SIMILAR_GUI",
                "@name": {},
                "value": "0.9",
                "@value": {},
                "description": "",
                "@description": {}
            }
        ],
        "@parameter": [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ]
    },
    "@inputs-parameters": {},
    "agents": {
        "agent": {
            "type": "superagent",
            "@type": {},
            "name": "BOT_GUI",
            "@name": {},
            "value": "LT-CHN-47654",
            "@value": {},
            "id": "B6336ad",
            "@id": {},
            "description": "",
            "@description": {}
        },
        "@agent": {}
    },
    "@agents": {},
    "descriptions": {
        "description": [
            {
                "key": "author",
                "@key": {},
                "value": "admin",
                "@value": {}
            },
            {
                "key": "creation date",
                "@key": {},
                "value": "26/02/2021 16:45:35",
                "@value": {}
            },
            {
                "key": "summary",
                "@key": {},
                "value": "Just a basic sample.",
                "@value": {}
            },
            {
                "key": "prerequisites",
                "@key": {},
                "value": "None",
                "@value": {}
            },
            {
                "key": "comments",
                "@key": {},
                "value": {
                    "comments": "",
                    "@comments": {}
                },
                "@value": {}
            },
            {
                "key": "libraries",
                "@key": {},
                "value": "Data,ETL,Files,Media,Security,Units",
                "@value": {}
            },
            {
                "key": "adapters",
                "@key": {},
                "value": "Database,DataCommunication,FileTransfer,Interface,NetworkCommunication,NetworkManagement,System,Telecommunication,Terminal,WebService",
                "@value": {}
            },
            {
                "key": "subunits",
                "@key": {},
                "value": "*",
                "@value": {}
            },
            {
                "key": "state",
                "@key": {},
                "value": "Writing",
                "@value": {}
            },
            {
                "key": "name",
                "@key": {},
                "value": "AUTOCASE",
                "@value": {}
            }
        ],
        "@description": [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ]
    },
    "@descriptions": {},
    "probes": {
        "probe": {
            "name": "probe01",
            "@name": {},
            "active": "False",
            "@active": {},
            "args": "",
            "@args": {},
            "type": "default",
            "@type": {}
        },
        "@probe": {}
    },
    "@probes": {}
}


## >> called on auto initialization
def description(self):
    # autocase description
    self.setPurpose(purpose="GUI_Automation_Capture")

    # steps description
    self.step1 = self.addStep(expected="Action executed with success", description="opening chrome",
                              summary="opening chrome", enabled=True, repeat=False, continueonException=False)
    self.step2 = self.addStep(expected="Action executed with success", description="enter", summary="enter",
                              enabled=True, repeat=False, continueonException=False)


## >> called on auto preparation, adapters and libraries definitions
def prepare(self):
    # adapters and libraries definitions
    self.Window = System.GUI.Window(parent=self, agent=agent('BOT_GUI'), debug=input('DEBUG'))
    self.Browser = System.GUI.Browser(parent=self, agent=agent('BOT_GUI'), debug=input('DEBUG'))


## >> called on error or to cleanup the auto properly
def cleanup(self, aborted):
    pass


## >> called on auto begin
def definition(self):
    ##CAPTURE_BROWSER>opening chrome
    if self.step1.isEnabled():
        self.step1.start()
        BROWSER_RET1 = self.Browser.doOpen(timeout=input('TIMEOUT_GUI'), targetUrl=input('BROWSER_TEXT_1'),
                                           withFirefox=input('BROWSER_USE_FIREFOX'), withIe=input('BROWSER_USE_IE'),
                                           withChrome=input('BROWSER_USE_CHROME'), withOpera=input('BROWSER_USE_OPERA'))
        if BROWSER_RET1:
            self.step1.setPassed('Executing with success: opening chrome')
        else:
            self.step1.setFailed('Step has an error,unable to execute opening chrome')
        self.step1.end()

    ##CAPTURE>enter
    if self.step2.isEnabled():
        self.step2.start()
        self.Window.typeShorcut(key=None, modifier=None, special=System.GUI.KEY_ENTER, other=None)
        if not self.Window.isActionAccepted(timeout=input('TIMEOUT_GUI')):
            self.step2.setFailed('Step has an error,unable to execute enter')
        else:
            self.step2.setPassed('Executing with success: enter')
        self.step2.end()
