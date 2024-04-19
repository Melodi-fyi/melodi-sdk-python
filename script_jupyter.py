from autoevals import LevenshteinScorer
from braintrust import Eval
from melodi import braintrust_reporter  # This imports the reporter from your package

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
                "expected": {"key":"name", "value":"Hi Foo", "type":"text"},
            },
            {
                "input": "Bar",
                "expected": {"key":"name", "value":"Hi Bar", "type":"text"},
            },
        ],  # Replace with your eval dataset
        task=task,  # Use the async task function
        scores=[LevenshteinScorer],
        reporter=braintrust_reporter.melodi_reporter,  # Use the reporter
    )
    return results

# If this script is run in an environment like Jupyter Notebook,
# you would use 'await' to run the asynchronous evaluation function
eval_result = await run_evaluation()
print(eval_result.summary.experiment_url)  
