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


class Chapter:
	"""
	属性: data
	row_data: [("a1","b1","c1")]
	merged: ["a1b1c1"]
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
		res: dict = {}
		seq = 1
		for t in self.merged:
			temp = ""
			for item in t:
				temp += item
			res[seq] = temp
			seq += 1

		return res

	def disjunctions(self, k: int) -> 'Chapter':
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
		for k, v in self.result.items():
			print(f"k={k} 时，有 {len(v)} 种不同结果")
			if print_info:
				for i in v:
					print(i)
				print("======================================")


def main() -> None:
	c = Chapter(
		Color(("a1", "a2")), Root(("b1", "b2", "b3")), Sound(("c1", "c2", "c3"))
	)

	c.disjunctions(3).print_result(True)


if __name__ == "__main__":
	main()
