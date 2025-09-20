# Apex-DT-250A SDR Hack Exploration
Research materials regarding whether or not an Apex DT 250A might be hacked to function as a software defined radio.

Disclosure: I am not an electrical engineer, I was a licensed amateur radio operator until late 2024 when I let my license expire. What is documented and described here represents, more or less, my knowledge and skill with this sort of thing. If you can and want to contribute to furthering this project please let me know. I have a few extra devices and would be happy to provide them, they can also be found pretty cheaply on Ebay. Any advice, tips, or tricks are welcome as well, especially if you can authoritatively say, "stop now, none of this will work and here's why."



# BACKGROUND:

Software Defined Radio has been increasing in popularity since the discovery that certain DVB-T usb sticks could be hacked to allow reception of more than just OTA tv broadcasts. There are many different versions of these sticks, but they are commonly referred to as 'RTL-SDR's. My understanding is that the functionality of these sticks as SDRs is possible because they have a 'debug mode', user's can gain access to the low-level programming of the hardware and with sufficient knowledge manipulate it to unlock other functionality.

Earlier this year (2025) I repaired the power supply of an Apex-DT-250A digital tv tuner that I had laying around. These were made back in 2007-2008 when the United States ended analogue tv broadcasts. They allow reception of digital broadcasts to be played on any tv with a composite RCA (yellow plug) or s-video input. During that process I noticed what looked like through holes for a serial console connection. I had recently used the tutorials found on https://www.makemehack.com/ to connect to and reflash DDWRT to a soft bricked Linksys E3200. Emboldened by this, I soldered on some headers to the 250A, connected a programmer, puttyed in, and sure enough a command line appeared.

I am now interested in seeing if this device can be hacked to harness the hardware as a general purpose SDR. Research on the internet and Reddit have at best yielded an answer of, "maybe/if" and "with enough knowledge and skill". Naysayers cited lack of appropriate hardware, hardware transparency, and hardware security measures as obstacles to hacking this type of device.     

Between poking around on the command line and researching it online I gained the following knowledge of the device:



## CPU:

Zoran SupraHD 740 SOC

Based on MIPS-32 CPU with suspected ASE's

There are block diagram level datasheets in the 'datasheets' folder that describe the features and specs of this family of system, the 640, 660, and 680. I could not find detailed datasheets nor anything specifically for the 740. Zoran merged with CSR in 2011 and CSR is now part of Qualcomm. There used to be an SDK that Zoran provided.

However, I am thus far undeterred because the debug terminal gives the user access to quite a bit of information, including read/write access to the system's registers, control of gpio state and direction, i2c bus devices, etcetera. As stated above I am not an electrical or computer engineer but it looks like everything one would want might be there. I successfully read ~ 75% of the registers to a file, 'registry\_dump.txt' in the 'dumps' folder. The debug utility command 'rrc' outputs the result of a read in C code in the form of a 'WriteTLReg' call.



## FLASH MEMORY:

The flash chip was made by Spansion/Infineon. There are pictures of it in the 'hi res images folder'. I attempted reading the chip with flashrom/flashprog run on a raspberry pi pico using the instructions for external flashing found on https://libreboot.org/docs/install/spi.html and confirmed that it is an S25FL016A. There is a preliminary datasheet for the chip in the datasheets folder. I successfully dumped the chip contents and verified the image, 'apex.bin' and 'apex\_verify.bin' are in the dumps folder. I used binwalk to analyze the image. Results can be seen in the dumps folder as well, MIPS CPU is confirmed.



## RAM:

The board very clearly has a Samsung K4H561638H-UCCC chip. There is a datasheet in 'datasheets' for the K4H561638H-UCCC and similar.



## OS:

The operating system is ThreadX. ThreadX is a RTOS and is still actively developed/maintained. Microsoft recently open sourced ThreadX and its source code can be found on GitHub. Debug terminal provides information on semaphores, tasks, allows task tracing, etcetera. For more info see:

https://threadx.io/

and

https://github.com/eclipse-threadx/threadx



## TUNER:

The tuner is a Thomson DTT76852, I could not find any other information on it.



## OTHER:

In the debug terminal there is a configuration switch printout that references various other chips and tuners. The AD9833 is mentioned in there somewhere and a datasheet is included in the folder.

The Association for Maximum Service Television (MSTV) and the National
Association of Broadcasters (NAB) tested a group of similar boxes back in 2008. Their report is found in the datasheets folder and named ConverterBox\_report.doc.pdf

## PORTS:

There are through holes for a 4 pin header which I used for console access. A 7 pin header near the edge of the board and a 6 pin next to the processor which I assume is an EJTAG port. There is a 'smart antenna' port in the back, the standard for these is CEA-909-A. The port is capable of bidirectional communication. The box also supports Analog RF Passthrough so you could pipe an antenna through the box and out again to an RTL or other SDR. The IR blaster connects to the main board using 4 pins of a 6 pin header on the same edge as the 7-pin and 4-pin. 



## IDEA/GOAL:

I ran and copied any debug command that seemed like it might be relevant, and having learned of putty's logging feature will script and run a complete dump soon. I am curious to know if there is enough information here to:

1. Create and flash a custom operating system, ThreadX, Linux, maybe something else.
2. Add hardware/functionality via the through hole ports or by reprogramming the smart antenna or IR ports. The latest ThreadX has support available for USB, Networking, and File Storage
3. Through some combination of the above modify the device to act as an 'RTL-like' SDR or extend its current functionality to allow it to play other signals than ATSC, FM/AM etcetera. Think a gqrx/SDR#/SDR++ like display but directly from the box to a tv.
4. Do any kind of interesting or neat hack with this box.



Ultimately, I want to improve my understanding of embedded systems and electronic hardware and have done so thus far.



## BUSINESS CASE:

From a market perspective (what would make this interesting in an RTL-SDR's world?) I think adding to existing functionality makes the most sense. Either by adding other signal reception to current capabilities internally in software, or by creating simple, easily repeatable mods that would, say, allow for an RTLSDR to be connected along with a Wifi chip/dongle (think OpenWRT router running RTL\_TCP but with ATSC decoding and smart antenna capability builtin). These can be had as or more cheaply than an RTLSDR v3 on Ebay and could make a fun addition to the DIY/SDR market. It has been a fun and cheap way to practice with a serial programmer and chip reading with a raspberry pi pico.



## RISKS:

### Hardware:

16Mb of flash and 256Mb(according to the datasheet) of RAM are not bad. Not much if any different from a consumer router and DDWRT can run on a MIPS based router. Also, running SDR++ on Ubuntu cost about 210mb of memory give or take. However if the goal is to run a processing intensive SDR program like SDR++ I don't think the CPU will be sufficient. On the other hand, it does already function this way for ATSC, and I wonder if the functions present in the DSP parts of the SoC could be reused to process other signal types. An unknown and beyond my knowledge/skill at this point.

### Unread/Unknown/Protected Registers:

Some of the registers that cause system reboot when reading is attempted have enticing labels like the following:
```
GPADC_CTRL_REG
GPADC_START_REG
GPADC_STATUS_REG
GPADC_DATA_REG
AFE_BYPASS_CTL_REG
DEBUG_PIN_DEBUGBUS_O_SEL_REG
IFAFE_ADCMODE_REG
IFAFE_ADCCONTROL1_REG
IFAFE_OUTPUT_OPTIONS_REG
```
Where I'm assuming:
`
AFE = Analogue Front End
`
 and 
`
ADC = Analogue to Digital Converter
`
and that,
```
AFE_BYPASS_CTL_REG
DEBUG_PIN_DEBUGBUS_O_SEL_REG
IFAFE_ADCMODE_REG
```
being unreadable might mean, "you won't be doing any cool RTLSDR like tricks without these." 

If these are necessary for modifying and they are protected then that could be prohibitive. 
Once more, I am not an EE/CE and don't know enough to know. Advice is welcome!



## NEXT STEPS:

Scripting a complete dump of every command in the debug terminal.

Checking the flash chip for software/hardware write protection, and if so, learning to unlock it and perform a bulk erase.

Understanding radio demodulation algorithms better and looking for firmware level instructions already present on device that might be reused. 

I know the I can flash new firmware to the device but have no experience writing firmware. So the next steps for me will have to be researching MIPS architecture, ThreadX OS, and creating a basic Linux firmware. As well as looking into what might be added (USB, Wifi, ...) via the exposed through holes or the IR pin headers.

Again, if you can and would like to contribute, especially with firmware knowledge, please contact me. I am willing to provide the hardware to work on. 


## REFERENCES:

I utilized the following sources/sites to figure out serial console access and flashchip reading. If you are new to hardware hacking check them out!

https://libreboot.org/ has a ton of info on bios/uefi firmware creation and flashing, and a lot of other neat info on privacy and Right-To-Repair.

https://www.youtube.com/watch?v=LSQf3iuluYo is YouTube Hardware Hacking Tutorial series. Really excellent, you can get an entire frame of mind for approaching a potential hack and very clear instruction in tools and methods to use. 

https://www.makemehack.com/ author site for the YouTube series.

For more info on SDR check out:

https://www.rtl-sdr.com/about-rtl-sdr/

and 

https://osmocom.org/projects/rtl-sdr/wiki

Ebay Search for hardware:

https://www.ebay.com/sch/i.html?_nkw=apex+dt250a&_sacat=0
