import sys
import os


def process_and_clean(input_file):
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"错误: 文件 '{input_file}' 编码不是 UTF-8")
        sys.exit(1)

    cleaned_lines = []
    for line in lines:
        content = line.split("//")[0].strip()
        if content and not content.startswith("#"):
            cleaned_lines.append(content)

    # 记录重复行删除信息
    original_count = len(cleaned_lines)
    cleaned_lines = list(dict.fromkeys(cleaned_lines))
    duplicate_count = original_count - len(cleaned_lines)

    suffixes = set()
    keywords = set()
    for line in cleaned_lines:
        if line.startswith("DOMAIN-SUFFIX,"):
            suffix = line.split(",")[1]
            suffixes.add(suffix)
        elif line.startswith("DOMAIN-KEYWORD,"):
            keyword = line.split(",")[1].lower()
            keywords.add(keyword)

    final_lines = []
    removed = set()
    removed_by_keyword = set()
    removed_by_suffix = set()

    DOMAIN = "DOMAIN,"
    DOMAIN_SUFFIX = "DOMAIN-SUFFIX,"
    DOMAIN_KEYWORD = "DOMAIN-KEYWORD,"

    for line in cleaned_lines:
        if line.startswith(DOMAIN):
            domain = line.split(",")[1]
            domain_lower = domain.lower()
            keyword_match = False
            for keyword in keywords:
                if keyword in domain_lower:
                    removed.add(line)
                    removed_by_keyword.add(f"{line} (包含关键词: {keyword})")
                    keyword_match = True
                    break

            if keyword_match:
                continue

            domain_parts = domain.split(".")
            for i in range(1, len(domain_parts)):
                possible_suffix = ".".join(domain_parts[i:])
                if possible_suffix in suffixes:
                    removed.add(line)
                    removed_by_suffix.add(f"{line} (匹配后缀: {possible_suffix})")
                    break
            else:
                final_lines.append(line)

        elif line.startswith(DOMAIN_SUFFIX):
            suffix = line.split(",")[1]
            suffix_lower = suffix.lower()
            keyword_match = False
            for keyword in keywords:
                if keyword in suffix_lower:
                    removed.add(line)
                    removed_by_keyword.add(f"{line} (包含关键词: {keyword})")
                    keyword_match = True
                    break

            if not keyword_match:
                final_lines.append(line)

        elif line.startswith(DOMAIN_KEYWORD):
            final_lines.append(line)

        else:
            final_lines.append(line)

    final_lines.sort()

    try:
        with open(input_file, "w", encoding="utf-8") as f:
            for line in final_lines:
                f.write(line + "\n")
    except IOError as e:
        print(f"错误: 写入文件 '{input_file}' 失败: {str(e)}")
        sys.exit(1)

    return len(removed), duplicate_count, removed_by_keyword, removed_by_suffix


def main():
    if len(sys.argv) != 2:
        print("使用方法: python Format-rules.py <文件路径>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)

    try:
        removed_count, duplicate_count, removed_by_keyword, removed_by_suffix = (
            process_and_clean(input_file)
        )
        print(f"\n处理文件: {input_file}")
        print(f"删除 {duplicate_count} 个完全重复的规则")
        print(f"删除 {removed_count} 个冗余规则")

        if removed_by_keyword:
            print("\n因包含关键词而删除的规则:")
            for item in sorted(removed_by_keyword):
                print(f"- {item}")

        if removed_by_suffix:
            print("\n因匹配后缀而删除的规则:")
            for item in sorted(removed_by_suffix):
                print(f"- {item}")

    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
