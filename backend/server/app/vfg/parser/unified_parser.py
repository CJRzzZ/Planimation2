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
import unified_planning as unip
from unified_planning.io import PDDLReader



sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../' + "parser"))
import Parser_Functions

def parse_domain_and_problem_text(domain_text, problem_text):
    """
    The function will parse both problem pddl and get the Initial predicates and
    and goal predicates
    :param problem_text: problem pddl text
    :param predicates_lists: all the available predicate from domain pddl
    :return: a dictionary contains INIT and GOAL states(predicates).
    """
    reader = PDDLReader()
    # reader = unip.io.PDDLReader()
    pddl_problem = reader.parse_problem_string(domain_text, problem_text)

    return pddl_problem

def get_problem_type(pddl_problem):
    is_numerical = False
    is_temporal = False

    if pddl_problem.timed_effects:
        is_temporal = True
    if any([(i.type.is_real_type() or i.type.is_int_type()) for i in pddl_problem.fluents]):
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