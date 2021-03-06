#!/usr/bin/env python3
# Copyright (c) 2015-2016 The Ilcoin Core developers
# All Rights Reserved. Ilgamos International 2017©
"""Test a node with the -disablewallet option.

- Test that validateaddress RPC works when running with -disablewallet
- Test that it is not possible to mine to an invalid address.
"""

from test_framework.test_framework import IlcoinTestFramework
from test_framework.util import *


class DisableWalletTest (IlcoinTestFramework):

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 1

    def setup_network(self, split=False):
        self.nodes = start_nodes(self.num_nodes, self.options.tmpdir, [['-disablewallet']])
        self.is_network_split = False
        self.sync_all()

    def run_test (self):
        x = self.nodes[0].validateaddress('3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy')
        assert(x['isvalid'] == False)
        x = self.nodes[0].validateaddress('mneYUmWYsuk7kySiURxCi3AGxrAqZxLgPZ')
        assert(x['isvalid'] == True)

        # Checking mining to an address without a wallet
        try:
            self.nodes[0].generatetoaddress(1, 'mneYUmWYsuk7kySiURxCi3AGxrAqZxLgPZ')
        except JSONRPCException as e:
            assert("Invalid address" not in e.error['message'])
            assert("ProcessNewBlock, block not accepted" not in e.error['message'])
            assert("Couldn't create new block" not in e.error['message'])

        try:
            self.nodes[0].generatetoaddress(1, '3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy')
            raise AssertionError("Must not mine to invalid address!")
        except JSONRPCException as e:
            assert("Invalid address" in e.error['message'])

if __name__ == '__main__':
    DisableWalletTest ().main ()
