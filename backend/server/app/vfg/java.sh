'Domain parsed\nProblem parsed\nGrounding..\nGrounding Time: 48\n(Pre Simplification) - |A|+|P|+|E|: 270\nAIBR :: Number of Supporters = 162\n(After Easy Simplification) - |A|+|P|+|E|: 90\n|F|:40\n|X|:2\nGrounding and Simplification finished\n|A|:90\n|P|:0\n|E|:0\nha:false htfalse\nAIBR selected\nAIBR :: Number of Supporters = 162\nSetting horizon to:NaN\nHelpful Action Pruning Activated\nRunning WA-STAR\nh(n = s_0)=53.0\nf(n) = 53.0 (Expanded Nodes: 0, Evaluated States: 0, Time: 0.007)\nProblem Solved\n0.0: (drive truck1 depot0 distributor1)\n1.0: (drive truck1 distributor1 distributor1)\n2.0: (drive truck0 distributor1 depot0)\n3.0: (lift hoist0 crate1 pallet0 depot0)\n4.0: (load hoist0 crate1 truck0 depot0)\n5.0: (lift hoist1 crate0 pallet1 distributor0)\n6.0: (drive truck0 depot0 distributor0)\n7.0: (load hoist1 crate0 truck0 distributor0)\n8.0: (unload hoist1 crate1 truck0 distributor0)\n9.0: (drop hoist1 crate1 pallet1 distributor0)\n10.0: (drive truck0 distributor0 distributor1)\n11.0: (unload hoist2 crate0 truck0 distributor1)\n12.0: (drop hoist2 crate0 pallet2 distributor1)\nPlan-Length:13\nMetric (Search):13.0\nPlanning Time:417\nHeuristic Time:42\nSearch Time:62\nExpanded Nodes:21\nStates Evaluated:58\nFixed constraint violations during search (zero-crossing):0\nNumber of Dead-Ends detected:6\nNumber of Duplicates detected:50\n'

pip install --upgrade unified_planning