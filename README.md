# Apex-DT-250/250A SDR Hack Exploration
Research materials regarding whether or not an Apex DT 250A might be hacked to function as a software defined radio.

Disclosure: I am not an electrical engineer, I was a licensed amateur radio operator until late 2024 when I let my license expire. What is documented and described here represents, more or less, my knowledge and skill with this sort of thing. If you can and want to contribute to furthering this project please let me know. I have a few extra devices and would be happy to provide them, they can also be found pretty cheaply on Ebay. Any advice, tips, or tricks are welcome as well, especially if you can authoritatively say, "stop now, none of this will work and here's why."


![board image](https://github.com/user-attachments/assets/a189e321-c0dc-4f05-ad1f-4e9d8747ac61)






# BACKGROUND:

Software Defined Radio has been increasing in popularity since the discovery that certain DVB-T usb sticks could be hacked to allow reception of more than just OTA tv broadcasts. There are many different versions of these sticks, but they are commonly referred to as 'RTL-SDR's. My understanding is that the functionality of these sticks as SDRs is possible because they have a 'debug mode', user's can gain access to the low-level programming of the hardware and with sufficient knowledge manipulate it to unlock other functionality.

Earlier this year (2025) I repaired the power supply of an Apex-DT-250A digital tv tuner that I had laying around. These were made back in 2007-2008 when the United States ended analogue tv broadcasts. They allow reception of digital broadcasts to be played on any tv with a composite RCA (yellow plug) or s-video input. During that process I noticed what looked like through holes for a serial console connection. I had recently used the tutorials found on https://www.makemehack.com/ to connect to and reflash DDWRT to a soft bricked Linksys E3200. Emboldened by this, I soldered on some headers to the 250A, connected a programmer, puttyed in, and sure enough a command line appeared.

I am now interested in seeing if this device can be hacked to harness the hardware as a general purpose SDR. Research on the internet and Reddit have at best yielded an answer of, "maybe/if" and "with enough knowledge and skill". Naysayers cited lack of appropriate hardware, hardware transparency, and hardware security measures as obstacles to hacking this type of device.     

What I have found so far:



## SOC: 

Zoran SupraHD 740

MIPS-32 CPU with Application Specific Extensions

Cascade2 CAS-220 Demodulator IC     - datasheet in folder   
NOTE: there is a Korean version of this device and the CAS-220 in this version includes FM demodulation capability similar to the dual role the rtl-sdr's can play.  

CVE3 NTSC/PAL/SECAM Video Encoder   - datasheet in folder

CVD2 NTSC/PAL/SECAM Video Decoder   - datasheet in folder

The debug terminal command 'rrc {start_register} {stop_register}' dumps the registry values in the specified range. Roughly ~75% of the registry values can be read this way, the other ~25% are read protected, the system reboots on an attempted read. There are 355 read protected registers and 293 of those appear to belong to the CVD2.  



## FLASH MEMORY:

The flash chip was made by Spansion/Infineon. There are pictures of it in the 'hi res images folder'. I attempted reading the chip with flashrom/flashprog run on a raspberry pi pico using the instructions for external flashing found on https://libreboot.org/docs/install/spi.html and confirmed that it is an S25FL016A/S25FL016A1F. There is a preliminary datasheet for the chip in the datasheets folder. I successfully dumped the chip contents and verified the image, 'apex.bin' and 'apex\_verify.bin' are in the dumps folder. I used binwalk to analyze the image. Results can be seen in the dumps folder as well, MIPS CPU is confirmed.



## RAM:

The 250 board has a Samsung K4H561638H-UCCC chip. There is a datasheet in 'datasheets' for the K4H561638H-UCCC and similar.

The 250A board has a Hynix HY5DU561622FTP-5.

Both chips are 256Mb

## OS:

The operating system is ThreadX. ThreadX is a RTOS and is still actively developed/maintained. Microsoft recently open sourced ThreadX and its source code can be found on GitHub. Debug terminal provides information on semaphores, tasks, allows task tracing, etcetera. For more info see:

https://threadx.io/

and

https://github.com/eclipse-threadx/threadx



## TUNER:

The 250 board tuner is a Thomson DTT76852, I could not find any other information on it.

The 250A has a Microtune MT2131F. There is a preliminary datasheet for the 2131 in datasheets

## OTHER:

In the debug terminal there is a configuration switch printout that references various other chips and tuners. The AD9833 is mentioned in there somewhere and a datasheet is included in the folder.

The Association for Maximum Service Television (MSTV) and the National
Association of Broadcasters (NAB) tested a group of similar boxes back in 2008. Their report is found in the datasheets folder and named ConverterBox\_report.doc.pdf

## PORTS:

There are through holes for a 4 pin header which I used for console access. A 7 pin header near the edge of the board and a 6 pin next to the processor which I'm assuming is an EJTAG port. There is a 'smart antenna' port in the back, the standard for these is CEA-909-A. The port is capable of bidirectional communication. The box also supports Analog RF Passthrough so you could pipe an antenna through the box and out again to an RTL or other SDR. The IR blaster connects to the main board using 4 pins of a 6 pin header on the same edge as the 7-pin and 4-pin. 



## IDEA/GOAL:

I ran and copied any debug command that seemed like it might be relevant, and having learned of putty's logging feature will script and run a complete dump soon. I am curious to know if there is enough information here to:

1. Create and flash a custom operating system, ThreadX, Linux, maybe something else.
2. Add hardware/functionality via the through hole ports or by reprogramming the smart antenna or IR ports. The latest ThreadX has support available for USB, Networking, and File Storage. An MCP2221 demo board might work for this.
3. Through some combination of the above modify the device to act as an 'RTL-like' SDR or extend its current functionality to allow it to play other signals than ATSC, FM/AM etcetera. Think a GQRX/SDR#/SDR++ like display but directly from the box to a tv.
4. Do any kind of interesting or neat hack with this box.



Ultimately, I want to improve my understanding of embedded systems and electronic hardware and have done so thus far.



## BUSINESS CASE:

From a market perspective (what would make this interesting in an RTL-SDR's world?) I think adding to existing functionality makes the most sense. Either by adding other signal reception to current capabilities internally in software, or by creating simple, easily repeatable mods that would, say, allow for an RTLSDR to be connected along with a Wifi chip/dongle (think OpenWRT router running RTL\_TCP but with ATSC decoding and smart antenna capability builtin). These can be had as or more cheaply than an RTLSDR v3 on Ebay and could make a fun addition to the DIY/SDR market. It has been a fun and cheap way to practice with a serial programmer and chip reading with a raspberry pi pico.



## RISKS:

### Hardware:

16Mb of flash and 256Mb of RAM are not bad. Not much if any different from a consumer router and DDWRT can run on a MIPS based router. Also, running SDR++ on Ubuntu cost about 210mb of memory give or take. However if the goal is to run a processing intensive SDR program like SDR++ I don't think the CPU will be sufficient. On the other hand, it does already function this way for ATSC, and I wonder if the functions present in the DSP parts of the SoC could be reused to process other signal types. An unknown and beyond my knowledge/skill at this point.

### Protected Registers:

Some of the registers that are read/write protected have enticing labels like the following:
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
If these are necessary for modifying then that could be prohibitive. 
Once more, I am not an EE/CE and don't know enough to know. Advice is welcome!



## NEXT STEPS:

Scripting a complete dump of every command in the debug terminal.

Checking the flash chip for software/hardware write protection, and if so, learning to unlock it and perform a bulk erase.

Understanding radio demodulation algorithms better and looking for firmware level instructions already present on device that might be reused. 

I know the I can flash new firmware to the device but have no experience writing firmware. So the next steps for me will have to be researching MIPS architecture, ThreadX OS, and creating a basic Linux firmware. As well as looking into what might be added (USB, Wifi, ...) via the exposed through holes or the IR pin headers.

Again, if you can and would like to contribute, especially with firmware knowledge, please contact me. I am willing to provide the hardware to work on. 


## REFERENCES \ LINKS:

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


## UPDATES (as of 10/17/2025)

These are some other things I've learned or tried since starting the project:

There is now a much more detailed hardware datasheet for the SupraHD 748 in the datasheets folder.

Photos of the 250A board have been uploaded to the images folder.

Memory dumping via terminal only occurs 256 bytes at a time, even scripted it would take a very long time to complete. 

I mistook 16Mb to mean 16MB of flash and 256Mb of RAM to mean 256MB... so the flashchip has only 2 MegaBytes of space, and RAM 32 MegaBytes. This is a setback for this project.
However, I am still interested in at least getting a U-Boot console with UART access working.
Also, the 748 datasheet claims that it has flashchip compatibility up to 128Mb = 16MB, so I am going to try to replace the flashchip
with a larger one once I have a bootloader that works on the 2MB Spansion chip. The 748 also allows booting from UART, 
and the 'config' printout mentions SD Card booting. Worth exploring still I think.

I believe the 7-pin through hole connection to be for an LCD display connection. It looks like it is not fully implemented on the PCB but might be able to be.

The bin file read from flash has entropy that varies/peaks around 0.9 and lower, The following was found using Strings:

```
Copyrigh
t (c) 19
96-2003 
Express 
Logic In
c. * Thr
eadX MIP
S32_4Kx/
Green Hi
lls Vers
ion G4.0
-GB-GL-M
-D-DL-KM
L-CMR-Hj
ML2-GZ-K
C-NH-TD-
AP-HA-GF
MS-DW-US
A-CA-SD
```

MIPS CPU appears to be 4kx

Apparently Green Hills is a an embedded technology company. Here is a link:

https://www.ghs.com/

## Next Steps: Buildroot/OpenWRT/U-BOOT

I have learned to use Buildroot and OpenWRT's buildroot based build system well enough to create a basic image for RPI 0w that boots to a BusyBox terminal. 
Given that the CPU is MIPS 32 4kx I Used OpenWRT's build system to generate an image for the old Linksys WRT54g, flashed it to a 16MB Winbond chip and replaced
the Spansion chip on one of the 250a's. This did not work, could not get a UART terminal, and the machine is still unusable after re-flashing the original bin
read from flash. I have tested that the bin can be re-flashed after erasing the Spansion chip and it works.

So, currently I'm learning about U-Boot and trying to get a better understanding of the boot process in general. 

Questions I have include:

Flashing the original bin to a new and larger chip did not work, why? Is the chip incompatible? 

Flashprog/flashrom gave me an error that the image I was flashing is smaller than the chip's size to try and get around this I used 

```
dd if=/dev/zero of=padding.bin bs=1 count= chipsize-imagesize [seek]
```

and then

```
cat apex.bin padding.bin >> apex_padded.bin
```

and flashed padded.bin

After a struggle, the chip took the flash, but the machine did not function and no terminal output. I might repeat this with
a fresh flashclip, chip, and machine. But, I want to know more about this part before I do. I'm wondering if this failure simply means that
the chip is incompatible, ANY 16MB chip is incompatible, or if there is something else I am missing or doing wrong. Is the method I used for
padding the image correct?

I used Buildroot to make just a basic u-boot.bin for RPI 0w but could not get a terminal that way. It only works when the Linux kernel/SD Card image
is included, I'm trying to understand why that is and/or can U-Boot itself supply a basic console?

MIPS support in Buildroot and U-Boot seems lacking or at least highly board specific. I'm learning to compile U-Boot and want to understand
how to make a minimal configuration that would be small enough to fit in 2MB and also allow UART console access. I think there is enough 
info on the hardware to create a device tree spec, but not sure at this point.

## UPDATE (as of 10/27/2025)

Two new experiments have been performed. 

I tested the 6-pin header next to the SoC with a multimeter and logic analyzer. 5 pins read 3.3v and 1 0v, logic analyzer shows no activity during operation of the device. 
It was suggested in this helpful and friendly Reddit forum https://www.reddit.com/r/AskElectronics/ that I could gain further insight by connecting each pin to ground with a 1K ohm resistor and look at the voltage drops to determine whether or not the pin is an input or output. The results are shown in the diagram below:


<img width="461" height="421" alt="swd_uart_ejtag_test" src="https://github.com/user-attachments/assets/c725b135-36a6-40ea-8729-089c333662fb" />


Another concern I've begun to understand is that board's can implement security measures in the boot process. For example, if a firmware is signed with an encryption key in OTP memory than some other unsigned firmware may not load. I'm just starting to learn about the various ways this type of security can be implemented but it was easily available to the basic following check:

I had previously tested that the flashchip could be read, erased, and reflashed resultng in the device working properly still. So I wondered what would happen if I modified a random bit in the firmware .bin file and flashed that. I tried this twice, modifying bits at two different locations in the file. In one instance doing so soft bricked the device, in the other it did not. I suspect this does not confirm the lack of cryptographic security measures, but it does not suggest ending the project on account of them either. I think it plausible that since only some portions of the .bin appear encryoted the system will only brick if modifying those portions. I'll try repeating the tests with respect to areas in the .bin with high and low entropy according to the binwalk output and see if this determines whether or not the device functions. Maybe the crypto sec only checks parts of the flash?   
