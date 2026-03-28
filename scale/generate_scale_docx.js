const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
  TabStopType, TabStopPosition
} = require("docx");

// ===== 常量 =====
const PAGE_WIDTH = 11906; // A4
const PAGE_HEIGHT = 16838;
const MARGIN = 1440;
const CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN; // 9026
const FONT_CN = "SimSun";
const FONT_EN = "Times New Roman";
const COLOR_TITLE = "1F4E79";
const COLOR_HEADING = "2E75B6";
const COLOR_TABLE_HEADER = "D6E4F0";
const COLOR_TABLE_ALT = "F2F7FB";
const COLOR_LIGHT = "EAF1F8";

const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

// ===== 工具函数 =====
function cn(text, opts = {}) {
  return new TextRun({ text, font: FONT_CN, size: opts.size || 21, bold: opts.bold, italics: opts.italics, color: opts.color, ...opts });
}
function en(text, opts = {}) {
  return new TextRun({ text, font: FONT_EN, size: opts.size || 21, bold: opts.bold, italics: opts.italics, color: opts.color, ...opts });
}
function heading1(text) {
  return new Paragraph({
    spacing: { before: 360, after: 200 },
    children: [cn(text, { size: 28, bold: true, color: COLOR_TITLE })],
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR_HEADING, space: 4 } },
  });
}
function heading2(text) {
  return new Paragraph({
    spacing: { before: 280, after: 160 },
    children: [cn(text, { size: 24, bold: true, color: COLOR_HEADING })],
  });
}
function heading3(text) {
  return new Paragraph({
    spacing: { before: 200, after: 120 },
    children: [cn(text, { size: 22, bold: true, color: "333333" })],
  });
}
function para(children, opts = {}) {
  return new Paragraph({
    spacing: { before: opts.before || 60, after: opts.after || 60, line: opts.line || 360 },
    indent: opts.indent ? { firstLine: 420 } : undefined,
    alignment: opts.align,
    children: Array.isArray(children) ? children : [cn(children)],
  });
}
function emptyLine() {
  return new Paragraph({ spacing: { before: 60, after: 60 }, children: [] });
}

// 创建表格行
function headerRow(cells, colWidths) {
  return new TableRow({
    tableHeader: true,
    children: cells.map((text, i) =>
      new TableCell({
        borders, width: { size: colWidths[i], type: WidthType.DXA },
        shading: { fill: COLOR_TABLE_HEADER, type: ShadingType.CLEAR },
        margins: cellMargins,
        verticalAlign: "center",
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [cn(text, { bold: true, size: 20 })] })],
      })
    ),
  });
}
function dataRow(cells, colWidths, alt = false) {
  return new TableRow({
    children: cells.map((content, i) => {
      const isArray = Array.isArray(content);
      return new TableCell({
        borders, width: { size: colWidths[i], type: WidthType.DXA },
        shading: alt ? { fill: COLOR_TABLE_ALT, type: ShadingType.CLEAR } : undefined,
        margins: cellMargins,
        children: isArray ? content : [new Paragraph({ children: typeof content === "string" ? [cn(content, { size: 20 })] : [content] })],
      });
    }),
  });
}

// ===== 量表题项 =====
function scaleItemRow(id, text, source, reverse, colWidths, alt) {
  return dataRow([
    cn(id, { size: 20, bold: true }),
    cn(text, { size: 20 }),
    en(source, { size: 18, italics: true, color: "666666" }),
    cn(reverse ? "R" : "", { size: 20, bold: true, color: reverse ? "CC3333" : "333333" }),
  ], colWidths, alt);
}

// ===== Likert评分格子行 =====
function likertRow(id, text, colWidths7) {
  const cells = [
    new TableCell({ borders, width: { size: colWidths7[0], type: WidthType.DXA }, margins: cellMargins,
      children: [new Paragraph({ children: [cn(id, { size: 18, bold: true })] })] }),
    new TableCell({ borders, width: { size: colWidths7[1], type: WidthType.DXA }, margins: cellMargins,
      children: [new Paragraph({ children: [cn(text, { size: 18 })] })] }),
  ];
  for (let s = 2; s < 9; s++) {
    cells.push(new TableCell({ borders, width: { size: colWidths7[s], type: WidthType.DXA }, margins: cellMargins,
      verticalAlign: "center",
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [cn("\u25CB", { size: 20 })] })] }));
  }
  return new TableRow({ children: cells });
}

// ===== 构建文档 =====
const numbering = {
  config: [
    { reference: "refs", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "[%1]", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 420, hanging: 420 } } } }] },
  ],
};

// 量表定义
const PU_ITEMS = [
  ["PU1", "使用AI推荐能帮助我做出更好的消费决策", "Davis, 1989", false],
  ["PU2", "AI推荐提高了我的购物效率", "Davis, 1989", false],
  ["PU3", "AI推荐能帮我发现更符合需求的产品", "Davis, 1989", false],
  ["PU4", "依赖AI推荐能显著节省我的时间和精力", "Davis, 1989", false],
  ["PU5", "AI推荐提升了我消费决策的整体质量", "Davis, 1989", false],
  ["PU6", "AI推荐增强了我对购买选择的信心", "Davis, 1989", false],
  ["PU7", "总体而言，AI推荐系统对我的消费决策非常有用", "Davis, 1989", false],
];
const PEOU_ITEMS = [
  ["PEOU1", "学习使用AI推荐系统对我来说很容易", "Davis, 1989", false],
  ["PEOU2", "使用AI推荐进行消费决策无需太多思考", "Davis, 1989", false],
  ["PEOU3", "AI推荐系统的交互界面清晰易懂", "Davis, 1989", false],
  ["PEOU4", "理解AI给出的推荐理由对我来说很容易", "Davis, 1989", false],
  ["PEOU5", "使用AI推荐不需要复杂的操作步骤", "Davis, 1989", false],
  ["PEOU6", "总体而言，AI推荐系统使用起来很简便", "Davis, 1989", false],
];
const TR_ITEMS = [
  ["TR1", "我相信AI推荐系统具有做出准确推荐的能力", "Lee & See, 2004", false],
  ["TR2", "AI推荐系统的建议通常是可靠的", "Lee & See, 2004", false],
  ["TR3", "我能够判断何时应该依赖AI推荐、何时应该自主决策", "Lee & See, 2004", false],
  ["TR4", "AI推荐系统的推荐逻辑是透明可理解的", "Lee & See, 2004", false],
];
const AA_ITEMS = [
  ["AA1", "当AI推荐出现错误时，我对它的信任会大幅降低", "Dietvorst et al., 2015", true],
  ["AA2", "相比人类推荐，我更难以容忍AI推荐的失误", "Castelo et al., 2019", true],
  ["AA3", "我认为AI比人类更擅长处理消费决策中的信息分析", "Logg et al., 2019", false],
  ["AA4", "在需要客观判断的消费场景中，我更倾向于相信AI", "Castelo et al., 2019", false],
];
const AC_ITEMS = [
  ["AC1", "在消费决策中保持个人控制权对我非常重要", "Lee & See, 2004", true],
  ["AC2", "我愿意将日常消费决策完全交给AI处理", "Huang et al., 2019", false],
  ["AC3", "即使AI推荐了产品，我仍需要亲自比较和确认", "Lee & See, 2004", true],
];
const SF_ITEMS = [
  ["SI1", "我周围的人对AI推荐的使用态度影响了我的选择", "TAM2; Venkatesh & Davis, 2000", false],
  ["RP1", "过度依赖AI推荐可能导致不满意的购买决策", "Lee & See, 2004", true],
  ["RP2", "AI推荐可能会限制我接触到的产品多样性", "Huang et al., 2019", true],
];

const ITEM_COL_WIDTHS = [800, 5226, 2200, 800];

function buildScaleTable(items) {
  const rows = [headerRow(["编号", "题项内容", "文献来源", "计分"], ITEM_COL_WIDTHS)];
  items.forEach((item, i) => rows.push(scaleItemRow(item[0], item[1], item[2], item[3], ITEM_COL_WIDTHS, i % 2 === 1)));
  return new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: ITEM_COL_WIDTHS, rows });
}

// Likert问卷表格
const LIKERT_COLS = [600, 3426, 700, 700, 700, 700, 700, 700, 700];
function buildLikertHeader() {
  const labels = ["编号", "题项", "1\n非常\n不同意", "2\n不同意", "3\n有点\n不同意", "4\n中立", "5\n有点\n同意", "6\n同意", "7\n非常\n同意"];
  return new TableRow({
    tableHeader: true,
    children: labels.map((text, i) =>
      new TableCell({
        borders, width: { size: LIKERT_COLS[i], type: WidthType.DXA },
        shading: { fill: COLOR_TABLE_HEADER, type: ShadingType.CLEAR },
        margins: cellMargins, verticalAlign: "center",
        children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [cn(text, { bold: true, size: 16 })] })],
      })
    ),
  });
}
function buildLikertSection(title, items) {
  const rows = [
    new TableRow({
      children: [new TableCell({
        borders, columnSpan: 9,
        shading: { fill: COLOR_LIGHT, type: ShadingType.CLEAR },
        margins: cellMargins,
        children: [new Paragraph({ children: [cn(title, { bold: true, size: 20, color: COLOR_HEADING })] })],
      })],
    }),
  ];
  items.forEach(item => rows.push(likertRow(item[0], item[1], LIKERT_COLS)));
  return rows;
}

// ===== 主文档 =====
const sections = [];

// --- 封面页 ---
sections.push({
  properties: {
    page: { size: { width: PAGE_WIDTH, height: PAGE_HEIGHT }, margin: { top: 2880, right: MARGIN, bottom: MARGIN, left: MARGIN } },
  },
  children: [
    emptyLine(), emptyLine(), emptyLine(),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [cn("AI消费决策依赖等级量表", { size: 44, bold: true, color: COLOR_TITLE })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 },
      children: [en("AI Consumer Decision Delegation Scale (ACDDS)", { size: 24, italics: true, color: "555555" })] }),
    emptyLine(),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 },
      border: { top: { style: BorderStyle.SINGLE, size: 3, color: COLOR_HEADING, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 3, color: COLOR_HEADING, space: 8 } },
      children: [cn("L1-L5消费者AI依赖等级测量工具", { size: 26, color: COLOR_HEADING })] }),
    emptyLine(), emptyLine(),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
      children: [cn("理论基础", { size: 22, bold: true, color: "444444" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [en("Technology Acceptance Model (Davis, 1989)", { size: 20, color: "666666" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [en("Trust in Automation (Lee & See, 2004)", { size: 20, color: "666666" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [en("Algorithm Aversion (Dietvorst et al., 2015; Castelo et al., 2019)", { size: 20, color: "666666" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [en("Algorithm Appreciation (Logg et al., 2019)", { size: 20, color: "666666" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
      children: [en("The Feeling Economy (Huang et al., 2019)", { size: 20, color: "666666" })] }),
    emptyLine(), emptyLine(), emptyLine(),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [cn("量表共6个维度，26个题项", { size: 22, color: "444444" })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: [cn("采用7点Likert量表计分", { size: 22, color: "444444" })] }),
  ],
});

// --- 正文页 ---
const bodyChildren = [];

// ===== 第一部分：量表概述 =====
bodyChildren.push(heading1("第一部分  量表概述"));
bodyChildren.push(para([
  cn("AI消费决策依赖等级量表（", { size: 21 }),
  en("AI Consumer Decision Delegation Scale, ACDDS", { size: 21, italics: true }),
  cn("）是一套基于多个经典理论框架开发的心理测量工具，旨在测量消费者在消费决策过程中对AI推荐系统的依赖程度，并据此将消费者分类为L1至L5五个依赖等级。", { size: 21 }),
], { indent: true }));

bodyChildren.push(heading2("1.1  L1-L5等级定义"));

const levelDefs = [
  ["L1", "完全自主型\n(Autonomous)", "完全依靠个人判断和经验做出消费决策，不使用或忽视AI推荐。自主搜索和比较替代方案，决策时间最长，考虑替代品数量最多。", "控制需求高\n技术接受度低\n信任倾向低"],
  ["L2", "信息辅助型\n(Info Assisted)", "主要依靠自己的判断，但会参考AI建议作为辅助信息。对AI推荐采取人工审核（约70%概率接受），仍进行自主搜索。", "技术接受度中等\n信任倾向中等\n控制需求中等"],
  ["L3", "半委托型\n(Semi Delegated)", "AI和个人判断各占一半权重，形成均衡的决策模式。对AI推荐采取规则约束选择（约80%概率接受）。状态最稳定，不容易改变。", "各特质相对平衡\n既不过度信任\n也不过度怀疑"],
  ["L4", "高度依赖型\n(Highly Dependent)", "高度依赖AI推荐，个人判断仅作微调。直接采纳AI推荐的产品，决策时间最短，信息搜索深度最低。", "技术接受度高\n信任倾向高\n认知惰性高"],
  ["L5", "完全代理型\n(Fully Delegated)", "完全交给AI代理做决定，不进行人工审核。完全依赖AI推荐，不进行独立的信息搜索。", "技术接受度最高\n信任倾向最高\n控制需求最低"],
];
const levelColWidths = [600, 1600, 4226, 2600];
const levelRows = [headerRow(["等级", "类型名称", "行为特征描述", "消费者特质"], levelColWidths)];
levelDefs.forEach((row, i) => levelRows.push(dataRow(row.map(t => cn(t, { size: 19 })), levelColWidths, i % 2 === 1)));
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: levelColWidths, rows: levelRows }));

bodyChildren.push(heading2("1.2  理论框架与文献基础"));
bodyChildren.push(para("本量表的开发整合了以下六个核心理论与实证研究成果：", { indent: true }));

const theoryData = [
  ["技术接受模型\n(TAM)", "Davis (1989)\nMIS Quarterly", "感知有用性（PU）\n感知易用性（PEOU）", "PU和PEOU是预测技术使用意愿的两个核心变量，Cronbach's \u03B1通常>0.80，解释力达55%-75%。"],
  ["自动化信任理论", "Lee & See (2004)\nHuman Factors", "能力信任、可靠性感知\n透明度、校准信任", "信任通过分析、类比和情感三个层次形成；区分了信任不足(Disuse)和过度信任(Misuse)。"],
  ["算法厌恶理论", "Dietvorst et al. (2015)\nJ. Exp. Psych.: General", "错误敏感性\n信心损失", "人们在看到算法犯错后迅速失去信心，且对算法错误的容忍度低于对人类错误的容忍度。"],
  ["任务适配性", "Castelo et al. (2019)\nJ. Marketing Research", "主观性感知\n能力信任", "任务越主观，消费者越避免信任算法；增加感知客观性可提升算法信任。"],
  ["算法欣赏理论", "Logg et al. (2019)\nOrg. Behav. Hum. Dec. Proc.", "算法偏好\n建议接纳度", "在数值估计和预测任务中，人们更倾向于遵循算法建议而非人类建议。"],
  ["感知经济理论", "Huang et al. (2019)\nCalifornia Mgmt. Review", "人机协作\n任务分配", "AI能力从机械任务扩展到分析任务，预测感知经济将成为主导范式。"],
];
const theoryColWidths = [1400, 1800, 2100, 3726];
const theoryRows = [headerRow(["理论框架", "核心文献", "关键构念", "主要发现"], theoryColWidths)];
theoryData.forEach((row, i) => theoryRows.push(dataRow(row.map(t => cn(t, { size: 18 })), theoryColWidths, i % 2 === 1)));
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: theoryColWidths, rows: theoryRows }));

// ===== 第二部分：量表题项 =====
bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
bodyChildren.push(heading1("第二部分  量表题项详情"));
bodyChildren.push(para([
  cn("本量表共包含", { size: 21 }),
  cn("6个维度、26个题项", { size: 21, bold: true }),
  cn("，全部采用7点Likert量表计分（1=非常不同意，7=非常同意）。标注"R"的题项为反向计分。", { size: 21 }),
], { indent: true }));

bodyChildren.push(heading2("维度A：感知有用性（Perceived Usefulness, PU）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Davis, F. D. (1989). Perceived Usefulness, Perceived Ease of Use, and User Acceptance of Information Technology. MIS Quarterly, 13(3), 319-340.", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("测量消费者认为AI推荐系统能够提升其消费决策质量和效率的程度。", { indent: true }));
bodyChildren.push(buildScaleTable(PU_ITEMS));

bodyChildren.push(heading2("维度B：感知易用性（Perceived Ease of Use, PEOU）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Davis, F. D. (1989). MIS Quarterly, 13(3), 319-340.", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("测量消费者认为使用AI推荐系统的便利性和无需过多认知努力的程度。", { indent: true }));
bodyChildren.push(buildScaleTable(PEOU_ITEMS));

bodyChildren.push(heading2("维度C：AI信任（Trust in AI）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Lee, J. D., & See, K. A. (2004). Trust in Automation: Designing for Appropriate Reliance. Human Factors, 46(1), 50-80.", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("测量消费者对AI推荐系统在能力、可靠性、透明度等方面的信任水平。", { indent: true }));
bodyChildren.push(buildScaleTable(TR_ITEMS));

bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
bodyChildren.push(heading2("维度D：算法态度（Algorithm Attitude）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Dietvorst et al. (2015); Castelo et al. (2019); Logg et al. (2019)", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("综合测量消费者对算法的厌恶与欣赏程度，包括错误敏感性和任务适配性。", { indent: true }));
bodyChildren.push(buildScaleTable(AA_ITEMS));

bodyChildren.push(heading2("维度E：自主性与控制（Autonomy & Control）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Lee & See (2004); Huang et al. (2019)", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("测量消费者对决策控制权的需求程度及其将决策委托给AI的意愿。", { indent: true }));
bodyChildren.push(buildScaleTable(AC_ITEMS));

bodyChildren.push(heading2("维度F：社会影响与风险感知（Social Influence & Risk Perception）"));
bodyChildren.push(para([cn("来源：", { bold: true }), en("Venkatesh & Davis (2000) TAM2; Lee & See (2004); Huang et al. (2019)", { size: 20, italics: true })], { before: 40, after: 80 }));
bodyChildren.push(para("测量社会环境对消费者AI使用的影响，以及消费者对AI依赖风险的感知。", { indent: true }));
bodyChildren.push(buildScaleTable(SF_ITEMS));

// ===== 第三部分：计分方法 =====
bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
bodyChildren.push(heading1("第三部分  计分方法与等级划分"));

bodyChildren.push(heading2("3.1  反向计分"));
bodyChildren.push(para("以下6个题项需要反向计分（得分 = 8 - 原始分）：", { indent: true }));

const reverseItems = [
  ["AA1", "当AI推荐出现错误时，我对它的信任会大幅降低"],
  ["AA2", "相比人类推荐，我更难以容忍AI推荐的失误"],
  ["AC1", "在消费决策中保持个人控制权对我非常重要"],
  ["AC3", "即使AI推荐了产品，我仍需要亲自比较和确认"],
  ["RP1", "过度依赖AI推荐可能导致不满意的购买决策"],
  ["RP2", "AI推荐可能会限制我接触到的产品多样性"],
];
const revColWidths = [1000, 8026];
const revRows = [headerRow(["题项编号", "题项内容"], revColWidths)];
reverseItems.forEach((row, i) => revRows.push(dataRow(row.map(t => cn(t, { size: 20 })), revColWidths, i % 2 === 1)));
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: revColWidths, rows: revRows }));

bodyChildren.push(heading2("3.2  维度得分计算"));
bodyChildren.push(para("各维度得分为该维度下所有题项（反向计分后）的算术平均值：", { indent: true }));

const dimScoreData = [
  ["PU\u0305 (感知有用性)", "(PU1 + PU2 + PU3 + PU4 + PU5 + PU6 + PU7) / 7", "0.25"],
  ["PEOU\u0305 (感知易用性)", "(PEOU1 + PEOU2 + PEOU3 + PEOU4 + PEOU5 + PEOU6) / 6", "0.20"],
  ["TR\u0305 (AI信任)", "(TR1 + TR2 + TR3 + TR4) / 4", "0.20"],
  ["AA\u0305 (算法态度)", "(AA1R + AA2R + AA3 + AA4) / 4", "0.15"],
  ["AC\u0305 (自主性与控制)", "(AC1R + AC2 + AC3R) / 3", "0.10"],
  ["SF\u0305 (社会影响与风险)", "(SI1 + RP1R + RP2R) / 3", "0.10"],
];
const dimColWidths = [2200, 5026, 1800];
const dimRows = [headerRow(["维度", "计算公式", "权重 (w)"], dimColWidths)];
dimScoreData.forEach((row, i) => dimRows.push(dataRow(row.map(t => cn(t, { size: 19 })), dimColWidths, i % 2 === 1)));
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: dimColWidths, rows: dimRows }));
bodyChildren.push(para([cn("注：上标R表示该题项已进行反向计分处理。", { size: 19, italics: true, color: "666666" })]));

bodyChildren.push(heading2("3.3  总依赖度指数"));
bodyChildren.push(para("总依赖度指数（Delegation Index, DI）的计算公式为：", { indent: true }));
bodyChildren.push(emptyLine());
bodyChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 100 },
  border: { top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC", space: 6 }, bottom: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC", space: 6 } },
  children: [
    en("DI", { size: 24, bold: true, italics: true }),
    cn(" = 0.25\u00D7", { size: 22 }), en("PU\u0305", { size: 22, italics: true }),
    cn(" + 0.20\u00D7", { size: 22 }), en("PEOU\u0305", { size: 22, italics: true }),
    cn(" + 0.20\u00D7", { size: 22 }), en("TR\u0305", { size: 22, italics: true }),
    cn(" + 0.15\u00D7", { size: 22 }), en("AA\u0305", { size: 22, italics: true }),
    cn(" + 0.10\u00D7", { size: 22 }), en("AC\u0305", { size: 22, italics: true }),
    cn(" + 0.10\u00D7", { size: 22 }), en("SF\u0305", { size: 22, italics: true }),
  ] }));
bodyChildren.push(emptyLine());
bodyChildren.push(para("归一化依赖度指数（Normalized DI, NDI）转换到[0, 1]区间：", { indent: true }));
bodyChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 100 },
  children: [
    en("NDI", { size: 24, bold: true, italics: true }),
    cn(" = (", { size: 22 }), en("DI", { size: 22, italics: true }),
    cn(" \u2212 1) / 6", { size: 22 }),
  ] }));

bodyChildren.push(heading2("3.4  等级划分标准"));

const cutoffData = [
  ["L1", "完全自主型", "[0.00, 0.20)", "1.00 \u2013 2.20", "完全自主决策，不使用AI"],
  ["L2", "信息辅助型", "[0.20, 0.40)", "2.20 \u2013 3.40", "参考AI建议，自主判断为主"],
  ["L3", "半委托型", "[0.40, 0.60)", "3.40 \u2013 4.60", "AI与个人判断均衡协作"],
  ["L4", "高度依赖型", "[0.60, 0.80)", "4.60 \u2013 5.80", "高度依赖AI，个人仅微调"],
  ["L5", "完全代理型", "[0.80, 1.00]", "5.80 \u2013 7.00", "完全委托AI决策"],
];
const cutColWidths = [700, 1600, 1500, 1800, 3426];
const cutRows = [headerRow(["等级", "类型", "NDI区间", "DI原始分区间", "行为特征"], cutColWidths)];
cutoffData.forEach((row, i) => cutRows.push(dataRow(row.map(t => cn(t, { size: 19 })), cutColWidths, i % 2 === 1)));
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: cutColWidths, rows: cutRows }));

// ===== 第四部分：问卷正文 =====
bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
bodyChildren.push(heading1("第四部分  正式问卷"));
bodyChildren.push(emptyLine());
bodyChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
  children: [cn("AI消费决策依赖等级问卷", { size: 32, bold: true, color: COLOR_TITLE })] }));

bodyChildren.push(para([
  cn("尊敬的受访者：您好！感谢您参与本次调查。本问卷旨在了解您在消费决策中对AI推荐系统的使用态度和行为。问卷采用匿名方式，所有数据仅用于学术研究，请根据您的真实感受作答。每个题项采用1-7分制：1=非常不同意，4=中立，7=非常同意。", { size: 20 }),
]));
bodyChildren.push(emptyLine());

// 完整Likert格式的问卷
const allSections = [
  ["维度A：感知有用性（PU）", PU_ITEMS],
  ["维度B：感知易用性（PEOU）", PEOU_ITEMS],
  ["维度C：AI信任（TR）", TR_ITEMS],
  ["维度D：算法态度（AA）", AA_ITEMS],
  ["维度E：自主性与控制（AC）", AC_ITEMS],
  ["维度F：社会影响与风险感知（SF）", SF_ITEMS],
];

const likertRows = [buildLikertHeader()];
allSections.forEach(([title, items]) => {
  likertRows.push(...buildLikertSection(title, items));
});
bodyChildren.push(new Table({ width: { size: CONTENT_WIDTH, type: WidthType.DXA }, columnWidths: LIKERT_COLS, rows: likertRows }));

// ===== 第五部分：参考文献 =====
bodyChildren.push(new Paragraph({ children: [new PageBreak()] }));
bodyChildren.push(heading1("第五部分  参考文献"));

const refs = [
  "Castelo, N., Bos, M. W., & Lehmann, D. R. (2019). Task-dependent algorithm aversion. Journal of Marketing Research, 56(5), 809-825.",
  "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. MIS Quarterly, 13(3), 319-340.",
  "Dietvorst, B. J., Simmons, J. P., & Massey, C. (2015). Algorithm aversion: People erroneously avoid algorithms after seeing them err. Journal of Experimental Psychology: General, 144(1), 114-126.",
  "Huang, M. H., Rust, R., & Maksimovic, V. (2019). The feeling economy: Managing in the next generation of artificial intelligence (AI). California Management Review, 61(4), 43-65.",
  "Lee, J. D., & See, K. A. (2004). Trust in automation: Designing for appropriate reliance. Human Factors, 46(1), 50-80.",
  "Logg, J. M., Minson, J. A., & Moore, D. A. (2019). Algorithm appreciation: People prefer algorithmic to human judgment. Organizational Behavior and Human Decision Processes, 151, 90-103.",
  "Venkatesh, V., & Davis, F. D. (2000). A theoretical extension of the technology acceptance model: Four longitudinal field studies. Management Science, 46(2), 186-204.",
];
refs.forEach(ref => {
  bodyChildren.push(new Paragraph({
    numbering: { reference: "refs", level: 0 },
    spacing: { before: 60, after: 60, line: 340 },
    children: [en(ref, { size: 20 })],
  }));
});

// 正文section
sections.push({
  properties: {
    page: { size: { width: PAGE_WIDTH, height: PAGE_HEIGHT }, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } },
  },
  headers: {
    default: new Header({
      children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: COLOR_HEADING, space: 4 } },
        children: [cn("AI消费决策依赖等级量表 (ACDDS)", { size: 16, color: "999999" })],
      })],
    }),
  },
  footers: {
    default: new Footer({
      children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [cn("- ", { size: 18, color: "999999" }), new TextRun({ children: [PageNumber.CURRENT], font: FONT_EN, size: 18, color: "999999" }), cn(" -", { size: 18, color: "999999" })],
      })],
    }),
  },
  children: bodyChildren,
});

const doc = new Document({ numbering, sections });

const outputPath = process.argv[2] || "AI消费决策依赖等级量表_ACDDS.docx";
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outputPath, buffer);
  console.log("Document created: " + outputPath);
});
