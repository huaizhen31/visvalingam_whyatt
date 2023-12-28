import math
import numpy as np


# 计算2D三角形的面积
def cal_triangle_area(pt1, pt2, pt3) -> float:
    # 计算三角形三个边长
    side1 = math.sqrt(
        math.pow(pt1[0] - pt2[0], 2) +
        math.pow(pt1[1] - pt2[1], 2)
    )
    side2 = math.sqrt(
        math.pow(pt1[0] - pt3[0], 2) +
        math.pow(pt1[1] - pt3[1], 2)
    )
    side3 = math.sqrt(
        math.pow(pt2[0] - pt3[0], 2) +
        math.pow(pt2[1] - pt3[1], 2)
    )
    # 三边无法构成三角形
    if side1 + side2 <= side3 or side1 + side3 <= side2 or side3 + side2 <= side1:
        return 0.0
    # 计算三角形面积
    # 海伦公式。s=sqr(p*(p-a)(p-b)(p-c))
    p = (side1 + side2 + side3) / 2.0
    area = math.sqrt(p * (p - side1) * (p - side2) * (p - side3))
    return area


# 计算3D空间三角形的面积
def cal_triangle_area_3d(pt1, pt2, pt3) -> float:
    # 计算三角形三个边长
    side1 = math.sqrt(
        math.pow(pt1[0] - pt2[0], 2) +
        math.pow(pt1[1] - pt2[1], 2) +
        math.pow(pt1[2] - pt2[2], 2)
    )
    side2 = math.sqrt(
        math.pow(pt1[0] - pt3[0], 2) +
        math.pow(pt1[1] - pt3[1], 2) +
        math.pow(pt1[2] - pt3[2], 2)
    )
    side3 = math.sqrt(
        math.pow(pt2[0] - pt3[0], 2) +
        math.pow(pt2[1] - pt3[1], 2) +
        math.pow(pt2[2] - pt3[2], 2)
    )
    # 三边无法构成三角形
    if side1 + side2 <= side3 or side1 + side3 <= side2 or side3 + side2 <= side1:
        return 0.0
    # 计算三角形面积
    # 海伦公式。s=sqr(p*(p-a)(p-b)(p-c))
    p = (side1 + side2 + side3) / 2.0
    area = math.sqrt(p * (p - side1) * (p - side2) * (p - side3))
    return area


# Visvalingam-Whyatt
def vw_simplier(point_list, target_pts_num=20, is_3d=False):
    # Visvalingam-Whyatt
    # 使用堆排序方法找三角形的最小面积
    # 按照算法原理一次删除1个点

    cal_triangle_area_func = {
        True: cal_triangle_area_3d,
        False: cal_triangle_area,
    }

    len_pts = len(point_list)

    # 构造所有三角形并计算面积
    triangle_list = []  # 列表中的元素结构是 (pt1, pt2, pt3, area), 分别是三角形的3个顶点和面积
    log_arr = np.ones(len_pts, dtype=int)  # 用于记录各个点是否被抛弃的数组，点可用为1，不可用为0

    current_pts_num = len_pts

    while current_pts_num > target_pts_num:  # 当前点的数量仍大于目标值
        # print(f"{datetime.datetime.now()}: {current_pts_num}")

        id_arr = np.where(log_arr == 1)[0]  # 找到所有可用点的id, id_arr保存了所有可用点的id
        avail_num = id_arr.shape[0]  # 可用点的总数
        if avail_num < 3:  # 少于3个点，构不成三角形
            break
        triangle_list.clear()  # 清空triangle_list
        # 依次构造三角形
        for i_p in range(0, avail_num - 2):
            pt1 = point_list[id_arr[i_p]]  # 第1个点
            pt2 = point_list[id_arr[i_p + 1]]  # 第2个点
            pt3 = point_list[id_arr[i_p + 2]]  # 第3个点
            area = cal_triangle_area_func[is_3d](pt1, pt2, pt3)
            # 将三角形放入三角形列表中
            triangle_list.append((id_arr[i_p], id_arr[i_p + 1], id_arr[i_p + 2], area))

        # 基于当前可用的点，使用小顶堆排序找到面积最小的三角形
        trg_len = len(triangle_list)  # 三角形的数量
        start = int((trg_len - 1 - 1) / 2)  # 最后一个非叶子节点作为开始
        # 构造最小堆
        for parent in range(start, -1, -1):  # 从最后一个非叶子节点逐步向前遍历
            child = parent * 2 + 1  # 根据父节点找左子节点
            while child < trg_len:  # 子节点的位置没有超限
                # 如果右子节点比左子节点更小，则child指向右子节点
                if child < trg_len - 1 and triangle_list[child + 1][3] < triangle_list[child][3]:
                    child += 1
                # 父节点比子节点小，属于正常，跳出该循环
                if triangle_list[parent][3] <= triangle_list[child][3]:
                    break
                else:
                    # 如果父节点小于子节点，则交换父与子节点
                    temp = triangle_list[parent]
                    triangle_list[parent] = triangle_list[child]
                    triangle_list[child] = temp

                    # 原父子节点交换后，可能子节点的树不满足堆的条件，下一轮while循环调整这个子树
                    parent = child
                    child = parent * 2 + 1
        # 构造完最小的堆，现在队列的第0个元素应该是最小值的节点，即小堆的顶
        top = triangle_list[0]
        # top表示的三角形就是面积最小的三角形，去掉该三角形的节点pt2
        log_arr[top[1]] = 0  # 在log_arr中用0标记pt2，表示该点已移除
        current_pts_num -= 1  # current_pts_num减1，表示可用的点少了1个

    # 最后提取log_arr中记录的所有可用点
    id_arr = np.where(log_arr == 1)[0]
    result = []
    for i in range(id_arr.shape[0]):
        result.append(point_list[id_arr[i]])
    return result
    # 使用堆排序对面积进行排序
    # 堆的性质：
    # （1）堆是完全二叉树。数组和二叉树坐标对应关系：0是顶点，1和2是0的左右叶子，3和4是1的左右叶子，5和6是2的左右叶子，7和8是5的左右叶子...
    # （1）任意的叶子节点小于（或大于）它所有的父节。又分为大顶堆和小顶堆。
    #      * 当前节点位置为i，则左叶子位置2i+1、右叶子位置2i+2
    # （2）大顶堆要求节点的元素都要大于其孩子
    #      * array[i] >= array[2i+1] && array[i] >= array[2i+2]
    # （3）小顶堆要求节点元素都小于其左右孩子，两者对左右孩子的大小关系不做任何要求。

    # 利用堆排序，就是基于大顶堆或者小顶堆的一种排序方法。
    # 经典小顶堆的堆排序主要分为两大步：
    # Step 0: 准备，数组array长度为L
    # Step 1: 构建堆：构建小顶堆,堆的顶节点（即数组0位置）是数组最小值 array[0]
    #         （1）从最后一个非叶子节点 (array.length-1-1)/2 开始，即start=int((array.length-1-1)/2)
    #         （2）它的左右孩子分别是 lchild=i*2+1, rchild=i*2+2
    #         （3）array[start] 与 左右孩子的最大值进行交换 max(array[lchild], array[rchild])
    #         （4）对下一个非叶子节点进行（1）~（3）处理
    # Step 2: 堆顶与数组最后一个值交换：堆顶array[0]与数组最后一个位置array[L-1]的值进行交换，最小值作为数组最后一个值
    # 对 array[0:L-1]进行Step 1~Step 2。然后array[0:L-2]、array[0:L-3]...


# Visvalingam-Whyatt Fast
def vw_simplier_batch_delete(point_list, target_pts_num=20, tolerance=0.01, is_3d=False):
    # 更快的Visvalingam-Whyatt
    # 使用np.min方法找三角形的最小面积
    # 使用 min_area*(1+tolerance) 作为阈值，筛选出低于阈值的点集
    # 批量删除点集，删除顺序是随机的

    cal_triangle_area_func = {
        True: cal_triangle_area_3d,
        False: cal_triangle_area,
    }

    len_pts = len(point_list)

    # 构造所有三角形并计算面积
    triangle_list = []  # 列表中的元素结构是 (pt1, pt2, pt3, area), 分别是三角形的3个顶点和面积
    area_list = []  # 专用于保存三角形面积
    log_arr = np.ones(len_pts, dtype=int)  # 用于记录各个点是否被抛弃的数组，点可用为1，不可用为0

    current_pts_num = len_pts

    while current_pts_num > target_pts_num:  # 当前点的数量仍大于目标值
        id_arr = np.where(log_arr == 1)[0]  # 找到所有可用点的id, id_arr保存了所有可用点的id
        avail_num = id_arr.shape[0]  # 可用点的总数
        if avail_num < 3:  # 少于3个点，构不成三角形
            break
        triangle_list.clear()  # 清空triangle_list
        area_list.clear()
        # 依次构造三角形
        for i_p in range(0, avail_num - 2):
            pt1 = point_list[id_arr[i_p]]  # 第1个点
            pt2 = point_list[id_arr[i_p + 1]]  # 第2个点
            pt3 = point_list[id_arr[i_p + 2]]  # 第3个点
            area = cal_triangle_area_func[is_3d](pt1, pt2, pt3)
            # 将三角形放入三角形列表中
            triangle_list.append((id_arr[i_p], id_arr[i_p + 1], id_arr[i_p + 2], area))
            area_list.append(area)

        # 计算最小面积min_area
        min_area = np.min(area_list)
        # 批量找到小于 min_area*1.01 的点
        id_arr = np.where(np.array(area_list) <= min_area * (1 + tolerance))[0]
        # 对待删除的点进行随机排序
        # 在有效点接近目标数量时，随机删除能保证被删除的点位置是随机的，不会造成排序靠前的坐标被大量删除而靠后的坐标大量保留的情况
        np.random.shuffle(id_arr)
        for i in range(id_arr.shape[0]):
            log_id = triangle_list[id_arr[i]][1]
            # top表示的三角形就是面积最小的三角形，去掉该三角形的节点pt2
            log_arr[log_id] = 0  # 在log_arr中用0标记pt2，表示该点已移除
            current_pts_num -= 1  # current_pts_num减1，表示可用的点少了1个
            if current_pts_num <= target_pts_num:
                break

    # 最后提取log_arr中记录的所有可用点
    id_arr = np.where(log_arr == 1)[0]
    result = []
    for i in range(id_arr.shape[0]):
        result.append(point_list[id_arr[i]])
    return result
