# EECS4422_Project

Relative Performance differentials of Saliency models on Corresponding IR-VIS images

Author: Peter Caruana
Instructor: Dr. Calden Wloka
York University, EECS_4422 - 2019/20

This is the repository for my research project, for EECS 4422 - Computer Vision. 

<B>Motivation</B>

There are many different models of saliency detection which have been developed over the years in the field of computer vision. The goal 
is to try and localize areas of interest, often with respect to how humans determine the salient parts of images. This normally tends to 
be subjects like animals and people or things like vehicles and electronics. Saliency maps can be quite useful for object localization 
and feature bounding. Most saliency models are designed to work on images which are captured using light of visible wavelengths, however 
many of the subjects of interest for saliency are actually quite distinct in the infrared light spectrum. With this in mind, there are 
many applications where VIS imaging would be unable to function (Low light scenarios), but IR or NIR imaging may still have enough 
information to be useful. The question that this project aims to answer is whether saliency models used on VIS images yield the same or 
similar results to those models used on IR images.

<B>Approach</B>

Multiple saliency models will be run on image sets from the Visible-Infrared Database, where each image set contains corresponding VIS and IR images for a given subject. This will generate pairs of saliency maps for each model. Since each image pair is co-registered, each pixel pair should correspond to the same mapping in world space. Analysis will be done to determine the relative differences between each saliency map pair. Meta analysis can then be done on the relative performance across datasets. This will show which areas are the saliency maps similar, or different, and by how much. The idea is to determine the types of subjects (if any) that have performance independent of image type.The saliency models that will be used are IKN, AIM, AWS, GBVS, which are fairly common and popular approaches. This list may be changed or grow as the project progresses.

<B>Expected Results</B>

There are 3 primary outcomes which this research may produce, each with their own implications. First, it may be the case that there are none or very small differences in the saliency maps generated. This would suggest that VIS and IR images are equivalent for generating saliency maps. Another outcome could be that the above is true, but only for certain datasets (subject types). The implications are similar in this case, but narrow the range in which it is applicable. Finally, for all datasets the IR and VIS saliency maps vary wildly which would provide some strong evidence that IR and VIS images are not interchangeable at all for saliency.
