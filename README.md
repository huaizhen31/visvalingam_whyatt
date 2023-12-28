# visvalingam_whyatt
使用Numpy实现了 Visvalingam Whyatt 算法，用于对曲线进行压缩。  
核心代码在simplier_utils.py中，包括两个方法： vw_simplier和vw_simplier_batch_delete。  
vw_simplier，
按照 Visvalingam Whyatt 算法原理进行了实现，每轮使用小顶堆的堆排序寻找最小三角形面积，然后根据三个点在队列中的顺序删除中间点。  
vw_simplier_batch_delete，批量删除点，让运算速度更快。使用np.min方法寻找最小面积，然后设置阈值 min_area*(1+tolerance)，
批量删除面积小于阈值的三角形的中间点。  
  
vw_simplier:
```python
def vw_simplier(
        point_list,
        target_pts_num=20,
        is_3d=False
):
    '''
    Visvalingam-Whyatt算法，本次实现主要用于曲线压缩。
    :param point_list: List(tuple(float, float [, float]))。点列表，2D平面坐标系的形式是[(x0,y0,), (x1,y1), (x2,y2)...]。3D平面坐标系的形式是[(x0,y0,z0), (x1,y1,z1), (x2,y2,z2)...]。
    :param target_pts_num: Int。输出的目标点的数量。
    :param is_3d: Boolean。point_list是否为3D点，该参数与计算三角形面积时取坐标的前2维还是前3维有关。
    :return: List(tuple(float, float [, float]))。曲线压缩后返回的点列表。
    '''
```
   
vw_simplier_batch_delete:  
```python
def vw_simplier_batch_delete(point_list, target_pts_num=20, tolerance=0.01, is_3d=False):
    '''
    Visvalingam-Whyatt 批量删除点的算法，运行速度更快。核心是使用np.min方法寻找最小面积，然后设置阈值 min_area*(1+tolerance)， 批量删除面积小于阈值的三角形的中间点。
    :param point_list: List(tuple(float, float [, float]))。点列表，2D平面坐标系的形式是[(x0,y0,), (x1,y1), (x2,y2)...]。3D平面坐标系的形式是[(x0,y0,z0), (x1,y1,z1), (x2,y2,z2)...]。
    :param target_pts_num: Int。输出的目标点的数量。
    :param tolerance: float。公差系数，用于计算批量删除点的面积阈值。面积阈值=min_area*(1+tolerance)
    :param is_3d: Boolean。point_list是否为3D点，该参数与计算三角形面积时取坐标的前2维还是前3维有关。
    :return: List(tuple(float, float [, float]))。曲线压缩后返回的点列表。
    '''
```


使用方法请看test_vw.py，核心：
```python
new_curve = vw_simplier_batch_delete(old_curve, target_pts_num=32, tolerance=0.01, is_3d=False)
```
![test](/files/plt_plot.png)  

参考和学习资料，这些资料帮助我学习算法原理和代码思路，并复用和改造了部分代码[2]，感谢相关作者：   
[1] https://zhuanlan.zhihu.com/p/355323735  
[2] https://blog.csdn.net/weixin_68266041/article/details/132205446  
[3] https://github.com/Permafacture/Py-Visvalingam-Whyatt  