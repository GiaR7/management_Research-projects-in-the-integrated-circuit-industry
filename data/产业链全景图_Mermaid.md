```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'fontSize': '14px', 'fontFamily': 'Arial, sans-serif'}}}%%
graph LR

subgraph upstream[" "]
    direction TB
    A1["<b>半导体设备</b><br/>──────<br/>产值 300亿<br/>光刻/刻蚀/薄膜沉积/量测<br/>代表：新凯来、中微半导体"]
    A2["<b>半导体材料</b><br/>──────<br/>产值 250亿<br/>硅片/光刻胶/特气/靶材<br/>代表：重投天科、鼎泰芯源"]
    A3["<b>零部件与耗材</b><br/>──────<br/>产值 58亿<br/>石英件/密封件/射频电源<br/>代表：深圳、东莞供应商"]
end

subgraph midstream[" "]
    direction TB
    B1["<b>IC设计</b><br/>──────<br/>产值 2,109亿（58.6%）<br/>手机SoC / AI芯片 / FPGA<br/>代表：海思、中兴微、全志"]
    B2["<b>晶圆制造</b><br/>──────<br/>产值 92亿（2.6% ▲102%）<br/>12英寸 / SiC / GaN<br/>代表：粤芯、中芯深圳、增芯"]
    B3["<b>封装测试</b><br/>──────<br/>产值 795亿（22.1%）<br/>先进封装SiP / FC / WLCSP<br/>代表：气派科技、华天科技"]
end

subgraph downstream[" "]
    direction TB
    C1["<b>消费电子</b><br/>──────<br/>900亿<br/>智能手机 / 无人机 / 智能家居<br/>代表：华为终端、OPPO、大疆"]
    C2["<b>通信设备</b><br/>──────<br/>800亿<br/>5G基站 / 光通信 / AI服务器<br/>代表：华为、中兴通讯"]
    C3["<b>汽车电子</b><br/>──────<br/>600亿<br/>车规MCU / IGBT / SiC<br/>代表：比亚迪半导体、英诺赛科"]
    C4["<b>人工智能</b><br/>──────<br/>400亿<br/>AI加速卡 / NPU / GPU<br/>代表：华为昇腾、海思"]
    C5["<b>工业电子</b><br/>──────<br/>300亿<br/>工控 / 电力电子 / IoT<br/>代表：汇顶科技、全志科技"]
end

A1 --> B2
A1 --> B3
A2 --> B2
A2 --> B3
A3 --> B2
A3 --> B3

B1 --> C1
B1 --> C2
B1 --> C3
B1 --> C4
B1 --> C5
B2 --> C1
B2 --> C3
B2 --> C4
B3 --> C1
B3 --> C2
B3 --> C3
B3 --> C4
B3 --> C5

classDef upstreamBox fill:#4198AC,color:#fff,stroke:#2E7A82,stroke-width:2px
classDef upstreamBox2 fill:#7BC0CD,color:#1a1a1a,stroke:#5A9FAD,stroke-width:2px
classDef upstreamBox3 fill:#BFDFD2,color:#1a1a1a,stroke:#9FC0B2,stroke-width:2px

classDef midBox1 fill:#BFDFD2,color:#1a1a1a,stroke:#9FC0B2,stroke-width:2px
classDef midBox2 fill:#DBCB92,color:#1a1a1a,stroke:#BBA872,stroke-width:2px
classDef midBox3 fill:#ECB66C,color:#1a1a1a,stroke:#CC9650,stroke-width:2px

classDef downBox1 fill:#ECB66C,color:#1a1a1a,stroke:#CC9650,stroke-width:2px
classDef downBox2 fill:#EA9E58,color:#1a1a1a,stroke:#CA7E38,stroke-width:2px
classDef downBox3 fill:#ED8D6A,color:#fff,stroke:#CD6D4A,stroke-width:2px

class A1 upstreamBox
class A2 upstreamBox2
class A3 upstreamBox3

class B1 midBox1
class B2 midBox2
class B3 midBox3

class C1,C4 downBox1
class C2,C5 downBox2
class C3 downBox3

style upstream fill:#EDF5F7,stroke:#51999F,stroke-width:3px,stroke-dasharray:6 3
style midstream fill:#FDF8F0,stroke:#DBCB92,stroke-width:3px,stroke-dasharray:6 3
style downstream fill:#FEF5EC,stroke:#ED8D6A,stroke-width:3px,stroke-dasharray:6 3
```

> **图：广东省集成电路产业链全景图**
>
> 数据来源：深芯盟/深圳市半导体行业协会（2025.10）、中商产业研究院（2025.02）
>
> **使用方法：** 复制上方 Mermaid 代码到 [Mermaid Live Editor](https://mermaid.live) 即可渲染，支持导出 SVG/PNG。
>
> **配色说明：** 上游蓝调（#4198AC → #7BC0CD → #BFDFD2）→ 中游过渡米黄（#DBCB92 / #ECB66C）→ 下游橙调（#ECB66C / #EA9E58 / #ED8D6A），体现从「供给端」到「应用端」的色彩过渡。
