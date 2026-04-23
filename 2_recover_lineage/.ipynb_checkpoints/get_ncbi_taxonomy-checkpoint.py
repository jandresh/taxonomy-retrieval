##original script found here, modified https://stackoverflow.com/questions/36503042/how-to-get-taxonomic-specific-ids-for-kingdom-phylum-class-order-family-gen

import csv
import re
from ete3 import NCBITaxa

ncbi = NCBITaxa()

def get_desired_ranks(taxid, desired_ranks):
    #print taxid
    lineage = ncbi.get_lineage(taxid)
    #print lineage
    #taxid2name = ncbi.get_taxid_translator([taxid])
    #print taxid2name
    lineage2ranks = ncbi.get_rank(lineage)
    #print lineage2ranks
    ranks2lineage = dict((rank, ncbi.get_taxid_translator([taxid])) for (taxid, rank) in list(lineage2ranks.items()))
    #print ranks2lineage
    buffer = str(['{}'.format(v) for k,v in ranks2lineage.items()])
    m = re.findall(r"'(.*?)'", buffer)
    print(m)
    #original - return {'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}
    return {'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}

def main(taxids, desired_ranks, path):
    with open(path, 'w') as csvfile:
        fieldnames = ['{}_id'.format(rank) for rank in desired_ranks]
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for taxid in taxids:
            writer.writerow(get_desired_ranks(taxid, desired_ranks))

if __name__ == '__main__':
    f = open("taxids_output.fixed.txt")
    taxids = f.readlines()
    desired_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    path = 'full_ranks.txt'
    main(taxids, desired_ranks, path)
