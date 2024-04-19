import asyncio
from autoevals import LevenshteinScorer
from braintrust import Eval
from melodi import braintrust_reporter

async def task(input):
    # Perform your task here; this is a simple synchronous operation for demonstration
    return "Hi " + input

# Define an async function to run the evaluation
async def run_evaluation():
    # Run the Eval class instance
    results = await Eval(
        "Say Hi Bot",
        data=lambda: [
            {
                "input": "Foo",
                "expected": {"key": "name", "value": "Hi Foo", "type": "text"},
            },
            {
                "input": "Bar",
                "expected": {"key": "name", "value": "Hi Bar", "type": "text"},
            },
        ],
        task=task,
        scores=[LevenshteinScorer],
        reporter=braintrust_reporter.melodi_reporter,
    )
    return results

# Run the async function from the event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    eval_result = loop.run_until_complete(run_evaluation())
    print(eval_result.summary.experiment_url)  # Assuming this attribute exists
