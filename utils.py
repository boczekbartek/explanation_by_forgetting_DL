import os

# This is an example puython programme which shows how to use the different stand-alone versions of OWL reasoners and forgetting programme

# Choose the ontology (in the OWL format) for which you want to explain the entailed subsumption relations.
# inputOntology = "datasets/pizza_super_simple.owl"
inputOntology = "pizza_lethe_3/1ontology.owl"

# Choose the set of subclass for which you want to find an explanation.
# this file can be generated using the second command (saveAllSubClasses)
os.system("java -jar kr_functions.jar " + "saveAllSubClasses" + " " + inputOntology)
os.system("sort -u pizza_lethe_3/subClasses.nt > pizza_lethe_3/subClasses.uniq1.nt")
inputSubclassStatements = "pizza_lethe_3/subClasses.uniq1.nt"

subcls_l = []
os.makedirs("expl1", exist_ok=True)
with open(inputSubclassStatements) as f:
    sub = list(f.readlines())
with open(inputSubclassStatements) as f:
    for c, l in enumerate(f):
        fname = f"expl1/{c}.subCls.nt"
        with open(fname, "wt") as f1:
            print(l.strip(), file=f1)
        subcls_l.append(fname)

# Choose the ontology to which you want to apply forgetting. This can be the inputOntology, but in practise
# should be a smaller ontology, e.g. created as a justification for a subsumption

# Decide on a method for the forgetter (check the papers of LETHE to understand the different options).
# The default is 1, I believe.
# 1 - ALCHTBoxForgetter
# 2 - SHQTBoxForgetter
# 3 - ALCOntologyForgetter

# Choose the symbols which you want to forget.
# signature = "datasets/signature.txt"

# 1. PRINT ALL SUBCLASSES (inputOntology):
# print all subClass statements (explicit and inferred) in the inputOntology
# --> uncomment the following line to run this function
# os.system("java -jar kr_functions.jar " + "printAllSubClasses" + " " + inputOntology)

# 2. SAVE ALL SUBCLASSES (inputOntology):
# save all subClass statements (explicit and inferred) in the inputOntology to file datasets/subClasses.nt
# --> uncomment the following line to run this function

# 3. PRINT ALL EXPLANATIONS (inputOntology, inputSubclassStatements):
# print explanations for each subClass statement in the inputSubclassStatements
# --> uncomment the following line to run this function
# for c, f in enumerate(subcls_l):
#     print(sub[c], f)
# os.system(
#     "java -jar kr_functions.jar "
#     + "printAllExplanations"
#     + " "
#     + inputOntology
#     + " "
#     + f
# )

# 4. SAVE ALL EXPLANATIONS (inputOntology, inputSubclassStatements):
# save explanations for each subClass statement in the inputSubclassStatements to file datasets/exp-#.owl
# --> uncomment the following line to run this function
for c, f in enumerate(subcls_l):
    print(sub[c], f)
    os.system(
        "java -jar kr_functions.jar "
        + "saveAllExplanations"
        + " "
        + inputOntology
        + " "
        + f
    )
    if os.path.isfile("pizza_lethe_3/exp-1.omn"):
        os.rename("pizza_lethe_3/exp-1.omn", f + "expl.omn")
        print("->", f + "expl.omn")

# For running LETHE forget command:
# --> uncomment the following line to run this function
# os.system(
#     "java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile "
#     + inputOntology
#     + " --method "
#     + method
#     + " --signature "
#     + signature
# )

