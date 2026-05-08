from fpdf import FPDF
import os

# Dynamic output path - save to user's Desktop/report/save/
output_dir = os.path.join(os.path.expanduser("~"), "Desktop", "report", "save")
os.makedirs(output_dir, exist_ok=True)
output_pdf = os.path.join(output_dir, "实验5.21_金属逸出功实验.pdf")

class ExperimentReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)
    
    def header(self):
        if self.page_no() > 1:
            self.set_font('SimSun', '', 9)
            self.cell(0, 10, '实验5.21 金属逸出功实验', 0, 0, 'C')
            self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('SimSun', '', 9)
        self.cell(0, 10, f'第 {self.page_no()} 页', 0, 0, 'C')
    
    def section_title(self, title):
        self.set_font('SimHei', '', 14)
        self.set_text_color(0, 0, 0)
        self.ln(4)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def sub_section_title(self, title):
        self.set_font('SimHei', '', 12)
        self.set_text_color(0, 0, 0)
        self.ln(2)
        self.cell(0, 8, title, 0, 1, 'L')
        self.ln(1)
    
    def body_text(self, text):
        self.set_font('SimSun', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, text)
        self.ln(2)
    
    def equation(self, text):
        self.set_font('SimSun', '', 11)
        self.set_text_color(0, 0, 0)
        self.ln(2)
        x = self.get_x()
        self.set_x((210 - self.w) / 2)  # Center
        self.multi_cell(170, 7, text, 0, 'C')
        self.ln(2)
    
    def add_table(self, headers, data, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        
        # Header
        self.set_font('SimHei', '', 10)
        self.set_fill_color(230, 230, 230)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        
        # Data
        self.set_font('SimSun', '', 10)
        for row in data:
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), 1, 0, 'C')
            self.ln()
        self.ln(3)

# Create PDF
pdf = ExperimentReport()

# Add fonts - use system font paths dynamically
font_dir = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
simsun_path = os.path.join(font_dir, "simsun.ttc")
simhei_path = os.path.join(font_dir, "simhei.ttf")

pdf.add_font('SimSun', '', simsun_path, uni=True)
pdf.add_font('SimHei', '', simhei_path, uni=True)

# Title page
pdf.add_page()
pdf.ln(50)
pdf.set_font('SimHei', '', 24)
pdf.cell(0, 15, '实 验 报 告', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('SimHei', '', 18)
pdf.cell(0, 12, '实验5.21 金属逸出功实验', 0, 1, 'C')
pdf.ln(20)

# Info table
pdf.set_font('SimSun', '', 12)
info = [
    ('课程名称：', '大学物理实验'),
    ('姓    名：', '【待补充】'),
    ('学    号：', '【待补充】'),
    ('专业班级：', '【待补充】'),
    ('开课学期：', '【待补充】'),
    ('实验日期：', '【待补充】'),
]
for label, value in info:
    pdf.set_x(40)
    pdf.cell(30, 10, label, 0, 0, 'L')
    pdf.cell(80, 10, value, 0, 1, 'L')

pdf.ln(30)
pdf.set_font('SimSun', '', 12)
pdf.cell(0, 10, '物理与光电学院公共教学实验中心', 0, 1, 'C')
pdf.cell(0, 10, '2025年3月', 0, 1, 'C')

# Page 2: Content
pdf.add_page()

# Section 1
pdf.section_title('一、实验目的')
pdf.body_text('用 Richardson 直线法测定金属钨的电子逸出功。')

# Section 2
pdf.section_title('二、实验原理')
pdf.body_text(
    '金属中的电子在热运动过程中，如果其动能足以克服表面势垒，就能逸出金属表面形成热电子发射。'
    '根据 Richardson-Dushman 方程，热电子发射电流密度为：'
)
pdf.equation('J = AT² exp(-eW/kT)')
pdf.body_text(
    '其中 J 为发射电流密度，A 为 Richardson 常数，T 为绝对温度，W 为电子逸出功，'
    'e 为元电荷，k 为 Boltzmann 常数。'
)
pdf.body_text('对于实际阴极，发射电流为：')
pdf.equation('I = AST² exp(-eW/kT)')
pdf.body_text('其中 S 为阴极发射面积。取对数得：')
pdf.equation('lg(I/T²) = lg(AS) - (eW/(k·ln10)) × (1/T)')
pdf.body_text('以 lg(I/T²) 为纵坐标，1/T 为横坐标作图，可得一条直线，其斜率为：')
pdf.equation('m = -eW/(k·ln10)')
pdf.body_text('由此可求得逸出功：')
pdf.equation('W = -m × (k/e) × ln10')
pdf.body_text(
    '由于实际测量中存在接触电势差和空间电荷效应，需要在不同阳极电压 Ua 下测量阳极电流 Ia，'
    '然后外推到 Ua = 0 得到零场发射电流 I。'
)
pdf.body_text('根据 Schottky 效应，lg Ia 与 √Ua 成线性关系：')
pdf.equation('lg Ia = a√Ua + lg I')

# Section 3
pdf.section_title('三、实验仪器')
pdf.body_text('理想二极管实验装置、直流稳压电源、数字万用表等。')

# Section 4
pdf.section_title('四、实验内容与数据记录')
pdf.sub_section_title('1. 测量不同灯丝电流下的阳极电流')
pdf.body_text(
    '在灯丝电流 If = 0.600~0.700 A 范围内，以 0.025 A 为间隔调节灯丝电流，'
    '对每个 If 值，测量不同阳极电压 Ua 下的阳极电流 Ia（单位：μA）。'
)
pdf.body_text('温度计算公式：T = 900 + 1430 If（单位：K）')

pdf.sub_section_title('2. 原始数据记录')
pdf.set_font('SimSun', '', 10)
pdf.cell(0, 8, '附录表5.21.1 不同 Ua 和 If 下的 Ia 数据（单位：μA）', 0, 1, 'C')
pdf.ln(2)

# Raw data table
headers = ['Ua/V', '0.16', '0.25', '0.36', '0.49', '0.64', '0.81', '1.00']
data = [
    ['If = 0.600 A', '59', '62', '66', '69', '68', '72', '76'],
    ['If = 0.625 A', '110', '117', '125', '127', '131', '137', '142'],
    ['If = 0.650 A', '199', '211', '221', '230', '238', '244', '252'],
    ['If = 0.675 A', '336', '365', '383', '399', '410', '423', '437'],
    ['If = 0.700 A', '544', '603', '637', '670', '693', '719', '736'],
]
pdf.add_table(headers, data, [25, 23, 23, 23, 23, 23, 23, 23])

# Page 3: Data processing
pdf.add_page()
pdf.section_title('五、数据处理')
pdf.sub_section_title('1. 计算各灯丝电流对应的温度')
pdf.set_font('SimSun', '', 10)
pdf.cell(0, 8, '灯丝电流与温度对应关系', 0, 1, 'C')
pdf.ln(2)

headers = ['If/A', '0.600', '0.625', '0.650', '0.675', '0.700']
data = [['T/K', '1758.0', '1793.8', '1829.5', '1865.2', '1901.0']]
pdf.add_table(headers, data, [35, 31, 31, 31, 31, 31])

pdf.sub_section_title('2. lg Ia - √Ua 线性拟合')
pdf.body_text(
    '对每个温度下（即每个 If 值）的 lg Ia 与 √Ua 进行线性拟合，得到截距 lg I（零场电流对数）。'
)
pdf.set_font('SimSun', '', 10)
pdf.cell(0, 8, 'lg Ia - √Ua 线性拟合结果', 0, 1, 'C')
pdf.ln(2)

headers = ['If/A', 'T/K', '斜率', 'lg I', '相关系数 r']
data = [
    ['0.600', '1758.0', '0.1688', '1.7093', '0.9753'],
    ['0.625', '1793.8', '0.1750', '1.9798', '0.9867'],
    ['0.650', '1829.5', '0.1664', '2.2399', '0.9904'],
    ['0.675', '1865.2', '0.1786', '2.4682', '0.9799'],
    ['0.700', '1901.0', '0.2083', '2.6700', '0.9728'],
]
pdf.add_table(headers, data, [30, 30, 30, 30, 30])

pdf.sub_section_title('3. Richardson 直线法求逸出功')
pdf.body_text(
    '根据 Richardson-Dushman 方程，以 lg(I/T²) 为纵坐标，1/T 为横坐标作直线拟合。'
)
pdf.set_font('SimSun', '', 10)
pdf.cell(0, 8, 'Richardson 直线法数据', 0, 1, 'C')
pdf.ln(2)

headers = ['T/K', 'lg I', 'lg(I/T²)', '10⁴/T K⁻¹']
data = [
    ['1758.0', '1.7093', '-4.7808', '5.688'],
    ['1793.8', '1.9798', '-4.5277', '5.575'],
    ['1829.5', '2.2399', '-4.2848', '5.466'],
    ['1865.2', '2.4682', '-4.0733', '5.361'],
    ['1901.0', '2.6700', '-3.8880', '5.260'],
]
pdf.add_table(headers, data, [40, 40, 40, 40])

pdf.body_text('线性拟合结果：')
pdf.equation('lg(I/T²) = -20962.8553 × (1/T) + 7.1561')
pdf.body_text('相关系数 r = -0.9992')

pdf.sub_section_title('4. 逸出功计算')
pdf.body_text('斜率 m = -20962.8553')
pdf.equation('W = -m × (k/e) × ln10 = 20962.8553 × 8.6173×10⁻⁵ × 2.3026 = 4.1595 eV')

# Section 6
pdf.section_title('六、实验结果')
pdf.body_text('金属钨的电子逸出功测量值为：')
pdf.equation('W = 4.1595 eV')
pdf.body_text('钨的逸出功理论值约为 4.5 eV，测量值与理论值基本吻合。')

# Save PDF
pdf.output(output_pdf)
print(f"PDF saved to: {output_pdf}")
