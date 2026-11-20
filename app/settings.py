import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = ROOT / 'sample_data'
DB = Path(os.getenv('WORKBENCH_DB', str(ROOT/'state/ledger.sqlite3')))
TITLE = '光纤跳接核对'
SLUG = 'fiber-odf'
KEY = '链路单'
FIELDS = ('始端', '末端', '双向跳接', '光损预算')
ROLE = '园区光纤档案员'
UNIT = 'dB'
SIGNATURE = '接续端子'
RULE_VERSION = 'fiber-odf-1.0'
TABS = {'intake': '来源采信', 'contract': '字段解释', 'quality': '隔离裁决', 'domain': '跳接路径', 'reconcile': '独立对账', 'runs': '批次复算', 'review': '交付复核'}
