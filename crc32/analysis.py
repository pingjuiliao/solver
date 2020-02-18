#!/usr/bin/env python3
import angr

p = angr.Project("./challenge")

state = p.factory.entry_state(add_options={angr.options.LAZY_SOLVES})

sm = p.factory.simulation_manager()

sm.explore(find=(0x08048893,))

solution = sm.found[0]

print("Constraints : ")
print(solution.solver.constraints)
