* https://cloud-images.ubuntu.com/releases/focal/release/
1. wsl aufsetzen mit 20.04
2. xilinx toolchain installieren
3. github runner einrichten (siehe anleitung github, muss ich hier nicht wiederholen)
4. ggf. hier dann eine tabelle oder liste rein mit den eingaben für die Konfiguration, sofern das notwendig ist.
ssowas wie tagss name etc. kann man drauf eingehen ssollte aber eigentlich erstmal für mich egal ssein

Wichtige Konfiguration:
.env des Runner anpassen und auf die Xilinx Tools pointen da der source Befehl der Xilinx Tools nicht zwingend von dem runner ausgeführt wird. -> TODO: Den .env file mit ins repository committen da er mit default values bestückt ist. ACHTUNG SECRETS RAUSNEHMEN UND LEER LASSEN. die muss der user dann einfüllen. (ggf. kann ich dummy secret hinterlegen die man austauschen kann)

ACHTUNG -> Vivado braucht dringend ein `source` update bevor es irgendwas anderes macht. Warum? im headless mode wird der XHub von Vivado nicht geladen/assoziiert., Die Folge: Die Board-Parts wenn mittels GUI installiert können nicht aufgelöst warden. Der globale Fix für den Vivado Runner: 

```bash
mkdir -p \~/.Xilinx/Vivado
echo 'set\_param board.repoPaths \[get\_property LOCAL\_ROOT\_DIR \[xhub::get\_xstores xilinx\_board\_store]]' >> \~/.Xilinx/Vivado/Vivado\_init.tcl
```