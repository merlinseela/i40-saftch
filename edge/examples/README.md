# I40-SAFTCH Edge Examples
This directory contains reference implementations of hardware-in-the-loop tests designed for the I40-SAFTCH Edge Daemon. These examples demonstrate how to interact with the Programmable Logic (PL) and utilize the framework's injected resources.

## Content
| Example                                                           | Description                                                                                                                                                                                         |
| ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**simple_adder**](./simple_adder/hil_test_simple_adder.py)       | The baseline introductory payload. Demonstrates fundamental AXI GPIO memory mapping, basic hardware interaction, and how to dump a custom JSON vector log into the framework's artifacts directory. |
| [**sobel_detector**](./sobel_detector/hil_test_sobel_detector.py) | Demonstrates heavier data streaming and image artifact generation, showing how the framework handles larger domain-specific outputs and how to utilize the additional payload directory.            |

## The HiLTestExecutor Contract
To write your own test payload for the I40-SAFTCH framework, your code must adhere to the "consenting adults" abstract contract. The framework provides the tools; you provide the logic.

1. **Inherit the Base Class:** Your main test class must subclass `HiLTestExecutor`.
2. **Inject the Context:** You must implement the execution method with the exact signature: `execute(self, context: JobContext) -> None:`.
3. **Flexible Naming:** You retain full authority over your source code. You can name your main Python file whatever makes sense for your project (e.g., `adder_validation.py`). Simply specify this file as the entry point when registering your job with the Star-API proxy, and the server will dynamically rename it to `hil_test.py` in-memory before shipping it to the edge node.
4. **Log for Humans:** Use `context.logger` to record chronological test steps. The framework will automatically bind these to the official `log.txt` artifact.
5. **Dump Heavy Data:** The `execute()` method returns `None`. If your test generates JSON arrays, CSVs, or binary data, use `context.workspace.get_path_additional_test_artifacts()` to save them. The framework will automatically zip up whatever it finds in this folder when the test concludes. Meaning you have to write your own logic to save your data to that directory.