import glob
from pathlib import Path
import argparse
import sys


def merge_rule_files(input_patterns: str, output_file: str) -> bool:
    try:
        rules = set()
        files_processed = 0

        for pattern in input_patterns.split(","):
            pattern = pattern.strip()
            matched_files = glob.glob(pattern)
            if not matched_files:
                print(f"警告: 未找到匹配的文件 '{pattern}'")
                continue

            for file_path in matched_files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#"):
                                rules.add(line)
                    files_processed += 1
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {str(e)}")
                    return False

        if files_processed == 0:
            print("错误: 没有处理任何文件")
            return False

        sorted_rules = sorted(rules)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            for rule in sorted_rules:
                f.write(rule + "\n")

        print(f"成功处理了 {files_processed} 个文件")
        print(f"合并了 {len(sorted_rules)} 条规则")
        print(f"输出文件: {output_file}")
        return True

    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="合并规则文件并按字母顺序排序")
    parser.add_argument(
        "-i", "--input", default="*.list", help="输入文件匹配模式，多个模式用逗号分隔"
    )
    parser.add_argument(
        "-o", "--output", default="merged_rules.list", help="输出文件路径"
    )

    args = parser.parse_args()

    success = merge_rule_files(args.input, args.output)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
