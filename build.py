from pathlib import Path
from tsfpga.vivado.project import VivadoProject
from tsfpga.module import get_modules

def main():
    root = Path(__file__).parent.resolve()
    modules_dir = root / "modules"
    project_dir = root / "vivado_project"
    modules = get_modules([modules_dir])
    tcl_sources = [modules_dir / "zedboard_simple_adder" / "tcl" / "design_1.tcl"]

    proj = VivadoProject(
        name="zedboard_simple_adder",
        modules=modules,
        part="xc7z020clg484-1", # zedboard zynq chip part number
        board="avnet.com:zedboard:part0:1.4", # board support package pointer zedboard
        top="design_1_wrapper", # vhdl topmodule
        tcl_sources=tcl_sources
    )

    proj.create(project_path=project_dir)
    proj.build(project_path=project_dir, output_path=project_dir / "output")

if __name__ == "__main__":
    main()