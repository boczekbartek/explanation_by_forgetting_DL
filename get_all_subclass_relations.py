import argparse
from logging import log
import os
import logging

p = argparse.ArgumentParser()
p.add_argument("ontology")
p.add_argument("output")


def main(ontology, output):
    ontology_dir = os.path.dirname(ontology)
    output_dir = os.path.dirname(output)
    os.makedirs(output_dir, exist_ok=True)
    os.system("java -jar kr_functions.jar " + "saveAllSubClasses" + " " + ontology)
    os.rename(f"{ontology_dir}/subClasses.nt", output)
    logging.info(f"Subclasses saved to {output}.")


if __name__ == "__main__":
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO)
    main(**vars(args))
