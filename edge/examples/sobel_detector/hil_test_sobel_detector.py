# Standard Imports
# Third Party Imports
from pynq import Overlay, allocate
from PIL import Image
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
# Local Imports
from core.hiltestexecutor import HiLTestExecutor
from core.context import JobContext

class hil_test(HiLTestExecutor):
    def execute(self, context: JobContext) -> None:
        context.logger.info("[TEST EXECUTION] Initiating Sobel Edge Detector Hardware Validation...")
        
        in_buffer = None
        out_buffer = None
        
        try:
            # Prepare/Flash FPGA
            overlay = Overlay(str(context.workspace.get_path_bitstream()))
            context.logger.info("[TEST EXECUTION] Flashed bitstream successfully.")
            dma = overlay.axi_dma_0

            # Prepare Image Data
            image_path = context.workspace.get_path_additional_test_payloads_directory() / "test_image.jpg"
            context.logger.info(f"[TEST EXECUTION] Loading test image from {image_path}...")
            original_image = Image.open(image_path).convert('L')
            image_array = np.array(original_image)
            height, width = image_array.shape
            context.logger.info(f"[TEST EXECUTION] Original image resolution: {width}x{height}")
            patches = sliding_window_view(image_array, (3, 3))
            out_height, out_width = patches.shape[0], patches.shape[1]
            num_patches = out_height * out_width
            flattened_patches = patches.reshape(num_patches, 9)
            context.logger.info(f"[TEST EXECUTION] Total patches to process: {num_patches}")
            context.logger.info(f"[TEST EXECUTION] Input buffer size: {flattened_patches.nbytes} bytes")

            # Prepare Storage
            context.logger.info("[TEST EXECUTION] Allocating DMA buffers...")
            in_buffer = allocate(shape=(num_patches, 9), dtype=np.uint8)
            out_buffer = allocate(shape=(num_patches,), dtype=np.uint8)
            context.logger.info("[TEST EXECUTION] Allocated the buffers.")
            np.copyto(in_buffer, flattened_patches)
            context.logger.info("[TEST EXECUTION] Copied flattened patches into in_buffer.")

            # Start Sobel Detection
            context.logger.info("[TEST EXECUTION] Starting DMA transfers (recv channel first)...")
            dma.recvchannel.transfer(out_buffer)
            dma.sendchannel.transfer(in_buffer)
            context.logger.info("[TEST EXECUTION] recv channel and send channel started.")
            dma.sendchannel.wait()
            context.logger.info("[TEST EXECUTION] sendchannel done.")
            dma.recvchannel.wait()
            context.logger.info("[TEST EXECUTION] recvchannel done.")

            # Reconstruct results 
            result_array = np.array(out_buffer).reshape(out_height, out_width)
            result_image = Image.fromarray(result_array)

            # Save results
            raw_output_path = context.workspace.get_path_additional_test_artifacts() / "sobel_hardware_output.jpg"
            context.logger.info(f"[TEST EXECUTION] Saving raw result image to {raw_output_path}...")
            result_image.save(raw_output_path)
            
            context.logger.info("[TEST EXECUTION] Sobel test finished successfully.")

        except Exception as e:
            context.logger.error(f"[TEST EXECUTION] Fatal error during hardware execution: {e}")
            
        finally:
            # WARNING: Not freeing channels can lead to PS/PL-lockups and state bleeding between jobs!
            if in_buffer is not None:
                in_buffer.close()
            if out_buffer is not None:
                out_buffer.close()
            context.logger.info("[TEST EXECUTION] Hardware DMA buffers freed.")