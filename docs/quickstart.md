# A first typed decision

[Back to the collection](../README.md) · [中文](quickstart.zh-CN.md)

This example follows the [official Python SDK](https://github.com/typesafe-ai/typesafe-sdk-python), using an explicit model version. It requires TypeSafe API access and usage charges apply. We checked the interface without executing a live model call.

## Install

```sh
pip install typesafe-sdk
```

Set `TYPESAFE_API_KEY` in your environment using your own key. Do not commit keys to the repository. See the [official quick start](https://docs.typesafe.ai/introduction/quickstart) for account setup.

## Ask a Choice question

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

`choice` is one of your supplied options; `probabilities` contains their distribution. `confidence` summarizes that distribution and is not a guarantee of correctness. Application code decides whether to act, request more context, or send the case for review. Choose thresholds using held-out examples from your own workload.

## Next steps

- [Confidence and its formulas](https://docs.typesafe.ai/confidence)
- [Noul](https://docs.typesafe.ai/primitives/noul) for yes/no probabilities; [Score](https://docs.typesafe.ai/primitives/score) for ordered rubrics.
- [Model versions and aliases](https://docs.typesafe.ai/models). An alias can change; log the returned model ID for evaluation.
- [System One Adapter](https://github.com/typesafe-ai/system-one-adapter-python) for comparisons with LLM baselines.
