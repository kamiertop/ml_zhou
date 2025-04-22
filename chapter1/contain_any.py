"""
* Author: XiaoLiang and LiJie
* Time 2025/04/22
* File: ml_zhou/chapter1/contain_any.py
* Project: ml_zhou/chapter1
* Function: 考虑任意情况, 计算k个合取式进行析取产生的假设空间
"""
from itertools import combinations


class Features:
	"""
	basic_features: 基本的特征组合, 一共18种
	"""

	def __init__(self, colors: list[str], roots: list[str], sounds: list[str]):
		self.colors = colors
		self.roots = roots
		self.sounds = sounds
		basic_features: list[tuple[str, str, str]] = []
		seq: int = 0
		value_map = {}
		for a in colors:
			for b in roots:
				for c in sounds:
					basic_features.append((a, b, c))
					value_map[seq] = (a, b, c)
					seq += 1
		# 记录索引值和特征组合之间的关系, 索引值是0-17, 每对儿特征值元组可以理解为一个合取式, mapping方便decode下文的结果
		# ("青绿","蜷缩","沉闷") 理解为一个合取式
		self.mapping = value_map
		# 特征值组合, 一共18种
		self.basic_features = basic_features

	def build_disjunctions(self) -> list[list[int]]:
		"""
		列出单个合取式的所有假设空间[(2+1)*(3+1)*(3+1) = 48]
		:return: 返回一个数组, 每个数组元素又都是一个数组(长度为18), 将包含任意值的所有假设映射到了基本的假设空间中
		"""
		disjunctions: list[list[int]] = []
		colors = self.colors + ["*"]
		roots = self.roots + ["*"]
		sounds = self.sounds + ["*"]

		for c in colors:
			for r in roots:
				for s in sounds:
					"""
					构造48种假设空间(48个特征组合)
					当前假设为(c,r,s), 将当前假设映射到基本的特征中, 一个假设可能会映射到多个, 比如
						(1,1,*) 包含 (1,1,1)和(1,1,2)和(1,1,3)
					初始化一个长度为len(self.basic_features)的全0数组, 每个位置用来表示一个基本的假设(也是一个合取式)
					当前假设每覆盖一个基本假设, 就在对应位置设置为1, 比如
						特征数组[(1,1,1),(1,1,2),(1,1,3),(1,2,1),(1,2,3)]
						(1,1,*) 包含 (1,1,1)和(1,1,2)和(1,1,3), 那么数组的第1个,第2个, 第3个位置就都是1
					"""
					vector = [0] * 18
					for idx, (color, root, sound) in enumerate(self.basic_features):
						# 此处是将(c,r,s)和self.basic_features中的元组(color, root, sound)进行一一比对, 注意(c,r,s)是可能包含*的

						match = True
						# 对每个位置匹配, 如果不是*, 也不相等, 那就不匹配
						if c != "*" and color != c:
							match = False
						if r != "*" and root != r:
							match = False
						if s != "*" and sound != s:
							match = False
						if match:
							# 18个基本特征中, idx位置的被覆盖了, 置1
							vector[idx] = 1
					disjunctions.append(vector)
		return disjunctions


class EnumK:
	def __init__(self, disjunctions: list[list[int]], k: int):
		self.disjunctions = disjunctions
		self.k = k
		self.result = set()

	def combinations(self) -> 'EnumK':
		# 对k个合取式进行析取
		merged_vectors = set()
		# 穷举所有取k个析取式的组合
		for combo in combinations(self.disjunctions, self.k):
			merged = [0] * 18
			# 把这k个析取式一个个合进去
			for vec in combo:
				new_merged = []
				for m, v in zip(merged, vec):
					# 做析取操作 or
					if m == 1 or v == 1:
						new_merged.append(1)
					else:
						# 全0为0
						new_merged.append(0)
				merged = new_merged  # 更新合并后的结果
			merged_vectors.add(tuple(merged))
		self.result = merged_vectors
		return self

	def print_result(self, print_info=False) -> None:
		print(f"k={self.k} 时，最终合并后有 {len(self.result)} 种不同结果")
		if print_info:
			for i, vec in enumerate(self.result):
				print(f"{i}: {vec}")


def main() -> None:
	k = 3  # 手动设置k方便调试
	features = Features(colors=["青绿", "乌黑"], roots=["蜷缩", "硬挺", "稍蜷"], sounds=["沉闷", "清脆", "浊响"])
	# features = Features(colors=["a1", "a2"], roots=["b1", "b2", "b3"], sounds=["c1", "c2", "c3"])

	EnumK(features.build_disjunctions(), k).combinations().print_result(True)


if __name__ == "__main__":
	main()
