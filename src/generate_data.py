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

#tests_dir = "./unison/test/fast/Hexagon/speed/"
#new_dir = "functions/"
#
#test_files = os.listdir(tests_dir)
#
#function_names = []
#for test_file in test_files:
#    if ".mir" in test_file:
#        function_name = test_file[0:test_file.index(".mir")]
#        if ".asm" not in function_name:
#            function_names.append(function_name)
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
#try:
#    try:
#        os.mkdir("functions")
#    except Exception:
#        pass
#    try:
#        for function in function_names:
#            nd = new_dir + function + "/"
#            try:
#                os.mkdir(nd)
#            except Exception:
#                pass
#            for ext in [".mir", ".asm.mir"]:
#                shutil.copyfile(tests_dir + function + ext, nd + function + ext)
#    except Exception as e:
#        pass
#except Exception as e:
#    print("Top-level failure during dir structure", e)
#
## Run uni_generate on everything
#for function in function_names:
#    path = new_dir + function + "/"
#    os.chdir(path)
#    # Generate the files
#    command = "../../uni_generate.sh " + function + ".mir " + function + ".asm.mir"
#    print("Executing command:", command)
#    subprocess.call(shlex.split(command))
#    os.chdir("../..")

strategies = { "difference": "diff", "schedule": "sched", "registers": "registers" }
solution_distances = [1, 10, 100, 1000]

#for function in function_names:
#    path = new_dir + function
#    os.chdir(path)
#    # Run gecode solver
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            output_dir = function + "." + output + "." + str(dist)
#            command = "gecode-solver -num-solutions 1000 -solution-distance {} -o {} -diversify {} {}" \
#                .format(dist, output_dir, strat, function + ".ext.json" )
#            print("Executing command:", command)
#            subprocess.call(shlex.split(command))
#
#            #export_command = "../../export_directory " + function + ".alt.uni " + output_dir + "/"
#            #print("Executing command:", export_command)
#            #subprocess.call(shlex.split(export_command))
#    os.chdir("../..")

## Due to the gecode search engine requiring the constrain() function to be monotonic
## (which the diversify implementation is not) sometimes duplicates are generated. To fix
## this I used the "duder" utility to find the duplicates and then generated more solutions
## for that function until I had 1000 unique versions. Does some versions might have the
## wrong label (since I remove the duplicates)

for function in function_names:
    path = new_dir + function
    for strat, output in strategies.items():
        for dist in solution_distances:
            output_dir = function + "." + output + "." + str(dist)
            for i, f in enumerate(os.listdir(output_dir)):
                version = int(f)
                print(version)
#
## Export
#for function in function_names:
#    path = new_dir + function
#    os.chdir(path)
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            output_dir = function + "." + output + "." + str(dist)
#
#            export_command = "../../export_directory " + function + ".alt.uni " + output_dir + "/"
#            print("Executing command:", export_command)
#            subprocess.call(shlex.split(export_command))
#    os.chdir("../..")

## Make program directories
#for strat, output in strategies.items():
#    for dist in solution_distances:
#        try:
#            os.mkdir("program.{}.{}".format(strat, dist))
#        except Exception:
#            pass
#
## Move everything around
#for function in function_names:
#    old_path = new_dir + function
#    for strat, output in strategies.items():
#        for dist in solution_distances:
#            new_dir = "program.{}.{}".format(strat,dist)
#            old_dir = old_path + "/{}.{}.{}/exported".format(function, strat, dist)
#            for f in os.listdir(old_dir):
#                version = f[0:f.index(".unison.mir")]
#                new_path = new_dir + "/" + version
#                try:
#                    os.makedir(new_path)
#                except Exception:
#                    pass
#                print(old_dir + f, new_path + function + version)
#                #shutil.copyfile(old_dir + f, new_path + function)
