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