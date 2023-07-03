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

