"""
Lerp Helpers
"""
def lerp(i, f, t):
  return i + (f-i) * t

def lerpi(i,f,t):
  return int(lerp(i,f,t))

def lerpColor(i, f, t):
  return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))