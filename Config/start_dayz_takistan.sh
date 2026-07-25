#!/bin/bash

cd /home/jordan/Games/DayZ_Server

# Start server
./DayZServer -config=server_takistan.cfg -port=2301 "-mod=@CF;@Dabs Framework;@TakistanPlus;@DayZ-Expansion-Licensed;@DayZ-Expansion-Bundle;@Community-Online-Tools;@Takistan Clothing;@PVEZ Reloaded" "-serverMod=@DayZ-Dynamic-AI-Addon" -BEpath=battleye -profiles=profiles_takistan -dologs -adminlog -netlog -freezecheck

read -p "Done. Press Enter to close..."