import re

# 조건에 맞지 않는 라인만 남기고, 이름 순으로 정렬하는 예제 코드
filtered_logs = set()

# 해시 코드 패턴과 다른 필터 조건
hash_pattern = r'^[a-f0-9]{7,8}$'
filter_conditions = ["jaehyun so", "sojae", "명재철", "임채동", "박 유빈", "authored", "Merge branch"]

with open("commits.txt", "r", encoding="utf-8") as file:
    logs = file.readlines()

for line in logs:
    stripped_line = line.strip()
    # 해시 패턴 또는 필터 조건에 맞는 라인은 건너뜀
    if re.match(hash_pattern, stripped_line) or any(condition in stripped_line for condition in filter_conditions):
        continue
    # 조건에 맞지 않는 라인만 집합에 추가하여 중복 제거
    filtered_logs.add(stripped_line)

# 이름 순으로 정렬
sorted_logs = sorted(filtered_logs)

# 결과 출력
for log in sorted_logs:
    print(log)