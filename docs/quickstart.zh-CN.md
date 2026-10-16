# 第一个类型化决策

[返回资源列表](../README.zh-CN.md) · [English](quickstart.md)

示例依据[官方 Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python)，并固定模型版本。需要 TypeSafe API 访问权限，实际调用会产生费用。本项目仅核对接口，没有执行实时模型调用。

## 安装

```sh
pip install typesafe-sdk
```

将自己的 API key 设置在环境变量 `TYPESAFE_API_KEY` 中，不要提交到仓库。账户设置参见[官方快速开始](https://docs.typesafe.ai/introduction/quickstart)。

## 提出 Choice 问题

```python
from typesafe_sdk import Choice, TypeSafeClient

with TypeSafeClient() as client:
    result = client.system_one(
        model="jev-1.13.0",
        state={"ticket": "I was charged twice. Please fix this."},
        questions={
            "category": Choice(
                instructions="What is this ticket about?",
                criteria={
                    "billing": "Charges, payments, or refunds",
                    "technical": "Bugs or technical failures",
                    "other": "None of the above",
                },
            )
        },
    )

answer = result.choices["category"]
print(answer.choice, answer.probabilities, answer.confidence)
```

`choice` 是你给出的候选项之一，`probabilities` 包含候选项的概率分布。`confidence` 是分布的摘要统计量，不保证答案正确。应用代码决定执行、补充上下文或交给人工复核；阈值应在自身任务的独立测试样例上验证。

## 继续阅读

- [置信度与计算公式](https://docs.typesafe.ai/confidence)
- [Noul](https://docs.typesafe.ai/primitives/noul)：是非概率；[Score](https://docs.typesafe.ai/primitives/score)：有序评分标准。
- [模型版本与别名](https://docs.typesafe.ai/models)：别名会改变，评测时记录响应中的模型 ID。
- [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python)：与 LLM 基线进行比较。
