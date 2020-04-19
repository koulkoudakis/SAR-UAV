# SAR-UAV
Co-author: Bryan Heilman

This project has an overall aim of developing a light, aerial search and rescue platform by integrating a radio direction-finder (RDF) into a small unmanned aerial vehicle (UAV) using commercial, off-the-shelf (COTS) components. The finished platform will be able to locate emergency locator transmitter (ELT) beacons from the air.

At this phase of the project, the RDF system is being built using a four-channel COTS software-defined radio (SDR) receiver, an open-source signal processing script, and COTS antennas. Data will be relayed between the ground station and the aircraft using LoRa (Long Range) transceiver modules operating on the license-free 915 MHz radio band.

To achieve a reliable estimation of the angle of incidence or direction of arrival (DOA) of a signal source, the RDF we build will use the method of phase interferometry. This method involves the arrangement of two or more phase-coherent receiving elements at a known distance from each other, which are tuned in to the frequency of interest. Since each element receives the wave front of the signal at a marginally different time, the phase difference of the signal between each element can be calculated, and one of a number of signal processing algorithms (MUSIC, MEM, Capon, or Bartlett) can be applied to estimate the DOA.

Using the GPS coordinates of the aircraft, its compass heading, and the DOA, lines of bearing will be plotted on a geographic map in real-time to indicate the estimated location of the ELT using software developed specifically for the project.

Technologies used: Python 3, JavaScript, GNURadio, SOLIDWORKS, Linux, Raspberry Pi


