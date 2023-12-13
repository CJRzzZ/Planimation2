"""This component transfers the result generated by Predicate Solver into the final visualisation file"""
# -----------------------------Authorship-----------------------------------------
# -- Authors  : Ella & Yi Ding
# -- Group    : Planning Visualisation
# -- Date     : 13/August/2018
# -- Version  : 1.0
# --------------------------------------------------------------------------------
# -----------------------------Reviewer-------------------------------------------
# -- Authors  : Yi Ding
# -- Group    : Planning Visualisation
# -- Date     : 16/October/2018
# -- Version  : 1.1
# --------------------------------------------------------------------------------
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import Subgoal_adapter


def generate_visualisation_file(result, object_list, animation_profile, action_list):
    """
    This function generates the visualisation file.
    :param result: the dict to be converted
    :param object_list: list of all the name of the objects
    :param animation_profile: animation_profile
    :param action_list: list of actions
    :return: visualisation file for the Unity Visualiser
    """
    final = {"visualStages": []}
    one_stage = {}
    sprite_list = []
    lists = result["visualStages"]
    panel_size, shift = get_panel_size(result)
    index = 0
    for item in lists:
        one_stage = item["visualSprites"]
        transfered_stage = transfer(one_stage, object_list, panel_size, shift)
        transfered_stage["stageName"] = item["stageName"]
        transfered_stage["stageInfo"] = item["stageInfo"]
        if (index == len(action_list)):
            transfered_stage["isFinal"] = "true"
        else:
            transfered_stage["isFinal"] = "false"
        sprite_list.append(transfered_stage)
        index = index + 1
    final["visualStages"] = sprite_list
    finalSubgoal = Subgoal_adapter.generate_subgoal(result["subgoals"])
    final["subgoalPool"] = finalSubgoal["subgoalPool"]
    final["subgoalMap"] = finalSubgoal["subgoalMap"]
    final["transferType"] = 1  # designed to indicate the different animation method: fade in/out or linear etc
    final["imageTable"] = animation_profile["imageTable"]
    final["message"] = ""
    return final


def transfer(one_stage, initialobjects, panel_size, shift, padding=20):
    """
    This function turn absolution position(x,y,width,height) into (minx,miny,maxX,maxY) format. where (0,0) means
    the left bottom coner, and (1,1) means top right coner of the animation Panel.
    :param one_stage: a dictionary contains the locaiton of objects for one stage/step
    :param initialobjects: the list to store all objects that needed to be shown in the animation profile.
    :param panel_size: the panel_size of the animation panel
    :param shift: add shift to all the object x,y which make left corner start from 0,0
    :param padding: space around the animation panel
    :return: a dictionary which contain position information can be used for unity visualser
    """

    # list that stores object name
    transfered_stage = {}
    temp = []
    # dict that stores new position info
    position_dic = {"minX": "",
                    "maxX": "",
                    "minY": "",
                    "maxY": ""}
    # new position info
    min_x = 0.0
    max_x = 0.0
    min_y = 0.0
    max_y = 0.0
    # generate new json file
    for obj in one_stage:
        if "x" not in one_stage[obj] or "y" not in one_stage[obj]:
            continue
        one_stage[obj]
        # get all information about position
        x_num = one_stage[obj]["x"]
        y_num = one_stage[obj]["y"]
        width = one_stage[obj]["width"]
        # set the panel with after we got the panel width
        if type(width) is str:
            if width.lower() == "panel_size":
                width = panel_size - 2 * padding
                one_stage[obj]["width"] = width
        height = one_stage[obj]["height"]
        # transfer the position info into position needed in Unity
        min_x = (x_num + padding + shift) / panel_size
        max_x = (x_num + shift + width + padding) / panel_size
        min_y = (y_num + shift + padding) / panel_size
        max_y = (y_num + shift + height + padding) / panel_size
        position_dic["minX"] = round(min_x, 3)
        position_dic["maxX"] = round(max_x, 3)
        position_dic["minY"] = round(min_y, 3)
        position_dic["maxY"] = round(max_y, 3)
        # update the old dict
        one_stage[obj].update(position_dic)
        temp.append(one_stage[obj])
    transfered_stage["visualSprites"] = temp
    return transfered_stage


def get_panel_size(result, padding=20):
    """
    This function will for loop all the objects in the visualisaiton dictionary,
    and try to find the max_x and max_y of the animation panel.
    .........max_y
    .        .
    .        .
    .        .
    ........max_x
    :param result: visualisation dictionary that contain the location of each object
                   for different stages.
    :param padding: padding between the object and the edge of the screen.
    :return: panel_size(the panel is an square based on our design,width=height)
            and shift(make sure no negative x,y for any object)
    """

    lists = result["visualStages"]
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for stage in lists:
        stageitems = stage["visualSprites"]

        for item in stageitems:
            if "x" not in stageitems[item] or "y" not in stageitems[item]:
                continue
            x = stageitems[item]["x"]
            y = stageitems[item]["y"]

            if type(stageitems[item]["width"]) is int:
                new_x = x + stageitems[item]["width"]
                if new_x > max_x:
                    max_x = new_x
                if x < min_x:
                    min_x = x
            if type(stageitems[item]["height"]) is int:
                new_y = y + stageitems[item]["height"]
                if new_y > max_y:
                    max_y = new_y
                if y < min_y:
                    min_y = y
    shift = max(abs(min_x), abs(min_y))
    panel_size = max(max_x, max_y) + shift + 2 * padding
    return panel_size, shift
