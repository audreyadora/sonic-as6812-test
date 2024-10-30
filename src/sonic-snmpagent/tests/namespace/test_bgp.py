import os
import sys
import importlib
# noinspection PyUnresolvedReferences
import tests.mock_tables.dbconnector

modules_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(modules_path, 'src'))

from unittest import TestCase
from unittest.mock import patch, mock_open

import socket
from ax_interface.mib import MIBTable
from ax_interface.pdu import PDUHeader
from ax_interface.pdu_implementations import GetPDU, GetNextPDU
from ax_interface import ValueType
from ax_interface.encodings import ObjectIdentifier
from ax_interface.constants import PduTypes
from sonic_ax_impl.main import SonicMIB
from sonic_ax_impl.mibs.vendor.cisco import bgp4 

class TestSonicMIB(TestCase):
    @classmethod
    def setUpClass(cls):
        tests.mock_tables.dbconnector.load_namespace_config()
        importlib.reload(bgp4)
        cls.lut = MIBTable(bgp4.CiscoBgp4MIB) 
        for updater in cls.lut.updater_instances:
            updater.reinit_data()
            updater.update_data()

    def test_getpdu_established(self):
        print("hello")
        print(bgp4.CiscoBgp4MIB.bgpsession_updater.session_status_list)
        oid = ObjectIdentifier(20, 0, 0, 0, (1, 3, 6, 1, 4, 1, 9, 9, 187, 1, 2, 5, 1, 3, 1, 4, 10, 10, 0, 0))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(oid))
        self.assertEqual(value0.data, 6)

    def test_getpdu_idle(self):
        oid = ObjectIdentifier(20, 0, 0, 0, (1, 3, 6, 1, 4, 1, 9, 9, 187, 1, 2, 5, 1, 3, 1, 4, 10, 0, 0, 6))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(oid))
        self.assertEqual(value0.data, 1)

    def test_getpdu_active(self):
        oid = ObjectIdentifier(20, 0, 0, 0, (1, 3, 6, 1, 4, 1, 9, 9, 187, 1, 2, 5, 1, 3, 2, 16, 254, 192, 0, 0, 0, 0, 0, 0, 0, 0, 255, 255, 10, 250, 0, 7))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(oid))
        self.assertEqual(value0.data, 3)

    def test_getpdu_disappeared(self):
        oid = ObjectIdentifier(20, 0, 0, 0, (1, 3, 6, 1, 4, 1, 9, 9, 187, 1, 2, 5, 1, 3, 2, 16, 252, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0x10))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.NO_SUCH_INSTANCE)

    def test_getpdu_established_asic2(self):
        oid = ObjectIdentifier(20, 0, 0, 0, (1, 3, 6, 1, 4, 1, 9, 9, 187, 1, 2, 5, 1, 3, 1, 4, 10, 10, 0, 5))
        get_pdu = GetPDU(
            header=PDUHeader(1, PduTypes.GET, 16, 0, 42, 0, 0, 0),
            oids=[oid]
        )

        encoded = get_pdu.encode()
        response = get_pdu.make_response(self.lut)
        print(response)

        value0 = response.values[0]
        self.assertEqual(value0.type_, ValueType.INTEGER)
        self.assertEqual(str(value0.name), str(oid))
        self.assertEqual(value0.data, 6)

    @classmethod
    def tearDownClass(cls):
        tests.mock_tables.dbconnector.clean_up_config()
