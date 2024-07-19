# Melodi
Melodi is a platform for feedback, QA, and online evaluations of LLM applications. The python SDK is a set of helper functions built on our [public APIs](https://docs.melodi.fyi/introduction) including:
- Production: Logging and end user feedback
- Pre-production: Programmatically create experiments for Expert Review in the Melodi UI for rating LLM outputs, editing LLM calls for ideal/golden datasets, and AB/preference testing.

For a working example, please review [the quickstart notebook](https://github.com/Melodi-fyi/melodi-sdk-python/blob/master/examples/quickstart.ipynb)

## Installation

To install `melodi`, use pip:

```bash
pip install melodi
```

## Setup

```python
from melodi.api import MelodiClient
from melodi.data_models import (
    BinarySample,
    BakeoffSample,
    FeedbackSample,
    Feedback,
    User,
    Item
)

os.environ["MELODI_API_KEY"] = "<YOUR_KEY>"

client = MelodiClient(verbose=True)
```

## Production functions
We provide two main APIs to collect information from your production environment: Log and Feedback

### Create log
Logs are used to track production LLM responses after the response has been generated. Online auto-evaluators can be configured in Melodi to monitor your logs and send alerts via slack.
```python 
item = Item(projectName="My First Project", versionName="1.0", data={"key": "value"})
client.create_log(item)
```

### Create user feedback
This API is intended to collect in app, end-user feedback via your production UI. This is distinct from Expert Reviews, which use the Melodi app to collect direct evaluations from your team. 

For convenience, [we also provide a react component](https://github.com/Melodi-fyi/melodi-sdk-react/), which is built on this API: 

```python
sample = FeedbackSample(
    project="My First Project",
    projectVersion="1.0",
    input="Some input data",
    output="Some output data",
    metadata={"key": "value"}
)

feedback = Feedback(
    feedbackType="POSITIVE",
    feedbackText="This is some positive feedback"
)

user = User(
    id="userid123",
    email="user@example.com"
)

client.create_feedback(sample, feedback, user)
```

## Pre-production functions
These functions are designed to be incorporated into your experimentation and pre-production process. Typically, these functions are used in a notebook setting, where you're experimenting and developing a model (or pipeline) before deploying that model into a user facing app. These functions create experiments for manual review in the Melodi Expert Review UI, which can be used by you, your team, or shared externally with customers or labelers to evaluate LLM responses. 
- **Binary**: A simple pass/fail assessment. Best for initial model validation and for creating ideal/golden datasets by editing model responses in Melodi. 
- **Bake-off** (aka AB Test): Preference testing between different versions of a model. 

### Binary Experiment
#### Batch
```python
binary_samples = client.load_samples(
    file_path="./examples/binary_sample_data.jsonl", experiment_type="binary"
)

client.create_binary_evaluation_experiment(
    name="My Binary Experiment",
    instructions="Here are some instructions",
    samples=binary_samples,
)
```
#### One-by-one
Issue a new experiment ID
```python
client.create_experiment(
    name="My First Experiment", instructions="Here are some sample instructions.", project="My First Project"
)
```

Add an individual sample to experiment
```python
EXP_ID = <YOUR_EXPERIMENT_ID>

sample_A = BinarySample(response="This is a response", title="This is a title")
client.log_binary_sample(experiment_id=EXP_ID, sample=sample_A)
```
### Bake-off Experiment
#### Batch
```python
bakeoff_samples = client.load_samples(
    file_path="./examples/bakeoff_sample_data.jsonl", experiment_type="bake_off"
)

client.create_bake_off_evaluation_experiment(
    name="My Bake-off Experiment",
    instructions="Here are some instructions",
    comparisons=bakeoff_samples,
    project="Test Project",
)
```
#### One-by-one
Issue a new experiment ID
```python
client.create_experiment(
    name="My First Experiment", instructions="Here are some sample instructions.", project="My First Project"
)
```
Add an individual sample to experiment
```python
EXP_ID = <YOUR_EXPERIMENT_ID>

sample_A = BakeoffSample(version="version A", response="response A")
sample_B = BakeoffSample(version="version B", response="response B")

client.log_bake_off_comparison(
    experiment_id=EXP_ID, sample_1=sample_A, sample_2=sample_B
)
```
### Get a shareable link for Expert Review
This returns a no-auth link so that you can collect Expert Reviews without having to create logins for your reviewers.
```python
client.make_shareable(EXP_ID)
```

## Contact

If you have any questions or feedback, please contact info@melodi.fyi

## License

This project is licensed under the MIT License.

Copyright 2024, Melodi Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
