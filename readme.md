# Melodi


Melodi is a platform for feedback, QA, and evaluations of LLM applications. This package provides a custom reporter for use with Braintrust evaluations, allowing users to log results to Melodi and generate shareable links for experiments.

This is very much a work in progress and should be considered an alpha release.

## Installation

To install `melodi`, simply use pip:

```bash
pip install melodi
```

## Usage

This package contains a custom Reporter for the Braintrust Data evaluation framework.
- https://www.braintrustdata.com/docs/guides/evals#custom-reporters

After installation, you can import the reporter in your project as follows:

```python
from melodi import braintrust_reporter
```

To use the reporter with Braintrust's `Eval` class:

```python
from braintrust import Eval
# Other imports as necessary

# Define your evaluation task, data, etc.
# ...

Eval(
    "Your Project Name",
    data=your_data_function,
    task=your_task_function,
    scores=your_scores_list,
    reporter=braintrust_reporter.melodi_reporter,
)
```

Make sure that you set your Melodi API key in your environment variables:

```bash
export MELODI_API_KEY='your_melodi_api_key_here'
```

## Features

- Easy integration with Braintrust evaluations.
- Automatic logging to Melodi for result comparison.
- Generation of shareable Melodi experiment links.

## Development

For development purposes, you can clone the repository and install the dependencies as follows:

```bash
git clone https://github.com/yourusername/melodi-braintrust-reporter.git
cd melodi-braintrust-reporter
pip install -r requirements.txt
```

## Testing

To run the tests included in the package:

```bash
python -m unittest discover tests
```



## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please contact info@melodi.fyi