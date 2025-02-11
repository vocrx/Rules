import sys
import argparse
import os
import glob
import json


def convert_list_to_yaml(input_file, output_file, skip_no_resolve=False):
    domain_set = []
    domain_suffix_set = []
    domain_keyword_set = []
    ip_cidr_set = []
    ip_cidr6_set = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("DOMAIN,"):
                domain_set.append(line.split(",")[1])
            elif line.startswith("DOMAIN-SUFFIX,"):
                domain_suffix_set.append(line.split(",")[1])
            elif line.startswith("DOMAIN-KEYWORD,"):
                domain_keyword_set.append(line.split(",")[1])
            elif line.startswith("IP-CIDR,"):
                ip_cidr_set.append(line.split(",")[1])
            elif line.startswith("IP-CIDR6,"):
                ip_cidr6_set.append(line.split(",")[1])

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        if not skip_no_resolve:
            f.write("no_resolve: true\n")

        if domain_set:
            f.write("domain_set:\n")
            for domain in domain_set:
                f.write(f"  - {domain}\n")

        if domain_suffix_set:
            f.write("domain_suffix_set:\n")
            for suffix in domain_suffix_set:
                f.write(f"  - {suffix}\n")

        if domain_keyword_set:
            f.write("domain_keyword_set:\n")
            for keyword in domain_keyword_set:
                f.write(f"  - {keyword}\n")

        if ip_cidr_set:
            f.write("ip_cidr_set:\n")
            for ip in ip_cidr_set:
                f.write(f"  - {ip}\n")

        if ip_cidr6_set:
            f.write("ip_cidr6_set:\n")
            for ip in ip_cidr6_set:
                f.write(f"  - {ip}\n")


def process_files(pattern, skip_no_resolve_files=None):
    if skip_no_resolve_files is None:
        skip_no_resolve_files = []

    files = glob.glob(pattern)

    for file_path in files:
        if not file_path.endswith(".list"):
            continue

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        egern_dir = file_dir.replace("Surge", "Egern")
        output_path = os.path.join(egern_dir, file_name[:-5] + ".yaml")

        skip_no_resolve = file_path in skip_no_resolve_files

        convert_list_to_yaml(file_path, output_path, skip_no_resolve)
        print(f"Converted {file_path} to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert list format to yaml format")
    parser.add_argument(
        "--pattern",
        help="Glob pattern for input files (e.g., 'Rules/Surge/*.list')",
        required=True,
    )
    parser.add_argument(
        "--skip-no-resolve-files",
        help="JSON array of file paths that should skip no_resolve: true",
        default="[]",
    )

    args = parser.parse_args()

    try:
        skip_no_resolve_files = json.loads(args.skip_no_resolve_files)
        if not isinstance(skip_no_resolve_files, list):
            raise ValueError("skip-no-resolve-files must be a JSON array")
    except json.JSONDecodeError:
        print("Error: skip-no-resolve-files must be a valid JSON array")
        sys.exit(1)

    process_files(args.pattern, skip_no_resolve_files)


if __name__ == "__main__":
    main()
