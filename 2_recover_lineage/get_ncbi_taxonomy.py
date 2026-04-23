##original script found here, modified https://stackoverflow.com/questions/36503042/how-to-get-taxonomic-specific-ids-for-kingdom-phylum-class-order-family-gen

import csv
import re
from ete3 import NCBITaxa
import plotly.graph_objects as go
import random

ncbi = NCBITaxa()

def get_desired_ranks(taxid, desired_ranks, species_data):
    lineage = ncbi.get_lineage(taxid)
    lineage2ranks = ncbi.get_rank(lineage)
    ranks2lineage = dict((rank, ncbi.get_taxid_translator([taxid])) for (taxid, rank) in list(lineage2ranks.items()))
    species_data.append({rank: list(ranks2lineage.get(rank, {1: None}).values())[0] for rank in desired_ranks})
    return {'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}

def sankey_graph():
   nodes = dict(
       label=["A", "B", "C", "D", "E", "F"],
       color=["blue", "blue", "blue", "red", "red", "red"]
   )

   links = dict(
       source=[0, 1, 1, 2, 3, 4],
       target=[3, 3, 4, 5, 5, 5],
       value=[8, 4, 2, 8, 4, 2]
   )

   fig = go.Figure(data=[go.Sankey(node=nodes, link=links)])

   fig.update_layout(title_text="Ejemplo de Gráfica Sankey", font_size=10)
   fig.show()

def taxonomy_graph(species_data):
    taxonomy_tree = {}

    for specie in species_data:
        superkingdom = specie['superkingdom']
        kingdom = specie['kingdom']
        phylum = specie['phylum']
        class_id = specie['class']
        order = specie['order']
        family = specie['family']
        genus = specie['genus']
        specie_name = specie['species']

        if superkingdom not in taxonomy_tree:
            taxonomy_tree[superkingdom] = {}
        if kingdom not in taxonomy_tree[superkingdom]:
            taxonomy_tree[superkingdom][kingdom] = {}
        if phylum not in taxonomy_tree[superkingdom][kingdom]:
            taxonomy_tree[superkingdom][kingdom][phylum] = {}
        if class_id not in taxonomy_tree[superkingdom][kingdom][phylum]:
            taxonomy_tree[superkingdom][kingdom][phylum][class_id] = {}
        if order not in taxonomy_tree[superkingdom][kingdom][phylum][class_id]:
            taxonomy_tree[superkingdom][kingdom][phylum][class_id][order] = {}
        if family not in taxonomy_tree[superkingdom][kingdom][phylum][class_id][order]:
            taxonomy_tree[superkingdom][kingdom][phylum][class_id][order][family] = {}
        if genus not in taxonomy_tree[superkingdom][kingdom][phylum][class_id][order][family]:
            taxonomy_tree[superkingdom][kingdom][phylum][class_id][order][family][genus] = []

        if specie_name not in taxonomy_tree[superkingdom][kingdom][phylum][class_id][order][family][genus]:
            taxonomy_tree[superkingdom][kingdom][phylum][class_id][order][family][genus].append(specie_name)

        # print(taxonomy_tree)

    # Matriz de comunidades proveniente de wolfram

    matrix = [
        [
            1,
            7,
            10,
            15,
            16,
            19,
            26,
            27,
            28,
            29,
            32,
            53,
            64,
            82,
            91,
            98,
            101,
            103,
            104,
            119,
            122,
            144,
            150,
            194,
            195,
            206,
        ],
        [
            8,
            17,
            30,
            36,
            46,
            89,
            110,
            140,
            141,
            151,
            152,
            153,
            158,
            165,
            169,
            181,
            186,
            196,
            197,
            202,
            211,
            213,
            229,
            236,
            239,
        ],
        [
            4,
            31,
            34,
            54,
            58,
            62,
            65,
            74,
            75,
            78,
            93,
            95,
            96,
            129,
            135,
            142,
            149,
            162,
            164,
            178,
            200,
            219,
            233,
        ],
        [
            2,
            3,
            24,
            48,
            51,
            72,
            90,
            137,
            138,
            139,
            175,
            176,
            192,
            203,
            210,
            214,
            226,
            238,
        ],
        [68, 84, 114, 127, 148, 172, 204, 215, 216, 221, 222, 232],
        [49, 73, 146, 187, 201, 227, 231],
        [56, 80, 86, 108, 109, 168, 199],
        [22, 39, 55, 59, 154, 193],
        [35, 45, 69, 81],
        [136, 166, 218],
        [159, 209, 230],
        [14, 107],
        [21, 228],
        [33, 147],
        [42, 47],
        [44, 223],
        [116, 155],
        [118, 160],
        [120, 220],
        [143, 145],
        [174, 205],
        [190, 207],
        [191, 198],
        [5],
        [6],
        [9],
        [11],
        [12],
        [13],
        [18],
        [20],
        [23],
        [25],
        [37],
        [38],
        [40],
        [41],
        [43],
        [50],
        [52],
        [57],
        [60],
        [61],
        [63],
        [66],
        [67],
        [70],
        [71],
        [76],
        [77],
        [79],
        [83],
        [85],
        [87],
        [88],
        [92],
        [94],
        [97],
        [99],
        [100],
        [102],
        [105],
        [106],
        [111],
        [112],
        [113],
        [115],
        [117],
        [121],
        [123],
        [124],
        [125],
        [126],
        [128],
        [130],
        [131],
        [132],
        [133],
        [134],
        [156],
        [157],
        [161],
        [163],
        [167],
        [170],
        [171],
        [173],
        [177],
        [179],
        [180],
        [182],
        [183],
        [184],
        [185],
        [188],
        [189],
        [208],
        [212],
        [217],
        [224],
        [225],
        [234],
        [235],
        [237],
    ]

    with open("SpeciesListTaxAPOE.txt", "r") as file:
        species_list = [line.strip().lower().replace(" ", "") for line in file.readlines()]
        # print(species_list)

    def specie_to_index(specie):
        specie = specie.strip().lower().replace(" ", "")
        for index, item in enumerate(species_list):
            if specie in item:
                return index

        return None

    def random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        color_hex = f'#{r:02x}{g:02x}{b:02x}'

        return color_hex

    comunity_colors = [random_color() for _ in matrix]

    species_vs_comunity = {}
    for comunity, species in enumerate(matrix):
        for specie in species:
            species_vs_comunity[specie] = comunity

    def get_comunity(text):
        index = specie_to_index(text)
        print(f"{text}:{index}")
        if index is not None:
            return species_vs_comunity[index+1]

        return None

    def get_item_color(item = None):
        comunity = get_comunity(item) if item is not None else None
        if comunity is not None and comunity <= len(comunity_colors):
            return comunity_colors[comunity]

        return "#d9d9d6"

    def string_cut(string, length):
        if len(string) < length:
            return string
        print(string[:length])
        return string[:length]

    def process_graph_data(taxonomy: dict, labels: list, parents: list, colors: list):
        for superkingdom, kingdoms in taxonomy.items():
            if not superkingdom:
                continue
            parents.append("")
            labels.append(superkingdom)
            colors.append(get_item_color())
            for kingdom, phyla in kingdoms.items():
                if not kingdom:
                  continue
                parents.append(superkingdom)
                labels.append(kingdom)
                colors.append(get_item_color())
                for phylum, classes in phyla.items():
                    if not phylum:
                        continue
                    parents.append(kingdom)
                    labels.append(phylum)
                    colors.append(get_item_color())
                    for class_, orders in classes.items():
                        if not class_:
                            continue
                        parents.append(phylum)
                        labels.append(class_)
                        colors.append(get_item_color())
                        for order, families in orders.items():
                            if not order:
                                continue
                            parents.append(class_)
                            labels.append(order)
                            colors.append(get_item_color())
                            for family, genera in families.items():
                                if not family:
                                    continue
                                parents.append(order)
                                labels.append(family)
                                colors.append(get_item_color())
                                for genus, species in genera.items():
                                    if not genus:
                                        continue
                                    parents.append(family)
                                    labels.append(genus)
                                    colors.append(get_item_color())
                                    for specie in species:
                                        if not specie:
                                            continue
                                        specie_cut = string_cut(specie, 17)
                                        if specie_cut not in labels:
                                            parents.append(genus)
                                            labels.append(specie_cut)
                                            colors.append(get_item_color(specie))

    parents = []
    labels = []
    colors = []
    process_graph_data(taxonomy_tree, labels, parents, colors)

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        marker=dict(colors=colors),
        textfont=dict(size=20)
    ))

    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0))
    fig.show()
    fig.write_html("outputTreemap.html")


def main(taxids, desired_ranks, path):
    species_data = []
    with open(path, 'w') as csvfile:
        fieldnames = ['{}_id'.format(rank) for rank in desired_ranks]
        writer = csv.DictWriter(csvfile, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for taxid in taxids:
            writer.writerow(get_desired_ranks(taxid, desired_ranks, species_data))
    print(f"species_data={species_data}")

    taxonomy_graph(species_data)

if __name__ == '__main__':
    f = open("taxids_output.fixed.txt")
    taxids = f.readlines()
    desired_ranks = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    path = 'full_ranks.txt'
    main(taxids, desired_ranks, path)
