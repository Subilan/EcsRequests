from fn import DBNAME_ECS, getIP
from db import database

def getIId():
    """Get current instance id. Return `None` if not found."""
    with database(DBNAME_ECS) as d:
        cur = d.cursor()
        cur.execute("SELECT instance FROM `status` WHERE id=1")
        r = cur.fetchone()
        if r:
            if len(r) > 0:
                return r[0]
        return None

def getLastInvocation():
    with database(DBNAME_ECS) as d:
        cur = d.cursor()
        cur.execute("SELECT invocation_id FROM `cmd_history` ORDER BY id DESC")
        r = cur.fetchall()
        if r:
            if len(r) > 0:
                if len(r[0]) > 0:
                    return r[0][0]
        return None

def writeActionHistory(id, action):
    ip = getIP()
    ip = ip or '0.0.0.0'
    with database(DBNAME_ECS) as d:
        cur = d.cursor()
        cur.execute('INSERT INTO history (instance, action, created_at, created_by) VALUES ("%s", "%s", NOW(), "%s")' % (str(id), action, ip))
        d.commit()
    pass

def writeCommandHistory(cid, iid):
    ip = getIP()
    ip = ip or '0.0.0.0'
    with database(DBNAME_ECS) as d:
        cur = d.cursor()
        cur.execute('INSERT INTO cmd_history (command_id, invocation_id, created_at, created_by) VALUES ("%s", "%s", NOW(), "%s")' % (str(cid), str(iid), ip))
        d.commit()
    pass

def setIId(id):
    """Update current instance id."""
    with database(DBNAME_ECS) as d:
        cur = d.cursor()
        cur.execute("UPDATE `status` SET instance='%s'" % str(id))
        d.commit()
    pass