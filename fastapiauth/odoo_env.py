import os
from typing import Callable, List
import requests


def odoo_env() -> Callable[[str, str, tuple], List[dict]]:
    """Getting an environment to use odoo remotely"""
    env = os.environ.get
    url = env('ODOO_HOST', 'localhost')
    header = {'Content-Type': 'application/json'}
    db = env('ODOO_DB', 'demo')
    passwd = env('ODOO_PASSWORD', 'admin')
    user = env('ODOO_LOGIN', 'admin')
    vals = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {"service": "common",
                       "method": "login",
                       "args": [db, user, passwd]}
        }
    data = requests.post(url, json=vals, headers=header)
    result = data.json()
    uid = result.get('result')

    def invoke(model, method, *args):
        vals.update({
            "params": {
                "service": "object",
                "method": "execute",
                "args": [db, uid, passwd, model, method, *args]}
            })
        data = requests.post(url, json=vals, headers=header)
        return data.json()['result']
    return invoke
