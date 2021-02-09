a = {'data':[{
  "get_send_message_401": {
    "path": "accounts",
    "Content-Type": "application/json",
	"Host": "spl9-pt99-2.parentlink.net",
      "expected_status_code": 401,
    "payload": {
        "organizationID": "2000001175"
		},
    "expected_content_type" : "text/html; charset=utf-8"
    }

  },
{
  "get_send_message_402": {
    "path": "accounts",
    "Content-Type": "application/json",
	"Host": "spl9-pt99-2.parentlink.net",
      "expected_status_code": 401,
    "payload": {
        "organizationID": "2000001175"
		},
    "expected_content_type" : "text/html; charset=utf-8"
    }

  },
{
  "get_send_message_403": {
    "path": "accounts",
    "Content-Type": "application/json",
	"Host": "spl9-pt99-2.parentlink.net",
      "expected_status_code": 401,
    "payload": {
        "organizationID": "2000001175"
		},
    "expected_content_type" : "text/html; charset=utf-8"
    }

  }]}

print(a['data'][2])