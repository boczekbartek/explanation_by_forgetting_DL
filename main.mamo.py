from argparse import ArgumentError
import os
import subprocess
from collections import defaultdict
from typing import List
import shutil
from pprint import pprint
import argparse
import random
import sys

random.seed(22)


def run_cmd(cmd):
    """ Run command and return its output as string """
    return subprocess.check_output(cmd, shell=True, universal_newlines=True)


def create_freq_index(subclasses: str) -> dict:
    """ 
    Create frequency table for subclasses 
    
    Parameters
    ----------
    subclasses: str
        File with subclasses. Created with 'kr_functions.jar saveAllSubClasses' function.
    """
    counter = defaultdict(int)
    with open(subclasses, "rt") as fd:
        for l in fd:
            if "subClassOf" in l:
                _class = l.split(" ")[0].strip().replace("<", "").replace(">", "")
                counter[_class] += 1
        return counter


def get_all_subclasses(ontology: str, workdir: str, out: str):
    """
    Get all subclasses and dump the to file

    Parameters
    ----------
    ontology: str
        File with ontology
    workdir: str
        Working directory
    out: str
        Output file for subclasses
    """
    os.system(f"java -jar kr_functions.jar saveAllSubClasses {ontology} 2>/dev/null")
    os.system(
        f"sort -u {workdir}/subClasses.nt | grep -v ObjectIntersectionOf | grep -v ObjectSomeV > {out}"
    )


def run_forgetter(
    ontology: str, out_fname: str, symbols_fname, method: str = "2"
) -> str:
    """
    Run LETHE forgetting tool.

    Parameters
    ----------
    ontology: str
        File with ontology from which we want to forget
    out_fname: str
        Filename of output file for new ontologi
    symbols_fname: str
        File with symbols to forget from ontology
    method: str
        Method for LETHE: 1 - ALCHTBoxForgetter, 2 - SHQTBoxForgetter, 3 - ALCOntologyForgetter
    """
    cmd = f"java -cp lethe-standalone.jar uk.ac.man.cs.lethe.internal.application.ForgettingConsoleApplication --owlFile {ontology} --method {method} --signature {symbols_fname}"
    os.system(cmd)
    os.rename("result.owl", out_fname)


def explain(ontology: str, subclass_statement: str, expl_f: str, workdir: str) -> str:
    """ 
    Create explanation for subclass statement
    
    Parameters
    ----------
    ontology: str
        File with ontology from which we want to forget
    subclass_statements: str
        File with subclass statement (entailment) to explain
    expl_f: str
        Output file for explanation
    workdir: str
        Working directory
    """
    cmd = f"java -jar kr_functions.jar saveAllExplanations {ontology} {subclass_statement} 2>/dev/null"
    os.system(cmd)
    if not os.path.exists('f"{workdir}/exp-1.omn"'):
        os.rename(f"{workdir}/exp-1.omn", expl_f)
    else:
        raise AssertionError(f"No explanation: {cmd}")


def wc_l(fname: str) -> int:
    """ Count number of lines in file (aka uniq wc -l command)"""
    cnt = 0
    with open(fname) as f:
        for _ in f:
            cnt += 1
    return cnt


def explain_by_forgetting(
    my_entailment_f: str,
    ontology: str,
    method: str,
    nforget: int,
    sel_method: str,
    workdir: str = "",
):
    """ 
    Explain entailment by sequence of forgetting. Forget most occurrent subclass each step. 
    
    Parameters
    ----------
    my_entailment_f: str
        File with entailment to explain
    ontology: str
        File with ontology
    method: str
        Forgetting method for LETHE tool: 1 - ALCHTBoxForgetter, 2 - SHQTBoxForgetter, 3 - ALCOntologyForgetter
    workdir: str
        Working directory (will be created if not exists)
    """
    # filter out symbol we want to explain
    os.makedirs(workdir, exist_ok=True)
    it = 0
    with open(my_entailment_f) as fd:
        my_entailment = fd.read()
    not_forget_s1 = (
        my_entailment.split(" ")[0].strip().replace("<", "").replace(">", "")
    )  # Cajun
    not_forget_s2 = (
        my_entailment.split(" ")[2].strip().replace("<", "").replace(">", "")
    )  # Food
    first_ontology = f"{workdir}/{it}ontology.owl"
    shutil.copyfile(ontology, first_ontology)

    subclasses_f = f"{workdir}/{it}all_subcls.nt"
    get_all_subclasses(first_ontology, workdir, subclasses_f)
    print(f"Subcls: {subclasses_f}", flush=True, file=sys.stderr)
    counter = create_freq_index(subclasses_f)
    while len(counter) > 2:
        cur_ontology = f"{workdir}/{it}ontology.owl"
        print(f"Iteration {it}, symbols: {len(counter)}", flush=True, file=sys.stderr)
        # get most frequent symbol

        vocab = list(counter.keys())
        with open(f"{workdir}/{it}vocab.txt", "wt") as fd:
            for c in vocab:
                print(c, file=fd)
        counter = {
            k: v for k, v in counter.items() if k not in (not_forget_s1, not_forget_s2)
        }

        # # get explanation for this step
        expl_f = f"{workdir}/{it}exp.omn"

        # TODO here is the problem in 2nd iteration -> it won't explain the entailment
        explain(cur_ontology, my_entailment_f, expl_f, workdir)

        expl_len = wc_l(expl_f)
        print(f"Explanation length: {expl_len}", flush=True, file=sys.stderr)

        counter = {
            k: v for k, v in counter.items() if k not in (not_forget_s1, not_forget_s2)
        }

        if sel_method == "most_freq":
            freqs = sorted(counter.items(), key=lambda it: it[1], reverse=True)[
                0:nforget
            ]
            symbols = [x[0] for x in freqs]
        elif sel_method == "random":
            if nforget <= len(list(counter.keys())):
                symbols = random.sample(list(counter.keys()), nforget)
            else:
                symbols = list(counter.keys())

        else:
            raise ArgumentError(f"Method not suupported: {method}")
        # prepare for forgetting
        symbols_f = f"{workdir}/{it}symbols.txt"
        with open(symbols_f, "wt") as fd:
            for s in symbols:
                # TODO this is sstupi hardcode, this should be derived from ontology, works only for pizza_super_simple.owl
                print(s, file=fd)

        next_ontology = f"{workdir}/{it+1}ontology.owl"
        print(counter, file=sys.stderr, flush=True)
        print(not_forget_s1, file=sys.stderr, flush=True)
        print(not_forget_s2, file=sys.stderr, flush=True)

        print(
            f"Forgetting: I_OWL: {cur_ontology}, O_OWL: {next_ontology}, S: {symbols_f} {symbols}",
            flush=True,
            file=sys.stderr,
        )
        run_forgetter(
            ontology=cur_ontology,
            symbols_fname=symbols_f,
            out_fname=next_ontology,
            method=method,
        )
        it += 1
        subclasses_f = f"{workdir}/{it}all_subcls.nt"
        get_all_subclasses(next_ontology, workdir, subclasses_f)
        print(f"Subcls: {subclasses_f}", flush=True, file=sys.stderr)
        counter = create_freq_index(subclasses_f)


if __name__ == "__main__":
    # ontology = "datasets/pizza_super_simple.owl"
    p = argparse.ArgumentParser()
    p.add_argument("nforget", type=int)
    p.add_argument("--method", required=True, choices=("most_freq", "random"), type=str)

    here = os.path.abspath(os.path.dirname(__file__))
    ontology = f"mamo_ontology/ontology/mamo-xml.owl"
    m = "1"
    args = p.parse_args()
    nforget = args.nforget
    method = args.method
    workdir = f"mamo_ontology/workdir_{nforget}_{method}"
    os.makedirs(workdir, exist_ok=True)

    # This is the entailment we want to explain
    # my_entailment = "<http://www.co-ode.org/ontologies/pizza/pizza.owl#Cajun> <http://www.w3.org/2000/01/rdf-schema#subClassOf>  <http://www.co-ode.org/ontologies/pizza/pizza.owl#Food> ."
    my_entailment = "<http://identifiers.org/mamo/MAMO_0000204> rdfs:subClassOf <http://identifiers.org/mamo/MAMO_0000037> ."
    my_entailment_f = f"{workdir}/my_entailment.nt"
    with open(my_entailment_f, "wt") as fd:
        print(my_entailment, file=fd)

    counter = explain_by_forgetting(
        my_entailment_f,
        ontology,
        method=m,
        workdir=workdir,
        nforget=nforget,
        sel_method=method,
    )

