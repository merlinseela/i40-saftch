# Standard Imports
import time
import json
# Third Party Imports
from pynq import Overlay
# Local Imports
from core.hiltestexecutor import HiLTestExecutor
from core.context import JobContext

class hil_test(HiLTestExecutor):
    def execute(self, context: JobContext) -> None:
        context.logger.info("[TEST EXECUTION] Initiating Simple Adder Hardware Validation...")
        try:
            context.logger.info(f"[TEST EXECUTION] Flashing FPGA...")
            overlay = Overlay(str(context.workspace.get_path_bitstream()))

            gpio_operands = overlay.axi_gpio_0
            gpio_result = overlay.axi_gpio_1
            gpio_leds = overlay.axi_gpio_2
            port_a = gpio_operands.channel1
            port_b = gpio_operands.channel2
            port_c = gpio_result.channel1
            port_led = gpio_leds.channel1

            test_vectors = [
                {"a": 13, "b": 29, "expected": 42},
                {"a": 100, "b": 100, "expected": 200},
                {"a": 50, "b": 10, "expected": 60}
            ]
            vector_result_log = []
            for idx, vector in enumerate(test_vectors):
                port_a.write(vector["a"], 0xFF)
                port_b.write(vector["b"], 0xFF)
                result = port_c.read()
                vector_log = {
                    "vector_index": idx,
                    "input_a": vector["a"],
                    "input_b": vector["b"],
                    "expected": vector["expected"],
                    "actual": result,
                    "passed": bool(result == vector["expected"])
                }
                vector_result_log.append(vector_log)
                
                if result == vector["expected"]:
                    context.logger.info(f"[TEST EXECUTION] Vector {idx+1} PASSED: {vector['a']} + {vector['b']} = {result}")
                else:
                    context.logger.warning(f"[TEST EXECUTION] Vector {idx+1} FAILED: Expected {vector['expected']}, got {result}")

                # sleep for human visual feedback LEDs
                port_led.write(result, 0xFF)    
                time.sleep(2)

            vector_log_path = context.workspace.get_path_additional_test_artifacts() / "simple_adder_vectors.json"
            context.logger.info(f"[TEST EXECUTION] Saving vector log to {vector_log_path}...")
            with open(vector_log_path, "w") as f:
                json.dump({"vector_result_log": vector_result_log}, f, indent=4)
                
        except Exception as e:
            context.logger.error(f"[TEST EXECUTION] Fatal error during hardware execution: {e}")
