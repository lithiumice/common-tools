# 人体运动轨迹表示与坐标转换

## 基础概念

朝向向量是平行于地面并指向人体面朝方向的向量。通过将人体根坐标的$z$轴与世界坐标$z$轴对齐，得到的$y$轴即为朝向向量。这种方法比使用容易产生奇异性的欧拉角更稳定。

## 全局与自我中心表示

已知每个人的无遮挡身体运动$\Theta^i$，我们需要恢复其全局轨迹$(\vec{T}^i, \vec{R}^i)$。通过全局轨迹预测器$\mathcal{T}$，将身体运动序列$\Theta = (\theta_1,\ldots,\theta_m)$转换为全局轨迹$(T, R)$，其中$T = (\tau_1,\ldots,\tau_m)$为根节点平移，$R = (\gamma_1,\ldots,\gamma_m)$为旋转。

为处理轨迹歧义，使用DiffTraj构建预测器：

$$\Psi = \mathcal{T}(\Theta, \eta)$$

$$(T, R) = \text{EgoToGlobal}(\Psi)$$


## 自我中心轨迹表示

自我中心轨迹$\Psi$是全局轨迹$(T, R)$的等价表示，其主要优点包括：将全局轨迹转换为相对局部差异，在朝向坐标系下表示旋转和平移，不受绝对$xy$平移和朝向影响，且适合长轨迹预测。

时刻$t$的自我中心轨迹分量$\psi_t = (\delta x_t, \delta y_t, z_t, \delta\phi_t, \eta_t)$计算如下：

$$(\delta x_t, \delta y_t) = \text{ToHeading}(\tau^{xy}_t - \tau^{xy}_{t-1})$$

$$z_t = \tau^z_t, \quad \delta\phi_t = \gamma^h_t - \gamma^h_{t-1}$$

$$\eta_t = \text{ToHeading}(\gamma_t)$$

其中$\tau^{xy}_t$为水平平移分量，$\tau^z_t$为高度分量，$\gamma^h_t$为朝向角度，$\eta_t$为局部旋转。

## 坐标转换

### 全局转局部

对于全局坐标$(\mathbf{T} = [\mathbf{xy}, z], \mathbf{q})$，局部转换步骤为：

$$\mathbf{q}' = \mathbf{q} \otimes \mathbf{q}_{\text{base}}^*$$
$$\theta = \text{getHeading}(\mathbf{q}')$$
$$\mathbf{q}_h = \text{getHeadingQuaternion}(\mathbf{q}')$$
$$\mathbf{q}_l = \text{deheadingQuaternion}(\mathbf{q}', \mathbf{q}_h)$$
$$\mathbf{R}_l = \text{quaternionToRot6D}(\mathbf{q}_l)$$
$$\Delta\mathbf{xy}_{\text{local}} = \text{rot2D}(\mathbf{xy}_{t+1} - \mathbf{xy}_t, -\theta_t)$$

### 局部转全局

对于局部坐标$\mathbf{\Psi} = [\Delta\mathbf{xy}_{\text{local}}, z, \mathbf{R}_l, \mathbf{v}_{\theta}]$，全局转换步骤为：

$$\theta_{\text{global}} = \sum_{t=0}^T \text{vectorToHeading}(\mathbf{v}_{\theta})$$
$$\mathbf{xy} = \sum_{t=0}^T \text{rot2D}(\Delta\mathbf{xy}_{\text{local}}, \theta_{\text{global}})$$
$$\mathbf{q} = \text{headingToQuaternion}(\theta_{\text{global}}) \otimes \text{rot6DToQuaternion}(\mathbf{R}_l) \otimes \mathbf{q}_{\text{base}}$$

## 实现要点

在实现过程中需要注意以下关键点：初始值$(\delta x_0, \delta y_0)$和$\delta\phi_0$需要存储起始位置和朝向，训练时使用真实初始值但推理时允许任意起始条件，通过视频证据匹配来修正轨迹漂移，保持四元数单位化，并使用6D旋转表示以避免旋转序列不连续。