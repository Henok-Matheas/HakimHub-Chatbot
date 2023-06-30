import json

def load_json(file):
    f = open(file)

    data = json.load(f)

    # Closing file
    f.close()
    return data


def dump_json(data, outFile):
    with open(outFile, "w") as outfile:
        json.dump(data, outfile, indent=4)