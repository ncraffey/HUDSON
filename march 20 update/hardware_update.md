# The HUDSON Project

Nick Craffey & John Craffey

___

## Goal for this Submission

Our goal this week was to develop a custom overlay that includes access to the HDMI I/O on the pynqboard as well as access to any custom HLS code that we want to write to accelerate tasks. We learned that since we cannot use the base overlay and our custom overlay simultaneously that we must create one that includes the aspects of the base overlayt that we need, and then integrate our IP into it.

## Custom IP

We created a sort of place holder custom IP that reads through a memory buffer, modifies some color data, and writes the modified frame back to a memory buffer for software to pick up again. In it's current state it is functionally garbage, as the HLS code is not de4veloped right now. The goal was to see if we can get data in and out of our hardware in a custom IP without throwing any crashing errors, and we achieved that goal.

![alt text](redDMA_bd.png "Full BD")

## Base Overlay Modifications

The base overlay is vary big and takes a long time to synthesize so we needed to take out all the parts we are not using. We only wanted the HDMI I/O so we had to strip down the Base Overlay in vivado until it was just the HDMI related blocks. This was a lot easier said than done, as the base overlay vivado project is very sensitive to small changes and we went through many iterations of failed builds and non-funtional IP. Ultimately after following this tutorial very closely<sub>[1]</sub>  we were able to get a stripped down version of base overlay that just handled HDMI functionality.

## Combined design functionality

Once we knew that both of our overlays were functioning on their own, we combined them together as one big block diagram in vivado and exported the final design. This allowed us to talk to both the HDMI I/O as well as the custom frame-modifying IP in one overlay. The hdmi_hudson_overlay_test jupyter notebook was a successfull test of this functionality.

### Completed Combined Overlay:

![alt text](full_test_bd.png "Full BD")

### Input and Output Frame from the Hardware

![alt text](inputframe.png "Full BD")

![alt text](redshifted.png "Full BD")

## Future Plans

Although it doesnt seem like much right now, this is a massive step in moving forward with our hardware design. Knowing that we can include both the HDMI communication as well as our own HLS design in one overlay is very important in the pursuit of a design that does something useful.

From here, we need to understand how the frame data is structured so we can manipulate it in more meaningful ways than just making the frame more red. A big bottleneck in these designs is the large amount of time it takes to test different possibilities, so for this submission the goal was simply to get a design that functioned without critical error, and from here we can move towards more interesting algorithms in HLS.

## References

1. [Adding IP to a PYNQ overlay (From Base Overlay)](https://www.youtube.com/watch?v=LomArt-hi4M)