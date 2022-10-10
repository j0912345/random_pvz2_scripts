#this file is licensed under the MIT License

#Copyright (c) 2022 j0

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
print("//// welcome to jo's plantlevels.json stat extender ////")
print("free download and source code is here: https://github.com/j0912345/random_pvz2_scripts\n")
import json
import pathlib
import os


def copy_level_stats_levels_for_plant_x_times(plant_name, x, json: dict, stat_list_len=2):
    not_done = True
    i = 0
    plant_json_segment = {}
    plant_json_segment = extract_plant_segment_from_json(plant_name=plant_name, jsonobj=json)
    # get the plant we are looking for
#    while not_done:
#        plant_json_segment = json["objects"][i]
#        if plant_json_segment["aliases"][0] == plant_name:
#            not_done = False
#            plant_json_segment["__TMP_SCRIPT_INDEX_NUMBER_NOT_INGAME__"] = [i]
#        i+=1
    print("\nfound the plant. json data:")
    print(plant_json_segment, end="\n\n")

    objdata = plant_json_segment["objdata"]
    objdata["Usesleveling"] = True
    objdata["LevelCap"] = x

    names_to_extend = get_names_of_only_lists_in_dict(objdata)
    print("extracted the lists. json data:")
    print(names_to_extend)

    # im is used to keep track of which exact value we're copying
    # i.e. an item number in a list. when im would become greater than len(list), it gets reset to 0
    im = 0
    # obj data gets modded, this copy doesn't
    im_objdata_copy = objdata

#    i = 0
    # si is used for the current sub list getting extended
    si = 0
    not_done = True

    # this has all of the top level values like float stats
    for ext_i in range(0,len(names_to_extend)):
        #this does all of the sub lists
        not_done_adding_stats = True
        current_toplevel_name = names_to_extend[ext_i]
        # this does float stats
        print(current_toplevel_name)
        si = 0
        while len(objdata[current_toplevel_name]) > si:
            for xx in range(0, x):
#                print("this name contains:")
#                print(type(objdata[current_toplevel_name][si]))
                if type(objdata[current_toplevel_name][0]) != int:
                    objdata[current_toplevel_name][si]["Values"].append(im_objdata_copy[current_toplevel_name][si]["Values"][im])
                else:
                    si+=1
                    objdata[current_toplevel_name].append(im_objdata_copy[current_toplevel_name][im])
                
                im = (im+1)%stat_list_len
            
#                print(objdata[current_toplevel_name][si]["Values"])
            si+=1
    plant_json_segment["objdata"] = objdata
    return plant_json_segment


def get_names_of_only_lists_in_dict(x: dict):
    names = []
    not_names = []
    # this list only has string names
    y = list(x)
    for i in range(0, len(y)):
        current_item = x[ y[i] ]
        if type( current_item) == list:
            names += [y[i]]
        else:
            not_names += [y[i]]

    return names


def get_json_and_create_backup(path, sub_path):
    with open(path, "r") as f:
        pl_data = f.read()
        r = json.loads(pl_data)
        f.close()
        with open(sub_path, "w") as wf:
            wf.write(pl_data)
            wf.close()
        return r

def get_json(path):
    with open(path, "r") as f:
        pl_data = f.read()
        r = json.loads(pl_data)
        f.close()
        return r

def save_edited_plant_segment(seg: dict, file_path: str):
    json_obj = get_json(file_path)
    json_obj["objects"][seg["__TMP_SCRIPT_INDEX_NUMBER_NOT_INGAME__"][0]] = seg
    with open(file_path, "w") as f:
        json.dump(fp=f, obj=json_obj, indent=4)

def extract_plant_segment_from_json(plant_name: str, jsonobj: dict):
    plant_json_segment = {}
    not_done = True
    i = 0
    while not_done:
        plant_json_segment = jsonobj["objects"][i]
        if plant_json_segment["aliases"][0] == plant_name:
            not_done = False
            plant_json_segment["__TMP_SCRIPT_INDEX_NUMBER_NOT_INGAME__"] = [i]
        i+=1
    return plant_json_segment

if __name__ == "__main__":
    sub_path = r""
    using_sub_path = bool(int(input("save backup file in cwd? (pick 1 if you don't know what this is.) (1/0, 1 or invalid input = yes, 0 = no)")))
    if using_sub_path == True or using_sub_path == None:
        sub_path = os.path.dirname(os.getcwd()) + "/backup_of_plant_levels.json"
    else:
        sub_path = "./backup_of_plant_levels.json"
    print(f"ok, backup will be saved in \"{sub_path}\"")
    path = input("where is your plant_levels.json file that you'd like to edit? ")
    # // start //
    plant_seg = copy_level_stats_levels_for_plant_x_times(input("which plant do you want to edit? (this needs to be the name in plantlevels)"),
    int(input("how many times do you want the stats to be repeated? (this many stats wil get added, not be the final total)")),
    get_json_and_create_backup(path, sub_path),
    int(input("how many different stats are there? (how many levels until it gets looped back to the first one)")))
    print("saving file...")
    save_edited_plant_segment(plant_seg, path)
    print("done. if you find that you don't like the changes make there is a backup of the file before it was edited here: ")
