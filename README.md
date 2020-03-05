# SAR-UAV
Co-author: Bryan Heilman

This project has an overall aim of developing a light aerial search and rescue platform by integrating a radio direction-finder (RDF) into a small unmanned aerial vehicle (UAV) using commercial, off-the-shelf (COTS) components.The finished platform will be able to locate emergency locator transmitter (ELT) beacons from the air.

At this phase of the project, the RDF is being built using a combination of four COTS software-defined radio (SDR) receivers, COTS antennas, and a Linux-based open source SDR development platform, GNU Radio.

To achieve a reliable calculation of the angle of incidence or azimuth of a radio signal source, the RDF we develop will use the method of phase interferometry. This method involves the arrangement of two or more phase-coherent receiving elements at a known distance from each other, which are tuned in to and excited by the signal of interest (121.5MHz or 243MHz for ELT’s). Since each element receives the wave front of the signal at a marginally different time, the relative phase and the phase difference of the signal between each element can be calculated, and a trigonometric function can be used to estimate the angle of incidence of the wave front. The reliable calculation of phase difference will involve the conversion of the COTS SDR Receivers into phase-coherent versions by synchronizing each device to the same physical oscillator.

The functional RDF will run from a Linux-based OS on a laptop, as a precursor to
miniaturized version which can be mounted on a small COTS air frame.

Technologies used: Python 3, GNURadio, SOLIDWORKS, Linux, Raspberry Pi


