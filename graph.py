import matplotlib.pyplot as plt

# 数据整理
data = [1, 2, 3]  # 分别是三个季度的行业分类境内股票投资组合数据

# 绘制图形
plt.figure(figsize=(8, 6))
plt.pie(data, labels=['农业', '制造业', '金融业'], colors=['#ff9999', '#66b3ff', '#99ff99'], autopct='%1.1f%%', startangle=90)
plt.title("红塔红土盛世普益混合发起式基金2023年第三季度按行业分类的境内股票投资组合情况")
plt.axis('equal')  # 使饼图比例相等
plt.show()