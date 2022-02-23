import os
from odoorpc import ODOO


def odoo_env() -> ODOO:
    """Getting an environment to use odoo remotely"""
    env = os.environ.get
    conn = ODOO(host=env('ODOO_HOST', 'localhost'),
                port=env('ODOO_PORT', 9069),
                protocol=env('ODOO_PROTOCOL', 'jsonrpc'),
                timeout=env('ODOO_TIMEOUT', 9999))
    conn.login(db=env('ODOO_DB', 'demo'),
               login=env('ODOO_LOGIN', 'admin'),
               password=env('ODOO_PASSWORD', 'admin'))
    return conn
