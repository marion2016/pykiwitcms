from tcms_api import TCMS
import ssl

#need config ~/.tcms.conf as below
'''
[tcms]
url=https://92.120.145.188/xml-rpc/
username=hake.huang@nxp.com
password=Happy123
verify=False
'''

#remove the SSL authoriztion error 
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context



def connect():
    rpc_client = TCMS()
    return rpc_client


def get_function_by_type(rpc_client, type):
    TYPE_LIST = {
        "TestCase" : rpc_client.exec.TestCase.filter,
        "Product" : rpc_client.exec.Product.filter, 
        "Category" : rpc_client.exec.Category.filter,
        "Priority" : rpc_client.exec.Priority.filter,
        "Component": rpc_client.exec.Component.filter,
        "Build" : rpc_client.exec.Build.filter,
        "TestCaseRun" : rpc_client.exec.TestCaseRun.filter,
        "TestCaseStatus" : rpc_client.exec.TestCaseStatus.filter,
        "TestPlan" : rpc_client.exec.TestPlan.filter,
        "TestRun" : rpc_client.exec.TestRun.filter,
        "User" : rpc_client.exec.User.filter,
        "Version" : rpc_client.exec.Version.filter,
        }
    if type not in TYPE_LIST.keys():
        print("shall be one of %s"% TYPE_LIST.keys())
        return None
    return TYPE_LIST[type]

def get_all_items(rpc_client, type):
    fn = get_function_by_type(rpc_client, type)
    if fn == None:
        return None
    print("all %s are:"% type)
    for item in fn({}):
        print(item)
    return fn({})

def query_item(rpc_client, type, hash):
    fn = get_function_by_type(rpc_client, type)
    if fn == None:
        print("not found")
        return None
    for item in fn(hash):
        print(item)
    return fn(hash)

def creat_case(rpc_client ,hash):
    '''
    values = {
    'category': 135,
    'product': 61,
    'summary': 'Testing XML-RPC',
    'priority': 1,
    }
    '''
    mdict = {}
    for item in hash:
        if hash[item].__class__.__name__ == "dict":
            key = list(hash[item].keys())[0]
            content = get_all_items(rpc_client, item.capitalize())
            for cn in content:
                if key in cn and cn[key] == hash[item][key]:
                    mdict[item] = cn['id']
        else:
            mdict[item] = hash[item]
    print("create case with")
    print(mdict)
    result = rpc_client.exec.TestCase.create(mdict)
    return result

def update_case(rpc_client, case_id, hash):
    '''
    case_id (int) – PK of TestCase to be modified
    values (dict) – Field values for tcms.testcases.models.TestCase. 
                    The special keys setup, breakdown, action and effect are recognized 
                    and will cause update of the underlying tcms.testcases.models.TestCaseText object!
    hash = {
        'setup' : 'do setup',
        'breakdown' : 'do break down',
        'action' : 'do action',
        'effect' : 'effect'
    }
    '''

    res = rpc_client.exec.TestCase.update(case_id, hash)
    return res


def test_get_all_items():
    rpc_client = connect()
    get_all_items(rpc_client, "TestCase")
    get_all_items(rpc_client, "Product")
    get_all_items(rpc_client, "Category")
    get_all_items(rpc_client, "Priority")
    get_all_items(rpc_client, "Component")
    get_all_items(rpc_client, "Build")
    get_all_items(rpc_client, "TestCaseRun")
    get_all_items(rpc_client, "TestCaseStatus")
    get_all_items(rpc_client, "TestPlan")
    get_all_items(rpc_client, "TestRun")
    get_all_items(rpc_client, "User")
    get_all_items(rpc_client, "Version")

def test_query_item():
    rpc_client = connect()
    query_item(rpc_client, "TestCase", {'case_id': 1})
    query_item(rpc_client, "TestCase", {'summary': 'hello world'})
    query_item(rpc_client, "Product", {'id': 1})
    query_item(rpc_client, "Product", {'name': 'MCU_SDK'})
    query_item(rpc_client, "Category", {'id': 2})
    query_item(rpc_client, "Category", {'name': 'Demo'})
    query_item(rpc_client, "Priority", {'id': 1})
    query_item(rpc_client, "Priority", {'value': 'P1'})
    query_item(rpc_client, "Component", {'id': 1})
    query_item(rpc_client, "Component", {'name': 'FRDMK64F'})
    query_item(rpc_client, "Build", {'build_id': 1})
    query_item(rpc_client, "Build", {'name': 'unspecified'})
    query_item(rpc_client, "TestCaseRun", {'case_run_id': 1, 'run_id': 1})
    query_item(rpc_client, "TestCaseRun", {'case_run_id': 1, 'run_id': 1})
    query_item(rpc_client, "TestCaseStatus", {'name': 'PROPOSED'})
    query_item(rpc_client, "TestCaseStatus", {'id': 1})
    query_item(rpc_client, "TestPlan", {'name': 'test plan trial'})
    query_item(rpc_client, "TestPlan", {'plan_id': 3})
    query_item(rpc_client, "TestRun", {'run_id': 1})
    query_item(rpc_client, "User", {'username': 'hake.huang@nxp.com'})
    query_item(rpc_client, "Version", {'value': 'TEST_EAR'})


def test_create_case():
    values = {
    'category': {'name': 'Demo'},
    'product': {'name': 'MCU_SDK'},
    'summary': 'Testing XML-RPC',
    'priority': 1,
    'estimated_time' : "00:00:05",

    }
    rpc_client = connect()
    res = creat_case(rpc_client, values)
    print(res)

def test_update_case():
    hash = {
        'setup' : 'do setup',
        'breakdown' : 'do break down',
        'action' : 'do action',
        'effect' : 'effect'
    }
    rpc_client = connect()
    res = update_case(rpc_client, '3', hash)
    print(res)

if __name__ == "__main__":
    #test_get_all_items()
    #test_query_item()
    #test_create_case()
    test_update_case()
