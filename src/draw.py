
import cv2
from random import randint
import tool


class DrawNode:
    def __init__(self, resource_id, bound, isDraw=True):
        self.initNode(bound)
        self.resource_id = resource_id
        self.bound = bound
        self.isDraw = isDraw
        self.im = None
        
    def initNode(self, bound):        
        if bound:
            ltrb = tool.matchBound(bound)
            self.l = ltrb[0]
            self.t = ltrb[1]
            self.r = ltrb[2]
            self.b = ltrb[3]        

    def draw(self, im, index):  
        if self.bound is None or not self.isDraw:
            return               
        l, t, r, b = self.l, self.t, self.r, self.b
        color = randint(0, 255)               
        cv2.rectangle(im, (l, t),(r, b),(0,color,0), 5)
        y = t + ((b - t) / 2 )
        cv2.putText(im, str(index), (l, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 0), thickness=5, lineType=cv2.LINE_AA)                     

    def getPoint(self):
        if self.bound is None:
            return 0, 0
        x = self.l + int((self.r - self.l) / 2)
        y = self.t + int((self.b - self.t) / 2)
        return x, y

    def getBound(self):
        if self.bound is None:
            return None
        return str(self.bound)


if __name__ == "__main__":
    drawNode = DrawNode("id/1", "[0,0][1080,2028]")
    print(drawNode)
    