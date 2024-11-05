import re
import argparse


# 해시 코드 패턴과 다른 필터 조건
hash_pattern = r"^[a-f0-9]{7,8}$"
date_pattern = r"^[A-Za-z]{3} \d{2}, \d{4}$"  # 예: "Nov 01, 2024"
filter_conditions = [
    "avatar",
    "authored",
    "Merge branch",
]

# 명령줄 인자 설정
parser = argparse.ArgumentParser(description="Filter and sort commit logs.")
parser.add_argument("--todo", action="store_true", help="Add '- [ ]' to each log line")
args = parser.parse_args()

# 파일 읽기
with open("commits.txt", "r", encoding="utf-8") as file:
    logs = file.readlines()

# 구간을 나누어 배포 변경점 사이의 내용만 처리
output_logs = []
inside_section = False
section_logs = []

for line in logs:
    stripped_line = line.rstrip("\n")

    # '## 배포 변경점'이 시작되면 해당 섹션을 표시하고 넘어감
    if stripped_line == "## 배포 변경점":
        output_logs.append(stripped_line)
        output_logs.append("")
        inside_section = True
        continue
    elif stripped_line == "## 특이 사항":
        # "배포 변경점" 구간 종료 -> 필터 및 정렬 처리 후 결과에 추가
        inside_section = False
        filtered_section = [
            log
            for log in section_logs
            if not (
                log == ""
                or re.match(hash_pattern, log)
                or re.match(date_pattern, log)
                or any(condition in log for condition in filter_conditions)
            )
        ]
        sorted_section = sorted(
            filtered_section, key=lambda x: (x != "", x)
        )  # 빈 줄 우선 정렬
        if args.todo:
            for i in range(len(sorted_section)):
                sorted_section[i] = f"- [ ] {sorted_section[i]}"
        output_logs.extend(sorted_section)
        output_logs.append("")
        output_logs.append(stripped_line)
        continue

    # 섹션 안의 내용만 따로 저장
    if inside_section:
        section_logs.append(stripped_line)
    else:
        output_logs.append(stripped_line)

# 최종 출력
for log in output_logs:
    print(log)
