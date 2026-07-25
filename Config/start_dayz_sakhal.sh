#!/bin/bash

cd /home/jordan/Games/DayZ_Server

# Start server
./DayZServer -config=server_sakhal.cfg -port=2301 "-mod=@CF;@Dabs Framework;@DayZ-Expansion-Licensed;@DayZ-Expansion-Bundle;@Community-Online-Tools" "-serverMod=@DayZ-Dynamic-AI-Addon" -BEpath=battleye -profiles=profiles_sakhal -dologs -adminlog -netlog -freezecheck

read -p "Done. Press Enter to close..."