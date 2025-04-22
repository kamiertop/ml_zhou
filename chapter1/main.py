"""
* Author: XiaoLiang and LiJie
* Time 2025/04/22
* File: ml_zhou/chapter1/main.py
* Project: ml_zhou/chapter1
* Function: 不考虑任意情况, 仅考虑基本特征组合出来的18种假设空间
"""

import argparse
from itertools import combinations


class Color:
	"""
	色泽
	"""

	def __init__(self, data: tuple[str, ...]):
		self.data = data


class Root:
	"""
	根蒂
	"""

	def __init__(self, data: tuple[str, ...]):
		self.data = data


class Sound:
	"""
	敲声
	"""

	def __init__(self, data: tuple[str, ...]):
		self.data = data


class Feature:
	"""
	属性: data
	row_data: [("a1","b1","c1"),("a1","b1","c2")]
	merged: [("a1","b1","c1")]->["a1b1c1"] 紧凑展示
	"""
	row_data: list[tuple[str, str, str]] = []
	merged: list[str] = []
	result: dict[int, list] = {}

	def __init__(self, a: Color, b: Root, c: Sound):
		# 生成所有可能的组合
		for i in a.data:
			for j in b.data:
				for k in c.data:
					self.merged.append(i + j + k)
					self.row_data.append((i, j, k))

	def encode_to_dict(self) -> dict[int, str]:
		"""
		将data转换为dict,key是序号, value是属性值的字符拼接
		:return: dict[int,str]用于调试查看信息
		"""
		res: dict[int, str] = {}
		seq = 1
		for t in self.merged:
			res[seq] = t
			seq += 1

		return res

	def disjunctions(self, k: int) -> 'Feature':
		"""
		析取
		:param: k: 多少个式子析取
		:return:
		"""
		result: dict[int, list] = {}
		if k <= 0:
			raise ValueError("k must be greater than 0")
		for i in range(1, k + 1):
			temp = []
			for combo in combinations(self.merged, i):
				temp.append(combo)
			result[i] = temp

		self.result = result

		return self

	def print_result(self, print_info: bool = False):
		"""
		打印结果
		:param print_info: 是否打印详细信息, 默认False, 只打印结果
		"""
		# self.result是dict类型, items方法使它的k和v可以同时被迭代
		for k, v in self.result.items():
			# k: int
			# v: list[tuple[str, ...]]
			print(f"k={k} 时，有 {len(v)} 种不同结果")
			if print_info:
				for i in v:
					print(i)
				print("======================================")


def main() -> None:
	# 使用"a1","a2" 来表示"青绿", "乌黑"
	c = Feature(
		Color(("a1", "a2")), Root(("b1", "b2", "b3")), Sound(("c1", "c2", "c3"))
	)

	parser = argparse.ArgumentParser(description="请输入题目中所说的k")
	parser.add_argument("k", type=int, help="Example: python main.py 4", default=3)
	args = parser.parse_args()

	c.disjunctions(args.k).print_result(False)


if __name__ == "__main__":
	main()
