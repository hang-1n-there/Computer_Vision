## R-CNN

참고자료 : https://ganghee-lee.tistory.com/35

![Untitled](/0.%20Img/rcnn.png)

1. input image를 입력받는다.
2. selective search 알고리즘을 통해 region proposal을 추출한다.
3. 추출한 region proposal output을 cnn 모델에 넣어주기 전에, 모든 이미지의 size를 동일하게 wrap 시켜준다.
4. warped image를 cnn 모델에 넣어준다.
5. 각각의 convolution 결과에 대해 SVM 모델을 사용하여 Classification을 진행해준다.

> CNN fine-tuning을 위한 학습 데이터가 시기상 많지 않아서 Softmax를 적용시키면 오히려 성능이 낮아져서 SVM을 사용했다.
> 

## 1. Region proposal (영역 검출)

![Untitled](/0.%20Img/rcnn2.png)

- selective search 알고리즘으로 2000개의 region proposal을 생성하고, 동일한 크기로 wrapping 시켜준다.

## 2. CNN

![Untitled](/0.%20Img/rcnn3.png)

- 224 * 224 이미지를 cnn 모델에 넣어준다.
- cnn을 거쳐 각각의 region proposal로 부터 고정된 크기의 feature vector를 뽑아준다.

## 3. SVM

- cnn에서 추출된 feature vector들의 각 class별 확률값과 객체 여부 등을 판별하는 classifier 역할을 한다.

## 3-1. Bounding Box Regression

- selective search 알고리즘으로 뽑아낸 bounding box는 정확하지 않기 때문에, noise를 제거하기 위해 물체를 정확히 감싸도록 해주는 Bounding Box Regression 모델을 수행해준다.

---

## R-CNN의 문제점

- RoI마다 CNN 연산을 함으로써 속도가 느림
- 2-stage detection으로써 모델을 한 번에 학습시키지 못함

## Fast-R-CNN

참고자료 : https://ganghee-lee.tistory.com/36

- 순서
    1. selective search 알고리즘을 통해 RoI를 찾는다.
    2. 전체 이미지를 CNN에 통과시켜 feature map을 얻는다.
    3. feature map에 selective search로 얻은 RoI를 projection 시켜주고 grid로 구간을 나눈다.

### SPP (Spatial Pyramid Pooling)

- 먼저 CNN을 통과시켜 feature map을 추출한다.
- 그리고 미리 정해진 4 x 4, 2 x 2, 1 x 1 영역의 피라미드로 feature map을 나눠준다. 피라미드의 한 칸을 bin 이라고 한다.
- bin내에서 max pooling을 진행하여 각 피라미드의 크기에 맞게 max값을 뽑아낸다.
- 각 피라미드별로 뽑아낸 max값을 이어붙여 고정된 크기의 vector를 만들고 이게 fc layer의 입력값이 된다.

### RoI Pooling

![Untitled](/0.%20Img/rcnn4.png)

<aside>
💡 Fast-R-CNN에서 1개의 피라미드를 SPP를 이용하여 feature vector로 만드는 과정을 RoI Pooling이라고 한다.

</aside>

1. input image를 CNN에 통과시켜 feature map을 추출한다.
2. 그 후 selective search로 부터 추출한 RoI를 feature map에 projection 시킨다.
3. 미리 설정한 grid의 크기만큼 바꿔주기 위해서 (h / H) * (w / H)만큼 grid를 RoI 위에 만든다.
4. RoI를 각 grid의 크기만큼 split 시킨 후 grid 구간마다 하나의 max pooling값을 추출한다.
- 위 작업을 통해 feature map에 투영했던 **hxw크기의 RoI는 HxW크기의 고정된 feature vector로 변환**된다.

---

### end-to-end

- R-CNN의 문제점
    - R-CNN의 문제였던 multi-stage-pipline으로 인해 3가지 모델을 따로 학습시켜야 됬다.
    - bounding box regression은 CNN을 거치지 않은 Region proposal을 input으로 가지고, classification은 CNN을 거친 후의 feature map이 input으로 softmax로 들어가기 때문에 같이 연산되지 않는다.
- Fast-R-CNN
    - Fast-R-CNN은 RoI Pooling을 추가함으로써 CNN을 거친 후의 feature map에 RoI를 투영(projection) 시킬 수 있었다.
    - 따라서 동일 data가 각자 softmax(classification), Bbox regressor(localization)으로 들어가기에 연산을 공유한다.

---

### 결론

- Fast-R-CNN은 RoI Pooling을 추가함으로써
    1. CNN 한 번의 연산
    2. classification과 Bbox regression을 동시에 실행 가능

위 두 가지의 성과를 이룰 수 있었다.

### 단점

- 하지만 단점으로는 RoI를 추출하는 과정(selective search)이 CNN 외부에서 일어나므로 이 부분의 속도가 느리다는 단점이 있다.
- 이를 해결하기 위해 RoI도 CNN 내부에서 이루어질 수 있도록 Faster-R-CNN이 제안된다.

## Faster-R-CNN

### 기존 Fast-R-CNN의 문제점

- Fast-R-CNN에서 Selective search는 CNN외부에서 연산하므로 cpu에서 수행하게 되는데 이 부분이 병목 현상이였다.

---

### Fast-R-CNN

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