import sys
import argparse
import os
import glob
import yaml


def convert_surge_to_mihomo(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as f:
        surge_rules = f.readlines()

    mihomo_rules = []
    for rule in surge_rules:
        rule = rule.strip()
        if not rule or rule.startswith("#"):
            continue

        if rule.startswith(
            (
                "DOMAIN,",
                "DOMAIN-SUFFIX,",
                "DOMAIN-KEYWORD,",
                "IP-CIDR,",
                "IP-CIDR6,",
                "IP-ASN,",
                "PROCESS-NAME,",
            )
        ):
            mihomo_rules.append(rule)

    mihomo_data = {"payload": mihomo_rules}

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(mihomo_data, f, allow_unicode=True, sort_keys=False)


def process_files(pattern):
    files = glob.glob(pattern)

    for file_path in files:
        if not file_path.endswith(".list"):
            continue

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        mihomo_dir = file_dir.replace("Surge", "Mihomo")
        output_path = os.path.join(mihomo_dir, file_name[:-5] + ".yaml")

        try:
            convert_surge_to_mihomo(file_path, output_path)
            print(f"已转换 {file_path} 为 {output_path}")
        except Exception as e:
            print(f"转换 {file_path} 时出错: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="将 Surge 规则列表转换为 Mihomo 格式")
    parser.add_argument(
        "--pattern",
        help="输入文件的 Glob 模式 (例如: 'Surge/*.list')",
        required=True,
    )

    args = parser.parse_args()
    process_files(args.pattern)


if __name__ == "__main__":
    main()
