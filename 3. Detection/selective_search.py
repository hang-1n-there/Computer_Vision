import selective_search
import cv2
import matplotlib.pyplot as plt
import os
import selectivesearch

class Img():
    def img_read(self, img):
        
        self.img = cv2.imread(img)
        self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
        print('img.shape : ', self.img.shape)

        plt.figure(figsize=(8,8))
        plt.imshow(self.img_rgb)
        plt.show()
        
        return self.img_rgb
    
class Region():
    def __init__(self, img_rgb):
        self.img_rgb = img_rgb
        
    def region_proposal(self):
        # Region proposal을 추출
        _, self.regions = selectivesearch.selective_search(self.img_rgb, scale=100, min_size=2000)
        print(type(self.regions), len(self.regions))
        
    def rect(self):
        # rect 정보만 추출
        cand_rects = [cand['rect'] for cand in self.regions]
        print(cand_rects)
        
        return cand_rects
    
if __name__ == "__main__":
    img = '0. Img/IU.jpg'
    img_obj = Img()  # Img 클래스의 인스턴스 생성
    img_rgb = img_obj.img_read(img)  # img_read() 메서드 호출
    
    region = Region(img_rgb)
    region.region_proposal()
    region.rect()
    
    