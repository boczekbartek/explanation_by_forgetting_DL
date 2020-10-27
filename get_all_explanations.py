import argparse
from logging import log
import os
import logging
from re import sub
from tqdm import tqdm
from main import explain

p = argparse.ArgumentParser()
p.add_argument("ontology")
p.add_argument("output_dir")
p.add_argument("subclasses")


def wc_l(fname: str) -> int:
    """ Count number of lines in file (aka uniq wc -l command)"""
    cnt = 0
    with open(fname) as f:
        for _ in f:
            cnt += 1
    return cnt


def save_entailment(ent, fname):
    with open(fname, "wt") as fd:
        print(ent, file=fd)


def main(ontology, output_dir, subclasses):
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Opening subclasses file: {subclasses}")
    total = wc_l(subclasses)
    ontology_dir = os.path.dirname(ontology)
    with open(subclasses) as fd:
        for i, entailment in enumerate(tqdm(fd, total=total)):
            logging.info(f"Processing entailment: {entailment}")
            ent_fname = f"{output_dir}/{i}.ent.nt"
            logging.info(f"Saving entailment to: {ent_fname}")
            save_entailment(entailment, ent_fname)
            expl_fname = f"{output_dir}/{i}.expl.omn"
            logging.info(f"Saving explanation to: {expl_fname}")
            explain(ontology, ent_fname, expl_fname, workdir=ontology_dir)


if __name__ == "__main__":
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(**vars(args))
