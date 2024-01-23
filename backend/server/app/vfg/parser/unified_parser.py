"""This module is designed to help with getting predicate list, the Initial predicates and goal predicates
    It covers the Function in Problem_parser and Domain_parser 
"""

# -----------------------------Authorship-----------------------------------------
# -- Authors  : Jiarui CHEN
# -- Group    : Planning Visualisation
# -- Date     : 18/Jan/2023
# -- Version  : 1.0
# --------------------------------------------------------------------------------
import re
import sys
import os
import unified_planning as unip

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../' + "parser"))
import Parser_Functions

def parse_domain_and_problem_text(domain_text, problem_text):
    """
    The function will parse bith problem pddl and get the Initial predicates and
    and goal predicates
    :param problem_text: problem pddl text
    :param predicates_lists: all the available predicate from domain pddl
    :return: a dictionary contains INIT and GOAL states(predicates).
    """
    reader = unip.io.PDDLReader()
    pddl_problem = reader.parse_problem_string(domain_text, problem_text)

    return pddl_problem

def get_domain_json_unified(pddl_problem):
    PredicateList = {f.name:{"type": f.type, "arity": f.arity} for f in pddl_problem.fluents}
    
    return PredicateList

def get_problem_dic_unified(pddl_problem):
    
    result = [{"init": pddl_problem.initial_values}, {"goal": pddl_problem.goals}]
    
    return result