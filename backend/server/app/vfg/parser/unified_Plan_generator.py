"""This module is designed to help with getting predicate list, the Initial predicates and goal predicates
    It covers the Function in Problem_parser and Domain_parser 
"""

# -----------------------------Authorship-----------------------------------------
# -- Authors  : Jiarui CHEN
# -- Group    : Planning Visualisation
# -- Date     : 18/Jan/2023
# -- Version  : 2.0
# --------------------------------------------------------------------------------
import re
import sys
import os
import copy
import unified_planning as unip
from unified_planning.shortcuts import *
from unified_planning.engines.compilers import Grounder, GrounderHelper
#from unified_planning.io import PDDLReader




sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../' + "parser"))
import Parser_Functions





def parse_plan(problem, plan, solver):
    try:
        if solver == 'lama-first':
            plan_content = plan['result']['output']['sas_plan'].split(";")[0]
            
        elif solver == 'enhsp-2020':
            i1= plan['result']['output']['plan'].find("Problem Solved\n")
            i2= plan['result']['output']['plan'].find("Plan-Length:")

            raw_action_list = plan['result']['output']['plan'][i1+15:i2-1].split('\n')
            action_list = [i.split(":")[1] for i in raw_action_list]
            plan_content = '\n'.join(action_list)

        elif solver == 'optic':
            tmp = plan['result']['output']['plan'].split("* All goal deadlines now no later than")[0].split("Time")[1]
            index = tmp.find("\n")
            plan_content = tmp[(index+1):]

        elif solver == 'tfd':
            tmp = plan['result']['output']['plan'].split("Total time:")[1]
            index = tmp.find("\n")
            plan_content = tmp[(index+1):]
        print(plan_content)
        reader = unip.io.PDDLReader()
        plan_object = reader.parse_plan_string(problem, plan_content)
        
        return plan_object
    
    except:
        raise Exception("Failed to parse the plan from PaaS.")

   
def get_stages_from_plan(problem, plan):
    stage_object_list = []
    
    with SequentialSimulator(problem) as simulator:
        state = simulator.get_initial_state()
        stage_object_list.append(["Initial Stage", state])
        #print(state)

        for a in plan.actions:
            state = copy.copy(simulator.apply(state, a))
            #print(f"Applied action: {a}.")
            stage_object_list.append([a.__str__(), state, a.action.__str__()])

            #print(state)
        # if simulator.is_goal(state):
        #     print("Goal reached!")
    return stage_object_list

def assign_solver_from_problem(problem):
    problem_kind = problem.kind.__str__()
    if "TIME:" in problem_kind:
        return "optic"
    else:
        if "NUMBERS:" in problem_kind:
            return "enhsp-2020"
        else:
            return "lama-first"
   
def get_problem_type(problem):
    is_numerical = False
    is_temporal = False

    problem_kind = problem.kind.__str__()
    if "TIME:" in problem_kind:
        is_temporal = True
    if "NUMBERS:" in problem_kind:
        is_numerical = True

    return (is_numerical, is_temporal)

def get_domain_json_unified(pddl_problem):
    PredicateList = {f.name:{"type": f.type, "arity": f.arity} for f in pddl_problem.fluents}
    
    return PredicateList

def get_problem_dic_unified(pddl_problem):
    
    result = [{"init": [v for k, v in pddl_problem.initial_values.items() if v[k]]}, {"goal": pddl_problem.goals}]
    
    return result

def get_stages_unified(plan, problem_dic, problem_file, predicates_list):
    return 0

def TemporalSimulation(problem, plan):
    to_do_list = extract_temporal_effects(problem, plan)
    stage_object_list = get_temporal_stages(problem, to_do_list)
    return stage_object_list

def extract_temporal_effects(problem, plan):
    grounder = GrounderHelper(problem)
    to_do_list = []
    #print(plan.timed_actions)
    for start_time, a, duration in plan.timed_actions:
        end_time = start_time+duration
        grounded_act = grounder.ground_action(a.action, a.actual_parameters)
        
        #print(grounded_act.simulated_effects)
        print("this is inbuilt!")
        print(a)
        for timing, e in grounded_act.effects.items():
            print(timing.is_from_start(), timing.is_from_end())
            if timing.is_from_start():
                to_do_list.append((start_time, e, f'{float(start_time)}:{a.__str__()} at-start effect', a.action.__str__()))
            elif timing.is_from_end():
                to_do_list.append((end_time, e, f'{float(end_time)}:{a.__str__()} at-end effect', a.action.__str__()))
            else:
                to_do_list.append((timing.delay, e, f'{float(timing.delay)}:{a.__str__()} global timing effect', a.action.__str__()))
    return to_do_list

def get_temporal_stages(problem, to_do_list):
    stage_object_list = []

    current_state = problem.initial_values.copy()
    stage_object_list.append(["Initial Stage", current_state, ''])

    for time, update, stage_name, action_detail in to_do_list:
        next_state =  current_state.copy()
        for effect in update:
            if effect.is_assignment():
                next_state[effect._fluent] = effect._value
            elif effect.is_increase():
                next_state[effect._fluent] = next_state[effect._fluent]+effect._value
            elif effect.is_decrease():
                next_state[effect._fluent] = next_state[effect._fluent]-effect._value
        print(reduce_state(next_state))
        stage_object_list.append([stage_name, next_state, action_detail])
        current_state = next_state

    return stage_object_list

def get_action_name(action):
    s = []
    s.append(action.name)
    first = True
    for p in action.parameters:
        if first:
            s.append("(")
            first = False
        else:
            s.append(", ")
        s.append(str(p))
    if not first:
        s.append(")")
    print(s)
    print("".join(s))
    return "".join(s)

def stage_list_to_stages(input_data, objects):
    content = {"stages": [], "objects": objects, "subgoals": []}
    #output_data = []
    for item in input_data:
        transformed_item = {
            "items": reduce_state(item[1]),
            "add": "",
            "remove": "",
            "stageName": item[0],
            "stageInfo": item[2]
        }
        content['stages'].append(transformed_item)
    return content

def reduce_state(state):
    reduced_state = []
    for fluent, value in state.items():

        # if the predicate is boolean value, keep the True predicate and save them as "state" format
        if value.is_bool_constant():
            if value.constant_value():
                #reduced_state[fluent.__str__()] = value.constant_value()
                # print("11111")
                # print(fluent)
                # print(fluent.fluent().name)
                # print(fluent.args)
                # print(fluent.args[0])
                
                # print(type(fluent))
               
                reduced_state.append({"name": fluent.fluent().name, "objectNames": [arg.__str__() for arg in fluent.args], "value":value.constant_value()})
                # print(reduced_state)
                
        else:
            #reduced_state[fluent.__str__()] = value.constant_value()
            reduced_state.append({"name": fluent.fluent().name, "objectNames": [arg.__str__() for arg in fluent.args], "value":value.constant_value()})
 

    return reduced_state