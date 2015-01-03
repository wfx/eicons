Animations
======
Animated images used to represent loading web sites, or other background processing which may be less suited to 
more verbose progress reporting in the user interface. Animations should be a PNG with frames which are the size 
of the directory the animation is in, tiled in a WxH grid. Implementations should determine the number of frames 
by dividing the image into its frames, and iterating from left to right, wrapping to the first frame, after 
rendering the last. 
