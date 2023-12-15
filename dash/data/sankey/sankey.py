import re
import glob
import os
import pandas as pd
import json
from typing import Dict, List, Tuple, Set, TypedDict
from collections import OrderedDict

# Type aliases for clarity
NodeMap = Dict[str, str]
NodeEdge = Tuple[str, str, int]
SankeyData = Dict[str, any]


# define named class called sankey_section
class SankeySection(TypedDict):
    id: str
    desc: str
    linkcolor: int
    nodes: dict[str, str]
    edges: list[Tuple[str, str, int]]
    pos: list[str, str]


def add_prefix_to_dest_in_section(edges, nodes):
    # Map each destination node to its source node
    dest_map = {dest: src for src, dest, _ in edges}

    # Add prefix to destination nodes in edges
    new_edges = [
        (src, f"{src}_{dest}" if dest in dest_map else dest, value)
        for src, dest, value in edges
    ]

    # Rename nodes in the nodes map according to dest_map
    new_nodes = {
        node_id if node_id not in dest_map else f"{dest_map[node_id]}_{node_id}": label
        for node_id, label in nodes.items()
    }

    return new_edges, new_nodes


def create_sankey_section(fname: str) -> None:
    df = pd.read_csv(fname)
    node_keys = df["dest_abbrev"].tolist()
    node_labels = df["dest_name"].tolist()
    node_dict = dict(zip(node_keys, node_labels))
    df = df.dropna()
    src = df["source_abbrev"].tolist()
    dest = df["dest_abbrev"].tolist()
    amount = df["amount"].astype(int).tolist()
    edges = list(zip(src, dest, amount))

    sec_id = fname.replace(".csv", "")
    sec_xpos_map = {
        "goi": "l1",
    }

    if sec_id in sec_xpos_map:
        xpos = sec_xpos_map[sec_id]
    else:
        xpos = "l2"
    ypos = f"y{sec_id}"

    edges = sorted(edges, key=lambda x: x[2], reverse=True)
    if sec_id == "goi":
        node_tuples = list(node_dict.items())
        node_tuples = map(lambda x: (x[0].replace("g2_", ""), x[1]), node_tuples)
        node_dict = dict(node_tuples)
        edges = map(lambda x: (x[0], x[1].replace("g2_", ""), x[2]), edges)

    sankey_section: SankeySection = {
        "id": sec_id,
        "desc": f"{sec_id} section",
        "linkcolor": 0,  # Default link color, can be adjusted as needed
        "nodes": node_dict,
        "edges": edges,
        "pos": {"x": xpos, "y": ypos},
    }

    print(sankey_section)

    return sankey_section


def merge_sankey_sections(
    sections: List[SankeySection],
) -> Tuple[NodeMap, List[NodeEdge]]:
    """Merge all nodes and edges from all sections into one common data structure."""
    merged_nodes = {}
    merged_edges = []
    for section_idx, section in enumerate(sections):
        new_nodes = section["nodes"]
        new_edges = section["edges"]
        # if section_idx == 0:
        #     merged_nodes.update(section["nodes"])
        #     merged_edges.extend(section["edges"])
        #     continue

        # new_edges, new_nodes = add_prefix_to_dest_in_section(
        #     section["edges"], section["nodes"]
        # )

        merged_nodes.update(new_nodes)
        merged_edges.extend(new_edges)
    return merged_nodes, merged_edges


def dfs_emit_sections(
    start_node: str, edges: List[NodeEdge], nodes: NodeMap
) -> List[SankeySection]:
    """Do a DFS on the edges starting from root and emit a separate section for each intermediate node."""
    visited = set()
    sections = []

    def dfs(node: str, parent_section: SankeySection):
        visited.add(node)
        # Create a new section for the current node
        current_section = {
            "id": parent_section["id"] + "_" + node,
            "desc": f"{nodes[node]} section",
            "linkcolor": parent_section["linkcolor"],
            "nodes": {node: nodes[node]},
            "edges": [],
        }

        for edge in edges:
            src, dest, value = edge
            if src == node and dest not in visited:
                current_section["edges"].append(edge)
                current_section["nodes"][dest] = nodes[dest]
                # Recursive DFS call
                if "g2" in src:
                    dfs(dest, current_section)
        sections.append(current_section)

    # Start DFS from the root node
    root_section = {
        "id": "root",
        "desc": "Root section",
        "linkcolor": 0,  # Default link color, can be adjusted as needed
        "nodes": {start_node: nodes[start_node]},
        "edges": [],
    }
    dfs(start_node, root_section)
    return sections


def do_section_postprocess(section: dict) -> dict:
    section["edges"] = sorted(section["edges"], key=lambda x: x[2], reverse=True)
    yposkey = section["id"].split("_")[-1]
    sec_x = "l2"
    if section["id"] == "root_g2":
        sec_x = "l1"
    section["pos"] = {"x": sec_x, "y": f"y{yposkey}"}
    return section


def do_merge(sankey_json: dict, file_path_out: str):
    # Merge all nodes and edges into one common data structure
    merged_nodes, merged_edges = merge_sankey_sections(sankey_json["data"])

    # Perform DFS and emit sections
    sankey_sections = dfs_emit_sections(
        sankey_json["metadata"]["root"], merged_edges, merged_nodes
    )

    sankey_sections = sorted(sankey_sections, key=lambda x: x["id"])
    sankey_sections[0] = create_sankey_section("goi.csv")

    sankey_sections = list(map(do_section_postprocess, sankey_sections))
    for section in sankey_sections:
        sec_id = section["id"]
        # print(f'"{sec_id}",')
        print(f'"{sec_id}": 0.01,')
        # print(section["id"] + ",")

    sankey_sec_ids = [section["id"] for section in sankey_sections]
    sankey_sec_ypos = [section["pos"]["y"] for section in sankey_sections]
    metadata = sankey_json["metadata"]
    metadata["all"] = sankey_sec_ids
    metadata["active"] = sankey_sec_ids
    metadata["ypos"] = {ypos: 0.01 for ypos in sankey_sec_ypos}

    new_json = sankey_json
    new_json["metadata"] = metadata
    new_json["data"] = sankey_sections

    # Print or return the new sections
    new_json = json.dumps(new_json, indent=2)
    # print(new_json)
    return new_json
    pass


def do_sort_ypos(sankey_json: dict, file_path_out: str) -> dict:
    ypos_cur = sankey_json["metadata"]["ypos"]
    print(ypos_cur)
    g2_edges = sankey_json["data"][0]["edges"]
    print(g2_edges)
    g2_dests = [edge[1] for edge in g2_edges]
    print(g2_dests)
    # using numpy, generate a sequence 0, 0.02, 0.04 ...  <49 items>
    gap = 0.02
    offset = 0.01
    g2_pos = [(dest, offset + idx * gap) for idx, dest in enumerate(g2_dests)]
    g2_pos = [(f"y{k}", round(v, 2)) for k, v in g2_pos]
    print(g2_pos)
    g2_pos = [("yroot", 0.02), ("ygoi", 0.02)] + g2_pos
    g2_pos_dict = OrderedDict(g2_pos)
    print(g2_pos_dict)
    sankey_json["metadata"]["ypos"] = g2_pos_dict
    new_json = json.dumps(sankey_json, indent=2)
    return new_json


def run():
    # Load your JSON data
    dir_path = os.path.dirname(os.path.realpath(__file__))
    idx_in = 5
    file_name_in = f"sankey.v{idx_in}.json"
    file_path_in = f"{dir_path}/{file_name_in}"
    file_name_out = f"sankey.v{idx_in + 1}.json"
    file_path_out = f"{dir_path}/{file_name_out}"

    with open(file_path_in, "r") as file:
        sankey_json = json.load(file)
        # do_merge(sankey_json, file_path_out)
        new_json = do_sort_ypos(sankey_json, file_path_out)
        print(f"Writing to file: {file_path_out}")
        with open(file_path_out, "w") as file_out:
            file_out.write(new_json)


def run_csv():
    csv = "moe.csv"
    csv_id = csv.replace(".csv", "")
    df = pd.read_csv(csv)
    df = df.astype({"amount": int})
    node_abbrev = df["dest_abbrev"].tolist()
    node_label = df["dest_name"].tolist()
    node_map = dict(zip(node_abbrev, node_label))
    df = df[df["amount"] > 1000]
    df["source_abbrev"] = csv_id
    all_edges = list(zip(df["source_abbrev"], df["dest_abbrev"], df["amount"]))
    print(df)
    csv_obj = {
        "nodes": {e[1]: node_map[e[1]] for e in all_edges},
        "edges": sorted(all_edges, key=lambda x: x[2], reverse=True),
    }
    print(csv_obj)
    json_str = json.dumps(csv_obj, indent=2)
    json_out = f"{csv_id}.json"
    with open(json_out, "w") as file:
        file.write(json_str)
    pass


def create_sankey_section(out_dir: str, fname: str, data: dict) -> None:
    with open(f"{out_dir}/{fname}.json", "w") as file:
        file.write(json.dumps(data, indent=2))


def run_split_sankey():
    sankey_file = "sankey.v6.json"
    sankey = json.load(open(sankey_file))
    print(sankey)

    out_dir = sankey_file.replace(".json", "")
    os.makedirs(out_dir, exist_ok=True)

    create_sankey_section(out_dir, "metadata", sankey["metadata"])
    for section in sankey["data"]:
        sec_id = section["id"]
        sec_id = sec_id.replace("root_", "")
        create_sankey_section(out_dir, sec_id, section)


def run_join_sankey():
    sankey_dir = "sankey.v6"
    sankey_out = "sankey.v7.json"
    all_json = glob.glob(f"{sankey_dir}/*.json")

    sankey_data = {}
    read_file = lambda x: json.load(open(x))
    sankey_data["metadata"] = read_file(f"{sankey_dir}/metadata.json")

    data_json = [f for f in all_json if "metadata.json" not in f]
    sankey_data["data"] = [read_file(f) for f in data_json]

    with open(sankey_out, "w") as file:
        file.write(json.dumps(sankey_data, indent=2))
    pass


def run_salaries():
    salaries = json.load(open("salaries.raw.json"))
    agg_sal = {k: int(sum(v)) for k, v in salaries.items()}
    agg_sal_items = sorted(agg_sal.items(), key=lambda x: x[1], reverse=True)
    total = sum(agg_sal.values())
    print(agg_sal)
    print(total)

    # compute string abbrev by getting the first letter following whitespace of x.lower()
    get_abbrev = lambda x: x[0].lower() + "".join(re.findall(r"\s(\w)", x.lower()))
    node_map = {get_abbrev(k): k for k, v in agg_sal.items()}
    print(node_map)

    node_map_2 = {f"{k}_sal": f"{k.upper()} (Salaries)" for k in node_map}

    edges_1 = [
        (f"{get_abbrev(k)}", f"{get_abbrev(k)}_sal", v) for k, v in agg_sal.items()
    ]
    edges_1 = sorted(edges_1, key=lambda x: x[2], reverse=True)
    print(edges_1)

    edges_2 = [(f"{get_abbrev(k)}_sal", "all_salaries", v) for k, v in agg_sal.items()]
    edges_2 = sorted(edges_2, key=lambda x: x[2], reverse=True)
    section = {
        "id": "salaries",
        "desc": "Salaries section",
        "nodes": node_map_2,
        "edges": edges_1 + edges_2,
        "pos": {"x": "l2", "y": "ysal"},
    }

    with open("salaries.json", "w+") as f:
        f.write(json.dumps(section, indent=2))

    pass


if __name__ == "__main__":
    # run()
    run_csv()
    # run_salaries()
    # run_split_sankey()
    #  run_join_sankey()
