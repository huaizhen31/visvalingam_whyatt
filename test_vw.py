import time
import numpy as np
import matplotlib.pyplot as plt

from simplier_utils import vw_simplier_batch_delete, vw_simplier

if __name__ == "__main__":
    # 构建测试曲线
    # x坐标
    x0 = np.arange(-100, 400)
    # 分段的y坐标
    y0_1 = [0.1 * x ** 2 for x in range(-100, 100)]
    y0_2 = [1000 for x in range(100, 200)]
    y0_3 = [-5 * x + 2000 for x in range(200, 300)]
    y0_4 = [0.01 * x ** 2 - 6 for x in range(300, 400)]
    y0 = []
    for ls in [y0_1, y0_2, y0_3, y0_4]:
        y0.extend(ls)

    # point_list输入形式:
    # 2D平面坐标： point_list=[(x0,y0), (x1,y1), (x2,y2)...]
    # 3D空间坐标： point_list=[(x0,y0,z0), (x1,y1,z1), (x2,y2,z2)...]
    old_curve = []
    for i in range(len(x0)):
        old_curve.append((x0[i], y0[i]))
    t0 = time.time()
    new_curve_normal = vw_simplier(old_curve, target_pts_num=32, is_3d=False)
    t1 = time.time()
    new_curve_fast = vw_simplier_batch_delete(old_curve, target_pts_num=32, tolerance=0.01, is_3d=False)
    t2 = time.time()
    print(f"Normal: {t1 - t0} sec")
    print(f"Fast: {t2 - t1} sec")

    x1 = [x for x, y in new_curve_normal]
    y1 = [y for x, y in new_curve_normal]

    x2 = [x for x, y in new_curve_fast]
    y2 = [y for x, y in new_curve_fast]

    plt.figure()
    plt.subplot(3, 1, 1)
    plt.plot(x0, y0)
    plt.subplot(3, 1, 2)
    plt.plot(x1, y1, label=f'Visvalingam-Whyatt, target={len(x1)}, t={round(t1 - t0, 3)} sec')
    plt.scatter(x1, y1, s=12, c="red", marker='x')
    plt.legend()
    plt.subplot(3, 1, 3)
    plt.plot(x2, y2, label=f'Visvalingam-Whyatt Batch Delete Pts, target={len(x2)}, t={round(t2 - t1, 3)} sec')
    plt.scatter(x2, y2, s=12, c="red", marker='x')
    plt.legend()
    plt.show()
