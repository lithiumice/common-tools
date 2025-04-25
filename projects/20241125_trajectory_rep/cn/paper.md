# 朝向坐标系（Heading Coordinate）与自我中心轨迹表示（Egocentric Trajectory Representation）

朝向向量指向人体面部方向并平行于地面。我们通过将人体根坐标的$z$轴与世界坐标$z$轴对齐，并使用对齐后的根坐标$y$轴作为朝向向量。这种获取朝向的方法比使用容易出现奇异性且不稳定的欧拉角偏航角更为可靠。朝向坐标系的定义过程是：首先将世界坐标原点置于人体根节点位置，然后绕$z$轴（垂直方向）旋转世界坐标系，使$y$轴与朝向向量对齐。根据定义，在朝向坐标系中表示和预测人体轨迹可以使预测结果不受人体绝对$xy$平移和朝向的影响。在自我中心轨迹表示$\psi_t = (\delta x_t, \delta y_t, z_t, \delta\phi_t, \eta_t)$中，我们使用绝对高度$z_t$，因为人体相对地面的高度变化不大，且与人体运动高度相关。对于局部旋转$\eta_t$，我们采用6D旋转表示以避免不连续性。

通过运动填充器获得每个人的无遮挡身体运动$\Theta^i$后，仍存在一个关键问题：人体的估计轨迹$(\vec{T}^i, \vec{R}^i)$仍可能被遮挡且不在一致的全局坐标系中。为解决这个问题，我们提出学习一个全局轨迹预测器$\mathcal{T}$，从局部身体运动$\Theta^i$生成人体的无遮挡全局轨迹$(\vec{T}^i, \vec{R}^i)$。

给定输入的无遮挡身体运动$\Theta = (\theta_1,\ldots,\theta_m)$，轨迹预测器$\mathcal{T}$输出相应的全局轨迹$(T, R)$，包括根节点平移$T = (\tau_1,\ldots,\tau_m)$和旋转$R = (\gamma_1,\ldots,\gamma_m)$。为处理全局轨迹中的潜在歧义，我们使用CVAE构建全局轨迹预测器：

$$\Psi = \mathcal{T}(\Theta,v)$$

$$(T, R) = \text{EgoToGlobal}(\Psi)$$

其中全局轨迹预测器$\mathcal{T}$对应CVAE解码器，$v$是CVAE的隐编码。在上述公式中，全局轨迹预测器$\mathcal{T}$的直接输出是自我中心轨迹$\Psi = (\psi_1,\ldots,\psi_m)$，该轨迹可通过转换函数EgoToGlobal转换为全局轨迹$(T, R)$。

# 自我中心轨迹表示

自我中心轨迹$\Psi$是全局轨迹$(T, R)$的另一种表示形式。它将全局轨迹转换为相对局部差异，并在朝向坐标系（$y$轴与朝向即人体面向方向对齐）中表示旋转和平移。这样，自我中心表示不受绝对$xy$平移和朝向的影响。这种表示更适合预测长轨迹，因为网络只需输出每一帧的局部轨迹变化，而不是可能较大的全局轨迹偏移。

从全局轨迹到自我中心轨迹的转换由另一个函数给出：$\Psi = \text{GlobalToEgo}(T, R)$，该函数是EgoToGlobal的逆函数。具体而言，时刻$t$的自我中心轨迹$\psi_t = (\delta x_t, \delta y_t, z_t, \delta\phi_t, \eta_t)$计算如下：

$$(\delta x_t, \delta y_t) = \text{ToHeading}(\tau^{xy}_t - \tau^{xy}_{t-1})$$

$$z_t = \tau^z_t, \quad \delta\phi_t = \gamma^h_t - \gamma^h_{t-1}$$

$$\eta_t = \text{ToHeading}(\gamma_t)$$

其中$\tau^{xy}_t$是平移$\tau_t$的$xy$分量，$\tau^z_t$是$\tau_t$的$z$分量（高度），$\gamma^h_t$是旋转$\gamma_t$的朝向角度。ToHeading是一个将平移和旋转转换到由朝向$\gamma^h_t$定义的朝向坐标系的函数，$\eta_t$是局部旋转。特别地，$(\delta x_0, \delta y_0)$和$\delta\phi_0$用于存储初始$xy$平移$\tau^{xy}_0$和朝向$\gamma^h_0$。这些初始值在训练时设为真实值，在推理时可为任意值（因为轨迹可以从任何位置和朝向开始）。上述公式的逆过程定义了公式中使用的逆转换EgoToGlobal，该函数通过累积自我中心轨迹获得全局轨迹。为修正轨迹中的潜在漂移，我们将优化每个人的全局轨迹以匹配视频证据，其中包括平滑点$(\delta x_0, \delta y_0, \delta\phi_0)$。更多关于自我中心轨迹的细节请参见附录D。