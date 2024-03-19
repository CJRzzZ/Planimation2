"""
This file is used for testing the functionality.
The views.py in the parent folder is the main function on the server.


This module intergrate all the other module, it takes the domain PDDL, problem PDDL, and
animation profile, and it write the visualisation file to visualsation.json.

"""
# -----------------------------Authorship-----------------------------------------
# -- Authors  : Sai
# -- Group    : Planning Visualisation
# -- Date     : 13/August/2018
# -- Version  : 1.0
# --------------------------------------------------------------------------------
# -----------------------------Reviewer-------------------------------------------
# -- Authors  : Yi Ding
# -- Group    : Planning Visualisation
# -- Date     : 17/Oct/2018
# -- Version  : 1.0
# --------------------------------------------------------------------------------
import sys
import parser.Plan_generator
import parser.Animation_parser
import parser.Problem_parser
import parser.Predicates_generator
import parser.Domain_parser
import solver.Solver
import solver.Initialise as Initialise
import adapter.visualiser_adapter.Transfer as Transfer
import json

import parser.unified_parser
import unified_planning as unip
from unified_planning.shortcuts import *
import parser.unified_Plan_generator
import parser.Unified_problem_parser
from unified_planning.engines.compilers import Grounder, GrounderHelper
import solver.Unified_solver

def get_visualisation_file():
    # # This function will call the other modules to generate the visualisaiton file.
    # if len(sys.argv) < 4:
    # 	print("some file is missing, please follow the command below to run the program")
    # 	print("python main.py [dommainfile] [problemfile] [animationprofile]")
    # 	sys.exit()
    
    # domain_file = "problem_example/logistics_domain.pddl"
    # problem_file = "problem_example/logistics_prob01.pddl"
    # animation_file = "problem_example/logistics_ap.pddl"
    domain_file = "problem_example/DepotsTime_domain.pddl"
    problem_file = "problem_example/DepotsTime_prob01.pddl"
    animation_file = "problem_example/logistics_ap.pddl"
    url_link = "http://solver.planning.domains/solve"

    # read animation profile from json
    animation_content = open(animation_file, 'r',encoding='utf-8-sig').read()
    domain_content=open(domain_file, 'r',encoding='utf-8-sig').read().lower()
    problem_content=open(problem_file, 'r',encoding='utf-8-sig').read().lower()

    problem_object = parser.unified_parser.parse_domain_and_problem_text(domain_content, problem_content)
    
    #solver_name = 'tfd'
    solver_name = parser.unified_Plan_generator.assign_solver_from_problem(problem_object)

    #plan = parser.Plan_generator.get_plan_from_pass(domain_content, problem_content, "", solver)
    f = open('raw_deport_time_optic.json')
    plan = json.load(f)
    # plan = parser.Plan_generator.get_plan(domain_content,
    #                                           problem_content,
    #                                           url_link)
    # print(plan)
    # f = open('raw_log_lama.json')
    # plan = json.load(f)

    predicates_list = parser.Domain_parser.get_domain_json(domain_content)
    #problem_dic = parser.Problem_parser.get_problem_dic(problem_content, predicates_list)
    problem_dic = parser.Unified_problem_parser.get_problem_dic_unified(problem_object)
    #object_list = parser.Problem_parser.get_object_list(problem_content)
    object_list = parser.Unified_problem_parser.get_object_list_unified(problem_object)
    animation_profile = json.loads(parser.Animation_parser.get_animation_profile(animation_content, object_list))


    goal_state = problem_object.goals
    print(goal_state)

        #print(expression.object())
    #print(problem_object)
    # print("1.predicates_list")
    # print(predicates_list)
    # print("2.problem_dic")
    # print(problem_dic)
    # print("2.5.problem_dic")
    # print(problem_dic2)
    # print("3.object_list")
    # print(object_list)

    plan_object = parser.unified_Plan_generator.parse_plan(problem_object, plan, solver_name)
    is_numerical, is_temportal = parser.unified_Plan_generator.get_problem_type(problem_object)
    
    if is_temportal:
        to_do_list = parser.unified_Plan_generator.extract_temporal_effects(problem_object, plan_object)
        stage_list = parser.unified_Plan_generator.get_temporal_stages(problem_object, to_do_list)
   
    else:
        stage_list = parser.unified_Plan_generator.get_stages_from_plan(problem_object, plan_object)
    #print(stage_list)
    stages = parser.unified_Plan_generator.stage_list_to_stages(stage_list, object_list)
    #print(stages)
    print(stage_list[0])
    print(stages)
    result = solver.Unified_solver.get_visualisation_dic(stages, animation_profile, plan_object, problem_dic)

    #stages, 
    #result = solver.Solver.get_visualisation_dic(stages, animation_profile, plan['result']['plan'], problem_dic)
    # print("----------------------------------")
    print(stage_list[1])
    # print("----------------------------------")
    # print(stage_list[2])
    # # print(stage_list[2])
    # print("----------------------------------")
    # print(stage_list[-1])
    
    # print("To do example!")
    # print(to_do_list[0][1])
    # print(type(to_do_list[0][1][0]))
    # print(to_do_list[0][1][0]._fluent)
    # # initial_state = unip.model.state.UPState(problem_object.initial_values)
    # # next_state = initial_state.make_child(to_do_list[0][1])
    # print(problem_object.initial_values)
    # print(plan_object)
    # print(to_do_list)
    # print(to_do_list[0])
    
    # print(plan_object.timed_actions[0])
    # print(plan_object.timed_actions[0][1].action)
    # print(plan_object.timed_actions[0][1].actual_parameters)
    # grounder = GrounderHelper(problem_object)
    # print(plan_object.timed_actions[0][0]+plan_object.timed_actions[0][2])
    # grounded_act = grounder.ground_action(plan_object.timed_actions[0][1].action, plan_object.timed_actions[0][1].actual_parameters)
    # #grounded_action = Grounder(plan_object.timed_actions[0][1].action, plan_object.timed_actions[0][1].actual_parameters)
    # #print(grounded_action)
    # print(grounded_act.effects)
    # print(type(grounded_act.effects))
    # print(grounded_act.effects.keys())
    # print(type(list(grounded_act.effects.keys())[0]))
    # print("111")
    #print(plan_object.timed_actions[8])
    # stage_list = parser.unified_Plan_generator.get_stages_from_plan(problem_object, plan_object)
    # print(stage_list)

    #print(problem_object)

        # plan = parser.Plan_generator.get_plan(domain_content,
        #                                       problem_content,
        #                                       url_link)

        # predicates_list = parser.Domain_parser.get_domain_json(domain_content)

        # problem_dic = parser.Problem_parser.get_problem_dic(problem_content, predicates_list)
        # object_list = parser.Problem_parser.get_object_list(problem_content)
        # animation_profile = json.loads(parser.Animation_parser.get_animation_profile(animation_content, object_list))
        # stages = parser.Predicates_generator.get_stages(plan, problem_dic, problem_content,
        #                                                 predicates_list)



        # result = solver.Solver.get_visualisation_dic(stages, animation_profile, plan['result']['plan'], problem_dic)
        # # A file called visualistaion.json will be generated in the folder if successful
        #objects_dic = Initialise.initialise_objects(stages["objects"], animation_profile)
        # final = Transfer.generate_visualisation_file(result, list(objects_dic.keys()), animation_profile,
        #                                              plan['result']['plan'])
    


if __name__ == "__main__":
    get_visualisation_file()
