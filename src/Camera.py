
class Camera():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def move(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z