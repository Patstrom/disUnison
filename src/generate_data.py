import os
import shutil
import subprocess, shlex

"""
A short script for copying the test suite, generating the .ext.json file
and running the gecode-solver to generate 1000 version for all strategies at
distances [1, 10, 100, 1000]. It create the following structure:
    
    functions/
        <name>/
            <name>.<strat>.<distance>/
        <name>/
            <name>.<strat>.<distance>/

and so on...

It shall also run the "export_directory" to create .unison.mir and move everything into
a structure that looks like this:
    programs.<strat>.<distance>/
        0/
            <name>.unison.mir
            <name>.unison.mir
        1/
            <name>.unison.mir
            <name>.unison.mir

and so on... I.e all version "0" from "schedule" of distance "1" should be in programs.sched.1/0/

"""
FUNCTION_DIR = "functions"
PROGRAM_DIR = "programs"

# Setup top level directories
if not os.path.exists(FUNCTION_DIR):
    os.mkdir(FUNCTION_DIR)

if not os.path.exists(PROGRAM_DIR):
    os.mkdir(PROGRAM_DIR)


tests_dir = "./unison/test/fast/Hexagon/speed/"

test_files = os.listdir(tests_dir)

function_names = []
for test_file in test_files:
    if ".mir" in test_file:
        function_name = test_file[0:test_file.index(".mir")]
        if ".asm" not in function_name:
            function_names.append(function_name)
#
#function_names.remove("sphinx3.glist.glist_tail") # Already done
#function_names.remove("sphinx3.profile.ptmr_init") # Already done
#
#function_names.remove("h264ref.vlc.symbol2uvlc") # Already done
#function_names.remove("h264ref.memalloc.no_mem_exit") # Already done
#function_names.remove("h264ref.sei.UpdateRandomAccess") # Already done
#
#function_names.remove("gcc.alias.get_frame_alias_set") # Already done
#function_names.remove("gcc.c-decl.pushdecl_top_level") # Already done
#function_names.remove("gcc.varasm.data_section") # Already done
#function_names.remove("gcc.insn-output.output_51") # Already done
#function_names.remove("gcc.rtlanal.parms_set") # Already done
#function_names.remove("gcc.expmed.ceil_log2") # Already done
#function_names.remove("gcc.jump.unsigned_condition") # Already done
#
#function_names.remove("gobmk.barriers.autohelperbarrierspat145") # Already Done
#function_names.remove("gobmk.patterns.autohelperpat301") # Already done
#function_names.remove("gobmk.interface.init_gnugo") # Already done
#function_names.remove("gobmk.owl_defendpat.autohelperowl_defendpat421") # Already done
#function_names.remove("gobmk.owl_vital_apat.autohelperowl_vital_apat34") # Already done
#function_names.remove("gobmk.patterns.autohelperpat1088") # Already done
#
#function_names.remove("mesa.api.glIndexd") # Already done

function_names.remove("gcc.xexit.xexit") # Problematic
function_names.remove("hmmer.tophits.AllocFancyAli") # Problematic


# Create a new directory structure
#for function in function_names:
#    nd = os.path.join(FUNCTION_DIR, function, "")
#    print(nd)
#    try:
#        os.mkdir(nd)
#    except Exception:
#        pass
#    for ext in [".mir", ".asm.mir"]:
#        shutil.copyfile(tests_dir + function + ext, nd + function + ext)
#
## Run uni_generate on everything
#for function in function_names:
#    path = os.path.join(FUNCTION_DIR, function)
#    os.chdir(path)
#    # Generate the files
#    command = "../../uni_generate.sh {0}.mir {0}.asm.mir".format(function)
#    print("Executing command:", command)
#    subprocess.call(shlex.split(command))
#    os.chdir("../..")

strategies = { "difference": "diff", "schedule": "sched", "registers": "registers" }
solution_distances = [1, 10, 100, 1000]

#for function in function_names:
#    path = os.path.join(FUNCTION_DIR, function)
#    os.chdir(path)
#    # Run gecode solver
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            output_dir = "{}.{}.{}/".format(function, output, dist)
#            command = "gecode-solver -num-solutions 1000 -solution-distance {} -o {} -diversify {} {}.ext.json" \
#                .format(dist, output_dir, strat, function )
#            print("Executing command:", command)
#            subprocess.call(shlex.split(command))
#    os.chdir("../..")

# Due to the gecode search engine requiring the constrain() function to be monotonic
# (which the diversify implementation is not) sometimes duplicates are generated. To fix
# this I used the "duder" utility to find the duplicates and then generated more solutions
# for that function until I had 1000 unique versions. Does some versions might have the
# wrong label (since I remove the duplicates)


# Export
#for function in function_names:
#    path = os.path.join(FUNCTION_DIR, function)
#    os.chdir(path)
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            output_dir = "{}.{}.{}/".format(function, output, dist)
#
#            export_command = "../../export_directory {}.alt.uni {}".format(function, output_dir)
#            print("Executing command:", export_command)
#            subprocess.call(shlex.split(export_command))
#    os.chdir("../..")

# Move everything around
#for function in function_names:
#    old_path = os.path.join(FUNCTION_DIR, function)
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            old_dir = os.path.join(old_path, "{}.{}.{}".format(function, output, dist), "exported")
#            new_dir = os.path.join(PROGRAM_DIR, "program.{}.{}".format(output, dist))
#            for f in os.listdir(old_dir):
#                version = f[0:f.index(".unison.mir")]
#                new_path = os.path.join(new_dir, version)
#                if not os.path.exists(new_path):
#                    os.makedirs(new_path)
#                old_name = os.path.join(old_dir, f)
#                new_name = os.path.join(new_path, "{}-{}.unison.mir".format(function, version))
#                shutil.copyfile(old_name, new_name)

# Find the costs of everything and add it to the place where it belongs
import json
for function in function_names:
    function_base_dir = os.path.join(FUNCTION_DIR)
    for strat,output in strategies.items():
        for dist in solution_distances:
            raw_json_dir = os.path.join(function_base_dir, function, "{}.{}.{}".format(function, output, dist))
            files = [f for f in os.listdir(raw_json_dir) if os.path.isfile(os.path.join(raw_json_dir, f))] # Get all files from out_json_dir

            for f in files:
                with open(os.path.join(raw_json_dir, f)) as input_file:
                    version = int(f) # Make sure it's actually an integer
                    output_file = os.path.join(PROGRAM_DIR, "program.{}.{}".format(output, dist), str(version), "cost")
                    cost = json.load(input_file)["cost"][0] # Cost is a list in case multipl goals are specified. We only use one
                    with open(output_file, "a") as out:
                        out.write("{}: {}\n".format(function, cost))
