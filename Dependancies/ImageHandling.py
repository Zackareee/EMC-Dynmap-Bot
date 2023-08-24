
def Grid(Layer,Width,Height):
  for y in range(0, Height, 16):
    line = ((0, y), (Width, y))
    Layer.line(line, fill=128)
  for x in range(0, Width, 16):
    line = ((x, 0), (x, Height))
    Layer.line(line, fill=128)

def ImageSave(Image,Path):
  Image.save(str(Path))