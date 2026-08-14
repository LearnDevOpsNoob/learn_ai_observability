import asyncio

from src.evaluation.llm import evaluation_llm
from ragas.metrics.collections import Faithfulness


async def main():
    metric = Faithfulness(llm=evaluation_llm)

    result = await metric.ascore(
        user_input="What is the refund period?",
        response="Customers can request a refund within 30 days of purchase.",
        retrieved_contexts=[
            "Customers can request a refund within 30 days of purchase."
        ],
    )

    print("Evaluation Result")
    print("-----------------")
    print(f"Score : {result.value}")
    print(f"Reason: {result.reason}")


if __name__ == "__main__":
    asyncio.run(main())