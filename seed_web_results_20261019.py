"""Seed public web-search job results into the local job hunter DB."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import job_hunter  # noqa: E402


JOBS = [
    {
        "title": "财经 AI 应用产品经理",
        "company": "诺亚控股",
        "location": "上海-闵行区",
        "url": "https://www.quanzhi.com/job/6a2f3e9c1433e769ad745584",
        "source": "web",
        "jd": """
负责财经条线 AI 应用、财务系统优化及流程自动化项目的推进落地。结合财务共享、核算、应收应付、费控、资金、税务等场景及自动化经验，推动 AI 转型、数据化、MCP Agent 调用。推动 AI 助手、知识库、工作流、RPA、自动化平台等工具的接入、配置、测试、上线及推广。参与财务系统相关项目实施，包括需求梳理、流程优化、方案设计、测试验收、上线支持和问题闭环。协同财务、SSC、产品、研发、数据等团队，推动跨团队项目交付。沉淀财经 AI 应用、流程自动化和系统实施的方法、模板及实践。
要求：熟悉 ERP、财务共享平台、费控、资金、税务、OA、BPM、RPA、BI；熟练使用 AI 工具，了解 Claude、Codex、ChatGPT、VS Code/Cursor；具备 SQL、Python、脚本自动化、API、低代码平台或数据报表能力优先。
""",
    },
    {
        "title": "资深财务产品经理",
        "company": "网易集团",
        "location": "杭州-滨江区",
        "url": "https://www.liepin.com/job/1984867975.shtml",
        "source": "web",
        "jd": """
负责电商财务产品规划、设计和持续迭代，包括对账、结算、记账中台、会计引擎、收入成本核算及财务数据处理。深入理解订单、支付、退款、履约、渠道结算、发票和会计核算等流程，梳理业务流、资金流、数据流和账务流。识别财务工作中重复、高频、规则化场景，运用大模型、Agent、自动化工作流或网页自动化提升效率。建设面向财务团队的 Agent 及自动化能力，包括知识查询、业财核对、核算自动化、数据加工与分析、报表生成和系统运维辅助。建立测试、权限、监控、告警、审计及人工兜底机制。
要求：3年以上财务产品、财务数字化或企业财务系统建设经验；熟练 SQL，理解数据库、API、JSON、定时任务、日志和常见系统集成方式；对 AI 编程和 Agent 应用有真实实践。
""",
    },
    {
        "title": "财务AI Agent产品经理",
        "company": "上海汉得信息技术股份有限公司",
        "location": "上海-青浦区",
        "url": "https://www.liepin.com/job/1984229447.shtml",
        "source": "web",
        "jd": """
负责财务域 AI Agent 整体产品规划，基于费控、财务中台、共享中心现有流程，挖掘自动化、智能化创新场景，输出 AI Agent 产品方案、原型、需求文档。对接财务业务部门、研发团队、运营团队，梳理费用报销、发票审核、账务稽核、预算分析、财务问答等场景痛点，设计 AI Agent 交互逻辑、运行规则、风控策略。跟进 AI Agent 开发落地、测试上线、灰度迭代，收集业务反馈持续优化。要求 ToB 产品经验，有财务费控、财务中台、财务共享、企业数字化产品经验优先，有 AI Agent、大模型落地产品经验加分。
""",
    },
    {
        "title": "AI产品经理（财务系统方向）",
        "company": "德勤企业咨询",
        "location": "上海-黄浦区",
        "url": "https://www.zhaopin.com/jobdetail/CC000423050J40846839407.htm",
        "source": "web",
        "jd": """
AI产品经理，财务系统方向。要求3年以上互联网产品经理经验，其中至少1年负责 AI 驱动型产品，如 AIGC 工具、AI Agent 产品、Agentic Workflow；有 AI+财税落地经验。理解 LLM、AI Agent、Multi-Agent、Prompt Engineering、RAG、Fine-tuning，具备 Agentic AI 设计范式能力，具备工具调用、RAG、知识图谱、记忆管理等产品化经验。能够深入理解用户痛点，将复杂业务流程拆解为可执行的 Agent 任务规划。加分：Python、SQL、企业端到端业财流程、大型 ERP 项目实施经验。
""",
    },
    {
        "title": "财务AI Agent专家",
        "company": "罗普特",
        "location": "上海-普陀区",
        "url": "https://www.liepin.com/job/1983105039.shtml",
        "source": "web",
        "jd": """
主导公司财务 AI 智能体 Agent 整体规划、选型、部署与迭代，替代核算、对账、报税、报表、费用审核等重复性财务工作。深度理解总账、应收应付、税务、资金、FP&A 全流程，将财务需求转化为 Agent 能力，如 RPA+大模型协同、知识库 RAG、自动决策。负责财务大模型选型、私有化部署、Prompt 工程、智能体工作流编排；打通 Agent 与 ERP、财务系统、银行、税务平台的数据集成与安全对接。建立准确率、处理时效、差错率、人效提升等指标，解决模型幻觉、数据一致性、合规风险。
""",
    },
    {
        "title": "产品经理-财务系统",
        "company": "NIO蔚来",
        "location": "上海-闵行区",
        "url": "https://www.liepin.com/job/1984993385.shtml",
        "source": "web",
        "jd": """
负责财务相关系统调研、分析用户需求，设计和梳理系统流程，推动并完成系统功能实现，提升财务效率。完成系统配置、测试、用户培训、运营等工作。深度对接研发、数据团队，协同落地 RAG 知识库、财务智能 Agent 等 AI 能力，打通财务数据壁垒，实现数据自动化流转、智能化分析。负责财务数字化项目统筹与落地管控，搭建项目推进机制，把控进度、质量、风险和成本。要求6年以上财务数字化领域相关系统实施及运营经验，真实可落地的财务AI产品上线迭代经验，英语可作为工作语言。
""",
    },
    {
        "title": "财务数字化产品经理",
        "company": "思格新能源",
        "location": "上海-浦东新区",
        "url": "https://www.liepin.com/job/1985512765.shtml",
        "source": "web",
        "jd": """
负责财务数字化产品愿景、路线图和需求优先级，以金蝶 ERP 为核心规划财务系统能力，并以业务价值、内控要求和用户体验驱动持续迭代。深入财务、会计和业务一线，围绕 R2R、P2P、O2C 及资金、税务、预算、成本、合并报表等场景识别痛点。负责方案设计与关键决策，统筹主数据、权限、财务规则和报表，并推动 ERP 与 CRM、SCM、MES、WMS、PLM、银企及税务平台集成。推动智能对账、异常识别、预测预警等 AI 场景落地。要求5年以上财务数字化产品或 ERP 系统经验。
""",
    },
    {
        "title": "【财务】产品经理-财务系统",
        "company": "众安信息技术服务有限公司",
        "location": "上海-黄浦区",
        "url": "https://www.liepin.com/job/1985653505.shtml",
        "source": "web",
        "jd": """
主导财务核心系统 Oracle EBS、费控、资金、税务等的全生命周期管理，包括需求分析、方案设计、开发实施、上线交付及运维优化。AI赋能财务数字化转型，深入理解财务业务场景，识别 AI 可赋能环节，如智能审单、自动对账、智能预测、异常检测，推动 AI 解决方案设计与落地。负责财务 AI 项目如大模型应用、智能报表生成、财务知识库构建的立项、实施与效果评估。协同数据团队推动财务数据标准化、资产化，确保数据安全、隐私保护和合规。要求5年以上财务系统实施或项目管理经验，熟悉 ERP、AI、SQL/Python。
""",
    },
    {
        "title": "财务产品经理",
        "company": "金斯瑞生物科技",
        "location": "南京-江宁区",
        "url": "https://www.liepin.com/job/1984987711.shtml",
        "source": "web",
        "jd": """
负责把财务业务痛点翻译成可落地的 AI 产品与场景，拉通业务与技术，主导 AI 真正落进预算、核算、经营分析、资金、税务、内控等核心场景。运用精益流程分析工具识别财务流程 AI 重构机会，方向包括核算与关账、应收应付、经营分析、资金与司库、税务与合规、内控与审计、合同与单据。设计财务领域智能体的能力边界、交互模式与安全策略，含防提示注入、人机双审；沉淀可复用 Skill 与分析模板。推动财务结构化数据治理与非结构化知识沉淀，构建财务问答机器人 / Skill Hub。要求5年以上财务领域经验，有低代码/智能体平台经验，理解 RAG、Agent、Function Calling、MCP。
""",
    },
    {
        "title": "Agent工程师（财务）",
        "company": "玑蜜生物",
        "location": "广州-海珠区",
        "url": "https://www.liepin.com/job/1984921465.shtml",
        "source": "web",
        "jd": """
负责跨境电商财务 AI Agent 自研与迭代，搭建对账、回款、佣金结算、成本核算、税务风控、现金流管理自动化智能体系。参与研发多平台自动对账、海外网红佣金自动结算、多币种汇兑损益、SKU 全链路成本拆解、跨境税务巡检、财务风险内控等 Agent。对接店铺后台、收款通道、ERP、WMS、媒介系统，完成财务数据抓取与治理。基于大模型、RAG、工具调用实现形式发票、报关单据、物流费用、佣金合同、税务单据的 AI 智能解析与结构化归档。要求 Python、提示词工程、RAG 知识库、Function Call 工具调用、自动化工作流搭建。
""",
    },
    {
        "title": "财务智能体研发工程师 Python/Agent/RAG",
        "company": "北京科锐至诚科技有限公司",
        "location": "深圳-光明区",
        "url": "https://www.liepin.com/job/1985613633.shtml",
        "source": "web",
        "jd": """
负责财务 Agent、Skill、Workflow、知识库、工具调用、上下文管理、记忆管理及人工审批等核心能力的设计与开发。与 FA 和财务 SME 协作梳理数据来源、SOP、计算规则和交付物，将财务流程转化为标准化、可配置、可复用的 Agent Skill。对接 Excel、数据库、数据仓库、Power BI、企业 API 及公开数据，建设数据获取、清洗、转换、校验、聚合和指标计算能力。建设权限控制、数据隔离、结果校验、人工确认、异常重试、断点恢复、执行审计、数据溯源和系统可观测能力。要求5年以上后端或平台研发经验，Python/Go/Java，FastAPI/Spring Boot/Gin，LangGraph/LangChain，Docker、LLMOps。
""",
    }
]


def main() -> None:
    job_hunter.init_db()
    for job in JOBS:
        args = argparse.Namespace(
            title=job["title"],
            company=job["company"],
            location=job["location"],
            url=job["url"],
            source=job["source"],
            jd=job["jd"],
            jd_file=None,
        )
        try:
            job_hunter.add_job(args)
        except SystemExit as exc:
            print(f"skip {job['company']} - {job['title']}: {exc}")


if __name__ == "__main__":
    main()
