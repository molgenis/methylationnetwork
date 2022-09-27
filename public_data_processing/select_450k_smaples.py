import os
import argparse


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gse", dest="gse", type=str)
    return parser.parse_args()

arguments = parseArguments()
gse = arguments.gse
idat_dir = "/scratch/p283190/methylation/idat/%s/project_%s"%(gse, gse)
print("/data/p283190/gsm_platforms/uuid_%s_platforms.txt"%gse)
valid_gsm = set([item.strip() for item in
               open("/data/p283190/gsm_platforms/uuid_%s_platforms.txt"%gse, "r").readlines()])
idat_gsm = os.listdir(idat_dir)
for filename in idat_gsm:
    gsm = filename.split("_")[0]
    if gsm not in valid_gsm:
        print("Removing file ", os.path.join(idat_dir, filename))
        os.remove(os.path.join(idat_dir, filename))
    else:
        print("Actual 450k data!")