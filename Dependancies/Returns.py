import numpy as np

def MinimumReturn(List):
  return int(min([List[i][j] for i in range(len(List)) for j in range(len(List[i]))]))

def MaximumReturn(List):
  return int(max([List[i][j] for i in range(len(List)) for j in range(len(List[i]))]))

def ThreeDMaximumReturn(List):
  return int(max([List[i][j][f] for i in range(len(List)) for j in range(len(List[i])) for f in range(len(List[i][j]))]))

def ThreeDMinimumReturn(List):
  return int(min([List[i][j][f] for i in range(len(List)) for j in range(len(List[i])) for f in range(len(List[i][j]))]))

