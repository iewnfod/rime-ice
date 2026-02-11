import re
from pypinyin import pinyin, Style

def solve_file(f: str, headline: int):
	results = []
	success = 0
	skip = 0
	with open(f, "r", encoding="utf-8") as file:
		lines = file.readlines()
		for i in range(len(lines)):
			if i < headline:
				results.append(lines[i].rstrip("\n"))
				continue

			l = lines[i].strip()
			if l == "" or l.startswith("#"):
				results.append(l)
				skip += 1
			else:
				if re.search(r'[\s\d]', l):
					print(f"警告：第 {i+1} 行可能已有拼音，跳过：{l}")
					results.append(l)
					skip += 1
				else:
					pinyin_result = pinyin(l, style=Style.NORMAL, errors='default')
					pinyin_str = ' '.join([item[0] for item in pinyin_result])
					results.append(f"{l}\t{pinyin_str}")
					success += 1

	with open(f, "w", encoding="utf-8") as file:
		file.write("\n".join(results))

	print(f"完成文件：{f}，总计 {len(lines)} 行, 头部 {headline} 行，成功处理 {success} 行，跳过 {skip} 行。")

files = [
	("cn_dicts/game/yuanshen.dict.yaml", 6),
	("cn_dicts/game/mingchao.dict.yaml", 5),
]

for fp, headline in files:
	print(f"处理文件：{fp}")
	solve_file(fp, headline)
