## Faster-R-CNN

### 기존 Fast-R-CNN의 문제점

- Fast-R-CNN에서 Selective search는 CNN외부에서 연산하므로 cpu에서 수행하게 되는데 이 부분이 병목 현상이였다.

---



### Faster-R-CNN

![Untitled](/0.%20Img/rcnn5.png)

- 이를 해결하기 위해 Conv feature map과 RoI 사이에 Region proposal을 생성하는 RPN을 추가된 구조이다.
- CNN을 통과해 나온 feature map이 RPN의 입력값이 되는데, RPN에서 생성된 RoI는 feature map에 대한 RoI가 아닌 original image에 대한 것이다.
- 그래서 anchor box의 크기는 original image의 크기에 맞춰 생성하고, 이 anchor box와 network의 output 값 사이의 loss를 optimize 하도록 훈련시킨다.

---

![Untitled](/0.%20Img/rcnn6.png)

- original image에서 생성된 RoI가 feature map의 크기에 맞게 rescaling되고, feature map에 투영하게 된다.
- 투영한 뒤 classification과 bbox regression이 수행된다.

---

![Untitled](/0.%20Img/rcnn7.png)

- RoI pooling을 사용하기 때문에 RoI값이 달라도 되는것처럼 input size의 값이 달라도 되지만, **vgg의 경우 244x224, resNet의 경우 min : 600, max : 1024 등.. 으로 맞춰줄때 성능이 가장 좋기 때문에 original image에 대한 input size는 고정해주는 편이다.**
- 따라서 fc layer 대신 GAP을 많이 사용하는 추세이다. **GAP를 사용하면 input size와 관계없이 1 value로 average pooling하기에 filter의 개수만 고정되어있으면 되기 때문**이다.

---

### RPN

![Untitled](/0.%20Img/rcnn8.png)

- RPN의 input 값은 이전 CNN 모델에서 생성한 feature map이다.
- object의 크기와 비율이 어떻게 될지 모르므로 가능할 만한 k개의 anchor box를 만들어 놓는데, 여기서는 가로세로길이 3종류 x 비율 3종류 = 9개의 anchor box를 이용한다. 이 anchor box가 bounding box가 될 수 있다.
- Region proposal을 생성하기 위해 feature map 위에 sliding window 시킨다.
- 이 단계에서 1*1 convolusion(=fc layer와 같음)을 이용하여 classification과 bbox regression을 수행한다.
- 네트워크를 가볍게 만들기 위해 classification에서는 물체가 있는지 없는지만 판단하고, 무슨 물체인지 판단하는 것은 마지막 classification에서 수행된다.

---

### Non-maximum Suppression

- RPN 모델을 거치고 난 후 한 객체에 여러 proposal이 나오는데, proposal의 개수를 줄이기 위한 알고리즘이다.
    1. box들의 score를 기준으로 정렬한다.
    2. score가 가장 높은 박스부터 다른 모든 박스들과 IoU를 비교해서 0.7이상이면 같은 객체를 detect한 것으로 인식하고 해당 박스를 삭제한다.
    3. 최종적으로 한 객체에 가장 높은 scroe의 box들만 남게 된다.
    
    ![Untitled](/0.%20Img/rcnn9.png)
    
    ---
    
    ### Bounding box regression
    
    ![Untitled](/0.%20Img/rcnn10.png)