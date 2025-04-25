# 轨迹坐标变换

## 全局到局部朝向转换（GlobalToEgo）

给定全局坐标系中的轨迹（包含平移$\mathbf{T} = [\mathbf{xy}, z]$和方向四元数$\mathbf{q}$），转换到局部朝向坐标系的过程如下：

$$\mathbf{q}' = \mathbf{q} \otimes \mathbf{q}_{\text{base}}^*$$
$$\theta = \text{getHeading}(\mathbf{q}')$$


<!-- 展开的版本 -->
<!-- $$\Delta\mathbf{xy} = \mathbf{xy}_{t+1} - \mathbf{xy}_t$$
$$\Delta\mathbf{xy}_{\text{local}} = \text{rot2D}(\Delta\mathbf{xy}, -\theta_t)$$
$$\Delta\theta = \theta_{t+1} - \theta_t$$
$$\mathbf{v}_{\theta} = \text{headingToVector}(\Delta\theta)$$ -->

$$\Delta\mathbf{xy}_{\text{local}} = \text{rot2D}(\mathbf{xy}_{t+1} - \mathbf{xy}_t, -\theta_t)$$
$$\mathbf{v}_{\theta} = \text{headingToVector}(\theta_{t+1} - \theta_t)$$


<!-- 展开的版本 -->
<!-- $$\mathbf{q}_h = \text{getHeadingQuaternion}(\mathbf{q}')$$
$$\mathbf{q}_l = \text{deheadingQuaternion}(\mathbf{q}', \mathbf{q}_h)$$
$$\mathbf{R}_l = \text{quaternionToRot6D}(\mathbf{q}_l)$$ -->

$$\mathbf{R}_l = \text{quaternionToRot6D}(\text{deheadingQuaternion}(\mathbf{q}', \text{getHeadingQuaternion}(\mathbf{q}')))$$


由此得到局部轨迹表示：

$$\mathbf{\Psi} = [\Delta\mathbf{xy}_{\text{local}}, z, \mathbf{R}_l, \mathbf{v}_{\theta}]$$

## 局部到全局朝向转换（EgoToGlobal）

给定局部轨迹$\mathbf{\Psi} = [\Delta\mathbf{xy}_{\text{local}}, z, \mathbf{R}_l, \mathbf{v}_{\theta}]$，转换回全局坐标的过程如下：

<!-- 展开的版本 -->
<!-- $$\theta = \text{vectorToHeading}(\mathbf{v}_{\theta})$$
$$\theta_{\text{global}} = \sum_{t=0}^T \theta_t$$
$$\Delta\mathbf{xy}_{\text{global}} = \text{rot2D}(\Delta\mathbf{xy}_{\text{local}}, \theta_{\text{global}})$$
$$\mathbf{xy} = \sum_{t=0}^T \Delta\mathbf{xy}_{\text{global},t}$$
 -->

<!-- $$\mathbf{q}_h = \text{headingToQuaternion}(\theta_{\text{global}})$$
$$\mathbf{q}_l = \text{rot6DToQuaternion}(\mathbf{R}_l)$$
$$\mathbf{q} = \mathbf{q}_h \otimes \mathbf{q}_l \otimes \mathbf{q}_{\text{base}}$$ -->



$$\theta_{\text{global}} = \sum_{t=0}^T \text{vectorToHeading}(\mathbf{v}_{\theta})$$
$$\mathbf{xy} = \sum_{t=0}^T \text{rot2D}(\Delta\mathbf{xy}_{\text{local}}, \theta_{\text{global}})$$
$$\mathbf{q} = \text{headingToQuaternion}(\theta_{\text{global}}) \otimes \text{rot6DToQuaternion}(\mathbf{R}_l) \otimes \mathbf{q}_{\text{base}}$$



最终得到全局轨迹：

$$\mathbf{T} = [\mathbf{xy}, z], \quad \mathbf{Q} = \mathbf{q}$$

其中：
- quaternionToRot6D，rot6DToQuaternion是Pytorch3D中的API函数，表示6D旋转表示和四元数之间的转换。
- $\otimes$表示四元数乘法
- $\mathbf{q}^*$表示四元数共轭
- $\text{rot2D}(\mathbf{v}, \theta)$表示将二维向量$\mathbf{v}$旋转角度$\theta$
- $\Delta$表示相邻帧之间的差值
- 下标$t$表示时间步



## 具体的工具函数

### 朝向角度提取 getHeading

给定四元数$\mathbf{q} = [q_x, q_y, q_z, q_w]$，朝向角度$\theta$的提取公式为：

$$\theta = 2 \cdot \text{atan2}(q_w, q_x + \epsilon)$$

其中$\epsilon$是一个小常数（通常为$10^{-6}$），用于避免数值不稳定。

### 朝向四元数提取 getHeadingQuaternion

朝向四元数$\mathbf{q}_h$通过将原始四元数的$y$和$z$分量置零获得：

$$\mathbf{q}_h = \text{normalize}([q_x, 0, 0, q_w])$$
$$\text{normalize}(\mathbf{q}) = \frac{\mathbf{q}}{\|\mathbf{q}\|}$$

### 朝向移除操作 deheadingQuaternion

朝向移除操作用于去除四元数中的朝向分量：

$$\mathbf{q}_{\text{deheaded}} = \mathbf{q}_h^* \otimes \mathbf{q}$$

其中$\mathbf{q}_h^*$是朝向四元数的共轭。

### 角度到向量转换 headingToVector

对于朝向角度$\theta$：

$$\mathbf{v}_\theta = \begin{bmatrix}
    \cos(\theta) \\
    \sin(\theta)
\end{bmatrix}$$

### 向量到角度转换 vectorToHeading

对于朝向向量$\mathbf{v}_\theta = [v_x, v_y]$：

$$\theta = \text{atan2}(v_y, v_x)$$

### 朝向角度到四元数转换 headingToQuaternion

$$\mathbf{a} = [0, 0, \theta] \quad \text{(角轴表示)}$$
$$\mathbf{q}_h = \text{angleAxisToQuaternion}(\mathbf{a})$$

<!-- 其中角轴到四元数（angle_axis_to_quaternion）的转换定义为：

$$\theta = \|\mathbf{a}\|_2$$
$$\mathbf{v} = \frac{\mathbf{a}}{\theta}$$
$$\mathbf{q}_h = \begin{bmatrix}
    \mathbf{v}\sin(\theta/2) \\
    \cos(\theta/2)
\end{bmatrix}$$ -->


在实现过程中需要注意以下关键点：所有四元数均假定为单位四元数（归一化），朝向角度表示绕垂直轴（z轴）的旋转，朝向向量是水平面上的二维单位向量，安全的反正切（$\text{atan2}$）实现包含数值稳定性处理。

<!-- ## 关键数学运算

转换中使用的四元数运算：

$$\mathbf{q}_1 \otimes \mathbf{q}_2 = \begin{bmatrix}
    q_{1w}q_{2x} + q_{1x}q_{2w} + q_{1y}q_{2z} - q_{1z}q_{2y} \\
    q_{1w}q_{2y} - q_{1x}q_{2z} + q_{1y}q_{2w} + q_{1z}q_{2x} \\
    q_{1w}q_{2z} + q_{1x}q_{2y} - q_{1y}q_{2x} + q_{1z}q_{2w} \\
    q_{1w}q_{2w} - q_{1x}q_{2x} - q_{1y}q_{2y} - q_{1z}q_{2z}
\end{bmatrix}$$

$$\mathbf{q}^* = [-q_x, -q_y, -q_z, q_w]$$ -->